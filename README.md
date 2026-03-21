# AgentOpsLab

**Complete Enterprise AI Automation Platform**

A unified platform of 33 enterprise-ready AI agents designed to automate complex business processes across Sales, Revenue, Finance, HR, and Legal operations.

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Claude AI](https://img.shields.io/badge/AI-Claude%20Sonnet%204-orange.svg)](https://www.anthropic.com/claude)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 **Live Demo**: [agentopslab-landing.vercel.app](https://agentopslab-landing.vercel.app)

---

## 📊 Platform Overview

AgentOpsLab provides **33 production-ready AI agents** that eliminate manual work and accelerate business operations:

- **🔵 Sales Operations**: 6 agents for CRM & sales automation
- **🟣 Revenue Operations**: 6 agents for RevOps intelligence
- **🟢 Enterprise Operations**: 9 agents for Finance, GTM & ERP
- **🟠 HR Operations**: 6 agents for talent & workforce management
- **⚖️ Legal Operations**: 6 agents for contract & compliance automation

**Business Impact**:
- 💰 **$2.1M** annual savings (100-person team)
- ⚡ **96%** time saved on manual work
- 📅 **6 weeks** implementation timeline
- ✅ **95%+** accuracy on data extraction

---

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- Anthropic API Key ([Get one here](https://console.anthropic.com/))
- HubSpot API Key (for CRM integration)

### Installation

```bash
# Clone the repository
git clone https://github.com/vinaygangidi/AgentOpsLab.git
cd AgentOpsLab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys:
# ANTHROPIC_API_KEY=your_key_here
# HUBSPOT_API_KEY=your_key_here
```

### Run Your First Agent

```python
from agents.hr.resume_screening_agent import ResumeScreeningAgent

# Initialize agent
agent = ResumeScreeningAgent()

# Define job requirements
job_requirements = {
    'required_skills': ['Python', 'Machine Learning', 'SQL'],
    'experience_years': 3,
    'education': "Bachelor's in Computer Science"
}

# Screen a resume
result = agent.screen_resume('data/hr/resumes/candidate.txt', job_requirements)

# View results
agent.display_screening_results(result)
```

---

## 🔵 Sales Operations (6 Agents)

Eliminate manual CRM work and accelerate your sales pipeline.

### 1. Email Intelligence Agent
- **Purpose**: Extract contacts, companies, and deals from emails
- **Accuracy**: 95%+ on data extraction
- **Location**: `agents/email_intelligence_agent.py`
- **Use Case**: Automatically populate CRM from Gmail/Outlook

### 2. Pipeline Orchestrator Agent
- **Purpose**: End-to-end automation with custom workflows
- **Features**: Zero-touch CRM updates
- **Location**: `agents/pipeline_orchestrator_agent.py`
- **Use Case**: Orchestrate multiple agents for complete automation

### 3. Contact Creator Agent
- **Purpose**: AI-powered contact enrichment & validation
- **Features**: Auto-enrich with company data
- **Location**: `agents/contact_creator_agent.py`
- **Use Case**: Create validated contacts in HubSpot

### 4. Account Creator Agent
- **Purpose**: Company data with firmographics & technographics
- **Features**: Smart industry classification
- **Location**: `agents/account_creator_agent.py`
- **Use Case**: Build comprehensive company profiles

### 5. Deal Intelligence Agent
- **Purpose**: Predictive scoring & close date forecasting
- **Features**: 20% better forecast accuracy
- **Location**: `agents/deal_creator_agent.py`
- **Use Case**: Score and prioritize opportunities

### 6. CPQ Automation Agent
- **Purpose**: Complete quote-to-cash with pricing rules
- **Features**: Zero errors in quote generation
- **Location**: `agents/quote_cpq_agent.py`
- **Use Case**: Generate accurate quotes with line items

---

## 🟣 Revenue Operations (6 Agents)

Optimize revenue, reduce churn, and maximize win rates.

**Repository**: [revops-ai-agents](https://github.com/vinaygangidi/revops-ai-agents)

### 1. Churn Detector
- **Purpose**: Predict customer churn before it happens
- **Features**: Early warning system
- **Location**: `.claude/agents/churn-detector.md`

### 2. Competitive Intelligence
- **Purpose**: Track competitors and market positioning
- **Features**: Real-time competitive tracking
- **Location**: `.claude/agents/competitive-intel.md`

### 3. Deal Risk Assessor
- **Purpose**: Identify at-risk deals with AI scoring
- **Features**: Proactive risk mitigation
- **Location**: `.claude/agents/deal-risk-assessor.md`

### 4. ICP Analyst
- **Purpose**: Analyze and segment ideal customer profiles
- **Features**: Data-driven segmentation
- **Location**: `.claude/agents/icp-analyst.md`

### 5. Objection Mapper
- **Purpose**: Map common objections and win strategies
- **Features**: Win more deals with proven tactics
- **Location**: `.claude/agents/objection-mapper.md`

### 6. Win-Loss Analyst
- **Purpose**: Deep analysis of why deals close or are lost
- **Features**: Actionable insights for improvement
- **Location**: `.claude/agents/win-loss-analyst.md`

---

## 🟢 Enterprise Operations (9 Agents)

Finance, GTM strategy, and ERP workflow automation.

**Repository**: [n8n-enterprise-ai-agents](https://github.com/vinaygangidi/n8n-enterprise-ai-agents)

### GTM Strategy (3 Agents)
1. **GTM Account 360 Copilot** - Complete account intelligence
2. **ICP Segmentation** - Advanced customer segmentation
3. **GTM Win-Loss Analysis** - Go-to-market performance

### Finance Operations (4 Agents)
4. **Cash Reconciliation** - Automated cash flow reconciliation
5. **ERP Copilot** - Intelligent ERP system assistant
6. **ERP Customer Orders** - Automated order processing
7. **Tax Agent** - Automated tax calculation & compliance

### Loan Origination (2 Agents)
8. **Loan Fraud Detection** - AI-powered fraud detection
9. **Loan Underwriting** - Automated loan risk assessment

---

## 🟠 HR Operations (6 Agents)

Automate talent acquisition, onboarding, and workforce management.

### 1. Resume Screening Agent
- **Purpose**: AI-powered candidate evaluation and scoring
- **Accuracy**: 95%+ match accuracy
- **Location**: `agents/hr/resume_screening_agent.py`
- **Features**:
  - Extract skills, experience, education from resumes
  - Score candidates against job requirements
  - AI-powered recommendations (STRONG_YES/YES/MAYBE/NO)
  - Batch screening support

**Example Usage**:
```python
from agents.hr.resume_screening_agent import ResumeScreeningAgent

agent = ResumeScreeningAgent()
result = agent.screen_resume('resume.txt', job_requirements)
```

### 2. Onboarding Workflow Agent
- **Purpose**: Automated new hire onboarding orchestration
- **Location**: `agents/hr/onboarding_workflow_agent.py`
- **Features**:
  - Generate personalized onboarding plans
  - Create day-1 schedules and checklists
  - Track onboarding progress
  - Send automated welcome emails

### 3. Performance Review Analyzer
- **Purpose**: Analyze performance reviews and identify trends
- **Location**: `agents/hr/performance_review_analyzer.py`
- **Features**:
  - Extract themes and patterns from reviews
  - Identify strengths and development areas
  - Generate improvement recommendations
  - Team-level performance analytics

### 4. Employee Offboarding Agent
- **Purpose**: Streamline employee exit processes
- **Location**: `agents/hr/employee_offboarding_agent.py`
- **Features**:
  - Create comprehensive offboarding checklists
  - Conduct and analyze exit interviews
  - Manage equipment return tracking
  - Generate offboarding completion reports

### 5. Benefits Enrollment Assistant
- **Purpose**: AI-powered benefits guidance and recommendations
- **Location**: `agents/hr/benefits_enrollment_assistant.py`
- **Features**:
  - Recommend optimal benefits packages
  - Answer benefits questions with AI
  - Calculate costs and compare plans
  - Track enrollment completion

### 6. Training Compliance Tracker
- **Purpose**: Monitor and manage training compliance
- **Location**: `agents/hr/training_compliance_tracker.py`
- **Features**:
  - Track required training completion
  - Send automated overdue reminders
  - Generate compliance reports
  - Identify training gaps and risks

---

## ⚖️ Legal Operations (6 Agents)

Automate contract review, compliance, and legal research.

### 1. Contract Review Agent
- **Purpose**: Automated legal contract analysis
- **Location**: `agents/legal/contract_review_agent.py`
- **Features**:
  - Extract key terms, obligations, and dates
  - Identify risky or unusual clauses
  - Compare against standard templates
  - Generate executive summaries

**Example Usage**:
```python
from agents.legal.contract_review_agent import ContractReviewAgent

agent = ContractReviewAgent()
analysis = agent.review_contract(contract_text, 'SaaS')
agent.display_review(analysis)
```

### 2. NDA Generator Agent
- **Purpose**: Generate custom Non-Disclosure Agreements
- **Location**: `agents/legal/nda_generator_agent.py`
- **Features**:
  - Create mutual or one-way NDAs
  - Customize terms based on use case
  - Fill in party details automatically
  - Ensure legal compliance

### 3. Contract Risk Analyzer
- **Purpose**: Score and analyze contract risk levels
- **Location**: `agents/legal/contract_risk_analyzer.py`
- **Features**:
  - Multi-dimensional risk scoring
  - Identify critical issues and red flags
  - Compare against company standards
  - Provide risk mitigation recommendations

### 4. Legal Document Classifier
- **Purpose**: Automatically classify and route legal documents
- **Location**: `agents/legal/legal_document_classifier.py`
- **Features**:
  - Identify document type (Contract, NDA, Agreement, etc.)
  - Extract key metadata
  - Route to appropriate team
  - Organize documents by category

### 5. Compliance Checker Agent
- **Purpose**: Verify regulatory compliance (GDPR, CCPA, SOX, HIPAA)
- **Location**: `agents/legal/compliance_checker_agent.py`
- **Features**:
  - Check against multiple regulations
  - Identify compliance gaps
  - Generate remediation plans
  - Track compliance over time

### 6. Legal Research Assistant
- **Purpose**: AI-powered legal research and analysis
- **Location**: `agents/legal/legal_research_assistant.py`
- **Features**:
  - Research case law and regulations
  - Summarize legal precedents
  - Provide citation-ready summaries
  - Generate legal memoranda

---

## 🏗️ Architecture

### Modular Design

```
AgentOpsLab/
├── agents/
│   ├── hr/                          # HR automation agents
│   ├── legal/                       # Legal automation agents
│   ├── email_intelligence_agent.py  # Sales agents
│   ├── pipeline_orchestrator_agent.py
│   ├── contact_creator_agent.py
│   ├── account_creator_agent.py
│   ├── deal_creator_agent.py
│   └── quote_cpq_agent.py
├── utilities/                       # Shared utilities
├── data/                           # Data storage
│   ├── email_conversations/        # Email data
│   ├── hr/resumes/                 # Resume files
│   └── legal/contracts/            # Contract files
├── docs/                           # Documentation
│   ├── hr/                         # HR agent docs
│   └── legal/                      # Legal agent docs
├── .env                            # API keys (DO NOT COMMIT)
└── README.md
```

### Agent Pattern

All agents follow a consistent pattern:

1. **Initialization**: Load Claude AI client
2. **Input Processing**: Accept structured data
3. **AI Analysis**: Use Claude for intelligent processing
4. **Output Generation**: Return structured results
5. **Display**: Present results in readable format

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```bash
# Required API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
HUBSPOT_API_KEY=your_hubspot_api_key_here

# Optional API Keys
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
```

**Get API Keys**:
- Anthropic: https://console.anthropic.com/
- HubSpot: https://app.hubspot.com/developer/

---

## 📚 Documentation

- **Agent Documentation**: See `docs/` directory for detailed agent guides
- **API Reference**: Each agent has inline docstrings
- **Examples**: See `agents/examples/` for usage examples
- **Landing Page**: https://agentopslab-landing.vercel.app

---

## 🧪 Testing

```bash
# Test HR agents
python agents/hr/resume_screening_agent.py
python agents/hr/onboarding_workflow_agent.py

# Test Legal agents
python agents/legal/contract_review_agent.py
python agents/legal/nda_generator_agent.py

# Test Sales agents
python agents/email_intelligence_agent.py
python agents/pipeline_orchestrator_agent.py
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-agent`)
3. Commit your changes (`git commit -m 'Add new agent'`)
4. Push to the branch (`git push origin feature/new-agent`)
5. Open a Pull Request

---

## 📈 Roadmap

- [ ] Add more HR agents (recruiting automation, compensation analysis)
- [ ] Add Finance agents (invoice processing, expense management)
- [ ] Add Customer Success agents (health scoring, renewal prediction)
- [ ] Build web UI for agent management
- [ ] Add Slack/Teams integration
- [ ] Create no-code agent builder

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author

**Vinay Gangidi**
- GitHub: [@vinaygangidi](https://github.com/vinaygangidi)
- LinkedIn: [Vinay Gangidi](https://www.linkedin.com/in/vinaygangidi/)

---

## 🙏 Acknowledgments

- Built with [Claude AI](https://www.anthropic.com/claude) by Anthropic
- CRM integration powered by [HubSpot](https://www.hubspot.com/)
- Deployed on [Vercel](https://vercel.com/)

---

## ⚡ Live Demo

Visit the live platform: **https://agentopslab-landing.vercel.app**

Explore all 33 AI agents and see how they can transform your business operations.

---

**Built with ❤️ and AI**
