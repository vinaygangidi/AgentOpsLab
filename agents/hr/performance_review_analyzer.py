"""
HR Performance Review Analyzer Agent

Analyzes performance reviews to:
1. Extract key themes and patterns from review text
2. Identify strengths and development areas
3. Generate performance improvement recommendations
4. Track performance trends over time

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class PerformanceReviewAnalyzer:
    """AI agent for analyzing employee performance reviews"""
    
    def __init__(self):
        """Initialize the Performance Review Analyzer with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def analyze_review(self, review_data: Dict) -> Dict:
        """
        Analyze performance review using Claude AI
        
        Args:
            review_data: Dict with employee_name, role, review_period, manager_feedback,
                        self_assessment, goals, ratings
            
        Returns:
            Dictionary with analysis, insights, and recommendations
        """
        
        prompt = f"""You are an expert HR performance analyst. Analyze this performance review and provide insights.

PERFORMANCE REVIEW:
Employee: {review_data.get('employee_name')}
Role: {review_data.get('role')}
Review Period: {review_data.get('review_period')}
Manager: {review_data.get('manager')}

MANAGER FEEDBACK:
{review_data.get('manager_feedback')}

SELF-ASSESSMENT:
{review_data.get('self_assessment', 'Not provided')}

GOALS FOR PERIOD:
{json.dumps(review_data.get('goals', []), indent=2)}

RATINGS (1-5 scale):
{json.dumps(review_data.get('ratings', {}), indent=2)}

Provide a comprehensive analysis in JSON format:
{{
    "overall_performance": {{
        "rating": "Average of all ratings (1-5)",
        "summary": "2-3 sentence overall performance summary",
        "performance_level": "EXCEPTIONAL / EXCEEDS / MEETS / NEEDS_IMPROVEMENT / UNSATISFACTORY"
    }},
    
    "key_strengths": [
        {{"strength": "Specific strength", "evidence": "Supporting evidence from feedback", "impact": "Business impact"}},
        {{"strength": "Another strength", "evidence": "Evidence", "impact": "Impact"}}
    ],
    
    "development_areas": [
        {{"area": "Area needing improvement", "current_state": "Current situation", "impact": "Impact of improvement"}},
        {{"area": "Another area", "current_state": "Current", "impact": "Impact"}}
    ],
    
    "goal_achievement": [
        {{"goal": "Goal description", "achievement": "percentage (0-100)", "status": "EXCEEDED / MET / PARTIALLY_MET / NOT_MET", "notes": "Comments"}}
    ],
    
    "themes": {{
        "positive_patterns": ["Theme 1", "Theme 2", "Theme 3"],
        "concerning_patterns": ["Concern 1", "Concern 2"],
        "alignment_with_company_values": "HIGH / MEDIUM / LOW"
    }},
    
    "recommendations": {{
        "immediate_actions": [
            {{"action": "Specific action to take", "timeline": "Timeframe", "owner": "Manager/Employee"}}
        ],
        "development_plan": [
            {{"area": "Skill/competency", "action": "Training or development activity", "timeline": "Duration"}}
        ],
        "career_growth": "Career growth recommendation",
        "next_review_focus": ["Focus area 1", "Focus area 2"]
    }},
    
    "manager_employee_alignment": {{
        "alignment_score": "1-10 scale",
        "gaps": ["Gap between manager and self assessment"],
        "discussion_topics": ["Topics for manager-employee discussion"]
    }},
    
    "retention_risk": {{
        "risk_level": "LOW / MEDIUM / HIGH",
        "risk_factors": ["Factor 1", "Factor 2"],
        "mitigation_strategies": ["Strategy 1", "Strategy 2"]
    }},
    
    "compensation_recommendation": {{
        "merit_increase_suggested": "percentage or amount",
        "bonus_recommendation": "Yes/No and reasoning",
        "promotion_readiness": "READY / NOT_READY / DISCUSS"
    }}
}}

Be objective, specific, and actionable. Return ONLY valid JSON."""

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
            
            # Extract JSON from response
            response_text = response.content[0].text
            
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            analysis = json.loads(json_str)
            
            # Add metadata
            analysis['employee_name'] = review_data.get('employee_name')
            analysis['review_period'] = review_data.get('review_period')
            analysis['analyzed_date'] = datetime.now().isoformat()
            analysis['agent'] = 'performance_review_analyzer'
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing performance review: {e}")
            raise
    
    def analyze_team_performance(self, reviews: List[Dict]) -> Dict:
        """
        Analyze performance across a team to identify patterns
        
        Args:
            reviews: List of analyzed review dictionaries
            
        Returns:
            Team-level insights and trends
        """
        
        # Calculate team averages
        total_rating = 0
        performance_distribution = {
            'EXCEPTIONAL': 0,
            'EXCEEDS': 0,
            'MEETS': 0,
            'NEEDS_IMPROVEMENT': 0,
            'UNSATISFACTORY': 0
        }
        
        all_strengths = []
        all_development_areas = []
        high_retention_risk = []
        
        for review in reviews:
            overall_perf = review.get('overall_performance', {})
            total_rating += overall_perf.get('rating', 3)
            perf_level = overall_perf.get('performance_level', 'MEETS')
            performance_distribution[perf_level] = performance_distribution.get(perf_level, 0) + 1
            
            # Collect strengths and development areas
            for strength in review.get('key_strengths', []):
                all_strengths.append(strength.get('strength'))
            
            for dev_area in review.get('development_areas', []):
                all_development_areas.append(dev_area.get('area'))
            
            # Track retention risks
            retention_risk = review.get('retention_risk', {})
            if retention_risk.get('risk_level') == 'HIGH':
                high_retention_risk.append({
                    'employee': review.get('employee_name'),
                    'factors': retention_risk.get('risk_factors', [])
                })
        
        team_count = len(reviews)
        avg_rating = total_rating / team_count if team_count > 0 else 0
        
        team_analysis = {
            'team_size': team_count,
            'average_rating': round(avg_rating, 2),
            'performance_distribution': performance_distribution,
            'top_team_strengths': self._find_common_items(all_strengths, 5),
            'common_development_areas': self._find_common_items(all_development_areas, 5),
            'retention_risks': {
                'high_risk_count': len(high_retention_risk),
                'employees': high_retention_risk
            },
            'team_health_score': self._calculate_team_health(performance_distribution, len(high_retention_risk), team_count)
        }
        
        return team_analysis
    
    def _find_common_items(self, items: List[str], top_n: int = 5) -> List[Dict]:
        """Find most common items in a list"""
        from collections import Counter
        
        if not items:
            return []
        
        counter = Counter(items)
        common = counter.most_common(top_n)
        
        return [{'item': item, 'count': count} for item, count in common]
    
    def _calculate_team_health(self, distribution: Dict, high_risk_count: int, team_size: int) -> int:
        """Calculate team health score 0-100"""
        # Weighted scoring
        score = 0
        score += distribution.get('EXCEPTIONAL', 0) * 25
        score += distribution.get('EXCEEDS', 0) * 20
        score += distribution.get('MEETS', 0) * 15
        score -= distribution.get('NEEDS_IMPROVEMENT', 0) * 10
        score -= distribution.get('UNSATISFACTORY', 0) * 20
        
        # Penalty for retention risks
        if team_size > 0:
            risk_penalty = (high_risk_count / team_size) * 30
            score -= risk_penalty
        
        # Normalize to 0-100
        max_possible = team_size * 25
        if max_possible > 0:
            normalized = int((score / max_possible) * 100)
            return max(0, min(100, normalized))
        
        return 50
    
    def display_analysis(self, analysis: Dict):
        """Display performance review analysis in readable format"""
        print("\n" + "="*80)
        print(" PERFORMANCE REVIEW ANALYSIS")
        print("="*80)
        
        print(f"\n EMPLOYEE: {analysis.get('employee_name')}")
        print(f" PERIOD: {analysis.get('review_period')}")
        
        overall = analysis.get('overall_performance', {})
        print(f"\n OVERALL RATING: {overall.get('rating')}/5")
        print(f" PERFORMANCE LEVEL: {overall.get('performance_level')}")
        print(f" {overall.get('summary')}")
        
        print(f"\n KEY STRENGTHS:")
        for strength in analysis.get('key_strengths', [])[:3]:
            print(f"  • {strength.get('strength')}")
            print(f"    Impact: {strength.get('impact')}")
        
        print(f"\n DEVELOPMENT AREAS:")
        for area in analysis.get('development_areas', [])[:3]:
            print(f"  • {area.get('area')}")
        
        print(f"\n🎓 GOAL ACHIEVEMENT:")
        for goal in analysis.get('goal_achievement', [])[:3]:
            status_emoji = "✅" if goal.get('status') == "MET" else "⚠️"
            print(f"  {status_emoji} {goal.get('goal')}: {goal.get('achievement')}%")
        
        retention = analysis.get('retention_risk', {})
        risk_emoji = "🔴" if retention.get('risk_level') == "HIGH" else "🟡" if retention.get('risk_level') == "MEDIUM" else "🟢"
        print(f"\n{risk_emoji} RETENTION RISK: {retention.get('risk_level')}")
        
        comp = analysis.get('compensation_recommendation', {})
        print(f"\n COMPENSATION:")
        print(f"  Merit Increase: {comp.get('merit_increase_suggested')}")
        print(f"  Promotion Ready: {comp.get('promotion_readiness')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Performance Review Analyzer"""
    
    # Initialize agent
    agent = PerformanceReviewAnalyzer()
    
    # Example review data
    review_data = {
        'employee_name': 'John Smith',
        'role': 'Software Engineer',
        'review_period': 'Q4 2025',
        'manager': 'Sarah Johnson',
        'manager_feedback': """
            John has shown exceptional technical skills this quarter. He successfully led 
            the migration of our legacy system to microservices, which was completed ahead 
            of schedule. His code quality is consistently high, and he mentors junior developers 
            effectively. However, John could improve his communication in cross-functional 
            meetings and be more proactive in sharing progress updates with stakeholders.
        """,
        'self_assessment': """
            I'm proud of the technical achievements this quarter, especially the microservices 
            migration. I enjoy mentoring the team and solving complex technical problems. I 
            recognize I need to work on my presentation skills and being more visible to leadership.
        """,
        'goals': [
            {'goal': 'Complete microservices migration', 'target': '100%'},
            {'goal': 'Mentor 2 junior engineers', 'target': 'Ongoing'},
            {'goal': 'Reduce system downtime by 50%', 'target': '50%'}
        ],
        'ratings': {
            'technical_skills': 5,
            'communication': 3,
            'teamwork': 4,
            'leadership': 4,
            'problem_solving': 5
        }
    }
    
    print(" Analyzing performance review...")
    
    # Analyze review
    # analysis = agent.analyze_review(review_data)
    # agent.display_analysis(analysis)
    
    print("\n Performance Review Analyzer ready!")
    print("\nTo use:")
    print("1. Prepare review data dictionary")
    print("2. analysis = agent.analyze_review(review_data)")
    print("3. agent.display_analysis(analysis)")


if __name__ == "__main__":
    main()
