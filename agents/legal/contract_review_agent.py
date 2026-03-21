"""
Legal Contract Review Agent

Automates contract review by:
1. Extracting key terms, obligations, and dates
2. Identifying risky or unusual clauses
3. Comparing against standard templates
4. Generating contract summaries

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class ContractReviewAgent:
    """AI agent for automated legal contract review"""
    
    def __init__(self):
        """Initialize the Contract Review Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def review_contract(self, contract_text: str, contract_type: str = "General") -> Dict:
        """
        Review contract and extract key information
        
        Args:
            contract_text: Full text of the contract
            contract_type: Type (NDA, SaaS, Employment, Vendor, Partnership, etc.)
            
        Returns:
            Dictionary with contract analysis and risk assessment
        """
        
        prompt = f"""You are an expert contract attorney. Review this {contract_type} contract and provide a comprehensive analysis.

CONTRACT TEXT:
{contract_text[:15000]}  # Limit to avoid token overflow

Provide analysis in JSON format:
{{
    "contract_summary": {{
        "contract_type": "{contract_type}",
        "parties": [
            {{"name": "Party 1 legal name", "role": "Provider/Vendor/Employer/etc"}},
            {{"name": "Party 2 legal name", "role": "Customer/Client/Employee/etc"}}
        ],
        "effective_date": "YYYY-MM-DD or TBD",
        "expiration_date": "YYYY-MM-DD or Indefinite",
        "contract_value": "Dollar amount if specified",
        "governing_law": "Jurisdiction"
    }},
    
    "key_terms": [
        {{"term": "Payment Terms", "details": "Net 30, invoiced monthly", "location": "Section 5.2"}},
        {{"term": "Term", "details": "12 months with auto-renewal", "location": "Section 2.1"}},
        {{"term": "Termination", "details": "30 days notice required", "location": "Section 8.1"}}
    ],
    
    "obligations": {{
        "party_1_obligations": [
            {{"obligation": "Deliver services", "deadline": "Within 30 days", "section": "3.1"}},
            {{"obligation": "Maintain insurance", "deadline": "Throughout term", "section": "7.2"}}
        ],
        "party_2_obligations": [
            {{"obligation": "Pay invoice", "deadline": "Net 30", "section": "5.1"}},
            {{"obligation": "Provide access", "deadline": "Prior to start", "section": "3.2"}}
        ]
    }},
    
    "important_dates": [
        {{"date": "2026-05-01", "event": "Contract effective date"}},
        {{"date": "2027-05-01", "event": "Initial term expiration"}},
        {{"date": "2027-04-01", "event": "Renewal notice deadline"}}
    ],
    
    "risk_assessment": {{
        "overall_risk_level": "LOW / MEDIUM / HIGH / CRITICAL",
        "red_flags": [
            {{"issue": "Unlimited liability clause", "severity": "HIGH", "location": "Section 9.3", "recommendation": "Negotiate cap on liability"}}
        ],
        "unusual_terms": [
            {{"term": "Unusual provision", "concern": "Why it's unusual", "impact": "Business impact"}}
        ],
        "missing_standard_clauses": ["Force majeure", "Dispute resolution"],
        "favorable_terms": ["Early termination for convenience", "No penalties for non-renewal"]
    }},
    
    "financial_terms": {{
        "pricing_model": "Fixed / Variable / Tiered",
        "payment_schedule": "Monthly / Quarterly / Annual",
        "price_increases": "CPI-adjusted annually",
        "late_payment_penalties": "1.5% per month",
        "currency": "USD"
    }},
    
    "intellectual_property": {{
        "ip_ownership": "Who owns what",
        "work_product": "Ownership of deliverables",
        "license_grants": "What licenses are granted",
        "concerns": "IP-related concerns"
    }},
    
    "termination_provisions": {{
        "termination_for_convenience": true,
        "notice_period": "30 days",
        "termination_for_cause": "Material breach",
        "cure_period": "15 days",
        "post_termination_obligations": ["Return confidential info", "Pay outstanding invoices"]
    }},
    
    "confidentiality": {{
        "confidentiality_term": "Duration of obligations",
        "permitted_disclosures": "When disclosure is allowed",
        "return_of_materials": "Required upon termination"
    }},
    
    "liability_indemnification": {{
        "liability_cap": "Amount or multiplier",
        "indemnification_scope": "What's covered",
        "insurance_requirements": "Required insurance",
        "concerns": "Liability concerns"
    }},
    
    "recommendations": [
        {{"priority": "HIGH", "recommendation": "Negotiate liability cap", "reasoning": "Current unlimited liability"}},
        {{"priority": "MEDIUM", "recommendation": "Add force majeure clause", "reasoning": "Missing standard protection"}}
    ]
}}

Be thorough, specific, and highlight any unusual or risky provisions. Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
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
            
            analysis = json.loads(json_str)
            analysis['reviewed_date'] = datetime.now().isoformat()
            analysis['agent'] = 'contract_review_agent'
            
            return analysis
            
        except Exception as e:
            print(f"Error reviewing contract: {e}")
            raise
    
    def compare_to_template(self, contract_analysis: Dict, template_standards: Dict) -> Dict:
        """
        Compare contract against company's standard template
        
        Args:
            contract_analysis: Analysis from review_contract
            template_standards: Company's standard terms
            
        Returns:
            Deviation report
        """
        
        deviations = []
        
        # Check payment terms
        if 'financial_terms' in contract_analysis:
            contract_payment = contract_analysis['financial_terms'].get('payment_schedule')
            standard_payment = template_standards.get('payment_schedule')
            
            if contract_payment != standard_payment:
                deviations.append({
                    'category': 'Payment Terms',
                    'standard': standard_payment,
                    'actual': contract_payment,
                    'severity': 'MEDIUM'
                })
        
        # Check liability cap
        liability = contract_analysis.get('liability_indemnification', {})
        if not liability.get('liability_cap') or liability.get('liability_cap') == 'Unlimited':
            deviations.append({
                'category': 'Liability',
                'standard': template_standards.get('liability_cap', 'Capped at contract value'),
                'actual': 'Unlimited or not specified',
                'severity': 'HIGH'
            })
        
        # Check termination notice
        termination = contract_analysis.get('termination_provisions', {})
        contract_notice = termination.get('notice_period')
        standard_notice = template_standards.get('termination_notice')
        
        if contract_notice != standard_notice:
            deviations.append({
                'category': 'Termination Notice',
                'standard': standard_notice,
                'actual': contract_notice,
                'severity': 'LOW'
            })
        
        return {
            'total_deviations': len(deviations),
            'deviations': deviations,
            'template_compliance_score': max(0, 100 - (len(deviations) * 10))
        }
    
    def generate_executive_summary(self, contract_analysis: Dict) -> str:
        """Generate executive summary of contract review"""
        
        summary = contract_analysis.get('contract_summary', {})
        risk = contract_analysis.get('risk_assessment', {})
        
        parties = summary.get('parties', [])
        party_names = [p.get('name') for p in parties]
        
        exec_summary = f"""
CONTRACT REVIEW EXECUTIVE SUMMARY
{'='*80}

PARTIES: {' and '.join(party_names)}
TYPE: {summary.get('contract_type')}
VALUE: {summary.get('contract_value', 'Not specified')}
TERM: {summary.get('effective_date')} to {summary.get('expiration_date')}

RISK LEVEL: {risk.get('overall_risk_level')}

KEY CONCERNS:
"""
        
        red_flags = risk.get('red_flags', [])
        for i, flag in enumerate(red_flags[:5], 1):
            exec_summary += f"{i}. {flag.get('issue')} ({flag.get('severity')} risk)\n"
        
        recommendations = contract_analysis.get('recommendations', [])
        if recommendations:
            exec_summary += "\nTOP RECOMMENDATIONS:\n"
            for i, rec in enumerate(recommendations[:3], 1):
                exec_summary += f"{i}. [{rec.get('priority')}] {rec.get('recommendation')}\n"
        
        return exec_summary
    
    def display_review(self, analysis: Dict):
        """Display contract review in readable format"""
        print("\n" + "="*80)
        print("📄 CONTRACT REVIEW ANALYSIS")
        print("="*80)
        
        summary = analysis.get('contract_summary', {})
        print(f"\n📋 CONTRACT TYPE: {summary.get('contract_type')}")
        
        parties = summary.get('parties', [])
        print(f"👥 PARTIES:")
        for party in parties:
            print(f"  • {party.get('name')} ({party.get('role')})")
        
        print(f"\n📅 TERM: {summary.get('effective_date')} to {summary.get('expiration_date')}")
        print(f"💰 VALUE: {summary.get('contract_value', 'Not specified')}")
        
        risk = analysis.get('risk_assessment', {})
        risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "⚫"}
        print(f"\n{risk_emoji.get(risk.get('overall_risk_level'), '❓')} RISK LEVEL: {risk.get('overall_risk_level')}")
        
        red_flags = risk.get('red_flags', [])
        if red_flags:
            print(f"\n🚩 RED FLAGS ({len(red_flags)}):")
            for flag in red_flags[:3]:
                print(f"  • {flag.get('issue')} - {flag.get('severity')}")
                print(f"    → {flag.get('recommendation')}")
        
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations[:3]:
                print(f"  [{rec.get('priority')}] {rec.get('recommendation')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Contract Review Agent"""
    
    agent = ContractReviewAgent()
    
    print("✅ Contract Review Agent ready!")
    print("\nTo use:")
    print("1. analysis = agent.review_contract(contract_text, 'SaaS')")
    print("2. agent.display_review(analysis)")
    print("3. summary = agent.generate_executive_summary(analysis)")


if __name__ == "__main__":
    main()
