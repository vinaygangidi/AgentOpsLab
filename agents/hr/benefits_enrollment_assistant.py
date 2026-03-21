"""
HR Benefits Enrollment Assistant Agent

Helps employees with benefits enrollment by:
1. Answering benefits questions using AI
2. Recommending optimal benefit choices based on employee profile
3. Calculating costs and comparing plans
4. Tracking enrollment completion

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class BenefitsEnrollmentAssistant:
    """AI agent for assisting employees with benefits enrollment"""
    
    def __init__(self):
        """Initialize the Benefits Enrollment Assistant with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def recommend_benefits(self, employee_profile: Dict, available_benefits: Dict) -> Dict:
        """
        Recommend optimal benefits package based on employee profile
        
        Args:
            employee_profile: Dict with age, family_status, health_conditions, salary, risk_tolerance
            available_benefits: Dict with health_plans, dental_plans, vision_plans, retirement_options
            
        Returns:
            Dictionary with personalized recommendations and cost analysis
        """
        
        prompt = f"""You are an expert benefits advisor. Recommend the best benefits package for this employee.

EMPLOYEE PROFILE:
- Age: {employee_profile.get('age')}
- Family Status: {employee_profile.get('family_status')} (Single / Married / Family)
- Dependents: {employee_profile.get('dependents', 0)}
- Annual Salary: ${employee_profile.get('salary', 0):,}
- Health Considerations: {employee_profile.get('health_considerations', 'None specified')}
- Risk Tolerance: {employee_profile.get('risk_tolerance', 'Medium')} (Low / Medium / High)
- Current Life Stage: {employee_profile.get('life_stage', 'Mid-career')}

AVAILABLE BENEFITS:
{json.dumps(available_benefits, indent=2)}

Provide personalized recommendations in JSON format:
{{
    "health_insurance": {{
        "recommended_plan": "Plan name",
        "reasoning": "Why this plan fits",
        "monthly_premium": 450.00,
        "annual_deductible": 1500,
        "out_of_pocket_max": 6000,
        "why_not_alternatives": "Why other plans weren't chosen"
    }},
    
    "dental_insurance": {{
        "recommended_plan": "Plan name",
        "reasoning": "Why this plan fits",
        "monthly_premium": 45.00
    }},
    
    "vision_insurance": {{
        "recommended_plan": "Plan name",
        "reasoning": "Why this plan fits",
        "monthly_premium": 12.00
    }},
    
    "retirement_401k": {{
        "recommended_contribution": "Percentage of salary",
        "reasoning": "Why this amount",
        "employer_match": "Percentage matched",
        "annual_contribution": 7500.00,
        "investment_strategy": "Aggressive / Moderate / Conservative"
    }},
    
    "life_insurance": {{
        "recommended_coverage": "Amount (e.g., 2x salary)",
        "reasoning": "Why this amount",
        "monthly_premium": 25.00
    }},
    
    "disability_insurance": {{
        "short_term": {{"recommended": true, "reasoning": "Why"}},
        "long_term": {{"recommended": true, "reasoning": "Why"}}
    }},
    
    "fsa_hsa": {{
        "type": "FSA / HSA / None",
        "recommended_contribution": 2000.00,
        "reasoning": "Why this account and amount",
        "tax_savings_estimate": 500.00
    }},
    
    "total_cost_summary": {{
        "monthly_employee_contribution": 650.00,
        "annual_employee_contribution": 7800.00,
        "annual_employer_contribution": 12000.00,
        "total_benefits_value": 19800.00,
        "percentage_of_salary": 7.8
    }},
    
    "key_recommendations": [
        "Recommendation 1 with specific action",
        "Recommendation 2 with specific action"
    ],
    
    "cost_optimization_tips": [
        "Tip 1 to save money",
        "Tip 2 to maximize value"
    ],
    
    "important_deadlines": [
        {{"deadline": "2026-04-30", "item": "Open enrollment ends"}}
    ]
}}

Be specific with numbers and provide clear reasoning. Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3500,
                temperature=0.4,
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
            
            recommendations = json.loads(json_str)
            recommendations['employee_age'] = employee_profile.get('age')
            recommendations['generated_date'] = datetime.now().isoformat()
            recommendations['agent'] = 'benefits_enrollment_assistant'
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating benefits recommendations: {e}")
            raise
    
    def answer_benefits_question(self, question: str, benefits_context: Dict) -> str:
        """
        Answer employee benefits questions using Claude AI
        
        Args:
            question: Employee's question about benefits
            benefits_context: Context about available benefits
            
        Returns:
            Clear, helpful answer to the question
        """
        
        prompt = f"""You are a friendly benefits advisor helping an employee understand their benefits.

AVAILABLE BENEFITS CONTEXT:
{json.dumps(benefits_context, indent=2)}

EMPLOYEE QUESTION:
{question}

Provide a clear, helpful answer that:
1. Directly answers the question
2. Explains any relevant terms or concepts
3. Provides specific examples if helpful
4. Mentions any important deadlines or actions needed
5. Is friendly and encouraging

Keep the answer concise (2-4 paragraphs) and easy to understand."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.6,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error answering benefits question: {e}")
            raise
    
    def compare_health_plans(self, plans: List[Dict], employee_usage_pattern: Dict) -> Dict:
        """
        Compare health insurance plans based on employee usage patterns
        
        Args:
            plans: List of health plan dictionaries
            employee_usage_pattern: Expected medical usage (doctor_visits, prescriptions, etc.)
            
        Returns:
            Comparison with total cost estimates
        """
        
        comparisons = []
        
        for plan in plans:
            # Calculate estimated annual cost
            annual_premium = plan.get('monthly_premium', 0) * 12
            
            # Estimate out-of-pocket costs based on usage
            doctor_visits = employee_usage_pattern.get('doctor_visits_per_year', 3)
            prescriptions = employee_usage_pattern.get('prescriptions_per_month', 1)
            
            copay_costs = (doctor_visits * plan.get('office_visit_copay', 30) +
                          prescriptions * 12 * plan.get('prescription_copay', 15))
            
            estimated_total = annual_premium + min(copay_costs, plan.get('out_of_pocket_max', 5000))
            
            comparisons.append({
                'plan_name': plan.get('name'),
                'monthly_premium': plan.get('monthly_premium'),
                'annual_premium': annual_premium,
                'deductible': plan.get('deductible'),
                'out_of_pocket_max': plan.get('out_of_pocket_max'),
                'estimated_annual_cost': estimated_total,
                'network_size': plan.get('network_size', 'Unknown'),
                'best_for': self._determine_best_fit(plan, employee_usage_pattern)
            })
        
        # Sort by estimated total cost
        comparisons.sort(key=lambda x: x['estimated_annual_cost'])
        
        return {
            'plans_compared': len(comparisons),
            'comparison': comparisons,
            'recommendation': comparisons[0]['plan_name'] if comparisons else None,
            'potential_savings': comparisons[-1]['estimated_annual_cost'] - comparisons[0]['estimated_annual_cost'] if len(comparisons) > 1 else 0
        }
    
    def _determine_best_fit(self, plan: Dict, usage: Dict) -> str:
        """Determine what type of user this plan is best for"""
        
        if plan.get('monthly_premium', 0) < 200 and plan.get('deductible', 0) > 3000:
            return "Low usage, healthy individuals"
        elif plan.get('monthly_premium', 0) > 400 and plan.get('deductible', 0) < 1000:
            return "High usage, frequent medical care"
        else:
            return "Average usage, moderate medical needs"
    
    def track_enrollment_completion(self, employee_id: str, enrolled_benefits: Dict) -> Dict:
        """Track which benefits employee has enrolled in"""
        
        required_benefits = ['health_insurance', 'retirement_401k']
        optional_benefits = ['dental_insurance', 'vision_insurance', 'life_insurance', 'disability_insurance']
        
        completion_status = {
            'employee_id': employee_id,
            'enrollment_complete': all(benefit in enrolled_benefits for benefit in required_benefits),
            'required_benefits_enrolled': sum(1 for b in required_benefits if b in enrolled_benefits),
            'total_required': len(required_benefits),
            'optional_benefits_enrolled': sum(1 for b in optional_benefits if b in enrolled_benefits),
            'total_optional': len(optional_benefits),
            'missing_required': [b for b in required_benefits if b not in enrolled_benefits],
            'completion_percentage': (
                (sum(1 for b in required_benefits if b in enrolled_benefits) / len(required_benefits) * 100)
                if required_benefits else 0
            )
        }
        
        return completion_status
    
    def display_recommendations(self, recommendations: Dict):
        """Display benefits recommendations in readable format"""
        print("\n" + "="*80)
        print("💼 PERSONALIZED BENEFITS RECOMMENDATIONS")
        print("="*80)
        
        health = recommendations.get('health_insurance', {})
        print(f"\n🏥 HEALTH INSURANCE: {health.get('recommended_plan')}")
        print(f"   Premium: ${health.get('monthly_premium', 0)}/month")
        print(f"   Reasoning: {health.get('reasoning')}")
        
        retirement = recommendations.get('retirement_401k', {})
        print(f"\n💰 401(K) RETIREMENT:")
        print(f"   Recommended: {retirement.get('recommended_contribution')} of salary")
        print(f"   Annual Contribution: ${retirement.get('annual_contribution', 0):,}")
        print(f"   Employer Match: {retirement.get('employer_match')}")
        
        fsa_hsa = recommendations.get('fsa_hsa', {})
        print(f"\n🏦 {fsa_hsa.get('type', 'FSA/HSA')}:")
        print(f"   Recommended: ${fsa_hsa.get('recommended_contribution', 0):,}/year")
        print(f"   Tax Savings: ${fsa_hsa.get('tax_savings_estimate', 0):,}")
        
        total = recommendations.get('total_cost_summary', {})
        print(f"\n📊 TOTAL COST SUMMARY:")
        print(f"   Your Monthly Cost: ${total.get('monthly_employee_contribution', 0):.2f}")
        print(f"   Total Benefits Value: ${total.get('total_benefits_value', 0):,}")
        print(f"   {total.get('percentage_of_salary', 0)}% of salary")
        
        print("\n" + "="*80)


def main():
    """Example usage of Benefits Enrollment Assistant"""
    
    agent = BenefitsEnrollmentAssistant()
    
    print("✅ Benefits Enrollment Assistant ready!")
    print("\nTo use:")
    print("1. recommendations = agent.recommend_benefits(employee_profile, available_benefits)")
    print("2. answer = agent.answer_benefits_question(question, benefits_context)")
    print("3. comparison = agent.compare_health_plans(plans, usage_pattern)")


if __name__ == "__main__":
    main()
