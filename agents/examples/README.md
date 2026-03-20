# Example Agents - Learning & Reference

This folder contains simplified example agents for learning purposes. These demonstrate core concepts but are superseded by the production agents in the main `agents/` folder.

## Files

### contact_validator.py

**Purpose:** Demonstrates Claude AI validation without creating records in HubSpot.

**What it does:**
- Validates email format
- Formats phone numbers
- Suggests job titles
- Assesses data quality
- Provides recommendations

**What it does NOT do:**
- Create records in HubSpot
- Bulk processing
- Production-ready operations

**Use this for:**
- Understanding Claude AI integration
- Testing validation logic
- Learning prompt engineering
- Experimenting with enrichment

**For production, use:** `agents/contact_creator_agent.py`

---

### single_contact_demo.py

**Purpose:** Simple example of creating a single contact with enrichment.

**What it does:**
- Creates one contact at a time
- Claude AI enrichment
- Basic error handling

**What it does NOT do:**
- Bulk operations
- Batch processing
- Flexible modes

**Use this for:**
- Understanding basic HubSpot API integration
- Learning single-record creation
- Simple proof-of-concept

**For production, use:** `agents/contact_creator_agent.py` (set MODE="single")

---

## Why These Exist

These examples were created during the development process to:

1. **Learn the fundamentals** - Start simple before building complex systems
2. **Test integrations** - Validate Claude AI and HubSpot API separately
3. **Prototype patterns** - Experiment with architecture before production
4. **Document evolution** - Show the learning journey

## Migration to Production Agents

All functionality from these examples is available in production agents:

| Example | Production Agent | Configuration |
|---------|-----------------|---------------|
| contact_validator.py | contact_creator_agent.py | MODE="single", ENRICH_WITH_CLAUDE=True |
| single_contact_demo.py | contact_creator_agent.py | MODE="single" |

## Running Examples
```bash
# Validation only (no HubSpot creation)
python agents/examples/contact_validator.py

# Single contact creation
python agents/examples/single_contact_demo.py
```

## Key Differences from Production

| Feature | Examples | Production Agents |
|---------|----------|-------------------|
| Flexibility | Single purpose | 1 to millions of records |
| Error Handling | Basic | Comprehensive |
| Rate Limiting | None | Built-in |
| Progress Tracking | None | Real-time |
| Batch Processing | No | Yes |
| Configuration | Hardcoded | Flexible MODE setting |

## Recommendation

**Use production agents for all real work.**

Keep these examples for:
- Learning reference
- Understanding core concepts
- Teaching others
- Historical context