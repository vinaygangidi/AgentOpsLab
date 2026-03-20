# AgentOpsLab - Intelligent Business Automation Platform

A comprehensive collection of AI-powered agents and utilities for automating CRM operations. Built with Claude AI for intelligent data processing and HubSpot integration for production deployment.

## Overview

AgentOpsLab provides production-ready AI agents that create, update, and manage CRM records intelligently. Each agent uses Anthropic's Claude AI to validate, enrich, and process data before interacting with external systems. The platform also includes non-AI utility scripts for quick verification and inspection.

## Project Structure
```
AgentOpsLab/
├── agents/                      # AI-POWERED AGENTS (Claude enrichment)
│   ├── contact_creator.py      # Contact validation
│   ├── hubspot_contact_real.py # Single contact creation
│   ├── bulk_contact_creator.py # Bulk contact operations
│   ├── account_creator.py      # Company/account creator
│   ├── deal_creator.py         # Deal/opportunity creator
│   ├── quote_creator.py        # Quote shell creator
│   ├── complete_quote_system.py # Complete CPQ system
│   └── product_catalog_generator.py # Product library generator
├── utilities/                   # NON-AI UTILITY SCRIPTS
│   ├── verify_contacts.py      # Check contacts
│   ├── verify_companies.py     # Check companies
│   ├── verify_deals.py         # Check deals
│   ├── verify_quotes.py        # Check quotes
│   └── verify_products.py      # Check products
├── docs/                        # Comprehensive documentation
└── .env                         # API credentials (not in repo)
```

## Current Capabilities

### AI-Powered Agents (with Claude)

1. **Contact Creator** - Validates and enriches contact data with AI
2. **Single Contact Creator** - Creates individual contacts with full enrichment
3. **Bulk Contact Creator** - Processes hundreds/thousands of contacts in batches
4. **Flexible Account Creator** - Creates companies in single or bulk mode
5. **Flexible Deal Creator** - Creates deals/opportunities with AI forecasting
6. **Flexible Quote Creator** - Creates quote shells (limited by HubSpot API)
7. **Complete Quote System** - Full CPQ with products, line items, pricing, totals
8. **Product Catalog Generator** - Creates 100+ products across multiple categories

### Utility Scripts (no AI)

1. **verify_contacts.py** - Quick contact inspection
2. **verify_companies.py** - Quick company inspection
3. **verify_deals.py** - Quick deal inspection
4. **verify_quotes.py** - Quick quote inspection
5. **verify_products.py** - Quick product inspection

All utilities provide fast, simple verification without AI overhead.

## Key Features

- AI-powered data validation and enrichment using Claude
- Flexible single or bulk operation modes
- Batch processing with automatic rate limiting
- Comprehensive error handling and progress tracking
- Production-ready code with professional documentation
- Extensible architecture for multiple business systems
- Quick utilities for data verification

## Technology Stack

- Python 3.12+
- Anthropic Claude API (Claude Sonnet 4)
- HubSpot CRM API
- Modular design for easy system integration
- Environment-based configuration for security

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/vinaygangidi/AgentOpsLab.git
cd AgentOpsLab
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install anthropic hubspot-api-client python-dotenv
```

### 4. Configure API Keys

Create a `.env` file in the project root:
```bash
touch .env
```

Add your API keys:
```
ANTHROPIC_API_KEY=your-anthropic-key-here
HUBSPOT_API_KEY=your-hubspot-key-here
```

### 5. Run an Agent
```bash
# AI-powered agents
python agents/contact_creator.py
python agents/bulk_contact_creator.py
python agents/account_creator.py
python agents/deal_creator.py
python agents/complete_quote_system.py
python agents/product_catalog_generator.py

# Utility scripts
python utilities/verify_contacts.py
python utilities/verify_products.py
```

## Complete Quote System Example

The most powerful feature - create complete, executable quotes:
```bash
python agents/complete_quote_system.py
```

**What it creates:**
- 3 products in catalog (or reuses existing)
- Deal with $42,500 total
- 3 line items with pricing and discounts
- All properly associated
- Ready to send to customer

## Documentation

Comprehensive documentation for each component:

### AI Agent Documentation
- [Contact Creator](docs/contact_creator.md) - Data validation
- [Real Contact Creator](docs/hubspot_contact_real.md) - Single record creation
- [Bulk Contact Creator](docs/bulk_contact_creator.md) - Bulk operations
- [Flexible Account Creator](docs/account_creator.md) - Company creation
- [Flexible Deal Creator](docs/deal_creator.md) - Deal/opportunity creation
- [Flexible Quote Creator](docs/quote_creator.md) - Quote shell creation
- [Complete Quote System](docs/complete_quote_system.md) - Full CPQ system
- [Product Catalog Generator](docs/product_catalog_generator.md) - Product library

### Utility Documentation
- [Utilities](docs/utilities.md) - All verification scripts

## Agent vs Utility - When to Use What

### Use AI Agents When:
- Creating new records
- Bulk operations needed
- Data enrichment required
- Intelligent processing needed
- Complex workflows

### Use Utilities When:
- Quickly checking if data exists
- Inspecting recent records
- Verifying API connectivity
- Debugging issues
- No AI needed

## Configuration Options

Each agent has configurable parameters:
```python
MODE = "single"              # "single" or "bulk"
TOTAL_RECORDS = 1000        # For bulk mode
ENRICH_WITH_CLAUDE = True   # Enable AI enrichment
BATCH_SIZE = 100            # Records per API call
RATE_LIMIT_DELAY = 0.5      # Seconds between batches
```

## Performance

### AI Agents (with Claude enrichment)
- Single mode: 2-4 seconds per record
- Bulk mode: 100 records in 5-10 seconds

### Utilities (no AI)
- Instant response
- 20 records displayed in <1 second

### Complete Quote System
- 3-product quote: ~5 seconds total
- Includes product creation, deal creation, line items, associations

## Use Cases

### Current Implementation (CRM)
- Import contacts from spreadsheets or databases
- Migrate data between CRM systems
- Enrich incomplete contact records with AI
- Bulk create companies/accounts
- Create sales opportunities and deals
- Generate complete quotes with products and pricing
- Build product catalogs
- Quick data verification

### Future Capabilities
- ERP system automation
- Legal document processing
- Revenue recognition
- Cross-system synchronization
- Compliance automation

## HubSpot Requirements

### Required Scopes

#### For Contacts:
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`

#### For Companies:
- `crm.objects.companies.read`
- `crm.objects.companies.write`

#### For Deals:
- `crm.objects.deals.read`
- `crm.objects.deals.write`

#### For Quotes:
- `crm.objects.quotes.read`
- `crm.objects.quotes.write`
- `crm.schemas.quotes.read`
- `crm.schemas.quotes.write`

#### For Products & Line Items:
- `crm.objects.products.read`
- `crm.objects.products.write`
- `crm.objects.line_items.read`
- `crm.objects.line_items.write`
- `e-commerce`

**Note:** After adding scopes, regenerate your access token!

## Security Best Practices

- API keys stored in `.env` file (never committed)
- `.gitignore` configured to exclude sensitive files
- Environment variables loaded at runtime
- No hardcoded credentials

## Cost Considerations

### Claude API Costs (AI Agents Only)

With enrichment enabled:
- Per record: ~$0.001 - $0.002
- 1,000 records: ~$1 - $2
- 10,000 records: ~$10 - $20

**Utilities have ZERO Claude costs** (no AI)

### HubSpot API Costs

Free within plan limits.

## Extending to Other Systems

To add support for a new business system:

1. Install the system's Python SDK
2. Add API credentials to `.env`
3. Copy an existing agent as template
4. Update API calls to match new system
5. Adjust field mappings
6. Test in single mode first
7. Deploy to bulk operations

## Troubleshooting

### Common Issues

**"Module not found" Error**
```bash
source venv/bin/activate
pip install anthropic hubspot-api-client python-dotenv
```

**"API key not found" Error**
```bash
cat .env  # Verify keys are present
```

**HubSpot Scope Errors**
- Add required scopes to Private App
- Regenerate access token
- Update token in .env file

## What We've Built

### Records Created
- ✅ 900 contacts
- ✅ Companies/accounts
- ✅ 100 deals
- ✅ 100 quotes
- ✅ 100 products
- ✅ Complete quotes with line items

### Capabilities
- ✅ Single & bulk operations
- ✅ AI enrichment
- ✅ Batch processing
- ✅ Rate limiting
- ✅ Error handling
- ✅ Progress tracking
- ✅ Complete CPQ workflow
- ✅ Product catalog management
- ✅ Quick verification utilities

## Future Roadmap

Planned enhancements:

- **Multi-System Support**: ERP, legal, CPQ, revenue recognition
- **Advanced Orchestration**: Multi-agent workflows
- **Data Validation**: Deduplication and quality checks
- **CSV Import/Export**: File-based operations
- **Database Integration**: Direct database connectivity
- **Webhook Triggers**: Event-driven automation
- **Email Notifications**: Completion alerts
- **Web Dashboard**: Visual monitoring
- **API Endpoints**: REST API
- **Association Management**: Link all objects
- **Custom Objects**: Support for custom HubSpot objects

## Contributing

This is a personal learning and automation project. Suggestions and feedback welcome.

## License

This project is for educational and business automation purposes.

## Contact

Created by Vinay Gangidi

Repository: https://github.com/vinaygangidi/AgentOpsLab

## Acknowledgments

- Anthropic for Claude AI
- HubSpot for CRM platform and API access
- Python community for excellent libraries