#!/usr/bin/env python3
"""
Relationship Mapper - Phase 3
Entity linking, timeline tracking, cross-references, and search indexing
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class RelationshipMapper:
    """Map relationships between files, entities, and projects"""
    
    def __init__(self):
        self.entity_patterns = self._load_entity_patterns()
        self.relationship_graph = defaultdict(list)
        self.timeline = []
        self.search_index = defaultdict(set)
    
    def _load_entity_patterns(self):
        """Load entity recognition patterns"""
        return {
            "people": [
                "Justin Harmon", "Justin", "Gamal Prather", "Gamal"
            ],
            "companies": [
                "Trustybits", "HCSS", "Hammer Consulting", "Marchon", 
                "COSTA", "Nike", "Fossil", "prtcl inc", "prtcl"
            ],
            "projects": [
                "Joju", "Forge", "8825", "TGIF", "VSP Innovation Lab",
                "Shot Tracker", "Chase Travel Rewards"
            ],
            "technologies": [
                "Rhino", "Figma", "Mural", "Python", "JavaScript",
                "React", "Firebase", "Vercel"
            ]
        }
    
    def extract_entities(self, file_data, classification):
        """
        Extract all entities from file
        
        Returns:
            dict: Entities by type
        """
        text = self._get_text_content(file_data)
        entities = {
            "people": [],
            "companies": [],
            "projects": [],
            "technologies": [],
            "dates": []
        }
        
        # Extract each entity type
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    entities[entity_type].append({
                        "name": pattern,
                        "type": entity_type,
                        "confidence": 100 if pattern in text else 80  # Exact vs case-insensitive
                    })
        
        # Extract dates
        entities["dates"] = self._extract_dates(text)
        
        # Deduplicate
        for entity_type in entities:
            entities[entity_type] = self._deduplicate_entities(entities[entity_type])
        
        return entities
    
    def _get_text_content(self, file_data):
        """Get all text content from file data"""
        text_parts = []
        
        # Filename
        text_parts.append(file_data.get("metadata", {}).get("filename", ""))
        
        # Content sample
        text_parts.append(file_data.get("content_data", {}).get("text_sample", ""))
        
        # Keywords
        keywords = file_data.get("content_data", {}).get("keywords", [])
        text_parts.extend(keywords)
        
        return " ".join(text_parts)
    
    def _extract_dates(self, text):
        """Extract dates from text"""
        dates = []
        
        # Common date patterns
        patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2025-11-07
            r'\d{2}/\d{2}/\d{4}',  # 11/07/2025
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',  # Nov 7, 2025
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                dates.append({
                    "value": match,
                    "type": "date",
                    "confidence": 90
                })
        
        return dates
    
    def _deduplicate_entities(self, entities):
        """Remove duplicate entities"""
        seen = set()
        unique = []
        
        for entity in entities:
            key = (entity.get("name", "").lower(), entity.get("type"))
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return unique
    
    def build_relationships(self, file_id, entities, classification):
        """
        Build relationship graph
        
        Creates connections between:
        - File → Entities
        - Entity → Entity (co-occurrence)
        - File → Project
        - File → Timeline
        """
        relationships = []
        
        # File → Project
        project = classification.get("project")
        if project:
            relationships.append({
                "from": file_id,
                "to": project,
                "type": "belongs_to",
                "confidence": classification.get("confidence", 0)
            })
        
        # File → Entities
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                relationships.append({
                    "from": file_id,
                    "to": entity.get("name"),
                    "type": f"mentions_{entity_type}",
                    "confidence": entity.get("confidence", 0)
                })
        
        # Entity → Entity (co-occurrence)
        all_entities = []
        for entity_list in entities.values():
            all_entities.extend([e.get("name") for e in entity_list])
        
        for i, entity1 in enumerate(all_entities):
            for entity2 in all_entities[i+1:]:
                relationships.append({
                    "from": entity1,
                    "to": entity2,
                    "type": "co_occurs_with",
                    "context": file_id,
                    "confidence": 70
                })
        
        return relationships
    
    def add_to_timeline(self, file_id, file_data, entities):
        """
        Add file to chronological timeline
        
        Uses:
        - File modification date
        - Extracted dates from content
        - Project dates
        """
        timeline_entry = {
            "file_id": file_id,
            "filename": file_data.get("metadata", {}).get("filename"),
            "modified": file_data.get("metadata", {}).get("modified"),
            "extracted_dates": [d.get("value") for d in entities.get("dates", [])],
            "timestamp": datetime.now().isoformat()
        }
        
        return timeline_entry
    
    def build_search_index(self, file_id, file_data, entities, classification):
        """
        Build search index for fast retrieval
        
        Indexes:
        - Filename tokens
        - Keywords
        - Entity names
        - Project
        - Category
        - Tags
        """
        index_terms = set()
        
        # Filename tokens
        filename = file_data.get("metadata", {}).get("filename", "")
        index_terms.update(self._tokenize(filename))
        
        # Keywords
        keywords = file_data.get("content_data", {}).get("keywords", [])
        index_terms.update(keywords)
        
        # Entity names
        for entity_list in entities.values():
            for entity in entity_list:
                index_terms.update(self._tokenize(entity.get("name", "")))
        
        # Project
        project = classification.get("project")
        if project:
            index_terms.add(project.lower())
        
        # Category
        category = classification.get("category")
        if category:
            index_terms.update(self._tokenize(category))
        
        # Tags
        tags = classification.get("tags", [])
        index_terms.update(tags)
        
        # Build inverted index: term → file_ids
        search_index = {}
        for term in index_terms:
            if term:  # Skip empty strings
                search_index[term.lower()] = file_id
        
        return search_index
    
    def _tokenize(self, text):
        """Tokenize text into searchable terms"""
        # Remove special characters and split
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = text.split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        
        return tokens
    
    def process_file(self, file_id, file_data, classification):
        """
        Complete relationship mapping for a file
        
        Returns:
            dict: All relationship data
        """
        # Extract entities
        entities = self.extract_entities(file_data, classification)
        
        # Build relationships
        relationships = self.build_relationships(file_id, entities, classification)
        
        # Add to timeline
        timeline_entry = self.add_to_timeline(file_id, file_data, entities)
        
        # Build search index
        search_index = self.build_search_index(file_id, file_data, entities, classification)
        
        return {
            "entities": entities,
            "relationships": relationships,
            "timeline": timeline_entry,
            "search_index": search_index
        }
    
    def search(self, query, index_data):
        """
        Search files by query
        
        Args:
            query: Search query string
            index_data: Dict of {term: file_id} mappings
        
        Returns:
            list: Matching file IDs
        """
        query_tokens = self._tokenize(query)
        matching_files = set()
        
        for token in query_tokens:
            if token in index_data:
                file_id = index_data[token]
                matching_files.add(file_id)
        
        return list(matching_files)
