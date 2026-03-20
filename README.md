# AgentOpsLab - Intelligent Business Automation Platform

Professional AI-powered agents for CRM automation with Claude AI integration. Production-ready code with comprehensive documentation.

## Overview

AgentOpsLab provides enterprise-grade AI agents that automate CRM operations intelligently. Each agent uses Anthropic's Claude AI to validate, enrich, and process data before creating records in HubSpot. All agents are flexible - handling anywhere from 1 record to millions with the same code.

## Project Structure
```
AgentOpsLab/
├── agents/                              # PRODUCTION AI AGENTS
│   ├── contact_creator_agent.py        # Creates contacts (1 to millions)
│   ├── account_creator_agent.py        # Creates companies (1 to millions)
│   ├── deal_creator_agent.py           # Creates deals (1 to millions)
│   ├── quote_cpq_agent.py              # Complete CPQ system
│   ├── email_intelligence_agent.py     # Extract CRM data from emails
│   └── email_intelligence_reader.py    # Demo mode (no HubSpot creation)
│
├── agents/examples/                     # LEARNING EXAMPLES
│   ├── README.md
│   ├── contact_validator.py            # Validation demo (no creation)
│   └── single_contact_demo.py          # Simple single-record example
│
├── utilities/                           # NON-AI UTILITIES
│   ├── product_catalog_generator.py    # Bulk product creation
│   ├── email_synthesizer.py            # Generate test email conversations
│   ├── verify_contacts.py
│   ├── verify_companies.py
│   ├── verify_deals.py
│   ├── verify_quotes.py
│   └── verify_products.py
│
├── docs/                                # COMPREHENSIVE DOCUMENTATION
│   ├── contact_creator_agent.md
│   ├── account_creator_agent.md
│   ├── deal_creator_agent.md
│   ├── quote_cpq_agent.md
│   ├── email_intelligence_agent.md
│   ├── product_catalog_generator.md
│   └── utilities.md
│
├── data/
│   └── email_conversations/            # Generated test email threads
│
└── .env                                 # API credentials (not in repo)
```

## Production Agents

### 1. Contact Creator Agent
**File:** `agents/contact_creator_agent.py`

Creates contacts with AI enrichment. Flexible: 1 contact to 1 million contacts with same code.

**Features:**
- Email validation and formatting
- Phone number standardization
- Job title suggestions
- Data quality assessment
- Batch processing with rate limiting

**Usage:**
```bash
python agents/contact_creator_agent.py
```

**Configuration:**
```python
MODE = "single"              # or "bulk"
TOTAL_CONTACTS = 1000       # for bulk mode
ENRICH_WITH_CLAUDE = True   # AI enrichment
```

---

### 2. Account Creator Agent
**File:** `agents/account_creator_agent.py`

Creates companies/accounts with AI enrichment. Flexible: 1 company to 1 million companies.

**Features:**
- Industry classification
- Company size estimation
- Revenue estimation
- Business descriptions
- Website validation

**Usage:**
```bash
python agents/account_creator_agent.py
```

**What it creates:** Complete company records with AI-enriched data

---

### 3. Deal Creator Agent
**File:** `agents/deal_creator_agent.py`

Creates deals/opportunities with AI forecasting. Flexible: 1 deal to 1 million deals.

**Features:**
- Close date prediction
- Deal stage suggestions
- Win probability assessment
- Strategic recommendations
- Pipeline management

**Usage:**
```bash
python agents/deal_creator_agent.py
```

**AI Enhancement:** Claude analyzes deal characteristics and suggests optimal stages and close dates.

---

### 4. Quote CPQ Agent
**File:** `agents/quote_cpq_agent.py`

Complete Configure-Price-Quote system. Creates production-ready quotes with products, line items, pricing, and totals.

**Features:**
- Product catalog management
- Deal creation with line items
- Automatic pricing calculations
- Discount handling
- Total calculations
- Full associations

**Usage:**
```bash
python agents/quote_cpq_agent.py
```

**What it creates:**
- Products in catalog (or reuses existing)
- Deal with complete pricing
- Line items with quantities and discounts
- Automatic total: $42,500 (example)
- Ready to send to customer

---

### 5. Email Intelligence Agent ⭐ MOST POWERFUL
**File:** `agents/email_intelligence_agent.py`

The most powerful agent - creates complete sales pipelines from messy, unstructured email conversations.

**Features:**
- Reads multi-party email threads
- Extracts contact, company, deal, product data
- Sentiment analysis and risk assessment
- Creates entire pipeline automatically
- Intelligence reporting with next steps

**Demo Mode:** `agents/email_intelligence_reader.py` - Shows extraction without creating HubSpot records

**Usage:**
```bash
# Step 1: Generate test conversations
python utilities/email_synthesizer.py

# Step 2: See extraction (no HubSpot creation)
python agents/email_intelligence_reader.py

# Step 3: Create full pipeline (requires HubSpot limits)
python agents/email_intelligence_agent.py
```

**What it creates from messy email:**
- Contact with full details
- Company with enrichment
- Deal with AI forecasting
- Products and line items
- Complete quote with pricing
- All associations
- Intelligence report with sentiment, concerns, next steps

**Example Input:**
```
From: Sarah Chen <s.chen@techflow.com>
Subject: Looking at enterprise solutions

Hi, we need software for ~50 users. Budget around $100k.
Can you send info?

[... 8 more messy emails with negotiations, off-topic chat,
pricing discussions, timeline pressure ...]

Final: "Let's go with $75k for the package you outlined"
```

**Example Output:**
- Contact: Sarah Chen, VP Engineering, TechFlow Industries
- Company: TechFlow Industries, 200 employees, $20M revenue
- Deal: $75,000, 85% win probability, closes Q2 2026
- Products: Enterprise License ($45k), Services ($20k), Training ($10k)
- Intelligence: Positive sentiment, high confidence, low risk

**This is the most valuable agent** - zero manual data entry from customer emails!

---

## Utilities (Non-AI Scripts)

### Verification Scripts

Quick data inspection without AI overhead:
```bash
python utilities/verify_contacts.py      # View recent contacts
python utilities/verify_companies.py     # View recent companies
python utilities/verify_deals.py         # View recent deals
python utilities/verify_quotes.py        # View recent quotes
python utilities/verify_products.py      # View recent products
```

### Product Catalog Generator
```bash
python utilities/product_catalog_generator.py
```

Creates 100+ products across 6 categories (Software, Services, Support, Hardware, Cloud, Subscriptions) without AI.

### Email Conversation Synthesizer
```bash
python utilities/email_synthesizer.py
```

Generates 3 realistic, messy email conversations for testing the Email Intelligence Agent:
- Enterprise software deal (8-10 emails, complex, multi-product)
- Hardware + services bundle (5-7 emails, medium complexity)
- Professional services (6-8 emails, time-based pricing)

**Output:** `data/email_conversations/*.txt`

---

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/vinaygangidi/AgentOpsLab.git
cd AgentOpsLab
python3 -m venv venv
source venv/bin/activate
pip install anthropic hubspot-api-client python-dotenv
```

### 2. Configure API Keys

Create `.env` file:
```bash
touch .env
```

Add keys:
```
ANTHROPIC_API_KEY=your-anthropic-key-here
HUBSPOT_API_KEY=your-hubspot-key-here
```

### 3. Run an Agent
```bash
# Create contacts
python agents/contact_creator_agent.py

# Create companies
python agents/account_creator_agent.py

# Create deals
python agents/deal_creator_agent.py

# Create complete quotes with products
python agents/quote_cpq_agent.py

# Generate product catalog
python utilities/product_catalog_generator.py

# Process email conversations (MOST POWERFUL)
python utilities/email_synthesizer.py          # Generate test emails
python agents/email_intelligence_reader.py     # Extract intelligence
python agents/email_intelligence_agent.py      # Create full pipeline

# Verify what was created
python utilities/verify_contacts.py
```

---

## Agent vs Utility - When to Use What

### Use Production Agents When:
- Creating new records
- Need AI enrichment
- Bulk operations (100s-1000s of records)
- Complex workflows
- Production deployments

### Use Utilities When:
- Quick verification
- Inspecting recent records
- Debugging
- No AI needed
- Instant results

### Use Examples When:
- Learning the codebase
- Understanding core concepts
- Experimenting with AI
- Teaching others

---

## Key Features

### All Production Agents Include:

- **Flexible Modes:** Single record or millions with same code
- **AI Enrichment:** Claude validates and enhances data
- **Batch Processing:** 100 records per API call
- **Rate Limiting:** Automatic delays to respect API limits
- **Error Handling:** Comprehensive try-catch with detailed logging
- **Progress Tracking:** Real-time progress for bulk operations
- **Professional Output:** Clean, formatted status messages

### Email Intelligence Agent Specifically:

- **Natural Language Processing:** Understands messy conversations
- **Multi-Party Thread Parsing:** Handles complex email chains
- **Sentiment Analysis:** Detects positive/neutral/negative sentiment
- **Risk Assessment:** Evaluates deal probability
- **Intelligence Reporting:** Provides next steps and recommendations
- **Zero Manual Entry:** Fully automated pipeline creation

---

## Documentation

Comprehensive guides for each component:

### Agent Documentation
- [Contact Creator Agent](docs/contact_creator_agent.md)
- [Account Creator Agent](docs/account_creator_agent.md)
- [Deal Creator Agent](docs/deal_creator_agent.md)
- [Quote CPQ Agent](docs/quote_cpq_agent.md)
- [Email Intelligence Agent](docs/email_intelligence_agent.md) ⭐

### Utility Documentation
- [Product Catalog Generator](docs/product_catalog_generator.md)
- [Verification Utilities](docs/utilities.md)

### Examples
- [Learning Examples](agents/examples/README.md)

---

## Configuration

All production agents use the same configuration pattern:
```python
# Mode selection
MODE = "single"              # "single" or "bulk"

# Bulk settings
TOTAL_RECORDS = 1000        # How many to create
BATCH_SIZE = 100            # Records per API call
RATE_LIMIT_DELAY = 0.5      # Seconds between batches

# AI settings
ENRICH_WITH_CLAUDE = True   # Enable AI enrichment
ENRICH_SAMPLE = False       # Enrich first 10 only (bulk mode)
```

---

## Performance

### With AI Enrichment:
- **Single mode:** 2-4 seconds per record
- **Bulk mode:** 100 records in 5-10 seconds
- **1,000 records:** 45-60 seconds
- **Email intelligence:** 3-5 seconds per conversation

### Without AI Enrichment:
- **Single mode:** 1-2 seconds per record
- **Bulk mode:** 100 records in 2-3 seconds
- **1,000 records:** 20-30 seconds

### Quote CPQ Agent:
- **3-product quote:** ~5 seconds total
- Includes: product creation, deal creation, line items, associations

---

## Cost Considerations

### Claude API Costs

**With AI enrichment:**
- Per record: ~$0.001 - $0.002
- Per email conversation: ~$0.003 - $0.005
- 1,000 records: ~$1 - $2
- 1,000 email conversations: ~$3 - $5

**Without AI enrichment or utilities:** $0

### HubSpot API Costs

Free within plan limits (250,000 daily requests).

---

## HubSpot Requirements

### Required Scopes

Add these to your HubSpot Private App:

**Contacts:**
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`

**Companies:**
- `crm.objects.companies.read`
- `crm.objects.companies.write`

**Deals:**
- `crm.objects.deals.read`
- `crm.objects.deals.write`

**Products & Line Items:**
- `crm.objects.products.read`
- `crm.objects.products.write`
- `crm.objects.line_items.read`
- `crm.objects.line_items.write`
- `e-commerce`

**Quotes:**
- `crm.objects.quotes.read`
- `crm.objects.quotes.write`
- `crm.schemas.quotes.read`
- `crm.schemas.quotes.write`

**Important:** After adding scopes, regenerate your access token!

---

## Use Cases

### 1. CRM Data Migration
```bash
# Import contacts
python agents/contact_creator_agent.py  # MODE="bulk", TOTAL=5000

# Import companies
python agents/account_creator_agent.py  # MODE="bulk", TOTAL=2000

# Import deals
python agents/deal_creator_agent.py     # MODE="bulk", TOTAL=1000
```

### 2. Sales Pipeline Setup
```bash
# Generate product catalog
python utilities/product_catalog_generator.py

# Create deals with products
python agents/quote_cpq_agent.py
```

### 3. Email Intelligence Automation
```bash
# Sales rep forwards customer email
# Agent extracts data and creates pipeline
python agents/email_intelligence_agent.py

# Zero manual data entry!
```

### 4. Data Enrichment
```bash
# Enrich existing data by creating enriched versions
python agents/contact_creator_agent.py  # ENRICH_WITH_CLAUDE=True
```

---

## What We've Built

### Records Created:
- 900+ contacts
- Companies/accounts (flexible quantity)
- 100+ deals
- 100+ products
- Complete quotes with line items and pricing
- Complete pipelines from email conversations

### Capabilities:
- 1-to-millions flexibility (all agents)
- AI enrichment with Claude
- Batch processing
- Rate limiting
- Error handling
- Progress tracking
- Complete CPQ workflow
- Product catalog management
- Email intelligence extraction
- Sentiment analysis
- Quick verification utilities

---

## Extending to Other Systems

To add support for a new business system:

1. Install the system's Python SDK
2. Add API credentials to `.env`
3. Copy `contact_creator_agent.py` as template
4. Update API calls to match new system
5. Adjust field mappings
6. Test in single mode
7. Deploy to bulk operations

The architecture is system-agnostic and designed for extension.

---

## Troubleshooting

### Common Issues

**Module not found:**
```bash
source venv/bin/activate
pip install anthropic hubspot-api-client python-dotenv
```

**API key not found:**
```bash
cat .env  # Verify keys exist
```

**HubSpot scope errors:**
1. Add required scopes to HubSpot Private App
2. Regenerate access token
3. Update token in `.env`

**HubSpot object limits (402 Payment Required):**
- Free/trial accounts have limits (1,000 contacts, etc.)
- Use reader mode for email intelligence
- Delete test records to free up space
- Or upgrade HubSpot plan

**Email intelligence extraction issues:**
- Ensure conversation has clear contact names and emails
- Look for pricing and product discussions in thread
- Use generated test conversations first

---

## Security

- API keys in `.env` (never committed)
- `.gitignore` excludes sensitive files
- Environment variables loaded at runtime
- No hardcoded credentials

---

## Future Roadmap

- Multi-system support (ERP, legal, revenue recognition)
- Advanced orchestration workflows
- Multi-language email processing
- Attachment processing (PDFs, images)
- CSV import/export
- Database integration
- Webhook triggers
- Web dashboard
- REST API endpoints
- Association management tools
- Custom object support
- Email response suggestions
- Calendar integration

---

## Contributing

This is a personal learning and automation project. Suggestions and feedback welcome via GitHub issues.

---

## License

Educational and business automation purposes.

---

## Contact

**Created by:** Vinay Gangidi

**Repository:** https://github.com/vinaygangidi/AgentOpsLab

---

## Acknowledgments

- Anthropic for Claude AI
- HubSpot for CRM platform
- Python community for excellent libraries