"""
Legal NDA Generator Agent

Generates custom NDAs by:
1. Creating mutual or one-way NDAs
2. Customizing terms based on use case
3. Filling in party details automatically
4. Ensuring legal compliance

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class NDAGeneratorAgent:
    """AI agent for generating custom Non-Disclosure Agreements"""
    
    def __init__(self):
        """Initialize the NDA Generator Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def generate_nda(self, nda_params: Dict) -> Dict:
        """
        Generate customized NDA based on parameters
        
        Args:
            nda_params: Dict with type, parties, purpose, duration, jurisdiction
            
        Returns:
            Dictionary with NDA text and metadata
        """
        
        prompt = f"""You are an expert corporate attorney. Generate a professional Non-Disclosure Agreement (NDA) based on these specifications.

NDA PARAMETERS:
- Type: {nda_params.get('nda_type', 'Mutual')} (Mutual / One-Way)
- Purpose: {nda_params.get('purpose')}
- Duration: {nda_params.get('confidentiality_term', '3 years')}
- Jurisdiction: {nda_params.get('jurisdiction', 'Delaware')}

PARTY 1 (Disclosing Party or Mutual):
- Legal Name: {nda_params.get('party1_name')}
- Address: {nda_params.get('party1_address')}
- Contact: {nda_params.get('party1_contact', 'Not specified')}

PARTY 2 (Receiving Party or Mutual):
- Legal Name: {nda_params.get('party2_name')}
- Address: {nda_params.get('party2_address')}
- Contact: {nda_params.get('party2_contact', 'Not specified')}

SPECIAL PROVISIONS:
{json.dumps(nda_params.get('special_provisions', []), indent=2)}

Generate a complete, professional NDA that includes:

1. PREAMBLE - Effective date and parties
2. RECITALS - Purpose and background
3. DEFINITIONS - Define Confidential Information clearly
4. CONFIDENTIALITY OBLIGATIONS - What must be kept confidential
5. PERMITTED DISCLOSURES - Exceptions (required by law, etc.)
6. TERM - Duration of confidentiality obligations
7. RETURN OF MATERIALS - Requirement to return/destroy
8. NO LICENSE - Clarify no IP transfer
9. REMEDIES - Injunctive relief, damages
10. MISCELLANEOUS - Governing law, entire agreement, amendments, etc.

Format as a professional legal document with:
- Clear section numbering
- Proper legal language
- Signature blocks
- Date fields

Return both the full NDA text AND a JSON summary."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            nda_content = response.content[0].text
            
            # Extract the NDA document and summary
            if "```" in nda_content:
                # Split document from JSON summary
                parts = nda_content.split("```")
                nda_text = parts[0].strip() if len(parts) > 0 else nda_content
                
                # Try to find JSON summary
                json_summary = {}
                for part in parts:
                    if "json" in part.lower():
                        try:
                            json_str = part.replace("json", "").strip()
                            json_summary = json.loads(json_str)
                        except:
                            pass
            else:
                nda_text = nda_content
                json_summary = {}
            
            result = {
                'nda_document': nda_text,
                'metadata': {
                    'nda_type': nda_params.get('nda_type'),
                    'party1': nda_params.get('party1_name'),
                    'party2': nda_params.get('party2_name'),
                    'purpose': nda_params.get('purpose'),
                    'term': nda_params.get('confidentiality_term'),
                    'jurisdiction': nda_params.get('jurisdiction'),
                    'generated_date': datetime.now().isoformat(),
                    'agent': 'nda_generator_agent'
                },
                'summary': json_summary
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating NDA: {e}")
            raise
    
    def generate_nda_checklist(self, nda_type: str, use_case: str) -> List[Dict]:
        """
        Generate checklist of terms to include based on NDA type and use case
        
        Args:
            nda_type: Mutual or One-Way
            use_case: Vendor relationship, M&A, Partnership, etc.
            
        Returns:
            List of required and optional clauses
        """
        
        prompt = f"""Create a comprehensive checklist of clauses for a {nda_type} NDA for {use_case}.

Provide in JSON format:
{{
    "required_clauses": [
        {{"clause": "Definition of Confidential Information", "importance": "CRITICAL", "notes": "Must be clear and comprehensive"}},
        {{"clause": "Non-disclosure obligations", "importance": "CRITICAL", "notes": "Core of the agreement"}}
    ],
    "recommended_clauses": [
        {{"clause": "Non-solicitation", "importance": "HIGH", "notes": "Prevents poaching employees"}},
        {{"clause": "Non-compete", "importance": "MEDIUM", "notes": "May be enforceable depending on jurisdiction"}}
    ],
    "optional_clauses": [
        {{"clause": "Standstill provision", "importance": "LOW", "notes": "Relevant for M&A discussions"}}
    ],
    "jurisdiction_specific": [
        {{"clause": "Choice of law", "notes": "Specify which state law governs"}},
        {{"clause": "Venue", "notes": "Where disputes will be resolved"}}
    ]
}}

Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            checklist = json.loads(json_str)
            return checklist
            
        except Exception as e:
            print(f"Error generating checklist: {e}")
            raise
    
    def customize_nda_for_scenario(self, base_nda: str, scenario_params: Dict) -> str:
        """
        Customize an existing NDA template for a specific scenario
        
        Args:
            base_nda: Base NDA template text
            scenario_params: Specific customizations needed
            
        Returns:
            Customized NDA text
        """
        
        prompt = f"""Customize this NDA template for the following scenario:

SCENARIO:
{json.dumps(scenario_params, indent=2)}

BASE NDA TEMPLATE:
{base_nda[:8000]}

Customize by:
1. Adjusting the definition of Confidential Information
2. Modifying the term/duration
3. Adding or removing specific provisions
4. Tailoring language to the relationship type

Return the complete customized NDA."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error customizing NDA: {e}")
            raise
    
    def validate_nda_completeness(self, nda_text: str) -> Dict:
        """
        Validate that NDA contains all essential clauses
        
        Args:
            nda_text: NDA document text to validate
            
        Returns:
            Validation report with missing or weak clauses
        """
        
        essential_clauses = [
            'confidential information',
            'obligations',
            'term',
            'return of materials',
            'remedies',
            'governing law',
            'signature'
        ]
        
        validation_report = {
            'complete': True,
            'missing_clauses': [],
            'weak_clauses': [],
            'recommendations': []
        }
        
        nda_lower = nda_text.lower()
        
        for clause in essential_clauses:
            if clause not in nda_lower:
                validation_report['complete'] = False
                validation_report['missing_clauses'].append(clause)
                validation_report['recommendations'].append(
                    f"Add {clause} section"
                )
        
        # Check for common weaknesses
        if 'injunctive relief' not in nda_lower:
            validation_report['weak_clauses'].append('Remedies section may be weak - consider adding injunctive relief')
        
        if 'entire agreement' not in nda_lower:
            validation_report['weak_clauses'].append('Missing entire agreement clause')
        
        return validation_report
    
    def save_nda(self, nda_data: Dict, filename: str):
        """Save generated NDA to file"""
        
        nda_text = nda_data.get('nda_document', '')
        
        # Add header with metadata
        metadata = nda_data.get('metadata', {})
        header = f"""
{'='*80}
NDA GENERATED BY AGENTOPSLAB
Generated: {metadata.get('generated_date')}
Type: {metadata.get('nda_type')}
Parties: {metadata.get('party1')} and {metadata.get('party2')}
{'='*80}

{nda_text}
"""
        
        with open(filename, 'w') as f:
            f.write(header)
        
        print(f"✅ NDA saved to {filename}")


def main():
    """Example usage of NDA Generator Agent"""
    
    agent = NDAGeneratorAgent()
    
    # Example NDA parameters
    nda_params = {
        'nda_type': 'Mutual',
        'purpose': 'Discussions regarding potential business partnership',
        'confidentiality_term': '3 years',
        'jurisdiction': 'Delaware',
        'party1_name': 'Acme Corporation',
        'party1_address': '123 Main St, San Francisco, CA 94102',
        'party2_name': 'TechVentures Inc.',
        'party2_address': '456 Market St, San Jose, CA 95113',
        'special_provisions': [
            'Include non-solicitation of employees',
            'Exclude publicly available information'
        ]
    }
    
    print("✅ NDA Generator Agent ready!")
    print("\nTo use:")
    print("1. nda = agent.generate_nda(nda_params)")
    print("2. agent.save_nda(nda, 'output.txt')")
    print("3. validation = agent.validate_nda_completeness(nda_text)")


if __name__ == "__main__":
    main()
