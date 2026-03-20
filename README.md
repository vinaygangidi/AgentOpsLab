# AgentOpsLab - Intelligent Business Automation Platform

A flexible collection of AI-powered agents that automate operations across multiple business systems including CRM, ERP, CPQ, legal, and revenue recognition platforms. Built with Claude AI for intelligent data processing and enrichment.

## Overview

AgentOpsLab provides production-ready AI agents that can create, update, and manage records across various enterprise systems. Each agent uses Anthropic's Claude AI to validate, enrich, and process data intelligently before interacting with external systems.

## Current Capabilities

This platform currently includes agents for CRM automation (HubSpot implementation):

1. **Contact Creator** - Validates and enriches contact data with AI before creation
2. **Single Contact Creator** - Creates individual contacts with full AI enrichment
3. **Bulk Contact Creator** - Processes hundreds or thousands of contacts in batches
4. **Flexible Account Creator** - Creates companies in single or bulk mode (1 to millions of records)

All agents use the same flexible architecture and can be adapted to work with other systems.

## Key Features

- AI-powered data validation and enrichment using Claude
- Flexible single or bulk operation modes
- Batch processing with automatic rate limiting
- Comprehensive error handling and progress tracking
- Production-ready code with professional documentation
- Extensible architecture for multiple business systems

## Technology Stack

- Python 3.12+
- Anthropic Claude API (Claude Sonnet 4)
- Modular design for easy system integration
- Environment-based configuration for security

## Project Structure
```
AgentOpsLab/
├── agents/                      # AI agent implementations
│   ├── contact_creator.py      # Contact validation and testing
│   ├── hubspot_contact_real.py # Single contact with AI enrichment
│   ├── bulk_contact_creator.py # Bulk contact operations
│   └── account_creator.py      # Flexible company/account creator
├── docs/                        # Comprehensive documentation
│   ├── contact_creator.md
│   ├── hubspot_contact_real.md
│   ├── bulk_contact_creator.md
│   └── account_creator.md
├── tools/                       # Utility functions (future)
├── data/                        # Data files (future)
└── .env                         # API credentials (not in repo)
```

## Prerequisites

Before you begin, you need:

1. Python 3.12 or higher installed
2. Anthropic API key (get from https://console.anthropic.com)
3. API access to your target system (currently HubSpot)
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

Test with contact validation:
```bash
python agents/contact_creator.py
```

Create a real record:
```bash
python agents/hubspot_contact_real.py
```

Process bulk records:
```bash
python agents/bulk_contact_creator.py
```

## Agent Architecture

### How Agents Work

All agents follow a consistent pattern:

1. **Data Input** - Accept data from user, file, or database
2. **AI Enrichment** - Claude validates and enriches data intelligently
3. **System Integration** - Formatted data sent to target system via API
4. **Result Tracking** - Success/failure logged and reported

### Flexible Operation Modes

Agents support both single and bulk operations:

**Single Mode:**
- Individual record processing
- Full AI enrichment
- Detailed error reporting
- Best for manual operations and testing

**Bulk Mode:**
- Batch processing (100+ records per request)
- Automatic rate limiting
- Progress tracking
- Production-ready for large datasets

## Use Cases

### Current Implementation (CRM)
- Import contacts from spreadsheets or databases
- Migrate data between CRM systems
- Enrich incomplete contact records with AI
- Bulk create companies/accounts
- Data quality validation before import

### Future Capabilities
- ERP system automation (orders, invoices, inventory)
- Legal document processing and management
- CPQ (Configure, Price, Quote) automation
- Revenue recognition record creation
- Cross-system data synchronization
- Compliance and audit trail generation

## Documentation

Detailed documentation for each agent is available in the `docs/` folder:

- [Contact Creator Agent](docs/contact_creator.md) - Data validation and testing
- [Real Contact Creator](docs/hubspot_contact_real.md) - Single record creation
- [Bulk Contact Creator](docs/bulk_contact_creator.md) - Bulk operations
- [Flexible Account Creator](docs/account_creator.md) - Single or bulk company creation

## Configuration Options

Each agent has configurable parameters:

### Contact and Account Creators
```python
MODE = "single"              # "single" or "bulk"
TOTAL_RECORDS = 1000        # For bulk mode
ENRICH_WITH_CLAUDE = True   # Enable AI enrichment
BATCH_SIZE = 100            # Records per API call
RATE_LIMIT_DELAY = 0.5      # Seconds between batches
```

## Security Best Practices

This project follows security best practices:

- API keys stored in `.env` file (never committed to Git)
- `.gitignore` configured to exclude sensitive files
- Environment variables loaded at runtime
- No hardcoded credentials in code

## Extending to Other Systems

To add support for a new business system:

1. Install the system's Python SDK
2. Add API credentials to `.env`
3. Copy an existing agent as a template
4. Update API calls to match new system
5. Adjust field mappings as needed
6. Test in single mode first
7. Deploy to bulk operations

The architecture is system-agnostic and designed for easy extension.

## Performance

### Single Mode
- 2-4 seconds per record with AI enrichment
- 1-2 seconds per record without enrichment

### Bulk Mode
- 100 records: 5-10 seconds
- 1,000 records: 40-60 seconds
- 10,000 records: 6-10 minutes
- Scales linearly with proper rate limiting

## API Rate Limits

Agents automatically respect system rate limits:
- Batch processing to maximize throughput
- Configurable delays between batches
- Automatic retry logic for transient failures
- Progress tracking for long-running operations

## Cost Considerations

### Claude API Costs

With Claude Sonnet 4:
- Per record enrichment: ~$0.001 - $0.002
- 1,000 records: ~$1 - $2
- 10,000 records: ~$10 - $20

Cost optimization strategies:
- Sample enrichment (enrich first 10-100 only)
- Conditional enrichment (only incomplete records)
- Batch processing to minimize overhead

### System API Costs

Most business systems provide free API access within plan limits. Check your specific system's documentation.

## Troubleshooting

### Common Issues

**"Module not found" Error**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"API key not found" Error**
```bash
cat .env  # Verify keys are present
```

**SSL Certificate Error**
```bash
pip install --upgrade certifi
```

**Rate Limit Exceeded**
- Increase RATE_LIMIT_DELAY
- Reduce BATCH_SIZE
- Wait before retrying

## Future Roadmap

Planned enhancements:

- **Multi-System Support**: ERP, legal, CPQ, revenue recognition
- **Advanced Orchestration**: Multi-agent workflows using CrewAI
- **Data Validation**: Deduplication and quality checks
- **CSV Import/Export**: File-based data operations
- **Database Integration**: Direct database connectivity
- **Webhook Triggers**: Event-driven automation
- **Email Notifications**: Completion and error alerts
- **Web Dashboard**: Visual monitoring and control
- **API Endpoints**: REST API for external integrations

## Contributing

This is a personal learning and automation project. Suggestions and feedback are welcome.

## License

This project is for educational and business automation purposes.

## Contact

Created by Vinay Gangidi

Repository: https://github.com/vinaygangidi/AgentOpsLab

## Acknowledgments

- Anthropic for Claude AI
- Business system providers for API access
- Python community for excellent libraries