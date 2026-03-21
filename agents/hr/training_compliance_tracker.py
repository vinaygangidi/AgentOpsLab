"""
HR Training Compliance Tracker Agent

Manages employee training compliance by:
1. Tracking required training completion
2. Sending automated reminders for overdue training
3. Generating compliance reports
4. Identifying training gaps and risks

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class TrainingComplianceTracker:
    """AI agent for tracking and managing training compliance"""
    
    def __init__(self):
        """Initialize the Training Compliance Tracker with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def analyze_training_requirements(self, employee_data: Dict, required_training: List[Dict]) -> Dict:
        """
        Analyze which training is required for an employee based on role and regulations
        
        Args:
            employee_data: Dict with role, department, location, certifications_held
            required_training: List of all available training courses
            
        Returns:
            Dictionary with required training and compliance status
        """
        
        prompt = f"""You are an expert HR compliance specialist. Determine which training courses are required for this employee.

EMPLOYEE INFORMATION:
- Role: {employee_data.get('role')}
- Department: {employee_data.get('department')}
- Location: {employee_data.get('location')}
- Current Certifications: {employee_data.get('certifications_held', [])}
- Years with Company: {employee_data.get('tenure_years', 0)}
- Manager Role: {employee_data.get('is_manager', False)}

AVAILABLE TRAINING COURSES:
{json.dumps(required_training, indent=2)}

Analyze and provide requirements in JSON format:
{{
    "required_training": [
        {{
            "course_name": "Course name",
            "category": "COMPLIANCE / SECURITY / ROLE_SPECIFIC / PROFESSIONAL_DEVELOPMENT",
            "required_reason": "Why required (regulatory, role-based, etc)",
            "frequency": "ONBOARDING / ANNUAL / BIENNIAL / ONE_TIME",
            "priority": "CRITICAL / HIGH / MEDIUM / LOW",
            "deadline_days": 30,
            "regulatory_requirement": "OSHA / SOX / HIPAA / GDPR / None",
            "consequences_if_missed": "Potential consequences"
        }}
    ],
    
    "optional_recommended": [
        {{
            "course_name": "Course name",
            "benefit": "How it helps the employee",
            "career_impact": "Career development value"
        }}
    ],
    
    "compliance_risk_level": "LOW / MEDIUM / HIGH / CRITICAL",
    "immediate_action_needed": ["Course 1", "Course 2"],
    
    "training_pathway": {{
        "first_30_days": ["Course 1", "Course 2"],
        "first_90_days": ["Course 3", "Course 4"],
        "annual_recurring": ["Course 5", "Course 6"]
    }}
}}

Consider:
- Regulatory requirements (OSHA, SOX, HIPAA, etc.)
- Role-specific needs
- Department policies
- Security and compliance mandates
- Return ONLY valid JSON"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.3,
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
            
            requirements = json.loads(json_str)
            requirements['employee_name'] = employee_data.get('name')
            requirements['analyzed_date'] = datetime.now().isoformat()
            requirements['agent'] = 'training_compliance_tracker'
            
            return requirements
            
        except Exception as e:
            print(f"Error analyzing training requirements: {e}")
            raise
    
    def check_compliance_status(self, employee_training_records: List[Dict], required_training: List[Dict]) -> Dict:
        """
        Check employee's training compliance status
        
        Args:
            employee_training_records: List of completed trainings with completion_date, expiry_date
            required_training: List of required training courses
            
        Returns:
            Compliance status report
        """
        
        current_date = datetime.now()
        
        completed_courses = {record['course_name']: record for record in employee_training_records}
        
        compliant = []
        overdue = []
        expiring_soon = []
        not_started = []
        
        for required in required_training:
            course_name = required.get('course_name')
            
            if course_name in completed_courses:
                record = completed_courses[course_name]
                completion_date = datetime.fromisoformat(record.get('completion_date'))
                expiry_date = datetime.fromisoformat(record.get('expiry_date')) if record.get('expiry_date') else None
                
                if expiry_date:
                    days_until_expiry = (expiry_date - current_date).days
                    
                    if days_until_expiry < 0:
                        # Expired
                        overdue.append({
                            'course_name': course_name,
                            'expired_date': record.get('expiry_date'),
                            'days_overdue': abs(days_until_expiry),
                            'priority': required.get('priority', 'MEDIUM'),
                            'regulatory': required.get('regulatory_requirement')
                        })
                    elif days_until_expiry <= 30:
                        # Expiring soon
                        expiring_soon.append({
                            'course_name': course_name,
                            'expiry_date': record.get('expiry_date'),
                            'days_remaining': days_until_expiry,
                            'priority': required.get('priority', 'MEDIUM')
                        })
                    else:
                        # Compliant
                        compliant.append({
                            'course_name': course_name,
                            'completion_date': record.get('completion_date'),
                            'expiry_date': record.get('expiry_date')
                        })
                else:
                    # No expiry (one-time training)
                    compliant.append({
                        'course_name': course_name,
                        'completion_date': record.get('completion_date')
                    })
            else:
                # Not completed
                deadline_days = required.get('deadline_days', 30)
                not_started.append({
                    'course_name': course_name,
                    'priority': required.get('priority', 'MEDIUM'),
                    'deadline_days': deadline_days,
                    'regulatory': required.get('regulatory_requirement'),
                    'consequences': required.get('consequences_if_missed')
                })
        
        total_required = len(required_training)
        total_compliant = len(compliant)
        compliance_rate = (total_compliant / total_required * 100) if total_required > 0 else 0
        
        # Determine overall compliance status
        if len(overdue) > 0 or compliance_rate < 70:
            status = "NON_COMPLIANT"
        elif len(expiring_soon) > 3 or compliance_rate < 85:
            status = "AT_RISK"
        elif compliance_rate >= 95:
            status = "FULLY_COMPLIANT"
        else:
            status = "COMPLIANT"
        
        compliance_report = {
            'compliance_status': status,
            'compliance_rate': round(compliance_rate, 1),
            'total_required': total_required,
            'total_compliant': total_compliant,
            'compliant_courses': compliant,
            'overdue_courses': overdue,
            'expiring_soon': expiring_soon,
            'not_started': not_started,
            'critical_action_needed': len(overdue) > 0 or len([c for c in not_started if c.get('priority') == 'CRITICAL']) > 0,
            'checked_date': current_date.isoformat()
        }
        
        return compliance_report
    
    def generate_compliance_report(self, team_training_data: List[Dict]) -> Dict:
        """
        Generate team-wide compliance report
        
        Args:
            team_training_data: List of employee compliance reports
            
        Returns:
            Team compliance summary
        """
        
        total_employees = len(team_training_data)
        
        status_counts = {
            'FULLY_COMPLIANT': 0,
            'COMPLIANT': 0,
            'AT_RISK': 0,
            'NON_COMPLIANT': 0
        }
        
        all_overdue_courses = []
        employees_with_overdue = []
        
        total_compliance_rate = 0
        
        for employee_data in team_training_data:
            status = employee_data.get('compliance_status', 'UNKNOWN')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            total_compliance_rate += employee_data.get('compliance_rate', 0)
            
            overdue = employee_data.get('overdue_courses', [])
            if overdue:
                employees_with_overdue.append({
                    'employee_name': employee_data.get('employee_name'),
                    'overdue_count': len(overdue),
                    'courses': [c['course_name'] for c in overdue]
                })
                all_overdue_courses.extend(overdue)
        
        avg_compliance_rate = total_compliance_rate / total_employees if total_employees > 0 else 0
        
        # Find most commonly overdue courses
        from collections import Counter
        overdue_course_names = [c['course_name'] for c in all_overdue_courses]
        common_overdue = Counter(overdue_course_names).most_common(5)
        
        team_report = {
            'team_size': total_employees,
            'average_compliance_rate': round(avg_compliance_rate, 1),
            'status_distribution': status_counts,
            'employees_fully_compliant': status_counts['FULLY_COMPLIANT'],
            'employees_at_risk': status_counts['AT_RISK'] + status_counts['NON_COMPLIANT'],
            'employees_with_overdue': len(employees_with_overdue),
            'total_overdue_courses': len(all_overdue_courses),
            'most_common_overdue': [{'course': name, 'count': count} for name, count in common_overdue],
            'employees_needing_attention': employees_with_overdue[:10],  # Top 10
            'report_date': datetime.now().isoformat()
        }
        
        return team_report
    
    def generate_reminder_email(self, employee_name: str, overdue_courses: List[Dict], expiring_courses: List[Dict]) -> str:
        """Generate automated reminder email for training"""
        
        prompt = f"""Generate a friendly but professional reminder email about required training.

EMPLOYEE: {employee_name}

OVERDUE TRAINING:
{json.dumps(overdue_courses, indent=2)}

EXPIRING SOON:
{json.dumps(expiring_courses, indent=2)}

Write an email that:
1. Is friendly but conveys urgency for overdue items
2. Clearly lists what training is needed
3. Explains why it's important (compliance, regulations)
4. Provides clear next steps
5. Includes a subject line

Keep it professional and encouraging."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.6,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating reminder email: {e}")
            raise
    
    def display_compliance_status(self, compliance_report: Dict):
        """Display compliance status in readable format"""
        print("\n" + "="*80)
        print("📚 TRAINING COMPLIANCE STATUS")
        print("="*80)
        
        status = compliance_report.get('compliance_status')
        rate = compliance_report.get('compliance_rate', 0)
        
        status_emoji = {
            'FULLY_COMPLIANT': '✅',
            'COMPLIANT': '🟢',
            'AT_RISK': '⚠️',
            'NON_COMPLIANT': '🔴'
        }
        
        print(f"\n{status_emoji.get(status, '❓')} STATUS: {status}")
        print(f"📊 Compliance Rate: {rate}%")
        print(f"✓ Compliant: {compliance_report.get('total_compliant')}/{compliance_report.get('total_required')}")
        
        overdue = compliance_report.get('overdue_courses', [])
        if overdue:
            print(f"\n🔴 OVERDUE TRAINING ({len(overdue)}):")
            for course in overdue[:5]:
                print(f"  • {course.get('course_name')} - {course.get('days_overdue')} days overdue")
        
        expiring = compliance_report.get('expiring_soon', [])
        if expiring:
            print(f"\n⚠️  EXPIRING SOON ({len(expiring)}):")
            for course in expiring[:5]:
                print(f"  • {course.get('course_name')} - {course.get('days_remaining')} days left")
        
        not_started = compliance_report.get('not_started', [])
        if not_started:
            print(f"\n📋 NOT STARTED ({len(not_started)}):")
            for course in not_started[:5]:
                priority_emoji = "🔴" if course.get('priority') == 'CRITICAL' else "🟡"
                print(f"  {priority_emoji} {course.get('course_name')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Training Compliance Tracker"""
    
    agent = TrainingComplianceTracker()
    
    print("✅ Training Compliance Tracker ready!")
    print("\nTo use:")
    print("1. requirements = agent.analyze_training_requirements(employee_data, courses)")
    print("2. status = agent.check_compliance_status(records, required)")
    print("3. report = agent.generate_compliance_report(team_data)")


if __name__ == "__main__":
    main()
