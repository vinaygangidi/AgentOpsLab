"""
HR Employee Offboarding Agent

Automates employee offboarding by:
1. Creating offboarding checklists
2. Conducting exit interview analysis
3. Managing equipment return and access revocation
4. Generating offboarding reports

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class EmployeeOffboardingAgent:
    """AI agent for automated employee offboarding workflows"""
    
    def __init__(self):
        """Initialize the Employee Offboarding Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def create_offboarding_checklist(self, employee_data: Dict) -> Dict:
        """
        Create comprehensive offboarding checklist
        
        Args:
            employee_data: Dict with name, role, department, last_day, reason, manager
            
        Returns:
            Dictionary with complete offboarding checklist and timeline
        """
        
        prompt = f"""You are an expert HR offboarding specialist. Create a comprehensive offboarding checklist for an exiting employee.

EMPLOYEE INFORMATION:
- Name: {employee_data.get('name')}
- Role: {employee_data.get('role')}
- Department: {employee_data.get('department')}
- Last Day: {employee_data.get('last_day')}
- Reason for Leaving: {employee_data.get('reason', 'Not specified')}
- Manager: {employee_data.get('manager')}
- Years with Company: {employee_data.get('tenure_years', 'Not specified')}

Create a detailed offboarding plan in JSON format:
{{
    "employee_name": "Name",
    "last_working_day": "Date",
    "offboarding_timeline": "Number of days before last day to start (typically 14-30)",
    
    "pre_departure_tasks": [
        {{"task": "Schedule exit interview", "owner": "HR", "deadline_days_before": 7, "priority": "HIGH", "completed": false}},
        {{"task": "Document handover plan", "owner": "Employee", "deadline_days_before": 14, "priority": "HIGH", "completed": false}},
        {{"task": "Transfer knowledge to team", "owner": "Employee/Manager", "deadline_days_before": 7, "priority": "HIGH", "completed": false}}
    ],
    
    "access_revocation": [
        {{"system": "Email", "owner": "IT", "revoke_timing": "End of last day", "completed": false}},
        {{"system": "Building access badge", "owner": "Facilities", "revoke_timing": "End of last day", "completed": false}},
        {{"system": "VPN", "owner": "IT", "revoke_timing": "End of last day", "completed": false}}
    ],
    
    "equipment_return": [
        {{"item": "Laptop", "serial_number": "TBD", "condition": "Good", "returned": false}},
        {{"item": "Monitor", "serial_number": "TBD", "condition": "Good", "returned": false}},
        {{"item": "Mobile phone", "serial_number": "TBD", "condition": "Good", "returned": false}}
    ],
    
    "knowledge_transfer": [
        {{"area": "Active projects", "documentation": "Required", "handover_to": "Team member name", "completed": false}},
        {{"area": "Client relationships", "documentation": "Required", "handover_to": "Manager", "completed": false}}
    ],
    
    "final_settlements": [
        {{"item": "Final paycheck", "owner": "Payroll", "deadline": "Last day", "completed": false}},
        {{"item": "Unused PTO payout", "owner": "Payroll", "deadline": "Last day", "completed": false}},
        {{"item": "Benefits termination notice", "owner": "HR", "deadline": "Last day", "completed": false}}
    ],
    
    "exit_interview": {{
        "scheduled": false,
        "interview_date": null,
        "interviewer": "HR Business Partner",
        "format": "In-person/Virtual",
        "duration": "45-60 minutes"
    }},
    
    "communication_plan": [
        {{"stakeholder": "Team", "message_type": "Departure announcement", "timing": "1 week before", "owner": "Manager"}},
        {{"stakeholder": "Clients", "message_type": "Transition plan", "timing": "1 week before", "owner": "Manager"}}
    ],
    
    "post_departure": [
        {{"task": "Remove from email distribution lists", "owner": "IT", "deadline_days_after": 1}},
        {{"task": "Update organizational chart", "owner": "HR", "deadline_days_after": 1}},
        {{"task": "Archive employee files", "owner": "HR", "deadline_days_after": 30}}
    ]
}}

Make the checklist:
- Comprehensive and role-specific
- Include compliance requirements
- Provide realistic timelines
- Cover legal and security aspects
- Return ONLY valid JSON, no additional text"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3500,
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
            
            offboarding_plan = json.loads(json_str)
            offboarding_plan['created_date'] = datetime.now().isoformat()
            offboarding_plan['agent'] = 'employee_offboarding_agent'
            
            return offboarding_plan
            
        except Exception as e:
            print(f"Error creating offboarding checklist: {e}")
            raise
    
    def analyze_exit_interview(self, exit_interview_data: Dict) -> Dict:
        """
        Analyze exit interview responses to extract insights
        
        Args:
            exit_interview_data: Dict with employee info and interview responses
            
        Returns:
            Analysis with themes, concerns, and recommendations
        """
        
        prompt = f"""Analyze this exit interview and provide insights for HR and leadership.

EXIT INTERVIEW:
Employee: {exit_interview_data.get('employee_name')}
Role: {exit_interview_data.get('role')}
Tenure: {exit_interview_data.get('tenure_years')} years
Reason for Leaving: {exit_interview_data.get('reason_for_leaving')}

RESPONSES:
1. What did you enjoy most about working here?
{exit_interview_data.get('enjoyed_most')}

2. What challenges did you face?
{exit_interview_data.get('challenges')}

3. Why are you leaving?
{exit_interview_data.get('reason_detail')}

4. How would you rate your relationship with your manager?
{exit_interview_data.get('manager_relationship')}

5. Would you recommend this company to others?
{exit_interview_data.get('would_recommend')}

6. Any suggestions for improvement?
{exit_interview_data.get('suggestions')}

Provide analysis in JSON format:
{{
    "exit_reason_category": "CAREER_GROWTH / COMPENSATION / MANAGEMENT / CULTURE / RELOCATION / PERSONAL / OTHER",
    "sentiment": "POSITIVE / NEUTRAL / NEGATIVE",
    "retention_possible": "YES / MAYBE / NO",
    
    "key_themes": [
        {{"theme": "Theme identified", "sentiment": "Positive/Negative", "evidence": "Quote or evidence"}}
    ],
    
    "red_flags": [
        {{"concern": "Specific concern raised", "severity": "HIGH/MEDIUM/LOW", "action_needed": "Suggested action"}}
    ],
    
    "positive_feedback": ["Positive point 1", "Positive point 2"],
    
    "actionable_insights": [
        {{"insight": "Specific insight", "department": "Affected department", "recommendation": "What to do"}}
    ],
    
    "rehire_eligibility": "ELIGIBLE / NOT_ELIGIBLE / CONDITIONAL",
    "retention_risk_for_team": "HIGH / MEDIUM / LOW"
}}

Return ONLY valid JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                temperature=0.4,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            analysis = json.loads(json_str)
            analysis['employee_name'] = exit_interview_data.get('employee_name')
            analysis['analyzed_date'] = datetime.now().isoformat()
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing exit interview: {e}")
            raise
    
    def generate_offboarding_report(self, offboarding_plan: Dict, completion_status: Dict) -> str:
        """Generate offboarding completion report"""
        
        total_tasks = 0
        completed_tasks = 0
        
        for section in ['pre_departure_tasks', 'access_revocation', 'equipment_return', 'final_settlements']:
            items = offboarding_plan.get(section, [])
            total_tasks += len(items)
            for item in items:
                if item.get('completed', False):
                    completed_tasks += 1
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        report = f"""
OFFBOARDING REPORT
{'='*80}
Employee: {offboarding_plan.get('employee_name')}
Last Day: {offboarding_plan.get('last_working_day')}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

COMPLETION STATUS: {completion_rate:.1f}%
Tasks Completed: {completed_tasks}/{total_tasks}

OUTSTANDING ITEMS:
"""
        
        for section in ['pre_departure_tasks', 'access_revocation', 'equipment_return']:
            items = offboarding_plan.get(section, [])
            outstanding = [item for item in items if not item.get('completed', False)]
            if outstanding:
                report += f"\n{section.replace('_', ' ').title()}:\n"
                for item in outstanding:
                    task_name = item.get('task') or item.get('system') or item.get('item')
                    report += f"  - {task_name}\n"
        
        return report


def main():
    """Example usage of Employee Offboarding Agent"""
    
    agent = EmployeeOffboardingAgent()
    
    employee_data = {
        'name': 'Alex Thompson',
        'role': 'Product Manager',
        'department': 'Product',
        'last_day': '2026-04-15',
        'reason': 'New opportunity',
        'manager': 'Jessica Lee',
        'tenure_years': 3
    }
    
    print("✅ Employee Offboarding Agent ready!")
    print("\nTo use:")
    print("1. plan = agent.create_offboarding_checklist(employee_data)")
    print("2. analysis = agent.analyze_exit_interview(interview_data)")
    print("3. report = agent.generate_offboarding_report(plan, status)")


if __name__ == "__main__":
    main()
