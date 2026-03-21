"""
Legal Contract Risk Analyzer Agent

Analyzes contract risk by:
1. Scoring overall contract risk
2. Identifying specific risk factors
3. Comparing against company risk tolerance
4. Providing risk mitigation recommendations

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class ContractRiskAnalyzer:
    """AI agent for analyzing contract risk levels"""
    
    def __init__(self):
        """Initialize the Contract Risk Analyzer with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def analyze_contract_risk(self, contract_text: str, contract_metadata: Dict) -> Dict:
        """
        Analyze contract risk across multiple dimensions
        
        Args:
            contract_text: Full contract text
            contract_metadata: Dict with contract_value, term_length, counterparty_info
            
        Returns:
            Comprehensive risk analysis with scores and recommendations
        """
        
        prompt = f"""You are an expert legal risk analyst. Analyze this contract for risk across all dimensions.

CONTRACT METADATA:
- Contract Value: {contract_metadata.get('contract_value', 'Unknown')}
- Term Length: {contract_metadata.get('term_length', 'Unknown')}
- Counterparty: {contract_metadata.get('counterparty', 'Unknown')}
- Industry: {contract_metadata.get('industry', 'Unknown')}

CONTRACT TEXT:
{contract_text[:12000]}

Analyze and provide risk assessment in JSON format:
{{
    "overall_risk_score": 75,
    "overall_risk_level": "LOW / MEDIUM / HIGH / CRITICAL",
    "recommendation": "APPROVE / APPROVE_WITH_CHANGES / REJECT / ESCALATE",
    
    "risk_categories": {{
        "financial_risk": {{
            "score": 80,
            "level": "MEDIUM",
            "factors": [
                {{"factor": "Unlimited liability exposure", "impact": "HIGH", "location": "Section 9.3"}},
                {{"factor": "No payment guarantees", "impact": "MEDIUM", "location": "Section 5.1"}}
            ],
            "mitigation": ["Cap liability at 2x contract value", "Add payment guarantee clause"]
        }},
        
        "operational_risk": {{
            "score": 60,
            "level": "LOW",
            "factors": [
                {{"factor": "Tight SLA requirements", "impact": "MEDIUM", "location": "Exhibit A"}}
            ],
            "mitigation": ["Negotiate more reasonable SLAs"]
        }},
        
        "legal_compliance_risk": {{
            "score": 85,
            "level": "LOW",
            "factors": [
                {{"factor": "Missing data privacy provisions", "impact": "MEDIUM", "location": "N/A"}}
            ],
            "mitigation": ["Add GDPR/CCPA compliance language"]
        }},
        
        "intellectual_property_risk": {{
            "score": 70,
            "level": "MEDIUM",
            "factors": [
                {{"factor": "Broad IP assignment", "impact": "HIGH", "location": "Section 6.2"}}
            ],
            "mitigation": ["Limit IP assignment to work product only"]
        }},
        
        "termination_risk": {{
            "score": 50,
            "level": "HIGH",
            "factors": [
                {{"factor": "Difficult termination provisions", "impact": "HIGH", "location": "Section 10.1"}}
            ],
            "mitigation": ["Add termination for convenience clause"]
        }},
        
        "reputational_risk": {{
            "score": 90,
            "level": "LOW",
            "factors": [],
            "mitigation": []
        }}
    }},
    
    "critical_issues": [
        {{
            "issue": "Unlimited liability clause",
            "severity": "CRITICAL",
            "location": "Section 9.3",
            "business_impact": "Company could face unlimited financial exposure",
            "probability": "LOW",
            "potential_cost": "Millions of dollars",
            "required_action": "MUST negotiate liability cap before signing"
        }}
    ],
    
    "unusual_provisions": [
        {{
            "provision": "Automatic renewal without notice",
            "concern": "Could lock company into unwanted renewal",
            "recommendation": "Change to opt-in renewal"
        }}
    ],
    
    "missing_protections": [
        {{
            "protection": "Force majeure clause",
            "importance": "HIGH",
            "recommendation": "Add standard force majeure language"
        }}
    ],
    
    "comparison_to_standards": {{
        "payment_terms": {{"standard": "Net 30", "actual": "Net 60", "variance": "Acceptable"}},
        "liability_cap": {{"standard": "2x contract value", "actual": "Unlimited", "variance": "Unacceptable"}},
        "termination_notice": {{"standard": "30 days", "actual": "90 days", "variance": "Concerning"}}
    }},
    
    "approval_requirements": {{
        "legal_review": true,
        "finance_approval": true,
        "executive_approval": true,
        "board_approval": false,
        "reasoning": "Contract value exceeds $500K and has high risk factors"
    }},
    
    "timeline_recommendations": {{
        "negotiation_priority": "HIGH",
        "target_close_date": "Within 30 days",
        "key_milestones": ["Legal review by Day 7", "Redlines by Day 14", "Final signatures by Day 30"]
    }}
}}

Be thorough and specific. Flag all material risks. Return ONLY valid JSON."""

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
            
            risk_analysis = json.loads(json_str)
            risk_analysis['analyzed_date'] = datetime.now().isoformat()
            risk_analysis['contract_value'] = contract_metadata.get('contract_value')
            risk_analysis['agent'] = 'contract_risk_analyzer'
            
            return risk_analysis
            
        except Exception as e:
            print(f"Error analyzing contract risk: {e}")
            raise
    
    def calculate_risk_score(self, risk_factors: List[Dict]) -> int:
        """
        Calculate overall risk score from individual risk factors
        
        Args:
            risk_factors: List of risk factors with severity and probability
            
        Returns:
            Risk score 0-100 (higher = more risky)
        """
        
        severity_weights = {
            'CRITICAL': 25,
            'HIGH': 15,
            'MEDIUM': 8,
            'LOW': 3
        }
        
        probability_multipliers = {
            'HIGH': 1.0,
            'MEDIUM': 0.6,
            'LOW': 0.3
        }
        
        total_score = 0
        
        for factor in risk_factors:
            severity = factor.get('severity', 'MEDIUM')
            probability = factor.get('probability', 'MEDIUM')
            
            base_score = severity_weights.get(severity, 8)
            multiplier = probability_multipliers.get(probability, 0.6)
            
            total_score += base_score * multiplier
        
        # Normalize to 0-100 scale
        normalized_score = min(100, total_score)
        
        return int(normalized_score)
    
    def compare_contracts(self, contract1_analysis: Dict, contract2_analysis: Dict) -> Dict:
        """
        Compare risk profiles of two contracts
        
        Args:
            contract1_analysis: Risk analysis of first contract
            contract2_analysis: Risk analysis of second contract
            
        Returns:
            Comparative analysis
        """
        
        score1 = contract1_analysis.get('overall_risk_score', 50)
        score2 = contract2_analysis.get('overall_risk_score', 50)
        
        comparison = {
            'contract1_score': score1,
            'contract2_score': score2,
            'score_difference': abs(score1 - score2),
            'lower_risk_contract': 'Contract 1' if score1 < score2 else 'Contract 2',
            'recommendation': 'Proceed with lower risk contract' if abs(score1 - score2) > 15 else 'Both contracts have similar risk profiles',
            
            'key_differences': []
        }
        
        # Compare critical issues
        critical1 = len(contract1_analysis.get('critical_issues', []))
        critical2 = len(contract2_analysis.get('critical_issues', []))
        
        if critical1 != critical2:
            comparison['key_differences'].append({
                'category': 'Critical Issues',
                'contract1': critical1,
                'contract2': critical2
            })
        
        return comparison
    
    def generate_risk_report(self, risk_analysis: Dict) -> str:
        """Generate executive risk report"""
        
        report = f"""
CONTRACT RISK ANALYSIS REPORT
{'='*80}
Generated: {risk_analysis.get('analyzed_date')}
Contract Value: {risk_analysis.get('contract_value', 'Unknown')}

OVERALL RISK ASSESSMENT
Overall Score: {risk_analysis.get('overall_risk_score')}/100
Risk Level: {risk_analysis.get('overall_risk_level')}
Recommendation: {risk_analysis.get('recommendation')}

CRITICAL ISSUES
"""
        
        critical = risk_analysis.get('critical_issues', [])
        if critical:
            for i, issue in enumerate(critical, 1):
                report += f"\n{i}. {issue.get('issue')}\n"
                report += f"   Severity: {issue.get('severity')}\n"
                report += f"   Impact: {issue.get('business_impact')}\n"
                report += f"   Action: {issue.get('required_action')}\n"
        else:
            report += "\nNo critical issues identified.\n"
        
        report += "\nRISK CATEGORY BREAKDOWN\n"
        categories = risk_analysis.get('risk_categories', {})
        for category, data in categories.items():
            report += f"\n{category.replace('_', ' ').title()}: {data.get('score')}/100 ({data.get('level')})\n"
        
        return report
    
    def display_risk_analysis(self, analysis: Dict):
        """Display risk analysis in readable format"""
        print("\n" + "="*80)
        print("⚠️  CONTRACT RISK ANALYSIS")
        print("="*80)
        
        score = analysis.get('overall_risk_score', 0)
        level = analysis.get('overall_risk_level', 'UNKNOWN')
        
        risk_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "⚫"}
        print(f"\n{risk_emoji.get(level, '❓')} OVERALL RISK: {level} ({score}/100)")
        print(f"📋 RECOMMENDATION: {analysis.get('recommendation')}")
        
        critical = analysis.get('critical_issues', [])
        if critical:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical)}):")
            for issue in critical[:3]:
                print(f"  • {issue.get('issue')}")
                print(f"    Impact: {issue.get('business_impact')}")
                print(f"    Action: {issue.get('required_action')}")
        
        print(f"\n📊 RISK BREAKDOWN:")
        categories = analysis.get('risk_categories', {})
        for category, data in categories.items():
            cat_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
            print(f"  {cat_emoji.get(data.get('level'), '❓')} {category.replace('_', ' ').title()}: {data.get('score')}/100")
        
        approvals = analysis.get('approval_requirements', {})
        print(f"\n✅ REQUIRED APPROVALS:")
        if approvals.get('legal_review'):
            print("  • Legal Review")
        if approvals.get('finance_approval'):
            print("  • Finance Approval")
        if approvals.get('executive_approval'):
            print("  • Executive Approval")
        
        print("\n" + "="*80)


def main():
    """Example usage of Contract Risk Analyzer"""
    
    agent = ContractRiskAnalyzer()
    
    print("✅ Contract Risk Analyzer ready!")
    print("\nTo use:")
    print("1. analysis = agent.analyze_contract_risk(contract_text, metadata)")
    print("2. agent.display_risk_analysis(analysis)")
    print("3. report = agent.generate_risk_report(analysis)")


if __name__ == "__main__":
    main()
