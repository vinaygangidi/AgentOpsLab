"""
Simple Contact Creator Agent
Uses Claude AI to validate and enrich contact data
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize Claude
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Mock contact data (pretend this came from a form)
mock_contact = {
    "name": "John Smith",
    "email": "jsmith@company.com",
    "phone": "5551234567",
    "company": "Acme Corp"
}

def create_contact(contact_data):
    """
    Agent that validates and enriches contact data using Claude
    """
    
    print("🤖 Contact Creator Agent Started...")
    print(f"📥 Processing: {contact_data['name']}")
    
    # Ask Claude to validate and enrich the contact
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
    
    # Call Claude
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Get Claude's response
    response = message.content[0].text
    
    print("\n✅ Agent Analysis Complete!")
    print("=" * 60)
    print(response)
    print("=" * 60)
    
    # In a real system, we would create the contact in HubSpot here
    # For now, we just show the validated data
    print("\n💾 Contact would be created in HubSpot with enriched data")
    
    return response

# Run the agent
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 HUBSPOT CONTACT CREATOR AGENT")
    print("=" * 60 + "\n")
    
    result = create_contact(mock_contact)
    
    print("\n✨ Agent completed successfully!")