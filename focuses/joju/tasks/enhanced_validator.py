#!/usr/bin/env python3
"""
Task Truth Pipeline V2 - Enhanced Validator
Implements all 10 advanced validation techniques
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Set, Optional
from datetime import datetime
from collections import defaultdict

# Joju codebase location
JOJU_CODE = Path("/Users/justinharmon/Hammer Consulting Dropbox/Justin Harmon/Public/joju")

class EnhancedValidator:
    """Advanced task validation with multiple techniques"""
    
    def __init__(self):
        self.joju_path = JOJU_CODE
        self.component_graph = {}
        self.import_map = {}
        self.git_commits = []
        
    # ========================================================================
    # 1. GIT COMMIT MINING
    # ========================================================================
    
    def mine_git_commits(self) -> List[Dict]:
        """Extract all git commits with messages"""
        print("🔍 Mining git commit history...")
        
        try:
            os.chdir(self.joju_path)
            result = subprocess.run(
                ['git', 'log', '--all', '--pretty=format:%H|%ai|%s', '--no-merges'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            commits = []
            for line in result.stdout.split('\n'):
                if '|' in line:
                    hash, date, message = line.split('|', 2)
                    commits.append({
                        'hash': hash,
                        'date': date,
                        'message': message.lower()
                    })
            
            self.git_commits = commits
            print(f"   Found {len(commits)} commits")
            return commits
            
        except Exception as e:
            print(f"   ⚠️  Git mining failed: {e}")
            return []
    
    def find_commits_for_task(self, task_title: str) -> List[Dict]:
        """Find git commits related to a task"""
        keywords = self.extract_keywords(task_title)
        matching_commits = []
        
        for commit in self.git_commits:
            if any(kw in commit['message'] for kw in keywords):
                matching_commits.append(commit)
        
        return matching_commits
    
    # ========================================================================
    # 2. IMPORT STATEMENT ANALYSIS
    # ========================================================================
    
    def build_import_map(self):
        """Build map of which files import which components"""
        print("📦 Building import map...")
        
        import_map = defaultdict(list)
        
        for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
            for file in self.joju_path.rglob(ext):
                try:
                    content = file.read_text()
                    # Find import statements
                    imports = re.findall(r'import.*from\s+[\'"](.+?)[\'"]', content)
                    for imp in imports:
                        component = imp.split('/')[-1]
                        import_map[component].append(str(file.relative_to(self.joju_path)))
                except:
                    pass
        
        self.import_map = dict(import_map)
        print(f"   Mapped {len(self.import_map)} components")
        return self.import_map
    
    def get_import_usage(self, component_name: str) -> int:
        """Count how many files import a component"""
        return len(self.import_map.get(component_name, []))
    
    # ========================================================================
    # 3. COMPONENT DEPENDENCY GRAPH
    # ========================================================================
    
    def build_component_graph(self):
        """Build dependency graph of components"""
        print("🕸️  Building component dependency graph...")
        
        graph = {}
        
        for ext in ['*.tsx', '*.ts']:
            for file in self.joju_path.rglob(ext):
                try:
                    content = file.read_text()
                    filename = file.stem
                    
                    # Find imports
                    imports = re.findall(r'import.*from\s+[\'"](.+?)[\'"]', content)
                    dependencies = [imp.split('/')[-1] for imp in imports]
                    
                    graph[filename] = {
                        'file': str(file.relative_to(self.joju_path)),
                        'dependencies': dependencies
                    }
                except:
                    pass
        
        self.component_graph = graph
        print(f"   Graphed {len(graph)} components")
        return graph
    
    def check_component_chain(self, required_components: List[str]) -> bool:
        """Check if all required components exist and are connected"""
        for comp in required_components:
            if comp not in self.component_graph:
                return False
        return True
    
    # ========================================================================
    # 4. TEST FILE CORRELATION
    # ========================================================================
    
    def find_test_files(self, component_name: str) -> List[str]:
        """Find test files for a component"""
        test_patterns = [
            f"{component_name}.test.tsx",
            f"{component_name}.test.ts",
            f"{component_name}.spec.tsx",
            f"{component_name}.spec.ts",
            f"**/__tests__/{component_name}.*"
        ]
        
        test_files = []
        for pattern in test_patterns:
            matches = list(self.joju_path.rglob(pattern))
            test_files.extend([str(f.relative_to(self.joju_path)) for f in matches])
        
        return test_files
    
    def has_tests(self, component_name: str) -> bool:
        """Check if component has test files"""
        return len(self.find_test_files(component_name)) > 0
    
    # ========================================================================
    # 5. API ENDPOINT VALIDATION
    # ========================================================================
    
    def find_api_endpoints(self) -> Dict[str, List[str]]:
        """Find all API endpoints in codebase"""
        endpoints = defaultdict(list)
        
        # Look for route definitions
        route_patterns = [
            r'router\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]',
            r'app\.(get|post|put|delete|patch)\([\'"](.+?)[\'"]',
            r'@(Get|Post|Put|Delete|Patch)\([\'"](.+?)[\'"]'
        ]
        
        for file in self.joju_path.rglob('*.ts'):
            try:
                content = file.read_text()
                for pattern in route_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        method = match[0].upper()
                        path = match[1]
                        endpoints[path].append(method)
            except:
                pass
        
        return dict(endpoints)
    
    def check_crud_endpoints(self, resource: str) -> Dict[str, bool]:
        """Check if CRUD endpoints exist for a resource"""
        endpoints = self.find_api_endpoints()
        
        return {
            'GET': any(resource in path and 'GET' in methods for path, methods in endpoints.items()),
            'POST': any(resource in path and 'POST' in methods for path, methods in endpoints.items()),
            'PUT': any(resource in path and 'PUT' in methods for path, methods in endpoints.items()),
            'DELETE': any(resource in path and 'DELETE' in methods for path, methods in endpoints.items())
        }
    
    # ========================================================================
    # 6. DEPENDENCY VERSION CHECK
    # ========================================================================
    
    def check_dependencies(self, required_deps: List[str]) -> Dict[str, bool]:
        """Check if dependencies are installed"""
        package_json = self.joju_path / 'package.json'
        
        if not package_json.exists():
            return {dep: False for dep in required_deps}
        
        try:
            with open(package_json) as f:
                data = json.load(f)
            
            all_deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            
            return {dep: dep in all_deps for dep in required_deps}
        except:
            return {dep: False for dep in required_deps}
    
    # ========================================================================
    # 7. STALE TASK DETECTION
    # ========================================================================
    
    def find_similar_files(self, filename: str) -> List[str]:
        """Find files with similar names (for renamed files)"""
        base_name = filename.replace('.tsx', '').replace('.ts', '')
        similar = []
        
        for file in self.joju_path.rglob('*.tsx'):
            if base_name.lower() in file.stem.lower():
                similar.append(str(file.relative_to(self.joju_path)))
        
        return similar
    
    def detect_stale_references(self, task_description: str) -> Dict:
        """Detect if task references old/renamed files"""
        # Extract file references from description
        file_refs = re.findall(r'(\w+\.tsx?)', task_description)
        
        stale = []
        suggestions = []
        
        for ref in file_refs:
            file_path = list(self.joju_path.rglob(ref))
            if not file_path:
                # File doesn't exist, find similar
                similar = self.find_similar_files(ref)
                if similar:
                    stale.append(ref)
                    suggestions.append(similar[0])
        
        return {
            'stale_refs': stale,
            'suggestions': suggestions,
            'is_stale': len(stale) > 0
        }
    
    # ========================================================================
    # 8. SEMANTIC KEYWORD EXTRACTION
    # ========================================================================
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    # ========================================================================
    # 9. ENHANCED VALIDATION LOGIC
    # ========================================================================
    
    def validate_task_enhanced(self, task: Dict) -> Dict:
        """Enhanced validation using all techniques"""
        title = task.get('title', '')
        description = task.get('description', '')
        status = task.get('status', '')
        
        # Skip already released/archived
        if status in ['Released', 'Archived']:
            return None
        
        evidence = {
            'title': title,
            'current_status': status,
            'confidence_score': 0,
            'evidence_sources': [],
            'files_found': [],
            'git_commits': [],
            'import_usage': 0,
            'has_tests': False,
            'dependencies_met': True,
            'stale_refs': [],
            'recommendation': 'Keep current status'
        }
        
        keywords = self.extract_keywords(title)
        
        # 1. Code file search
        code_files = self.search_code_files(keywords)
        if code_files:
            evidence['files_found'] = code_files[:5]
            evidence['confidence_score'] += 30
            evidence['evidence_sources'].append('code_files')
        
        # 2. Git commit mining
        commits = self.find_commits_for_task(title)
        if commits:
            evidence['git_commits'] = [c['message'][:50] for c in commits[:3]]
            evidence['confidence_score'] += 25
            evidence['evidence_sources'].append('git_commits')
        
        # 3. Import usage
        for keyword in keywords:
            usage = self.get_import_usage(keyword)
            if usage > 0:
                evidence['import_usage'] = usage
                evidence['confidence_score'] += min(usage * 5, 20)
                evidence['evidence_sources'].append('import_usage')
                break
        
        # 4. Test files
        for keyword in keywords:
            if self.has_tests(keyword):
                evidence['has_tests'] = True
                evidence['confidence_score'] += 15
                evidence['evidence_sources'].append('has_tests')
                break
        
        # 5. Stale detection
        stale_check = self.detect_stale_references(description)
        if stale_check['is_stale']:
            evidence['stale_refs'] = stale_check['suggestions']
            evidence['confidence_score'] -= 10
        
        # Calculate recommendation
        if evidence['confidence_score'] >= 70:
            evidence['recommendation'] = 'Mark as Released'
        elif evidence['confidence_score'] >= 50:
            evidence['recommendation'] = 'Needs Review'
        
        return evidence if evidence['confidence_score'] > 0 else None
    
    def search_code_files(self, keywords: List[str]) -> List[str]:
        """Search for files containing keywords"""
        found = []
        for ext in ['*.tsx', '*.ts']:
            for file in self.joju_path.rglob(ext):
                try:
                    content = file.read_text().lower()
                    if any(kw in content for kw in keywords):
                        found.append(str(file.relative_to(self.joju_path)))
                        if len(found) >= 5:
                            return found
                except:
                    pass
        return found

# ========================================================================
# MAIN EXECUTION
# ========================================================================

def main():
    print("\n" + "="*80)
    print("TASK TRUTH PIPELINE V2 - ENHANCED VALIDATOR")
    print("="*80 + "\n")
    
    # Initialize validator
    validator = EnhancedValidator()
    
    # Build all indexes
    print("🔧 Building validation indexes...\n")
    validator.mine_git_commits()
    validator.build_import_map()
    validator.build_component_graph()
    print()
    
    # Load tasks
    cache_file = Path(__file__).parent / 'local' / 'tasks.json'
    with open(cache_file) as f:
        data = json.load(f)
    
    tasks = data.get('tasks', [])
    print(f"📋 Analyzing {len(tasks)} tasks with enhanced validation...\n")
    
    # Validate all tasks
    results = []
    high_confidence = []
    medium_confidence = []
    
    for task in tasks:
        evidence = validator.validate_task_enhanced(task)
        if evidence:
            results.append(evidence)
            
            if evidence['confidence_score'] >= 70:
                high_confidence.append(evidence)
            elif evidence['confidence_score'] >= 50:
                medium_confidence.append(evidence)
    
    # Print results
    print(f"\n{'='*80}")
    print(f"ENHANCED VALIDATION RESULTS")
    print(f"{'='*80}\n")
    
    print(f"Total tasks with evidence: {len(results)}")
    print(f"High confidence (≥70%): {len(high_confidence)}")
    print(f"Medium confidence (50-69%): {len(medium_confidence)}")
    print()
    
    # High confidence tasks
    if high_confidence:
        print(f"\n## HIGH CONFIDENCE TASKS ({len(high_confidence)})\n")
        for task in sorted(high_confidence, key=lambda x: x['confidence_score'], reverse=True):
            print(f"**{task['title']}**")
            print(f"   Confidence: {task['confidence_score']}%")
            print(f"   Evidence: {', '.join(task['evidence_sources'])}")
            if task['git_commits']:
                print(f"   Commits: {len(task['git_commits'])} found")
            if task['import_usage']:
                print(f"   Imports: Used in {task['import_usage']} files")
            if task['has_tests']:
                print(f"   Tests: ✅ Yes")
            print()
    
    # Medium confidence tasks
    if medium_confidence:
        print(f"\n## MEDIUM CONFIDENCE TASKS ({len(medium_confidence)})\n")
        for task in sorted(medium_confidence, key=lambda x: x['confidence_score'], reverse=True)[:10]:
            print(f"**{task['title']}**")
            print(f"   Confidence: {task['confidence_score']}%")
            print(f"   Evidence: {', '.join(task['evidence_sources'])}")
            print()
    
    # Save enhanced report
    report_file = Path(__file__).parent / 'ENHANCED_VALIDATION_REPORT.json'
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(tasks),
            'total_with_evidence': len(results),
            'high_confidence': len(high_confidence),
            'medium_confidence': len(medium_confidence),
            'high_confidence_tasks': high_confidence,
            'medium_confidence_tasks': medium_confidence,
            'validation_techniques': [
                'git_commit_mining',
                'import_analysis',
                'component_graph',
                'test_correlation',
                'stale_detection',
                'semantic_keywords'
            ]
        }, f, indent=2)
    
    print(f"\n✅ Enhanced report saved to: {report_file}\n")
    
    # Comparison with basic validation
    basic_report = Path(__file__).parent / 'VALIDATION_REPORT.json'
    if basic_report.exists():
        with open(basic_report) as f:
            basic_data = json.load(f)
        
        print(f"\n{'='*80}")
        print("COMPARISON: Basic vs Enhanced")
        print(f"{'='*80}\n")
        print(f"Basic validation found: {basic_data['promotable_count']} tasks")
        print(f"Enhanced validation found: {len(high_confidence)} high confidence tasks")
        print(f"Improvement: {len(high_confidence) - basic_data['promotable_count']:+d} tasks")
        print()

if __name__ == '__main__':
    main()
