"""
Legal Document Classifier Agent

Classifies legal documents by:
1. Identifying document type automatically
2. Extracting key metadata
3. Routing to appropriate team or workflow
4. Organizing documents by category

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class LegalDocumentClassifier:
    """AI agent for classifying and routing legal documents"""
    
    def __init__(self):
        """Initialize the Legal Document Classifier with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def classify_document(self, document_text: str, filename: str = "") -> Dict:
        """
        Classify legal document and extract metadata
        
        Args:
            document_text: Full document text
            filename: Optional filename for additional context
            
        Returns:
            Classification with type, metadata, and routing information
        """
        
        prompt = f"""You are an expert legal document analyst. Classify this document and extract key metadata.

FILENAME: {filename}

DOCUMENT TEXT:
{document_text[:10000]}

Analyze and provide classification in JSON format:
{{
    "document_type": "Contract / NDA / Agreement / Policy / Memo / Letter / Amendment / Addendum / SOW / MSA / Other",
    "document_subtype": "More specific type (e.g., Employment Contract, SaaS Agreement, etc.)",
    "confidence_score": 95,
    
    "metadata": {{
        "parties": [
            {{"name": "Party name", "role": "Vendor/Customer/Employer/etc"}},
            {{"name": "Party 2 name", "role": "Role"}}
        ],
        "effective_date": "YYYY-MM-DD or null",
        "expiration_date": "YYYY-MM-DD or null",
        "document_date": "YYYY-MM-DD or null",
        "jurisdiction": "State/Country",
        "contract_value": "Dollar amount if applicable",
        "key_terms": ["Term 1", "Term 2", "Term 3"]
    }},
    
    "classification_reasoning": "Why this classification was chosen",
    
    "routing": {{
        "primary_team": "Legal / Contracts / Procurement / HR / Finance / Risk / Compliance",
        "secondary_teams": ["Team 1", "Team 2"],
        "priority": "URGENT / HIGH / MEDIUM / LOW",
        "requires_approval": true,
        "approvers": ["Legal Counsel", "CFO"]
    }},
    
    "document_characteristics": {{
        "is_executed": true,
        "is_template": false,
        "is_amendment": false,
        "is_renewal": false,
        "has_signature": true,
        "has_exhibits": true,
        "page_count_estimate": 12
    }},
    
    "action_items": [
        {{"action": "Review and execute", "owner": "Legal", "deadline": "Within 5 business days"}},
        {{"action": "Add to contract database", "owner": "Contracts team", "deadline": "Immediately"}}
    ]},
    
    "tags": ["vendor_contract", "saas", "technology", "recurring_revenue"],
    
    "compliance_flags": [
        {{"flag": "Contains personal data", "regulation": "GDPR", "action_required": "Add DPA"}}
    ]
}}

Be specific and accurate. Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.2,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            response_text = response.content[0].text
            
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            classification = json.loads(json_str)
            classification['filename'] = filename
            classification['classified_date'] = datetime.now().isoformat()
            classification['agent'] = 'legal_document_classifier'
            
            return classification
            
        except Exception as e:
            print(f"Error classifying document: {e}")
            raise
    
    def batch_classify_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Classify multiple documents in batch
        
        Args:
            documents: List of dicts with 'text' and 'filename'
            
        Returns:
            List of classification results
        """
        
        classifications = []
        
        for doc in documents:
            try:
                classification = self.classify_document(
                    doc.get('text', ''),
                    doc.get('filename', '')
                )
                classifications.append(classification)
            except Exception as e:
                print(f"Error classifying {doc.get('filename')}: {e}")
                classifications.append({
                    'filename': doc.get('filename'),
                    'error': str(e),
                    'document_type': 'UNKNOWN'
                })
        
        return classifications
    
    def generate_filing_structure(self, classifications: List[Dict]) -> Dict:
        """
        Generate recommended filing/folder structure based on classified documents
        
        Args:
            classifications: List of document classifications
            
        Returns:
            Recommended folder structure
        """
        
        folder_structure = {}
        
        for classification in classifications:
            doc_type = classification.get('document_type', 'Other')
            subtype = classification.get('document_subtype', 'General')
            
            if doc_type not in folder_structure:
                folder_structure[doc_type] = {}
            
            if subtype not in folder_structure[doc_type]:
                folder_structure[doc_type][subtype] = []
            
            folder_structure[doc_type][subtype].append(classification.get('filename', 'Unknown'))
        
        return {
            'folder_structure': folder_structure,
            'total_documents': len(classifications),
            'document_types_count': len(folder_structure),
            'recommendation': 'Organize documents in this folder hierarchy'
        }
    
    def extract_document_relationships(self, classifications: List[Dict]) -> List[Dict]:
        """
        Identify relationships between documents (amendments, renewals, etc.)
        
        Args:
            classifications: List of document classifications
            
        Returns:
            List of related document groups
        """
        
        relationships = []
        
        # Group by parties involved
        party_groups = {}
        for classification in classifications:
            parties = classification.get('metadata', {}).get('parties', [])
            if parties:
                party_key = tuple(sorted([p.get('name', '') for p in parties]))
                if party_key not in party_groups:
                    party_groups[party_key] = []
                party_groups[party_key].append(classification)
        
        # Find related documents
        for parties, docs in party_groups.items():
            if len(docs) > 1:
                # Check for amendments, renewals, etc.
                base_docs = [d for d in docs if not d.get('document_characteristics', {}).get('is_amendment')]
                amendments = [d for d in docs if d.get('document_characteristics', {}).get('is_amendment')]
                
                if base_docs and amendments:
                    relationships.append({
                        'relationship_type': 'AMENDMENT',
                        'base_document': base_docs[0].get('filename'),
                        'related_documents': [a.get('filename') for a in amendments],
                        'parties': list(parties)
                    })
        
        return relationships
    
    def generate_document_summary_report(self, classifications: List[Dict]) -> str:
        """Generate summary report of all classified documents"""
        
        total_docs = len(classifications)
        
        # Count by type
        type_counts = {}
        for classification in classifications:
            doc_type = classification.get('document_type', 'Unknown')
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        # Count by priority
        priority_counts = {}
        for classification in classifications:
            priority = classification.get('routing', {}).get('priority', 'MEDIUM')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Identify documents needing immediate action
        urgent_docs = [c for c in classifications if c.get('routing', {}).get('priority') == 'URGENT']
        
        report = f"""
LEGAL DOCUMENT CLASSIFICATION REPORT
{'='*80}
Generated: {datetime.now().isoformat()}
Total Documents: {total_docs}

DOCUMENT TYPES:
"""
        
        for doc_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  {doc_type}: {count}\n"
        
        report += f"\nPRIORITY DISTRIBUTION:\n"
        for priority, count in sorted(priority_counts.items()):
            report += f"  {priority}: {count}\n"
        
        if urgent_docs:
            report += f"\n🚨 URGENT DOCUMENTS REQUIRING IMMEDIATE ATTENTION:\n"
            for doc in urgent_docs[:10]:
                report += f"  • {doc.get('filename')} - {doc.get('document_type')}\n"
        
        return report
    
    def display_classification(self, classification: Dict):
        """Display document classification in readable format"""
        print("\n" + "="*80)
        print("📁 DOCUMENT CLASSIFICATION")
        print("="*80)
        
        print(f"\n📄 FILE: {classification.get('filename')}")
        print(f"📋 TYPE: {classification.get('document_type')} - {classification.get('document_subtype')}")
        print(f"✅ CONFIDENCE: {classification.get('confidence_score')}%")
        
        metadata = classification.get('metadata', {})
        parties = metadata.get('parties', [])
        if parties:
            print(f"\n👥 PARTIES:")
            for party in parties:
                print(f"  • {party.get('name')} ({party.get('role')})")
        
        print(f"\n📅 DATES:")
        print(f"  Effective: {metadata.get('effective_date', 'N/A')}")
        print(f"  Expiration: {metadata.get('expiration_date', 'N/A')}")
        
        routing = classification.get('routing', {})
        print(f"\n🔀 ROUTING:")
        print(f"  Primary Team: {routing.get('primary_team')}")
        print(f"  Priority: {routing.get('priority')}")
        
        actions = classification.get('action_items', [])
        if actions:
            print(f"\n✓ ACTION ITEMS:")
            for action in actions[:3]:
                print(f"  • {action.get('action')} - {action.get('owner')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Legal Document Classifier"""
    
    agent = LegalDocumentClassifier()
    
    print("✅ Legal Document Classifier ready!")
    print("\nTo use:")
    print("1. classification = agent.classify_document(document_text, 'contract.pdf')")
    print("2. agent.display_classification(classification)")
    print("3. report = agent.generate_document_summary_report(classifications)")


if __name__ == "__main__":
    main()
