#!/usr/bin/env python3
"""
Contact Matrix Manager
Manages contact information and relationship context
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class ContactMatrix:
    """Manages contact relationships and communication patterns"""
    
    def __init__(self, data_file: str = None):
        """
        Initialize contact matrix
        
        Args:
            data_file: Path to contact matrix JSON file
        """
        if data_file is None:
            data_file = Path(__file__).parent.parent / "data" / "contact_matrix.json"
        
        self.data_file = Path(data_file)
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> Dict:
        """Load contacts from file"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"contacts": [], "last_updated": datetime.now().isoformat()}
    
    def _save_contacts(self):
        """Save contacts to file"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.contacts['last_updated'] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def find_contact(self, name: str = None, phone: str = None, email: str = None) -> Optional[Dict]:
        """
        Find contact by name, phone, or email
        
        Args:
            name: Contact name
            phone: Phone number
            email: Email address
        
        Returns:
            Contact dict or None
        """
        for contact in self.contacts.get('contacts', []):
            if name and name.lower() in contact.get('name', '').lower():
                return contact
            if phone and phone in contact.get('phone', ''):
                return contact
            if email and email.lower() in contact.get('email', '').lower():
                return contact
        
        return None
    
    def add_contact(self, contact_data: Dict) -> str:
        """
        Add new contact
        
        Args:
            contact_data: Contact information
        
        Returns:
            Contact ID
        """
        # Generate ID
        contact_id = f"contact_{len(self.contacts.get('contacts', [])) + 1}"
        
        # Create contact entry
        contact = {
            "contact_id": contact_id,
            "name": contact_data.get('name', ''),
            "email": contact_data.get('email', ''),
            "phone": contact_data.get('phone', ''),
            "relationship": {
                "type": contact_data.get('relationship_type', 'professional'),
                "closeness": contact_data.get('closeness', 5),
                "formality": contact_data.get('formality', 'professional'),
                "communication_style": contact_data.get('communication_style', 'direct')
            },
            "context": {
                "current_projects": [],
                "shared_history": [],
                "communication_patterns": {},
                "preferences": {}
            },
            "interaction_history": {
                "last_contact": datetime.now().isoformat(),
                "frequency": "unknown",
                "typical_topics": [],
                "response_patterns": {}
            },
            "notes": contact_data.get('notes', ''),
            "tags": contact_data.get('tags', [])
        }
        
        # Add to contacts
        if 'contacts' not in self.contacts:
            self.contacts['contacts'] = []
        
        self.contacts['contacts'].append(contact)
        self._save_contacts()
        
        return contact_id
    
    def update_contact(self, contact_id: str, updates: Dict):
        """
        Update contact information
        
        Args:
            contact_id: Contact ID
            updates: Dictionary of updates
        """
        for contact in self.contacts.get('contacts', []):
            if contact['contact_id'] == contact_id:
                contact.update(updates)
                self._save_contacts()
                return True
        
        return False
    
    def log_interaction(self, contact_id: str, interaction_data: Dict):
        """
        Log an interaction with a contact
        
        Args:
            contact_id: Contact ID
            interaction_data: Interaction details
        """
        for contact in self.contacts.get('contacts', []):
            if contact['contact_id'] == contact_id:
                # Update last contact
                contact['interaction_history']['last_contact'] = datetime.now().isoformat()
                
                # Add to history
                if 'interactions' not in contact:
                    contact['interactions'] = []
                
                contact['interactions'].append({
                    'timestamp': datetime.now().isoformat(),
                    'type': interaction_data.get('type', 'message'),
                    'summary': interaction_data.get('summary', ''),
                    'response_used': interaction_data.get('response_used', None)
                })
                
                self._save_contacts()
                return True
        
        return False
    
    def get_relationship_context(self, contact_id: str) -> Dict:
        """
        Get relationship context for response generation
        
        Args:
            contact_id: Contact ID
        
        Returns:
            Relationship context dict
        """
        contact = None
        for c in self.contacts.get('contacts', []):
            if c['contact_id'] == contact_id:
                contact = c
                break
        
        if not contact:
            return self._default_context()
        
        return {
            'relationship_type': contact['relationship']['type'],
            'closeness': contact['relationship']['closeness'],
            'formality': contact['relationship']['formality'],
            'communication_style': contact['relationship']['communication_style'],
            'current_projects': contact['context']['current_projects'],
            'preferences': contact['context']['preferences']
        }
    
    def _default_context(self) -> Dict:
        """Default relationship context for unknown contacts"""
        return {
            'relationship_type': 'professional',
            'closeness': 5,
            'formality': 'professional',
            'communication_style': 'direct',
            'current_projects': [],
            'preferences': {}
        }
    
    def list_contacts(self, filter_by: Dict = None) -> List[Dict]:
        """
        List all contacts with optional filtering
        
        Args:
            filter_by: Optional filter criteria
        
        Returns:
            List of contacts
        """
        contacts = self.contacts.get('contacts', [])
        
        if not filter_by:
            return contacts
        
        # Apply filters
        filtered = []
        for contact in contacts:
            match = True
            
            if 'relationship_type' in filter_by:
                if contact['relationship']['type'] != filter_by['relationship_type']:
                    match = False
            
            if 'tags' in filter_by:
                if not any(tag in contact.get('tags', []) for tag in filter_by['tags']):
                    match = False
            
            if match:
                filtered.append(contact)
        
        return filtered

if __name__ == "__main__":
    # Test
    matrix = ContactMatrix()
    
    # Add test contact
    contact_id = matrix.add_contact({
        'name': 'John Doe',
        'email': 'john@example.com',
        'relationship_type': 'professional',
        'closeness': 7,
        'formality': 'professional',
        'communication_style': 'direct'
    })
    
    print(f"Added contact: {contact_id}")
    
    # Find contact
    contact = matrix.find_contact(name="John")
    print(f"\nFound contact: {contact['name']}")
    
    # Get context
    context = matrix.get_relationship_context(contact_id)
    print(f"\nRelationship context: {json.dumps(context, indent=2)}")
