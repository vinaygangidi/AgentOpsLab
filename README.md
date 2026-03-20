# AgentOpsLab - HubSpot AI Automation

A collection of AI-powered agents that automate HubSpot CRM operations using Claude AI for intelligent data processing.

## Overview

This project demonstrates how to build production-ready AI agents that integrate with HubSpot CRM. The agents use Anthropic's Claude AI to enrich and validate data before creating records in HubSpot.

## What This Project Does

This repository contains four AI agents:

1. **Contact Creator** - Tests contact validation with mock data
2. **Real HubSpot Contact Creator** - Creates single contacts in HubSpot with AI enrichment
3. **Bulk Contact Creator** - Creates hundreds of contacts in batches with rate limiting
4. **Flexible Account Creator** - Creates companies in single or bulk mode (1 to 1,000,000+ records)

All agents use Claude AI to intelligently process data before sending it to HubSpot.

## Key Features

- AI-powered data enrichment using Claude
- Real HubSpot CRM integration
- Batch processing with rate limiting
- Error handling and progress tracking
- Production-ready code structure

## Technology Stack

- Python 3.14
- Anthropic Claude API (Claude Sonnet 4)
- HubSpot API
- Environment-based configuration

## Project Structure
```
AgentOpsLab/
├── agents/                      # AI agent implementations
│   ├── contact_creator.py      # Mock data testing agent
│   ├── hubspot_contact_real.py # Single contact creator
│   └── bulk_contact_creator.py # Bulk contact creator
├── docs/                        # Detailed documentation
│   ├── contact_creator.md
│   ├── hubspot_contact_real.md
│   └── bulk_contact_creator.md
├── tools/                       # Future: Utility functions
├── data/                        # Future: Data files
└── .env                         # API credentials (not in repo)
```

## Prerequisites

Before you begin, you need:

1. Python 3.12 or higher installed
2. Anthropic API key (get from https://console.anthropic.com)
3. HubSpot Private App access token
4. Basic understanding of command line

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
pip install anthropic hubspot-api-client python-dotenv pydantic langchain-anthropic
```

### 4. Configure API Keys

Create a `.env` file in the project root:
```bash
touch .env
```

Add your API keys to the `.env` file:
```
ANTHROPIC_API_KEY=your-anthropic-key-here
HUBSPOT_API_KEY=your-hubspot-key-here
```

### 5. Run an Agent

Test the contact creator:
```bash
python agents/contact_creator.py
```

Create a real contact in HubSpot:
```bash
python agents/hubspot_contact_real.py
```

Create 900 contacts in bulk:
```bash
python agents/bulk_contact_creator.py
```

## Documentation

Detailed documentation for each agent is available in the `docs/` folder:

- [Contact Creator Agent](docs/contact_creator.md) - Mock data testing
- [Real HubSpot Contact Creator](docs/hubspot_contact_real.md) - Single contact creation
- [Bulk Contact Creator](docs/bulk_contact_creator.md) - Bulk operations for contacts
- [Flexible Account Creator](docs/account_creator.md) - Single or bulk company creation

## How It Works

### Data Flow

1. Agent generates or receives contact data
2. Claude AI analyzes and enriches the data (job titles, industries, formatting)
3. Agent sends enriched data to HubSpot via API
4. HubSpot creates the contact record
5. Agent reports success or failure

### Why Use AI for Data Enrichment

Traditional data entry often has issues:
- Inconsistent formatting
- Missing information
- Invalid data

Claude AI helps by:
- Validating email formats
- Formatting phone numbers consistently
- Suggesting appropriate job titles based on context
- Identifying data quality issues
- Enriching incomplete records

## Configuration Options

Each agent has configurable parameters at the top of the file:

### Bulk Contact Creator Configuration
```python
TOTAL_CONTACTS = 900      # How many contacts to create
BATCH_SIZE = 100          # Contacts per API call (HubSpot limit)
RATE_LIMIT_DELAY = 0.5    # Seconds to wait between batches
ENRICH_SAMPLE = False     # Set True to enrich first 10 with Claude
```

## API Rate Limits

This project respects HubSpot's API rate limits:

- Batch API: 100 contacts per request
- Rate limiting: 0.5 second delay between batches
- Error handling: Continues on failure, reports results

## Security

Important security practices used in this project:

- API keys stored in `.env` file (never committed to Git)
- `.gitignore` configured to exclude sensitive files
- Environment variables loaded at runtime
- No hardcoded credentials

## Troubleshooting

### SSL Certificate Error

If you see SSL certificate errors:
```bash
pip install --upgrade certifi
```

### Import Errors

Make sure you are in the virtual environment:
```bash
source venv/bin/activate
```

Reinstall dependencies if needed:
```bash
pip install -r requirements.txt
```

### HubSpot API Errors

Check that:
- Your HubSpot API key is valid
- Your Private App has correct scopes (contacts read/write)
- You have not exceeded API rate limits

## Future Enhancements

Planned features for this project:

- Account/Company creator agent
- Deal/Opportunity creator agent
- Quote and invoice generators
- CSV file import support
- Data deduplication
- Email notifications
- Webhook triggers
- Multi-agent pipelines

## Contributing

This is a personal learning project, but suggestions and feedback are welcome.

## License

This project is for educational purposes.

## Contact

Created by Vinay Gangidi

Repository: https://github.com/vinaygangidi/AgentOpsLab

## Acknowledgments

- Anthropic for Claude AI
- HubSpot for CRM platform
- Python community for excellent libraries