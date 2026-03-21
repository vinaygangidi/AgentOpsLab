"""
Legal Compliance Checker Agent

Checks documents for compliance by:
1. Verifying regulatory compliance (GDPR, CCPA, SOX, HIPAA, etc.)
2. Identifying compliance gaps
3. Generating compliance reports
4. Recommending necessary clauses

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class ComplianceCheckerAgent:
    """AI agent for checking legal and regulatory compliance"""
    
    def __init__(self):
        """Initialize the Compliance Checker Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def check_compliance(self, document_text: str, compliance_requirements: List[str]) -> Dict:
        """
        Check document against compliance requirements
        
        Args:
            document_text: Full document text
            compliance_requirements: List of regulations to check (GDPR, CCPA, SOX, HIPAA, etc.)
            
        Returns:
            Compliance report with gaps and recommendations
        """
        
        prompt = f"""You are an expert compliance attorney. Check this document against the following compliance requirements.

COMPLIANCE REQUIREMENTS TO CHECK:
{json.dumps(compliance_requirements, indent=2)}

DOCUMENT TEXT:
{document_text[:12000]}

Analyze and provide compliance assessment in JSON format:
{{
    "overall_compliance_status": "COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT / UNKNOWN",
    "compliance_score": 75,
    
    "regulatory_checks": [
        {{
            "regulation": "GDPR",
            "status": "COMPLIANT / PARTIALLY_COMPLIANT / NON_COMPLIANT / NOT_APPLICABLE",
            "required_elements": [
                {{"element": "Data processing agreement", "present": true, "location": "Section 8"}},
                {{"element": "Right to deletion", "present": false, "location": "Missing"}},
                {{"element": "Data breach notification", "present": true, "location": "Section 12"}}
            ],
            "gaps": [
                {{"gap": "Missing right to deletion clause", "severity": "HIGH", "recommendation": "Add Article 17 GDPR compliance language"}}
            ],
            "compliance_percentage": 75
        }},
        {{
            "regulation": "CCPA",
            "status": "COMPLIANT",
            "required_elements": [
                {{"element": "Consumer rights notice", "present": true, "location": "Section 9"}},
                {{"element": "Do not sell provision", "present": true, "location": "Section 10"}}
            ],
            "gaps": [],
            "compliance_percentage": 100
        }}
    ]},
    
    "industry_specific_compliance": [
        {{
            "standard": "SOX (Sarbanes-Oxley)",
            "applicable": true,
            "requirements": [
                {{"requirement": "Internal controls documentation", "met": true}},
                {{"requirement": "Audit trail requirements", "met": false}}
            ]
        }}
    ]},
    
    "missing_clauses": [
        {{
            "clause": "Force majeure",
            "regulation": "General best practice",
            "priority": "MEDIUM",
            "template_language": "Neither party shall be liable for failure to perform..."
        }},
        {{
            "clause": "Data protection addendum",
            "regulation": "GDPR Article 28",
            "priority": "HIGH",
            "template_language": "Parties agree to execute a DPA..."
        }}
    ]},
    
    "risky_language": [
        {{
            "phrase": "Unlimited data retention",
            "location": "Section 7.2",
            "regulation": "GDPR Article 5(1)(e)",
            "risk": "Violates data minimization principle",
            "recommendation": "Specify retention period and deletion schedule"
        }}
    ]},
    
    "certifications_needed": [
        {{"certification": "ISO 27001", "reason": "Data security requirements"}},
        {{"certification": "SOC 2 Type II", "reason": "Customer trust requirements"}}
    ]},
    
    "compliance_recommendations": [
        {{
            "priority": "CRITICAL",
            "recommendation": "Add GDPR-compliant data processing agreement",
            "regulation": "GDPR Article 28",
            "timeline": "Before contract execution",
            "responsible_party": "Legal"
        }},
        {{
            "priority": "HIGH",
            "recommendation": "Implement data breach notification procedures",
            "regulation": "GDPR Article 33-34",
            "timeline": "Within 30 days",
            "responsible_party": "IT Security"
        }}
    ]},
    
    "audit_requirements": {{
        "audit_frequency": "Annual",
        "audit_scope": ["Data processing", "Security controls", "Access logs"],
        "documentation_needed": ["Processing records", "Security policies", "Incident logs"]
    }}
}}

Be thorough and specific about compliance gaps. Return ONLY valid JSON."""

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
            
            compliance_report = json.loads(json_str)
            compliance_report['checked_date'] = datetime.now().isoformat()
            compliance_report['requirements_checked'] = compliance_requirements
            compliance_report['agent'] = 'compliance_checker_agent'
            
            return compliance_report
            
        except Exception as e:
            print(f"Error checking compliance: {e}")
            raise
    
    def generate_compliance_matrix(self, regulations: List[str]) -> Dict:
        """
        Generate compliance requirement matrix for given regulations
        
        Args:
            regulations: List of regulations to generate matrix for
            
        Returns:
            Compliance requirement matrix
        """
        
        prompt = f"""Create a comprehensive compliance requirement matrix for these regulations: {', '.join(regulations)}

For each regulation, provide:
1. Key requirements
2. Required documentation
3. Implementation timeline
4. Penalties for non-compliance

Return in JSON format with detailed requirements for each regulation."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
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
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error generating compliance matrix: {e}")
            raise
    
    def track_compliance_over_time(self, compliance_reports: List[Dict]) -> Dict:
        """
        Track compliance trends over multiple reports
        
        Args:
            compliance_reports: List of compliance reports over time
            
        Returns:
            Trend analysis
        """
        
        if not compliance_reports:
            return {'error': 'No reports to analyze'}
        
        scores = [report.get('compliance_score', 0) for report in compliance_reports]
        
        trend_analysis = {
            'reports_analyzed': len(compliance_reports),
            'average_score': sum(scores) / len(scores) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'improvement_trend': 'IMPROVING' if len(scores) > 1 and scores[-1] > scores[0] else 'DECLINING' if len(scores) > 1 and scores[-1] < scores[0] else 'STABLE',
            'score_change': scores[-1] - scores[0] if len(scores) > 1 else 0,
            'consistent_gaps': self._find_persistent_gaps(compliance_reports)
        }
        
        return trend_analysis
    
    def _find_persistent_gaps(self, compliance_reports: List[Dict]) -> List[str]:
        """Find compliance gaps that appear in multiple reports"""
        
        gap_counts = {}
        
        for report in compliance_reports:
            for reg_check in report.get('regulatory_checks', []):
                for gap in reg_check.get('gaps', []):
                    gap_text = gap.get('gap', '')
                    gap_counts[gap_text] = gap_counts.get(gap_text, 0) + 1
        
        # Return gaps that appear in more than half the reports
        threshold = len(compliance_reports) / 2
        persistent_gaps = [gap for gap, count in gap_counts.items() if count > threshold]
        
        return persistent_gaps
    
    def generate_remediation_plan(self, compliance_report: Dict) -> Dict:
        """
        Generate action plan to address compliance gaps
        
        Args:
            compliance_report: Compliance report with identified gaps
            
        Returns:
            Prioritized remediation plan
        """
        
        remediation_plan = {
            'plan_created': datetime.now().isoformat(),
            'total_gaps': 0,
            'critical_items': [],
            'high_priority_items': [],
            'medium_priority_items': [],
            'timeline': {}
        }
        
        # Collect all gaps from regulatory checks
        for reg_check in compliance_report.get('regulatory_checks', []):
            for gap in reg_check.get('gaps', []):
                severity = gap.get('severity', 'MEDIUM')
                
                item = {
                    'gap': gap.get('gap'),
                    'regulation': reg_check.get('regulation'),
                    'recommendation': gap.get('recommendation'),
                    'severity': severity
                }
                
                if severity == 'CRITICAL':
                    remediation_plan['critical_items'].append(item)
                elif severity == 'HIGH':
                    remediation_plan['high_priority_items'].append(item)
                else:
                    remediation_plan['medium_priority_items'].append(item)
        
        remediation_plan['total_gaps'] = (
            len(remediation_plan['critical_items']) +
            len(remediation_plan['high_priority_items']) +
            len(remediation_plan['medium_priority_items'])
        )
        
        # Generate timeline
        remediation_plan['timeline'] = {
            'immediate': f"{len(remediation_plan['critical_items'])} critical items - Address within 7 days",
            'short_term': f"{len(remediation_plan['high_priority_items'])} high priority - Address within 30 days",
            'medium_term': f"{len(remediation_plan['medium_priority_items'])} medium priority - Address within 90 days"
        }
        
        return remediation_plan
    
    def display_compliance_report(self, compliance_report: Dict):
        """Display compliance report in readable format"""
        print("\n" + "="*80)
        print("✅ COMPLIANCE CHECK REPORT")
        print("="*80)
        
        status = compliance_report.get('overall_compliance_status')
        score = compliance_report.get('compliance_score', 0)
        
        status_emoji = {
            'COMPLIANT': '✅',
            'PARTIALLY_COMPLIANT': '⚠️',
            'NON_COMPLIANT': '❌',
            'UNKNOWN': '❓'
        }
        
        print(f"\n{status_emoji.get(status, '❓')} STATUS: {status}")
        print(f"📊 COMPLIANCE SCORE: {score}%")
        
        print(f"\n📋 REGULATORY CHECKS:")
        for reg_check in compliance_report.get('regulatory_checks', []):
            reg_status = reg_check.get('status')
            reg_emoji = status_emoji.get(reg_status, '❓')
            print(f"  {reg_emoji} {reg_check.get('regulation')}: {reg_check.get('compliance_percentage')}%")
            
            gaps = reg_check.get('gaps', [])
            if gaps:
                for gap in gaps[:2]:
                    print(f"      • {gap.get('gap')}")
        
        missing = compliance_report.get('missing_clauses', [])
        if missing:
            print(f"\n⚠️  MISSING CLAUSES ({len(missing)}):")
            for clause in missing[:3]:
                print(f"  • {clause.get('clause')} ({clause.get('priority')} priority)")
        
        recommendations = compliance_report.get('compliance_recommendations', [])
        if recommendations:
            print(f"\n💡 TOP RECOMMENDATIONS:")
            for rec in recommendations[:3]:
                print(f"  [{rec.get('priority')}] {rec.get('recommendation')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Compliance Checker Agent"""
    
    agent = ComplianceCheckerAgent()
    
    print("✅ Compliance Checker Agent ready!")
    print("\nTo use:")
    print("1. report = agent.check_compliance(document_text, ['GDPR', 'CCPA', 'SOX'])")
    print("2. agent.display_compliance_report(report)")
    print("3. plan = agent.generate_remediation_plan(report)")


if __name__ == "__main__":
    main()
