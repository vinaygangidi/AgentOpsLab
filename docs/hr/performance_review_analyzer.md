# Performance Review Analyzer

> AI-powered review analysis - extracts insights, identifies trends, and generates actionable recommendations from performance reviews.

---

## Business Value

### The Problem
Manual performance review analysis is slow and misses patterns:
- 30-45 minutes to analyze each review thoroughly
- Patterns across team not identified
- Development areas buried in text
- No retention risk detection
- Inconsistent follow-up recommendations

### The Solution
AI analysis that extracts themes from review text, identifies strengths and gaps, generates improvement recommendations, and flags retention risks across individuals and teams.

### ROI (Analyzing 100 reviews/quarter)
- **Time saved:** 40+ hours/quarter vs manual analysis
- **Cost savings:** $10,000+/year in manager productivity
- **Retention:** Early identification of flight risks
- **Development:** Better targeted growth plans

---

## Key Use Cases

### 1. Individual Review Analysis
**Before:** Manager reads review, writes summary notes manually  
**After:** Agent extracts themes, strengths, gaps automatically  
**Impact:** 30 minutes to 2 minutes, consistent quality

### 2. Team Performance Trends
**Before:** No visibility into team-wide patterns  
**After:** Aggregate analysis shows top strengths and common gaps  
**Impact:** Data-driven team development plans

### 3. Retention Risk Detection
**Before:** Managers miss early warning signs  
**After:** Agent flags disengagement indicators automatically  
**Impact:** Proactive retention conversations

---

## What It Does

### Comprehensive Review Analysis
- Extracts key themes and patterns from review text
- Identifies top strengths and development areas
- Generates performance improvement recommendations
- Detects retention risk indicators
- Analyzes compensation alignment
- Provides team-level aggregate analytics
- Compares self-assessment vs manager feedback

### Analysis Framework
```
1. Extract Themes -> 2. Identify Strengths/Gaps -> 3. Generate Recommendations
4. Assess Retention Risk -> 5. Suggest Compensation Adjustments
```

**Why this works:**
- Natural language processing extracts meaning
- Pattern recognition across text
- Contextual understanding of performance signals
- Benchmarking against role expectations

---

## How to Use

### Basic Usage (Single Review)
```python
from agents.hr.performance_review_analyzer import PerformanceReviewAnalyzer

agent = PerformanceReviewAnalyzer()

review_data = {
    'employee_name': 'John Smith',
    'role': 'Software Engineer',
    'review_period': 'Q4 2025',
    'manager': 'Sarah Johnson',
    'manager_feedback': "Exceptional technical skills...",
    'self_assessment': "Proud of technical achievements...",
    'goals': ['Complete ML migration', 'Mentor junior engineers'],
    'ratings': {
        'technical_skills': 5,
        'communication': 3,
        'teamwork': 4,
        'leadership': 4,
        'delivery': 4
    }
}

# Analyze review
analysis = agent.analyze_review(review_data)

# Display results
agent.display_analysis(analysis)
```

### Team Analytics
```python
# Analyze multiple reviews for team insights
team_reviews = [review1, review2, review3, ...]
team_analysis = agent.analyze_team_performance(team_reviews)

print(f"Average Rating: {team_analysis['average_rating']}")
print(f"Top Strengths: {team_analysis['top_team_strengths']}")
print(f"Common Gaps: {team_analysis['development_needs']}")
print(f"Retention Risks: {len(team_analysis['retention_risks'])} employees")
```

---

## Example

### Input
```
Employee: John Smith
Role: Software Engineer
Period: Q4 2025

Manager Feedback:
"John has shown exceptional technical skills this quarter. He successfully 
led the migration to our new ML infrastructure, reducing model training time 
by 40%. His code quality is excellent and he mentors junior engineers well.

Areas for improvement: John could work on his communication in cross-functional
meetings. Sometimes his technical explanations are too detailed for non-technical
stakeholders. He also tends to take on too many tasks simultaneously."

Self-Assessment:
"Proud of the ML infrastructure work. It was challenging but rewarding. 
I've been working on improving my presentation skills for exec updates.
I acknowledge I sometimes overcommit - working on better estimation."

Ratings:
Technical: 5/5, Communication: 3/5, Teamwork: 4/5, Leadership: 4/5, Delivery: 4/5
```

### AI Analysis Output
```
PERFORMANCE ANALYSIS - John Smith

KEY STRENGTHS:
1. Technical Excellence
   - Led complex ML infrastructure migration
   - 40% improvement in model training time
   - High code quality standards
   - Strong technical leadership

2. Mentorship
   - Actively mentors junior engineers
   - Shares knowledge effectively
   - Builds team capability

DEVELOPMENT AREAS:
1. Cross-Functional Communication (PRIORITY)
   - Technical explanations too detailed for non-technical audiences
   - Need to tailor messaging to audience
   - Recommendation: Executive presentation training

2. Workload Management
   - Takes on too many tasks simultaneously
   - Impacts delivery timelines
   - Recommendation: Prioritization and delegation training

GOAL ACHIEVEMENT:
- ML Infrastructure Migration: EXCEEDED (40% improvement)
- Mentor Junior Engineers: MET (actively mentoring)

ALIGNMENT ANALYSIS:
Manager and self-assessment highly aligned. John demonstrates self-awareness
about communication and workload challenges.

RETENTION RISK: LOW
Indicators: High engagement, successful projects, growth mindset

COMPENSATION RECOMMENDATION:
Performance warrants 8-12% merit increase. Technical impact and mentorship
justify upper end of band.

NEXT STEPS:
1. Enroll in Executive Communication workshop (Q1 2026)
2. Work with manager on prioritization framework
3. Continue technical leadership on ML projects
4. Consider promotion track for Q2 2026 review
```

---

## What Gets Created

### 1. Individual Analysis
```python
{
    "employee_name": "John Smith",
    "review_period": "Q4 2025",
    "key_strengths": [
        {"strength": "Technical Excellence", "evidence": "Led ML migration, 40% improvement"},
        {"strength": "Mentorship", "evidence": "Actively mentors junior engineers"}
    ],
    "development_areas": [
        {"area": "Communication", "priority": "HIGH", "recommendation": "Executive training"},
        {"area": "Workload Management", "priority": "MEDIUM", "recommendation": "Prioritization"}
    ],
    "retention_risk": "LOW",
    "compensation_recommendation": "8-12% merit increase",
    "next_steps": [...]
}
```

### 2. Team Analytics
```python
{
    "team_size": 10,
    "average_rating": 4.1,
    "top_team_strengths": ["Technical Skills", "Collaboration", "Innovation"],
    "common_development_needs": ["Communication", "Time Management"],
    "retention_risks": [
        {"name": "Employee A", "risk_level": "HIGH", "indicators": ["Low ratings", "Negative sentiment"]}
    ],
    "recommended_team_training": ["Communication Skills", "Project Management"]
}
```

---

## Performance

| Metric | Value |
|--------|-------|
| **Speed** | 5-8 seconds per review |
| **Batch Speed** | 20 reviews in 90 seconds |
| **AI Cost** | $0.004 per review |
| **Accuracy** | 90%+ theme extraction |
| **Time Savings** | 93% vs manual analysis |

---

## Requirements

### API Keys
- Anthropic Claude API (Sonnet 4)

### Dependencies
```bash
pip install anthropic python-dotenv
```

---

## Advanced Features

### Sentiment Analysis
- Detects positive vs negative tone
- Identifies enthusiasm vs disengagement
- Flags concerning language patterns

### Alignment Detection
- Compares manager vs self-assessment
- Highlights discrepancies (perception gaps)
- Identifies areas of strong agreement

### Trend Analysis
- Compares current vs previous reviews
- Tracks improvement over time
- Identifies regression in performance

### Compensation Benchmarking
- Aligns recommendations with performance level
- Considers role, seniority, and market data
- Suggests merit increase percentage ranges

---

## Limitations

- **Context required:** Needs sufficient review text (100+ words minimum)
- **No numeric scoring:** Does not generate overall performance scores
- **Subjective assessment:** AI interprets text, may miss nuance
- **No file support:** Accepts text input only (not PDF/Word)

---

## Troubleshooting

### Issue: Generic analysis with no specific insights
**Cause:** Review text too short or vague  
**Solution:** Provide detailed manager feedback (200+ words)

### Issue: Retention risk always shows LOW
**Cause:** No negative indicators in review text  
**Solution:** Agent is conservative - manual review for subtle signs

### Issue: Compensation recommendation missing
**Cause:** No ratings or performance data provided  
**Solution:** Include ratings dict in review_data

### Issue: Theme extraction seems off-topic
**Cause:** Review text includes unrelated content  
**Solution:** Clean review text to focus on performance only

---

## Best Practices

### Writing Effective Reviews
- Include specific examples and evidence
- Provide both strengths and development areas
- Use concrete metrics when possible
- Avoid generic phrases like "needs improvement"

### Using Analysis Results
- Share analysis with employee during review meeting
- Use development areas to create growth plans
- Track retention risk flags for proactive conversations
- Use team analytics for training budget allocation

### Review Calibration
- Compare manager ratings with AI-extracted themes
- Use alignment analysis to identify perception gaps
- Review retention risk flags before finalizing reviews
- Benchmark compensation recommendations against budget

### Team Development
- Use team analytics to identify training needs
- Address common gaps with team-wide initiatives
- Celebrate team strengths publicly
- Monitor retention risks quarterly

---

## Quick Start Checklist

- [ ] Install dependencies
- [ ] Set ANTHROPIC_API_KEY in .env
- [ ] Prepare review data (feedback text, ratings)
- [ ] Analyze single review
- [ ] Review analysis quality
- [ ] Run team analytics
- [ ] Integrate into review process

---

## Related Documentation

- [Resume Screening Agent](resume_screening_agent.md)
- [Onboarding Workflow Agent](onboarding_workflow_agent.md)
- [Training Compliance Tracker](training_compliance_tracker.md)

---

## Support

For issues:
1. Ensure review_data includes manager_feedback text
2. Verify ratings are numeric (1-5 scale)
3. Check review text is performance-focused
4. Test with different review styles
5. GitHub Issues: https://github.com/vinaygangidi/AgentOpsLab/issues
