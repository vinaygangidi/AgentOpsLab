# Bulk Contact Creator Agent Documentation

## Overview

The Bulk Contact Creator Agent is a production-ready tool for creating hundreds or thousands of contacts in HubSpot efficiently. It uses HubSpot's batch API to create up to 100 contacts per request, includes rate limiting to respect API limits, and provides detailed progress tracking.

## Purpose

This agent demonstrates:
- Production-scale data operations
- Batch API usage for efficiency
- Rate limiting and error handling
- Progress tracking and reporting
- Mock data generation for testing

## File Location

`agents/bulk_contact_creator.py`

## What This Agent Does

### Overview of Process

1. **Generate or Load Contact Data**
   - Creates mock contacts for testing, or
   - In production, would load from CSV, database, or API

2. **Optional AI Enrichment**
   - Can enrich a sample of contacts with Claude AI
   - Configurable to balance cost vs. quality

3. **Batch Processing**
   - Groups contacts into batches of 100 (HubSpot's limit)
   - Sends each batch to HubSpot API
   - Tracks success and failure counts

4. **Rate Limiting**
   - Waits 0.5 seconds between batches
   - Prevents hitting HubSpot API rate limits

5. **Progress Reporting**
   - Shows batch number, success count, timing
   - Provides final summary with success rate

## How to Use

### Basic Usage

Run the agent with default settings (900 contacts):
```bash
python agents/bulk_contact_creator.py
```

### Expected Output
```
======================================================================
BULK HUBSPOT CONTACT CREATOR
======================================================================
Generating 900 mock contacts
Generated 900 contacts successfully

Starting bulk creation of 900 contacts
Batch size: 100 contacts per request
======================================================================

Batch 1/9: Processing 100 contacts
Batch 1 complete: 100 contacts created in 2.34s
Progress: 100/900 (11.1%)
Waiting 0.5s before next batch

Batch 2/9: Processing 100 contacts
Batch 2 complete: 100 contacts created in 2.45s
Progress: 200/900 (22.2%)
Waiting 0.5s before next batch

[... continues for all 9 batches ...]

======================================================================
BULK CREATION SUMMARY
======================================================================
Successfully created: 900 contacts
Failed: 0 contacts
Success rate: 100.0%

View in HubSpot: https://app.hubspot.com/contacts
======================================================================
```

### Time Estimates

Creating contacts takes approximately:
- 100 contacts: 3-5 seconds
- 500 contacts: 15-20 seconds
- 900 contacts: 25-30 seconds
- 5000 contacts: 2-3 minutes

## Configuration

### Key Constants

At the top of the file, you can adjust these settings:
```python
BATCH_SIZE = 100           # HubSpot API limit, do not change
RATE_LIMIT_DELAY = 0.5     # Seconds to wait between batches
```

### In the main() Function
```python
# Configuration
total_contacts = 900        # Change this number
enrich_sample = False       # Set to True to enrich first 10
```

### Changing Total Contacts

To create a different number of contacts:
```python
total_contacts = 5000  # Create 5000 contacts instead
```

### Enabling AI Enrichment

To enrich a sample with Claude AI:
```python
enrich_sample = True  # Enrich first 10 contacts
```

This adds 2-3 seconds per enriched contact but improves data quality.

## Mock Data Generation

### How It Works

The agent generates realistic mock data by combining:
- 10 first names
- 10 last names (with index appended for uniqueness)
- 10 companies
- 8 industries
- 8 job titles

### Example Generated Contact
```python
{
    "firstname": "Sarah",
    "lastname": "Johnson245",
    "email": "contact245@techcorp.com",
    "phone": "5550000245",
    "company": "TechCorp",
    "jobtitle": "Product Manager",
    "industry": "Technology"
}
```

### Customizing Mock Data

Edit the arrays in `generate_mock_contacts()`:
```python
first_names = ["Alice", "Bob", "Carol", "David"]  # Add your names
companies = ["Acme Inc", "Best Corp"]             # Add your companies
job_titles = ["CEO", "Manager", "Developer"]      # Add your titles
```

## Batch Processing Details

### Why Use Batches

HubSpot's batch API allows up to 100 contacts per request. Batching provides:
- Much faster than individual API calls (100x speedup)
- More efficient use of API rate limits
- Better error isolation (one batch fails, others continue)

### Batch API Format

The agent formats data like this:
```python
batch_input = {
    "inputs": [
        {"properties": {"firstname": "John", "lastname": "Smith", ...}},
        {"properties": {"firstname": "Jane", "lastname": "Doe", ...}},
        # ... up to 100 contacts
    ]
}
```

### Error Handling Per Batch

If a batch fails:
- The error is logged
- Failed contact count increases
- Processing continues with next batch
- Final summary shows total failures

## Rate Limiting

### Why Rate Limiting Matters

HubSpot enforces API rate limits:
- Free/Starter: 100 requests per 10 seconds
- Professional/Enterprise: Higher limits

Without rate limiting, you could hit these limits and get errors.

### How This Agent Handles It

The agent waits 0.5 seconds between batches:
```python
if i + batch_size < total:
    print(f"Waiting {RATE_LIMIT_DELAY}s before next batch")
    time.sleep(RATE_LIMIT_DELAY)
```

### Adjusting Rate Limit Delay

If you have a Professional/Enterprise account with higher limits:
```python
RATE_LIMIT_DELAY = 0.2  # Faster processing
```

If you are hitting rate limits:
```python
RATE_LIMIT_DELAY = 1.0  # Slower, safer processing
```

## AI Enrichment Option

### How Sample Enrichment Works

When `enrich_sample = True`, the agent:
1. Takes the first 10 contacts
2. Sends each to Claude AI
3. Gets improved job titles based on context
4. Updates contacts before creating in HubSpot

### Cost vs. Quality Tradeoff

Enriching contacts costs:
- Claude API: ~$0.001 per contact
- Processing time: ~2 seconds per contact

For 900 contacts with full enrichment:
- Cost: ~$0.90
- Additional time: ~30 minutes

Sample enrichment (10 contacts):
- Cost: ~$0.01
- Additional time: ~20 seconds

### When to Enrich

Enrich contacts when:
- Data quality is critical
- You have incomplete job titles
- Contacts are high-value leads or customers

Skip enrichment when:
- Data is already complete
- Speed is more important
- Processing thousands of contacts

## Production Usage

### Loading from CSV

Replace `generate_mock_contacts()` with CSV loading:
```python
import csv

def load_contacts_from_csv(filename):
    contacts = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contact = {
                "firstname": row['First Name'],
                "lastname": row['Last Name'],
                "email": row['Email'],
                "phone": row.get('Phone', ''),
                "company": row.get('Company', ''),
                "jobtitle": row.get('Job Title', ''),
                "industry": row.get('Industry', '')
            }
            contacts.append(contact)
    return contacts

# In main():
contacts = load_contacts_from_csv('contacts.csv')
```

### Database Integration

Load from a database:
```python
import sqlite3

def load_contacts_from_database():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT firstname, lastname, email, phone, company, jobtitle, industry
        FROM contacts
        WHERE synced_to_hubspot = 0
    """)
    
    contacts = []
    for row in cursor.fetchall():
        contact = {
            "firstname": row[0],
            "lastname": row[1],
            "email": row[2],
            "phone": row[3],
            "company": row[4],
            "jobtitle": row[5],
            "industry": row[6]
        }
        contacts.append(contact)
    
    conn.close()
    return contacts
```

### Adding Validation

Validate contacts before processing:
```python
def validate_contacts(contacts):
    valid = []
    invalid = []
    
    for contact in contacts:
        # Check required fields
        if not contact.get('email'):
            invalid.append((contact, "Missing email"))
            continue
        
        if not '@' in contact['email']:
            invalid.append((contact, "Invalid email"))
            continue
        
        if not contact.get('firstname') or not contact.get('lastname'):
            invalid.append((contact, "Missing name"))
            continue
        
        valid.append(contact)
    
    return valid, invalid

# In main():
valid_contacts, invalid_contacts = validate_contacts(contacts)
print(f"Valid: {len(valid_contacts)}, Invalid: {len(invalid_contacts)}")

if invalid_contacts:
    print("Invalid contacts:")
    for contact, reason in invalid_contacts:
        print(f"  {contact.get('email', 'No email')}: {reason}")

# Process only valid contacts
created, failed = create_contacts_in_batches(valid_contacts)
```

## Error Recovery

### Logging Failed Contacts

Save failed contacts for retry:
```python
failed_contacts = []

# In the batch processing loop:
except Exception as e:
    failed += len(batch)
    failed_contacts.extend(batch)
    print(f"Batch {batch_num} failed: {e}")

# After processing:
if failed_contacts:
    with open('failed_contacts.json', 'w') as f:
        json.dump(failed_contacts, f, indent=2)
    print(f"Failed contacts saved to failed_contacts.json")
```

### Retry Logic

Add automatic retry for failed batches:
```python
max_retries = 3

for retry in range(max_retries):
    try:
        api_response = hubspot.crm.contacts.batch_api.create(
            batch_input_simple_public_object_batch_input_for_create=batch_input
        )
        break  # Success, exit retry loop
    except Exception as e:
        if retry < max_retries - 1:
            wait_time = (retry + 1) * 2  # Exponential backoff
            print(f"Retry {retry + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)
        else:
            print(f"Failed after {max_retries} retries: {e}")
            failed += len(batch)
```

## Performance Optimization

### Current Performance

With default settings:
- 900 contacts in ~30 seconds
- 100 contacts per 2-3 seconds
- ~3 contacts per second

### Faster Processing

To speed up (requires higher API limits):
```python
RATE_LIMIT_DELAY = 0.1  # Reduce from 0.5 to 0.1
```

This can process:
- 900 contacts in ~15 seconds
- ~6 contacts per second

Warning: Only do this if you have Professional/Enterprise HubSpot.

### Parallel Processing

For extremely large datasets (10,000+ contacts), consider:
- Split into multiple files
- Run multiple instances of the agent
- Process in parallel

Note: Be careful not to exceed HubSpot's rate limits.

## Monitoring and Reporting

### Adding Email Notifications

Send email when complete:
```python
import smtplib
from email.mime.text import MIMEText

def send_completion_email(created, failed):
    msg = MIMEText(f"""
    Bulk contact creation complete:
    
    Successfully created: {created}
    Failed: {failed}
    Success rate: {(created/(created+failed)*100):.1f}%
    """)
    
    msg['Subject'] = 'HubSpot Bulk Import Complete'
    msg['From'] = 'agent@yourdomain.com'
    msg['To'] = 'admin@yourdomain.com'
    
    # Send email (configure your SMTP server)
    # s = smtplib.SMTP('localhost')
    # s.send_message(msg)
    # s.quit()

# In main():
send_completion_email(created, failed)
```

### Logging to File

Save detailed logs:
```python
import logging

logging.basicConfig(
    filename='bulk_import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In the batch processing:
logging.info(f"Batch {batch_num}: {batch_created} contacts created")
logging.error(f"Batch {batch_num} failed: {e}")
```

## Common Issues

### Issue: All Batches Failing

Possible causes:
- Invalid HubSpot API key
- Missing required permissions
- Network connectivity issues
- HubSpot API is down

Check:
1. Verify API key in `.env` file
2. Check Private App scopes
3. Test with single contact creator first

### Issue: Some Batches Failing

Possible causes:
- Duplicate email addresses
- Missing required fields
- Invalid data format
- Rate limit exceeded

Solution:
- Add validation before processing
- Check HubSpot error messages in output
- Reduce `RATE_LIMIT_DELAY`

### Issue: Slow Performance

Possible causes:
- Too much delay between batches
- Network latency
- Enrichment enabled for all contacts

Solutions:
- Reduce `RATE_LIMIT_DELAY` if you have higher limits
- Run from server with better connectivity
- Disable enrichment or use sample only

## Best Practices

### Before Running in Production

1. **Test with small batch**
```python
   total_contacts = 10  # Test with 10 first
```

2. **Validate your data**
   - Check for duplicate emails
   - Verify required fields are present
   - Test email format validity

3. **Backup existing data**
   - Export current HubSpot contacts
   - Keep source data file safe

4. **Monitor first run**
   - Watch for errors
   - Check HubSpot to verify data looks correct

### During Production Runs

1. **Monitor progress** - Check output regularly
2. **Verify in HubSpot** - Spot-check created contacts
3. **Save logs** - Redirect output to file for records
4. **Be ready to stop** - Use Ctrl+C if something looks wrong

### After Completion

1. **Review summary** - Check success rate
2. **Verify in HubSpot** - Confirm contact count matches
3. **Check data quality** - Spot-check several contacts
4. **Save results** - Keep logs for auditing

## Scaling Beyond 900 Contacts

### For 5,000-10,000 Contacts

The current agent handles this well:
- Processing time: 3-5 minutes
- No code changes needed
- Just change `total_contacts` value

### For 50,000+ Contacts

Consider:
- Split into multiple runs
- Add database checkpointing
- Implement resume capability
- Use more sophisticated error handling

### For Millions of Contacts

At this scale:
- Consider professional data import services
- Use HubSpot's import tool
- Work with HubSpot support for best practices

## Related Documentation

- [Contact Creator (Testing)](contact_creator.md)
- [Real HubSpot Contact Creator](hubspot_contact_real.md)
- [HubSpot Batch API Documentation](https://developers.hubspot.com/docs/api/crm/contacts)