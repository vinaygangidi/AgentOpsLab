# Real HubSpot Contact Creator Agent Documentation

## Overview

The Real HubSpot Contact Creator Agent creates actual contacts in your HubSpot CRM. Unlike the mock testing agent, this agent connects to HubSpot's API and creates real contact records. It uses Claude AI to enrich contact data before sending it to HubSpot.

## Purpose

This agent demonstrates:
- Real HubSpot API integration
- AI-powered data enrichment in production
- Single contact creation workflow
- Error handling for API operations

## File Location

`agents/hubspot_contact_real.py`

## What This Agent Does

### Step 1: Data Enrichment with Claude

The agent sends contact information to Claude AI for enrichment:
- Suggests appropriate job title based on name and company
- Identifies the company's industry
- Formats phone numbers consistently
- Validates email addresses

### Step 2: HubSpot Contact Creation

The agent takes the enriched data and:
- Prepares it in HubSpot's required format
- Calls HubSpot's contact creation API
- Returns the new contact ID
- Provides a direct link to view the contact in HubSpot

### Result

A new contact appears in your HubSpot CRM with enriched, validated data.

## How to Use

### Prerequisites

Before running this agent, make sure:
1. You have a HubSpot account
2. You have created a Private App in HubSpot
3. Your Private App has contact read/write permissions
4. Your HubSpot API key is in the `.env` file

### Basic Usage

Run the agent from the command line:
```bash
python agents/hubspot_contact_real.py
```

### Expected Output
```
======================================================================
REAL HUBSPOT CONTACT CREATOR WITH CLAUDE AI
======================================================================

Step 1: Enriching contact with Claude AI
Claude enrichment complete
JOB_TITLE: Software Engineer
INDUSTRY: Technology
FORMATTED_PHONE: (555) 987-6543
EMAIL_VALID: Yes

Step 2: Creating contact in HubSpot
Contact created successfully in HubSpot
Contact ID: 12345
View in HubSpot: https://app.hubspot.com/contacts/contact/12345

======================================================================
SUCCESS: Contact created in your HubSpot account
======================================================================
```

### Verify in HubSpot

After running the agent:
1. Go to https://app.hubspot.com/contacts
2. Look for the newly created contact
3. Check that enriched data (job title, industry) is populated

## Code Structure

### Main Components

1. **Client Initialization**
```python
   claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
   hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))
```

2. **Sample Contact Data**
```python
   MOCK_CONTACT = {
       "firstname": "Sarah",
       "lastname": "Johnson",
       "email": "sarah.johnson@techcorp.com",
       "phone": "5559876543",
       "company": "TechCorp Industries"
   }
```

3. **enrich_contact_with_claude() Function**
   - Sends contact to Claude for enrichment
   - Returns job title, industry, formatted phone, validation status

4. **create_hubspot_contact() Function**
   - Takes enriched data
   - Creates contact in HubSpot via API
   - Returns contact ID or error

5. **main() Function**
   - Orchestrates the two-step process
   - Handles overall workflow

## Configuration

### Modifying the Test Contact

Change the MOCK_CONTACT dictionary to test with different data:
```python
MOCK_CONTACT = {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@company.com",
    "phone": "5551234567",
    "company": "Example Corp"
}
```

### Adjusting Claude's Enrichment

Modify the enrichment prompt to ask for different information:
```python
prompt = f"""You are a contact enrichment agent. Review this contact:

[Your custom instructions]

Return ONLY in this exact format:
JOB_TITLE: [title]
INDUSTRY: [industry]
CUSTOM_FIELD: [value]
"""
```

### Adding More HubSpot Fields

Expand the properties dictionary to include additional HubSpot fields:
```python
properties = {
    "firstname": contact_data['firstname'],
    "lastname": contact_data['lastname'],
    "email": contact_data['email'],
    "phone": enriched_data.get('FORMATTED_PHONE'),
    "company": contact_data['company'],
    "jobtitle": enriched_data.get('JOB_TITLE'),
    "industry": enriched_data.get('INDUSTRY'),
    # Add more fields here
    "website": "https://example.com",
    "lifecyclestage": "lead",
    "hs_lead_status": "NEW"
}
```

## Advanced Usage

### Creating Multiple Contacts

To create multiple contacts one at a time:
```python
contacts_to_create = [
    {"firstname": "John", "lastname": "Smith", ...},
    {"firstname": "Jane", "lastname": "Doe", ...},
    {"firstname": "Bob", "lastname": "Wilson", ...}
]

for contact in contacts_to_create:
    enriched = enrich_contact_with_claude(contact)
    result = create_hubspot_contact(contact, enriched)
    time.sleep(1)  # Wait 1 second between creations
```

Note: For large batches, use the bulk creator agent instead.

### Reading from CSV

To read contacts from a CSV file:
```python
import csv

with open('contacts.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        contact = {
            "firstname": row['First Name'],
            "lastname": row['Last Name'],
            "email": row['Email'],
            "phone": row['Phone'],
            "company": row['Company']
        }
        enriched = enrich_contact_with_claude(contact)
        create_hubspot_contact(contact, enriched)
```

## Error Handling

### Common Errors

1. **"Invalid API key"**
   - Check that HUBSPOT_API_KEY is correct in `.env`
   - Verify the Private App is still active

2. **"Contact already exists"**
   - HubSpot prevents duplicate emails
   - Use update API instead, or check existing contacts first

3. **"Missing required property"**
   - Email is required for all contacts
   - Some HubSpot accounts require additional fields

4. **"Rate limit exceeded"**
   - You have made too many API calls
   - Wait and retry, or use bulk API

### Improving Error Handling

Add try-catch around the enrichment step:
```python
try:
    enriched = enrich_contact_with_claude(contact)
except Exception as e:
    print(f"Enrichment failed: {e}")
    # Use default values instead
    enriched = {
        "JOB_TITLE": "Unknown",
        "INDUSTRY": "Unknown",
        "FORMATTED_PHONE": contact['phone']
    }
```

## HubSpot API Details

### Contact Properties

HubSpot contacts have many standard properties:
- firstname, lastname, email (common)
- phone, mobilephone, company (common)
- jobtitle, industry, city, state (common)
- website, linkedin, twitter (social)
- lifecyclestage, hs_lead_status (sales process)

View all available properties in HubSpot:
Settings > Properties > Contact Properties

### API Scopes Required

Your HubSpot Private App needs these scopes:
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`

Without these, the agent will fail with permission errors.

### API Rate Limits

HubSpot has rate limits:
- 100 requests per 10 seconds (Free/Starter)
- Higher limits for Professional/Enterprise

This single-contact agent stays well within limits, but be careful when looping.

## Cost Considerations

### Claude API Costs

Each contact creation uses:
- Approximately 100 input tokens (your prompt)
- Approximately 50 output tokens (Claude's response)
- Total cost: ~$0.001 per contact (with Sonnet 4)

For 1000 contacts: approximately $1 in Claude API costs.

### HubSpot Costs

HubSpot API usage is free within your plan's limits. Contact storage depends on your HubSpot subscription tier.

## Performance

### Speed

Single contact creation takes:
- 1-2 seconds for Claude enrichment
- 1-2 seconds for HubSpot API call
- Total: 2-4 seconds per contact

### When to Use This Agent

Use this agent when:
- Creating individual contacts manually
- Testing the enrichment process
- Creating a small number of high-value contacts (under 50)

For bulk operations (100+ contacts), use the bulk creator agent instead.

## Security Best Practices

### Protecting API Keys

Never commit API keys to Git:
- Always use `.env` file
- Verify `.gitignore` includes `.env`
- Rotate keys if accidentally exposed

### Data Privacy

Be careful with contact data:
- Only create contacts you have permission to add
- Follow data protection regulations (GDPR, CCPA)
- Don't store sensitive data in code or logs

## Testing

### Test Mode

Before running in production, test with fake data:
```python
TEST_CONTACT = {
    "firstname": "Test",
    "lastname": "User",
    "email": f"test{time.time()}@example.com",  # Unique email
    "phone": "5555555555",
    "company": "Test Company"
}
```

You can delete test contacts from HubSpot afterward.

### Validation Before Creation

Add validation to prevent bad data:
```python
def validate_contact(contact):
    if not contact.get('email'):
        return False, "Email is required"
    if not '@' in contact['email']:
        return False, "Invalid email format"
    if not contact.get('firstname') or not contact.get('lastname'):
        return False, "First and last name required"
    return True, "Valid"

# Use before creating
valid, message = validate_contact(contact)
if not valid:
    print(f"Validation failed: {message}")
    return
```

## Limitations

1. **Single Contact at a Time**
   - Not optimized for bulk operations
   - Slower than batch API for large datasets

2. **No Duplicate Detection**
   - Does not check if contact already exists
   - HubSpot will reject duplicate emails

3. **Fixed Enrichment Logic**
   - Same enrichment for all contacts
   - No conditional logic based on data quality

4. **No Rollback**
   - If creation succeeds but you want to undo it
   - Must manually delete from HubSpot

## Next Steps

After mastering this agent:

1. **Scale Up**: Use the bulk contact creator for large datasets
2. **Customize**: Add more HubSpot fields specific to your needs
3. **Integrate**: Connect to your own data sources (databases, CRMs)
4. **Enhance**: Add duplicate detection and data validation
5. **Automate**: Trigger this agent from webhooks or scheduled jobs

## Related Documentation

- [Contact Creator (Testing)](contact_creator.md)
- [Bulk Contact Creator](bulk_contact_creator.md)
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/crm/contacts)