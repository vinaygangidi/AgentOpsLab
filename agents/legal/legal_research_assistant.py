"""
Legal Research Assistant Agent

Assists with legal research by:
1. Researching case law and regulations
2. Summarizing legal precedents
3. Providing citation-ready summaries
4. Analyzing legal arguments

Author: Vinay Gangidi
Date: March 2026
"""

import anthropic
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

class LegalResearchAssistant:
    """AI agent for legal research and analysis"""
    
    def __init__(self):
        """Initialize the Legal Research Assistant with Claude AI"""
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = "claude-sonnet-4-20250514"
        
    def research_legal_question(self, question: str, jurisdiction: str = "Federal") -> Dict:
        """
        Research a legal question and provide comprehensive analysis
        
        Args:
            question: Legal question to research
            jurisdiction: Relevant jurisdiction (Federal, State, etc.)
            
        Returns:
            Research summary with analysis and citations
        """
        
        prompt = f"""You are an expert legal researcher. Research this legal question and provide a comprehensive analysis.

LEGAL QUESTION:
{question}

JURISDICTION: {jurisdiction}

Provide research findings in JSON format:
{{
    "question": "The legal question being researched",
    "jurisdiction": "{jurisdiction}",
    
    "executive_summary": "2-3 sentence summary of the answer",
    
    "legal_analysis": {{
        "primary_conclusion": "Main legal conclusion",
        "confidence_level": "HIGH / MEDIUM / LOW",
        "key_considerations": [
            "Consideration 1",
            "Consideration 2"
        ]
    }},
    
    "relevant_statutes": [
        {{
            "statute": "17 U.S.C. § 102",
            "title": "Subject matter of copyright",
            "relevance": "Defines what is copyrightable",
            "key_provision": "Original works of authorship...",
            "application": "How this applies to the question"
        }}
    ],
    
    "relevant_case_law": [
        {{
            "case_name": "Feist Publications, Inc. v. Rural Telephone Service Co.",
            "citation": "499 U.S. 340 (1991)",
            "court": "Supreme Court of the United States",
            "year": 1991,
            "holding": "Facts are not copyrightable",
            "relevance": "How this case applies",
            "key_quote": "The sine qua non of copyright is originality"
        }}
    ],
    
    "relevant_regulations": [
        {{
            "regulation": "37 C.F.R. § 202.1",
            "title": "Material not subject to copyright",
            "agency": "U.S. Copyright Office",
            "relevance": "Lists excluded materials"
        }}
    ],
    
    "legal_principles": [
        {{
            "principle": "Originality requirement",
            "explanation": "Works must possess minimal creativity",
            "application": "Applied to the question at hand"
        }}
    ],
    
    "counterarguments": [
        {{
            "argument": "Alternative legal interpretation",
            "basis": "Case law or statute supporting this view",
            "strength": "STRONG / MODERATE / WEAK"
        }}
    ],
    
    "practical_implications": [
        "Implication 1 for business/client",
        "Implication 2 for business/client"
    ],
    
    "recommendations": [
        {{
            "recommendation": "Specific action to take",
            "priority": "HIGH / MEDIUM / LOW",
            "reasoning": "Why this is recommended"
        }}
    ],
    
    "further_research_needed": [
        "Area 1 requiring additional research",
        "Area 2 requiring additional research"
    ]
}}

Be accurate, thorough, and cite authoritative sources. Return ONLY valid JSON."""

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
            
            response_text = response.content[0].text
            
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            research_results = json.loads(json_str)
            research_results['researched_date'] = datetime.now().isoformat()
            research_results['agent'] = 'legal_research_assistant'
            
            return research_results
            
        except Exception as e:
            print(f"Error researching legal question: {e}")
            raise
    
    def analyze_case_law(self, case_facts: str, legal_issue: str) -> Dict:
        """
        Analyze case law relevant to specific facts
        
        Args:
            case_facts: Factual scenario to analyze
            legal_issue: Specific legal issue to address
            
        Returns:
            Case law analysis with relevant precedents
        """
        
        prompt = f"""Analyze relevant case law for this legal issue.

CASE FACTS:
{case_facts}

LEGAL ISSUE:
{legal_issue}

Identify relevant case law and analyze how it applies to these facts. Provide:
1. Most relevant cases
2. Key holdings
3. Factual similarities/differences
4. Likely outcome based on precedent

Return analysis in JSON format with case citations."""

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
            print(f"Error analyzing case law: {e}")
            raise
    
    def generate_legal_memo(self, research_results: Dict) -> str:
        """
        Generate formal legal memo from research results
        
        Args:
            research_results: Results from research_legal_question
            
        Returns:
            Formatted legal memorandum
        """
        
        question = research_results.get('question', 'Legal Question')
        summary = research_results.get('executive_summary', '')
        analysis = research_results.get('legal_analysis', {})
        
        memo = f"""
MEMORANDUM

TO:      Legal Team
FROM:    AgentOpsLab Legal Research Assistant
DATE:    {datetime.now().strftime('%B %d, %Y')}
RE:      {question}

{'='*80}

QUESTION PRESENTED

{question}

BRIEF ANSWER

{summary}

ANALYSIS

{analysis.get('primary_conclusion', '')}

"""
        
        # Add relevant statutes
        statutes = research_results.get('relevant_statutes', [])
        if statutes:
            memo += "\nRELEVANT STATUTES\n\n"
            for statute in statutes:
                memo += f"{statute.get('statute')} - {statute.get('title')}\n"
                memo += f"  {statute.get('key_provision')}\n\n"
        
        # Add case law
        cases = research_results.get('relevant_case_law', [])
        if cases:
            memo += "\nRELEVANT CASE LAW\n\n"
            for case in cases:
                memo += f"{case.get('case_name')}, {case.get('citation')}\n"
                memo += f"  Holding: {case.get('holding')}\n"
                memo += f"  Relevance: {case.get('relevance')}\n\n"
        
        # Add recommendations
        recommendations = research_results.get('recommendations', [])
        if recommendations:
            memo += "\nRECOMMENDATIONS\n\n"
            for i, rec in enumerate(recommendations, 1):
                memo += f"{i}. {rec.get('recommendation')}\n"
        
        memo += "\n" + "="*80 + "\n"
        
        return memo
    
    def compare_jurisdictions(self, legal_issue: str, jurisdictions: List[str]) -> Dict:
        """
        Compare how different jurisdictions handle a legal issue
        
        Args:
            legal_issue: Legal issue to compare
            jurisdictions: List of jurisdictions to compare
            
        Returns:
            Comparative analysis across jurisdictions
        """
        
        prompt = f"""Compare how these jurisdictions handle this legal issue:

LEGAL ISSUE: {legal_issue}
JURISDICTIONS: {', '.join(jurisdictions)}

Provide comparative analysis showing:
1. How each jurisdiction treats the issue
2. Key differences in approach
3. Which jurisdiction is most favorable/unfavorable
4. Practical implications

Return in JSON format."""

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
            print(f"Error comparing jurisdictions: {e}")
            raise
    
    def generate_citation_list(self, research_results: Dict, citation_format: str = "Bluebook") -> List[str]:
        """
        Generate properly formatted citation list
        
        Args:
            research_results: Research results with cases and statutes
            citation_format: Citation format (Bluebook, APA, etc.)
            
        Returns:
            List of formatted citations
        """
        
        citations = []
        
        # Format case citations
        for case in research_results.get('relevant_case_law', []):
            citation = f"{case.get('case_name')}, {case.get('citation')} ({case.get('year')})"
            citations.append(citation)
        
        # Format statute citations
        for statute in research_results.get('relevant_statutes', []):
            citation = f"{statute.get('statute')}"
            citations.append(citation)
        
        # Format regulation citations
        for reg in research_results.get('relevant_regulations', []):
            citation = f"{reg.get('regulation')}"
            citations.append(citation)
        
        return sorted(citations)
    
    def display_research_results(self, research_results: Dict):
        """Display research results in readable format"""
        print("\n" + "="*80)
        print("📚 LEGAL RESEARCH RESULTS")
        print("="*80)
        
        print(f"\n❓ QUESTION: {research_results.get('question')}")
        print(f"⚖️  JURISDICTION: {research_results.get('jurisdiction')}")
        
        analysis = research_results.get('legal_analysis', {})
        print(f"\n📊 CONCLUSION: {analysis.get('primary_conclusion')}")
        print(f"✅ CONFIDENCE: {analysis.get('confidence_level')}")
        
        print(f"\n📖 EXECUTIVE SUMMARY:")
        print(f"{research_results.get('executive_summary')}")
        
        cases = research_results.get('relevant_case_law', [])
        if cases:
            print(f"\n⚖️  RELEVANT CASES ({len(cases)}):")
            for case in cases[:3]:
                print(f"  • {case.get('case_name')}, {case.get('citation')}")
                print(f"    {case.get('holding')}")
        
        statutes = research_results.get('relevant_statutes', [])
        if statutes:
            print(f"\n📜 RELEVANT STATUTES ({len(statutes)}):")
            for statute in statutes[:3]:
                print(f"  • {statute.get('statute')} - {statute.get('title')}")
        
        recommendations = research_results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"  [{rec.get('priority')}] {rec.get('recommendation')}")
        
        print("\n" + "="*80)


def main():
    """Example usage of Legal Research Assistant"""
    
    agent = LegalResearchAssistant()
    
    print("✅ Legal Research Assistant ready!")
    print("\nTo use:")
    print("1. results = agent.research_legal_question(question, 'Federal')")
    print("2. agent.display_research_results(results)")
    print("3. memo = agent.generate_legal_memo(results)")


if __name__ == "__main__":
    main()
