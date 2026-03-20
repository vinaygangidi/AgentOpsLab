# Contact Creator Agent Documentation

## Overview

The Contact Creator Agent is a testing tool that validates and enriches contact data using Claude AI. It works with mock data and does not actually create contacts in HubSpot. This agent is useful for testing data quality and Claude's enrichment capabilities before running production operations.

## Purpose

This agent demonstrates:
- How to structure an AI agent
- How to interact with Claude API
- How to validate contact data
- What kind of enrichment Claude can provide

## File Location

`agents/contact_creator.py`

## What This Agent Does

### Input
The agent starts with basic contact information:
- Name
- Email address
- Phone number
- Company name

### Processing
The agent sends this data to Claude AI and asks it to:
1. Validate email format
2. Format phone number consistently
3. Suggest a professional job title
4. Rate the overall data quality on a scale of 1-10
5. Provide notes about concerns or improvement suggestions

### Output
Claude returns:
- Validation status (Valid: Yes/No)
- Properly formatted phone number
- Suggested professional title
- Data quality score
- Helpful notes and recommendations

## How to Use

### Basic Usage

Run the agent from the command line:
```bash
python agents/contact_creator.py
```

### Expected Output
```
============================================================
HUBSPOT CONTACT CREATOR AGENT
============================================================

Contact Creator Agent Started
Processing: John Smith

Agent Analysis Complete
============================================================
VALID: Yes
FORMATTED_PHONE: (555) 123-4567
SUGGESTED_TITLE: Sales Manager
DATA_QUALITY: 7/10
NOTES: Email format is valid. Phone number formatted. Consider adding 
       job title and department information for better data quality.
============================================================

Contact would be created in HubSpot with enriched data

Agent completed successfully
```

## Code Structure

### Main Components

1. **Environment Setup**
   - Loads API keys from .env file
   - Initializes Claude client

2. **Mock Data**
   - Sample contact stored in MOCK_CONTACT dictionary
   - Easy to modify for testing different scenarios

3. **create_contact() Function**
   - Main processing function
   - Builds prompt for Claude
   - Calls Claude API
   - Displays results

4. **main() Function**
   - Entry point for the script
   - Orchestrates the execution flow

### Key Variables
```python
MOCK_CONTACT = {
    "name": "John Smith",
    "email": "jsmith@company.com",
    "phone": "5551234567",
    "company": "Acme Corp"
}
```

Modify this dictionary to test different contact data.

## Customization

### Testing Different Contacts

Edit the MOCK_CONTACT dictionary at the top of the file:
```python
MOCK_CONTACT = {
    "name": "Your Name Here",
    "email": "yourname@example.com",
    "phone": "1234567890",
    "company": "Your Company"
}
```

### Changing Claude's Analysis

Modify the prompt in the `create_contact()` function to ask Claude for different types of analysis:
```python
prompt = f"""You are a contact validation agent. Review this contact information:

[Your custom instructions here]

Return your response in this format:
[Your custom format here]
"""
```

### Adjusting Output Verbosity

Change the print statements to show more or less information:
```python
# Minimal output
print(f"Processing: {contact_data['name']}")

# Detailed output
print(f"Processing contact: {contact_data['name']}")
print(f"Email: {contact_data['email']}")
print(f"Phone: {contact_data['phone']}")
```

## Common Use Cases

### 1. Testing Data Quality

Use this agent to check if your contact data is complete before importing to HubSpot.

### 2. Understanding AI Capabilities

See what kinds of insights Claude can provide about contact data.

### 3. Developing Prompts

Experiment with different prompts to get better results from Claude.

### 4. Training

Learn how AI agents work before building more complex systems.

## Technical Details

### API Model

Uses Claude Sonnet 4:
```python
model="claude-sonnet-4-20250514"
```

### Token Limit

Configured for 500 tokens maximum response:
```python
max_tokens=500
```

This is enough for validation responses but can be increased if needed.

### Error Handling

Currently minimal error handling. In production, you would add:
- Try-catch blocks around API calls
- Validation of API responses
- Fallback behavior if Claude is unavailable

## Limitations

1. **No Real HubSpot Integration**
   - Only simulates what would happen
   - Does not actually create contacts

2. **Single Contact Processing**
   - Processes one contact at a time
   - Not optimized for bulk operations

3. **Fixed Mock Data**
   - Uses hardcoded test data
   - Must edit code to test different contacts

4. **Basic Error Handling**
   - Does not handle API failures gracefully
   - No retry logic

## Next Steps

After understanding this agent, you can:

1. Move to `hubspot_contact_real.py` to create actual contacts
2. Use `bulk_contact_creator.py` for production bulk operations
3. Modify this agent to read from a CSV file
4. Add more sophisticated validation rules

## Troubleshooting

### "Module not found" Error

Make sure you are in the virtual environment:
```bash
source venv/bin/activate
```

### "API key not found" Error

Check that your `.env` file exists and contains:
```
ANTHROPIC_API_KEY=your-key-here
```

### Claude Not Responding

Verify:
- Your API key is valid
- You have API credits available
- Your internet connection is working

## Related Documentation

- [Real HubSpot Contact Creator](hubspot_contact_real.md)
- [Bulk Contact Creator](bulk_contact_creator.md)