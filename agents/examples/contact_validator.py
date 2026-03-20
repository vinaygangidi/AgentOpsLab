"""
Contact Creator Agent
Simple agent that validates and enriches contact data using Claude AI
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Sample contact data for testing
MOCK_CONTACT = {
    "name": "John Smith",
    "email": "jsmith@company.com",
    "phone": "5551234567",
    "company": "Acme Corp"
}


def create_contact(contact_data):
    """
    Validates and enriches contact data using Claude AI.
    
    Args:
        contact_data (dict): Contact information including name, email, phone, company
        
    Returns:
        str: Analysis result from Claude
    """
    
    print("Contact Creator Agent Started")
    print(f"Processing: {contact_data['name']}")
    
    # Build prompt for Claude
    prompt = f"""You are a contact validation agent. Review this contact information:

Name: {contact_data['name']}
Email: {contact_data['email']}
Phone: {contact_data['phone']}
Company: {contact_data['company']}

Tasks:
1. Validate the email format
2. Format the phone number to (555) 123-4567
3. Suggest a professional title based on the name and company
4. Rate the data quality (1-10)

Return your response in this format:
VALID: Yes/No
FORMATTED_PHONE: (555) 123-4567
SUGGESTED_TITLE: [title]
DATA_QUALITY: [score]/10
NOTES: [any concerns or suggestions]
"""
    
    # Call Claude API
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract response
    response = message.content[0].text
    
    print("\nAgent Analysis Complete")
    print("=" * 60)
    print(response)
    print("=" * 60)
    
    print("\nContact would be created in HubSpot with enriched data")
    
    return response


def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("HUBSPOT CONTACT CREATOR AGENT")
    print("=" * 60 + "\n")
    
    result = create_contact(MOCK_CONTACT)
    
    print("\nAgent completed successfully")


if __name__ == "__main__":
    main()