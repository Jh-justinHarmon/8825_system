#!/usr/bin/env python3
"""
Lane A Processor - Auto-assimilation for safe items
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from classifier import InboxItem
from deduplicator import Deduplicator


class LaneAProcessor:
    """Process Lane A items (safe auto-assimilation)"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent
        
        self.workspace_root = Path(workspace_root)
        self.inbox_path = Path.home() / 'Downloads' / '8825_inbox'
        self.processing_path = self.inbox_path / 'processing' / 'lane_a'
        self.completed_path = self.inbox_path / 'completed'
        
        # Load integration targets
        config_path = Path(__file__).parent / 'config' / 'integration_targets.json'
        with open(config_path, 'r') as f:
            self.targets = json.load(f)
        
        # Initialize deduplicator
        self.dedup = Deduplicator()
    
    def process(self, item: InboxItem) -> Dict[str, Any]:
        """
        Process Lane A item
        
        Steps:
        1. Check for duplicates
        2. Normalize to focus structure
        3. Integrate to target location
        4. Update index
        5. Move to completed/
        6. Log
        """
        result = {
            'item': item.original_file,
            'status': 'processing',
            'target_focus': item.target_focus
        }
        
        # Check for duplicates
        if self.dedup.is_duplicate(item):
            result['status'] = 'duplicate'
            result['action'] = 'skipped'
            return result
        
        # Check for similar items
        similar = self.dedup.find_similar(item, threshold=0.9)
        if similar:
            result['similar_items'] = len(similar)
            result['warning'] = 'High similarity to existing items'
        
        # Get integration target
        target_config = self.targets.get(item.target_focus)
        if not target_config:
            result['status'] = 'error'
            result['error'] = f'Unknown target_focus: {item.target_focus}'
            return result
        
        # Integrate to target
        try:
            target_location = self._integrate(item, target_config)
            result['target_location'] = str(target_location)
            result['status'] = 'completed'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            return result
        
        # Update index
        self.dedup.add_to_index(item, str(target_location))
        
        # Move original to completed
        self._move_to_completed(item)
        
        result['action'] = 'integrated'
        return result
    
    def _integrate(self, item: InboxItem, target_config: Dict[str, Any]) -> Path:
        """
        Integrate item to target location
        """
        target_type = target_config['type']
        
        if target_type == 'json_library':
            return self._integrate_to_json_library(item, target_config)
        elif target_type == 'folder':
            return self._integrate_to_folder(item, target_config)
        else:
            raise ValueError(f'Unknown target type: {target_type}')
    
    def _integrate_to_json_library(self, item: InboxItem, config: Dict[str, Any]) -> Path:
        """
        Integrate to JSON library (e.g., Joju)
        """
        target_path = self.workspace_root / config['path']
        
        # Ensure target exists
        if not target_path.exists():
            # Create with base structure
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w') as f:
                json.dump({
                    'meta': {
                        'created': datetime.now().isoformat(),
                        'focus': item.target_focus
                    },
                    'items': []
                }, f, indent=2)
        
        # Load existing
        with open(target_path, 'r') as f:
            library = json.load(f)
        
        # Add new item
        new_entry = {
            'id': f"{item.target_focus}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'content_type': item.content_type,
            'content': item.content,
            'metadata': item.metadata,
            'added_at': datetime.now().isoformat(),
            'source_file': item.original_file
        }
        
        if 'items' not in library:
            library['items'] = []
        
        library['items'].append(new_entry)
        
        # Save
        with open(target_path, 'w') as f:
            json.dump(library, f, indent=2)
        
        return target_path
    
    def _integrate_to_folder(self, item: InboxItem, config: Dict[str, Any]) -> Path:
        """
        Integrate to folder (e.g., HCSS knowledge)
        """
        target_dir = self.workspace_root / config['path']
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        file_naming = config.get('file_naming', '{date}_{content_type}.md')
        filename = file_naming.format(
            date=datetime.now().strftime('%Y%m%d'),
            content_type=item.content_type
        )
        
        target_path = target_dir / filename
        
        # If file exists, append number
        counter = 1
        while target_path.exists():
            base = target_path.stem
            target_path = target_dir / f"{base}_{counter}.md"
            counter += 1
        
        # Convert to markdown
        markdown = self._to_markdown(item)
        
        # Write file
        with open(target_path, 'w') as f:
            f.write(markdown)
        
        return target_path
    
    def _to_markdown(self, item: InboxItem) -> str:
        """
        Convert item to markdown format
        """
        lines = []
        
        # Header
        lines.append(f"# {item.content_type.replace('_', ' ').title()}")
        lines.append('')
        lines.append(f"**Focus:** {item.target_focus}")
        lines.append(f"**Date:** {item.timestamp.strftime('%Y-%m-%d')}")
        lines.append(f"**Source:** {item.source_channel}")
        lines.append('')
        lines.append('---')
        lines.append('')
        
        # Content
        def format_content(data, indent=0):
            result = []
            prefix = '  ' * indent
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        result.append(f"{prefix}**{key}:**")
                        result.extend(format_content(value, indent + 1))
                    else:
                        result.append(f"{prefix}**{key}:** {value}")
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (dict, list)):
                        result.extend(format_content(item, indent))
                    else:
                        result.append(f"{prefix}- {item}")
            else:
                result.append(f"{prefix}{data}")
            
            return result
        
        lines.extend(format_content(item.content))
        lines.append('')
        
        # Metadata
        lines.append('---')
        lines.append('')
        lines.append('## Metadata')
        lines.append('')
        lines.extend(format_content(item.metadata))
        
        return '\n'.join(lines)
    
    def _move_to_completed(self, item: InboxItem):
        """Move original file to completed/"""
        source = Path(item.original_file)
        
        if not source.exists():
            # Already moved by engine
            source = self.processing_path / source.name
        
        if source.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            target = self.completed_path / f"{timestamp}_{source.name}"
            shutil.move(str(source), str(target))
            
            # Also move metadata if exists
            meta_file = source.with_suffix('.meta.json')
            if meta_file.exists():
                meta_target = target.with_suffix('.meta.json')
                shutil.move(str(meta_file), str(meta_target))


if __name__ == '__main__':
    # Test Lane A processor
    from classifier import InboxClassifier
    
    classifier = InboxClassifier()
    processor = LaneAProcessor()
    
    test_data = {
        'content_type': 'note',
        'target_focus': 'hcss',
        'content': {
            'title': 'Test Meeting Notes',
            'date': '2025-11-08',
            'notes': 'This is a test of Lane A processing'
        },
        'metadata': {
            'source': 'test',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    item = classifier.classify(test_data, 'test_lane_a.json')
    result = processor.process(item)
    
    print(json.dumps(result, indent=2))
