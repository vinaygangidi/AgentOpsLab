"""
HR Resume Screening Agent

Automates resume screening by:
1. Extracting structured data from resumes (PDF/DOCX)
2. Scoring candidates against job requirements
3. Identifying top skills and experience
4. Creating HubSpot contacts for qualified candidates

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

class ResumeScreeningAgent:
    """AI agent for automated resume screening and candidate evaluation"""
    
    def __init__(self):
        """Initialize the Resume Screening Agent with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def extract_resume_data(self, resume_text: str, job_requirements: Optional[Dict] = None) -> Dict:
        """
        Extract structured data from resume using Claude AI
        
        Args:
            resume_text: Raw text from resume
            job_requirements: Optional dict with required_skills, experience_years, education
            
        Returns:
            Dictionary with extracted candidate data and score
        """
        
        # Build the job requirements context
        job_context = ""
        if job_requirements:
            job_context = f"""
            
JOB REQUIREMENTS:
- Required Skills: {', '.join(job_requirements.get('required_skills', []))}
- Years of Experience: {job_requirements.get('experience_years', 'Not specified')}
- Education: {job_requirements.get('education', 'Not specified')}
- Location: {job_requirements.get('location', 'Any')}
"""
        
        prompt = f"""You are an expert HR recruiter analyzing resumes. Extract the following information from this resume and provide a match score if job requirements are provided.

RESUME:
{resume_text}
{job_context}

Extract the following in JSON format:
{{
    "candidate_name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "City, State",
    "linkedin_url": "LinkedIn profile URL if available",
    
    "experience": {{
        "total_years": "Total years of professional experience",
        "current_role": "Current job title",
        "current_company": "Current company",
        "previous_roles": [
            {{"title": "Job title", "company": "Company name", "duration": "Years", "key_achievements": ["achievement 1", "achievement 2"]}}
        ]
    }},
    
    "skills": {{
        "technical": ["skill1", "skill2", "skill3"],
        "soft_skills": ["skill1", "skill2"],
        "certifications": ["cert1", "cert2"]
    }},
    
    "education": [
        {{"degree": "Degree type", "field": "Field of study", "university": "University name", "year": "Graduation year"}}
    ],
    
    "summary": "2-3 sentence professional summary",
    
    "match_score": {{
        "overall_score": 85,
        "skills_match": 90,
        "experience_match": 80,
        "education_match": 85,
        "reasoning": "Brief explanation of the score",
        "strengths": ["strength 1", "strength 2"],
        "gaps": ["gap 1", "gap 2"],
        "recommendation": "STRONG_YES / YES / MAYBE / NO"
    }}
}}

Important:
- Extract exact information from the resume
- If job requirements are provided, calculate match scores
- Recommendation: STRONG_YES (90-100), YES (75-89), MAYBE (60-74), NO (<60)
- If information is not available, use null
- Return ONLY valid JSON, no additional text"""

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
            
            # Find JSON in response (handle markdown code blocks)
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
            
            candidate_data = json.loads(json_str)
            
            # Add metadata
            candidate_data['processed_date'] = datetime.now().isoformat()
            candidate_data['agent'] = 'resume_screening_agent'
            
            return candidate_data
            
        except Exception as e:
            print(f"Error extracting resume data: {e}")
            raise
    
    def screen_resume(self, resume_path: str, job_requirements: Optional[Dict] = None) -> Dict:
        """
        Screen a resume file and return extracted data with scoring
        
        Args:
            resume_path: Path to resume file (PDF or TXT)
            job_requirements: Optional job requirements for scoring
            
        Returns:
            Dictionary with candidate data and match score
        """
        print(f"\n📄 Screening resume: {resume_path}")
        
        # Read resume file
        resume_text = self._read_resume_file(resume_path)
        
        if not resume_text:
            raise ValueError(f"Could not read resume from {resume_path}")
        
        print(f"✓ Read {len(resume_text)} characters from resume")
        
        # Extract and score
        print("🤖 Analyzing resume with Claude AI...")
        candidate_data = self.extract_resume_data(resume_text, job_requirements)
        
        # Display results
        self._display_screening_results(candidate_data)
        
        return candidate_data
    
    def screen_multiple_resumes(self, resume_folder: str, job_requirements: Optional[Dict] = None) -> List[Dict]:
        """
        Screen multiple resumes from a folder
        
        Args:
            resume_folder: Path to folder containing resumes
            job_requirements: Optional job requirements for scoring
            
        Returns:
            List of candidate data dictionaries, sorted by match score
        """
        print(f"\n📁 Screening resumes from: {resume_folder}")
        
        resume_path = Path(resume_folder)
        resume_files = list(resume_path.glob("*.txt")) + list(resume_path.glob("*.pdf"))
        
        print(f"Found {len(resume_files)} resumes to screen\n")
        
        candidates = []
        for resume_file in resume_files:
            try:
                candidate_data = self.screen_resume(str(resume_file), job_requirements)
                candidates.append(candidate_data)
            except Exception as e:
                print(f"❌ Error screening {resume_file.name}: {e}")
                continue
        
        # Sort by match score if available
        if candidates and 'match_score' in candidates[0]:
            candidates.sort(key=lambda x: x.get('match_score', {}).get('overall_score', 0), reverse=True)
        
        # Display summary
        print("\n" + "="*80)
        print("📊 SCREENING SUMMARY")
        print("="*80)
        
        for i, candidate in enumerate(candidates, 1):
            name = candidate.get('candidate_name', 'Unknown')
            score = candidate.get('match_score', {}).get('overall_score', 'N/A')
            recommendation = candidate.get('match_score', {}).get('recommendation', 'N/A')
            print(f"{i}. {name}: {score}% - {recommendation}")
        
        return candidates
    
    def _read_resume_file(self, file_path: str) -> str:
        """Read resume from text or PDF file"""
        path = Path(file_path)
        
        if path.suffix.lower() == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        elif path.suffix.lower() == '.pdf':
            # For PDF support, you'd need to install PyPDF2 or pdfplumber
            # For now, return instruction to convert
            print("⚠️  PDF support requires PyPDF2. Please convert to .txt or install: pip install PyPDF2")
            return None
        else:
            print(f"⚠️  Unsupported file format: {path.suffix}")
            return None
    
    def _display_screening_results(self, candidate_data: Dict):
        """Display screening results in a readable format"""
        print("\n" + "="*80)
        print("✅ CANDIDATE SCREENING RESULTS")
        print("="*80)
        
        # Basic Info
        print(f"\n👤 CANDIDATE: {candidate_data.get('candidate_name', 'N/A')}")
        print(f"📧 Email: {candidate_data.get('email', 'N/A')}")
        print(f"📱 Phone: {candidate_data.get('phone', 'N/A')}")
        print(f"📍 Location: {candidate_data.get('location', 'N/A')}")
        
        # Experience
        exp = candidate_data.get('experience', {})
        print(f"\n💼 EXPERIENCE: {exp.get('total_years', 'N/A')} years")
        print(f"Current: {exp.get('current_role', 'N/A')} at {exp.get('current_company', 'N/A')}")
        
        # Skills
        skills = candidate_data.get('skills', {})
        tech_skills = skills.get('technical', [])
        print(f"\n🛠️  TECHNICAL SKILLS: {', '.join(tech_skills[:5])}")
        
        # Match Score
        match = candidate_data.get('match_score', {})
        if match:
            print(f"\n📊 MATCH SCORE: {match.get('overall_score', 'N/A')}%")
            print(f"Recommendation: {match.get('recommendation', 'N/A')}")
            print(f"Reasoning: {match.get('reasoning', 'N/A')}")
            
            strengths = match.get('strengths', [])
            if strengths:
                print(f"\n✅ Strengths: {', '.join(strengths)}")
            
            gaps = match.get('gaps', [])
            if gaps:
                print(f"⚠️  Gaps: {', '.join(gaps)}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Resume Screening Agent"""
    
    # Initialize agent
    agent = ResumeScreeningAgent()
    
    # Example job requirements
    job_requirements = {
        'required_skills': ['Python', 'Machine Learning', 'SQL', 'AWS'],
        'experience_years': 3,
        'education': "Bachelor's in Computer Science or related field",
        'location': 'Remote or San Francisco'
    }
    
    # Example 1: Screen a single resume
    print("Example 1: Screen single resume")
    print("-" * 80)
    
    # You would replace this with actual resume path
    # result = agent.screen_resume('data/hr/resumes/candidate_1.txt', job_requirements)
    
    # Example 2: Screen multiple resumes from a folder
    print("\n\nExample 2: Screen multiple resumes")
    print("-" * 80)
    
    # You would replace this with actual folder path
    # candidates = agent.screen_multiple_resumes('data/hr/resumes/', job_requirements)
    
    # Save results
    # with open('data/hr/screening_results.json', 'w') as f:
    #     json.dump(candidates, f, indent=2)
    
    print("\n✅ Resume Screening Agent ready!")
    print("\nTo use:")
    print("1. Place resume files in data/hr/resumes/")
    print("2. Run: python agents/hr/resume_screening_agent.py")
    print("3. Results saved to data/hr/screening_results.json")


if __name__ == "__main__":
    main()
