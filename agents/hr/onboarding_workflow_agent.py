"""
HR Onboarding Workflow Agent

Automates new hire onboarding by:
1. Creating personalized onboarding checklists
2. Scheduling orientation and training sessions
3. Tracking onboarding progress
4. Sending automated reminders and welcome emails

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class OnboardingWorkflowAgent:
    """AI agent for automated employee onboarding workflows"""
    
    def __init__(self):
        """Initialize the Onboarding Workflow Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def create_onboarding_plan(self, employee_data: Dict) -> Dict:
        """
        Create personalized onboarding plan using Claude AI
        
        Args:
            employee_data: Dict with name, role, department, start_date, manager, location
            
        Returns:
            Dictionary with complete onboarding plan and timeline
        """
        
        prompt = f"""You are an expert HR onboarding specialist. Create a comprehensive onboarding plan for a new employee.

NEW EMPLOYEE INFORMATION:
- Name: {employee_data.get('name')}
- Role: {employee_data.get('role')}
- Department: {employee_data.get('department')}
- Start Date: {employee_data.get('start_date')}
- Manager: {employee_data.get('manager')}
- Location: {employee_data.get('location', 'Remote')}
- Employment Type: {employee_data.get('employment_type', 'Full-time')}

Create a detailed onboarding plan in JSON format:
{{
    "employee_name": "Name",
    "role": "Job Title",
    "onboarding_duration": "Number of days (typically 30, 60, or 90)",
    
    "welcome_message": "Personalized welcome message for the employee",
    
    "day_1_activities": [
        {{"time": "9:00 AM", "activity": "Welcome meeting with manager", "owner": "Manager name", "duration": "30 mins"}},
        {{"time": "10:00 AM", "activity": "IT setup and equipment", "owner": "IT Department", "duration": "1 hour"}}
    ],
    
    "week_1_checklist": [
        {{"task": "Complete I-9 and tax forms", "owner": "HR", "deadline_days": 1, "priority": "HIGH", "completed": false}},
        {{"task": "Review employee handbook", "owner": "Employee", "deadline_days": 3, "priority": "HIGH", "completed": false}}
    ],
    
    "first_30_days": [
        {{"task": "Complete all required training modules", "owner": "Employee", "deadline_days": 30, "priority": "HIGH"}},
        {{"task": "Schedule 1-on-1s with team members", "owner": "Manager", "deadline_days": 14, "priority": "MEDIUM"}}
    ],
    
    "training_required": [
        {{"course": "Company Culture & Values", "duration": "2 hours", "deadline_days": 7, "platform": "LMS"}},
        {{"course": "Security & Compliance Training", "duration": "1 hour", "deadline_days": 3, "platform": "LMS"}}
    ],
    
    "equipment_needed": [
        {{"item": "Laptop", "specs": "MacBook Pro 16-inch", "requested": false}},
        {{"item": "Monitor", "specs": "27-inch display", "requested": false}}
    ],
    
    "access_required": [
        {{"system": "Email", "access_level": "Standard", "requested": false}},
        {{"system": "HubSpot CRM", "access_level": "Sales Team", "requested": false}}
    ],
    
    "key_stakeholders": [
        {{"name": "Manager name", "role": "Direct Manager", "meeting_type": "Weekly 1-on-1"}},
        {{"name": "HR Business Partner", "role": "HRBP", "meeting_type": "Check-in at 30 days"}}
    ],
    
    "success_metrics": [
        {{"metric": "Complete all required training", "target": "100%", "deadline_days": 30}},
        {{"metric": "Submit first project deliverable", "target": "On time", "deadline_days": 45}}
    ],
    
    "milestones": [
        {{"day": 7, "milestone": "First week complete", "review_meeting": true}},
        {{"day": 30, "milestone": "First month review", "review_meeting": true}},
        {{"day": 90, "milestone": "Onboarding complete", "review_meeting": true}}
    ]
}}

Make the plan:
- Specific to the role and department
- Include all compliance and security requirements
- Provide realistic timelines
- Include both administrative and cultural onboarding
- Return ONLY valid JSON, no additional text"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.5,
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
            
            onboarding_plan = json.loads(json_str)
            
            # Add metadata
            onboarding_plan['created_date'] = datetime.now().isoformat()
            onboarding_plan['start_date'] = employee_data.get('start_date')
            onboarding_plan['agent'] = 'onboarding_workflow_agent'
            
            return onboarding_plan
            
        except Exception as e:
            print(f"Error creating onboarding plan: {e}")
            raise
    
    def generate_welcome_email(self, employee_data: Dict, onboarding_plan: Dict) -> str:
        """Generate personalized welcome email for new hire"""
        
        prompt = f"""Create a warm, professional welcome email for a new employee.

EMPLOYEE INFO:
- Name: {employee_data.get('name')}
- Role: {employee_data.get('role')}
- Start Date: {employee_data.get('start_date')}
- Manager: {employee_data.get('manager')}

FIRST DAY SCHEDULE:
{json.dumps(onboarding_plan.get('day_1_activities', []), indent=2)}

Write a welcome email that:
1. Welcomes them warmly to the team
2. Confirms their start date and first day schedule
3. Provides key information they need to know
4. Sets a positive, excited tone
5. Includes clear next steps

Format as a professional email with subject line."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating welcome email: {e}")
            raise
    
    def track_onboarding_progress(self, onboarding_plan: Dict, completed_tasks: List[str]) -> Dict:
        """
        Track onboarding progress and identify overdue items
        
        Args:
            onboarding_plan: The onboarding plan dictionary
            completed_tasks: List of completed task descriptions
            
        Returns:
            Progress report with completion percentage and overdue items
        """
        start_date = datetime.fromisoformat(onboarding_plan.get('start_date', datetime.now().isoformat()))
        current_date = datetime.now()
        days_elapsed = (current_date - start_date).days
        
        # Collect all tasks
        all_tasks = []
        all_tasks.extend(onboarding_plan.get('week_1_checklist', []))
        all_tasks.extend(onboarding_plan.get('first_30_days', []))
        all_tasks.extend(onboarding_plan.get('training_required', []))
        
        total_tasks = len(all_tasks)
        completed_count = len(completed_tasks)
        
        # Identify overdue tasks
        overdue_tasks = []
        upcoming_tasks = []
        
        for task in all_tasks:
            task_name = task.get('task') or task.get('course')
            deadline_days = task.get('deadline_days', 30)
            
            if task_name in completed_tasks:
                continue
            
            if days_elapsed > deadline_days:
                overdue_tasks.append({
                    'task': task_name,
                    'deadline_days': deadline_days,
                    'days_overdue': days_elapsed - deadline_days,
                    'priority': task.get('priority', 'MEDIUM')
                })
            elif days_elapsed + 3 >= deadline_days:  # Due soon (within 3 days)
                upcoming_tasks.append({
                    'task': task_name,
                    'deadline_days': deadline_days,
                    'days_remaining': deadline_days - days_elapsed,
                    'priority': task.get('priority', 'MEDIUM')
                })
        
        progress_report = {
            'employee_name': onboarding_plan.get('employee_name'),
            'start_date': onboarding_plan.get('start_date'),
            'days_elapsed': days_elapsed,
            'completion_percentage': round((completed_count / total_tasks * 100), 1) if total_tasks > 0 else 0,
            'tasks_completed': completed_count,
            'tasks_total': total_tasks,
            'tasks_remaining': total_tasks - completed_count,
            'overdue_tasks': overdue_tasks,
            'upcoming_tasks': upcoming_tasks,
            'status': self._get_onboarding_status(days_elapsed, completed_count, total_tasks)
        }
        
        return progress_report
    
    def _get_onboarding_status(self, days_elapsed: int, completed: int, total: int) -> str:
        """Determine onboarding status based on progress"""
        completion_rate = completed / total if total > 0 else 0
        
        if days_elapsed <= 7:
            expected_rate = 0.3
        elif days_elapsed <= 30:
            expected_rate = 0.7
        else:
            expected_rate = 0.9
        
        if completion_rate >= expected_rate:
            return "ON_TRACK"
        elif completion_rate >= expected_rate - 0.2:
            return "NEEDS_ATTENTION"
        else:
            return "AT_RISK"
    
    def display_onboarding_plan(self, onboarding_plan: Dict):
        """Display onboarding plan in readable format"""
        print("\n" + "="*80)
        print(" EMPLOYEE ONBOARDING PLAN")
        print("="*80)
        
        print(f"\n EMPLOYEE: {onboarding_plan.get('employee_name')}")
        print(f" ROLE: {onboarding_plan.get('role')}")
        print(f" START DATE: {onboarding_plan.get('start_date')}")
        print(f" DURATION: {onboarding_plan.get('onboarding_duration')} days")
        
        print(f"\n WELCOME MESSAGE:")
        print(f"{onboarding_plan.get('welcome_message')}")
        
        print(f"\n DAY 1 SCHEDULE:")
        for activity in onboarding_plan.get('day_1_activities', [])[:3]:
            print(f"  • {activity.get('time')} - {activity.get('activity')}")
        
        print(f"\n WEEK 1 CHECKLIST: ({len(onboarding_plan.get('week_1_checklist', []))} items)")
        for item in onboarding_plan.get('week_1_checklist', [])[:3]:
            priority = item.get('priority', 'MEDIUM')
            emoji = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
            print(f"  {emoji} {item.get('task')}")
        
        print(f"\n TRAINING REQUIRED: ({len(onboarding_plan.get('training_required', []))} courses)")
        for training in onboarding_plan.get('training_required', [])[:3]:
            print(f"  • {training.get('course')} ({training.get('duration')})")
        
        print(f"\n SUCCESS METRICS:")
        for metric in onboarding_plan.get('success_metrics', [])[:3]:
            print(f"  • {metric.get('metric')}: {metric.get('target')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Onboarding Workflow Agent"""
    
    # Initialize agent
    agent = OnboardingWorkflowAgent()
    
    # Example employee data
    employee_data = {
        'name': 'Sarah Chen',
        'role': 'Senior Software Engineer',
        'department': 'Engineering',
        'start_date': '2026-04-01',
        'manager': 'Michael Rodriguez',
        'location': 'Remote',
        'employment_type': 'Full-time'
    }
    
    print(" Creating onboarding plan...")
    
    # Create onboarding plan
    # onboarding_plan = agent.create_onboarding_plan(employee_data)
    # agent.display_onboarding_plan(onboarding_plan)
    
    # Generate welcome email
    # welcome_email = agent.generate_welcome_email(employee_data, onboarding_plan)
    # print("\n WELCOME EMAIL:")
    # print(welcome_email)
    
    # Track progress (after some time)
    # completed_tasks = [
    #     "Complete I-9 and tax forms",
    #     "Review employee handbook",
    #     "IT setup and equipment"
    # ]
    # progress = agent.track_onboarding_progress(onboarding_plan, completed_tasks)
    # print(f"\n Progress: {progress['completion_percentage']}% - Status: {progress['status']}")
    
    print("\n Onboarding Workflow Agent ready!")
    print("\nTo use:")
    print("1. Create employee data dictionary")
    print("2. agent.create_onboarding_plan(employee_data)")
    print("3. agent.track_onboarding_progress(plan, completed_tasks)")


if __name__ == "__main__":
    main()
