import json
import random
from datetime import datetime
from flask_mail import Mail, Message
from flask import current_app

def init_mail(app):
    """
    Initialize Flask-Mail configuration for Gmail SMTP
    """
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'deepanshichoudhary03@gmail.com'
    app.config['MAIL_PASSWORD'] = 'allyugertivulksr'
    app.config['MAIL_DEFAULT_SENDER'] = ('Complaint System', 'deepanshichoudhary03@gmail.com')

    app.mail = Mail(app)
    print("✅ Flask-Mail initialized successfully")
    print(f"📧 Email configured for: {app.config['MAIL_USERNAME']}")


def send_complaint_email(complaint_data, authority_email):
    """
    Send complaint email to the concerned authority
    """
    try:
        # Prepare email body
        email_body = f"Complaint Description:\n\n{complaint_data.get('description')}"
        
        # Add AI draft if available
        if complaint_data.get('aiDraft'):
            draft_content = complaint_data['aiDraft'].get('draft', '')
            
            # Clean up the draft content - remove Subject line and AI-Generated Draft header
            lines = draft_content.split('\n')
            cleaned_lines = []
            skip_next = False
            
            for line in lines:
                # Skip "Subject:" line and the line after it
                if line.strip().startswith('Subject:'):
                    skip_next = True
                    continue
                if skip_next:
                    skip_next = False
                    continue
                # Skip empty lines after Subject
                if skip_next and line.strip() == '':
                    continue
                cleaned_lines.append(line)
            
            # Join the cleaned lines
            cleaned_draft = '\n'.join(cleaned_lines).strip()
            
            # Add the cleaned draft to email body
            if cleaned_draft:
                email_body += f"\n\n{cleaned_draft}"
        
        # Prepare email
        msg = Message(
            subject=f"New Complaint: {complaint_data.get('category')}",
            recipients=[authority_email],
            body=email_body
        )

        current_app.mail.send(msg)

        # Save to email logs
        email_log = {
            'id': f"email_{random.randint(1000, 9999)}",
            'complaint_id': complaint_data.get('id'),
            'to': authority_email,
            'subject': msg.subject,
            'body': msg.body,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent',
            'type': 'complaint_notification'
        }
        save_email_log(email_log)
        
        return {
            'success': True,
            'message': 'Complaint email sent successfully',
            'email_id': email_log['id']
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send complaint email: {str(e)}'
        }


def send_confirmation_email(user_email, complaint_data):
    """
    Send confirmation email to the user
    """
    try:
        # Prepare email
        msg = Message(
            subject=f"Complaint Confirmation: {complaint_data.get('id')}",
            recipients=[user_email],
            body=f"Your complaint has been received successfully.\n\n"
                 f"Tracking ID: {complaint_data.get('id')}\n"
                 f"Category: {complaint_data.get('category')}\n"
                 f"Description: {complaint_data.get('description')}\n\n"
                 f"Our team will process your complaint shortly."
        )

        current_app.mail.send(msg)

        # Save to email logs
        email_log = {
            'id': f"email_{random.randint(1000, 9999)}",
            'complaint_id': complaint_data.get('id'),
            'to': user_email,
            'subject': msg.subject,
            'body': msg.body,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent',
            'type': 'confirmation'
        }
        save_email_log(email_log)
        
        return {
            'success': True,
            'message': 'Confirmation email sent successfully',
            'email_id': email_log['id']
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send confirmation email: {str(e)}'
        }


def save_email_log(email_log):
    """
    Save email log to JSON file
    """
    try:
        with open('data/email_logs.json', 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append(email_log)
    
    with open('data/email_logs.json', 'w') as f:
        json.dump(logs, f, indent=2)


def generate_feedback_email_with_gemini(feedback_data):
    """
    Generate feedback email content using Gemini AI
    """
    try:
        import google.generativeai as genai
        import os
        
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create prompt for Gemini
        prompt = f"""
Generate a professional feedback email for the JANAI civic complaint platform with the following user details:

User Name: {feedback_data.get('name')}
User Email: {feedback_data.get('email')}
User Message: {feedback_data.get('message')}

Requirements:
1. Create a professional headline with an emoji
2. Write well-formatted content explaining the feedback
3. Include the user's feedback details in a structured format
4. End with "Best regards" followed by:
   - Name
   - Email
   - Phone (if available)

Make it professional, well-structured, and engaging. The email should be for internal team review of user feedback.
        """
        
        # Generate response from Gemini
        response = model.generate_content(prompt)
        email_content = response.text
        
        return email_content
        
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        # Return error message instead of fallback template
        return f"Error generating AI content: {str(e)}"

def generate_complaint_draft_with_gemini(complaint_data):
    """
    Generate complaint draft content using Gemini AI
    """
    try:
        import google.generativeai as genai
        import os
        
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model with timeout
        model = genai.GenerativeModel('gemini-pro')
        
        # Extract data
        user_info = complaint_data.get('userInfo', {})
        address = complaint_data.get('address', {})
        issue_description = complaint_data.get('issueDescription', '')
        category = complaint_data.get('category', '')
        region = complaint_data.get('region', '')
        
        # Create prompt for Gemini
        prompt = f"""
Generate a professional complaint draft for a civic issue with the following details:

Issue Category: {category}
Issue Description: {issue_description}
Region: {region}

User Information:
- Name: {user_info.get('fullName', '')}
- Contact: {user_info.get('mobile', '')}
- Email: {user_info.get('email', '')}

Address Details:
- House No: {address.get('houseNo', '')}
- Address Line 1: {address.get('addressLine1', '')}
- Address Line 2: {address.get('addressLine2', '')}
- PIN Code: {address.get('pinCode', '')}

Requirements:
1. Create a professional subject line
2. Write a formal complaint letter addressed to the {category} Department
3. Include all the issue details in a structured format
4. Mention the location and address clearly
5. Include user's contact information
6. End with a professional closing
7. Format it as a proper email with subject and body

Make it professional, well-structured, and suitable for official communication with government authorities.
        """
        
        # Generate response from Gemini with timeout
        response = model.generate_content(prompt)
        draft_content = response.text
        
        return draft_content
        
    except Exception as e:
        print(f"Gemini AI Error for complaint draft: {e}")
        
        # Check if it's a network/proxy error
        if "DNS resolution failed" in str(e) or "proxy" in str(e).lower() or "timeout" in str(e).lower():
            print("Network/proxy issue detected. Using fallback template.")
            return generate_fallback_complaint_draft(complaint_data)
        
        # Return error message for other issues
        return f"Error generating complaint draft: {str(e)}"

def generate_fallback_complaint_draft(complaint_data):
    """
    Generate a fallback complaint draft when AI is unavailable
    """
    import random
    
    user_info = complaint_data.get('userInfo', {})
    address = complaint_data.get('address', {})
    issue_description = complaint_data.get('issueDescription', '')
    category = complaint_data.get('category', '')
    region = complaint_data.get('region', '')
    
    # Different subject line variations
    subject_variations = [
        f"Complaint regarding {category} issue in {region}",
        f"Urgent: {category} problem in {region}",
        f"Request for immediate action on {category} issue",
        f"Complaint about {category} services in {region}",
        f"Report of {category} issue requiring attention"
    ]
    
    # Different opening variations
    opening_variations = [
        f"Dear {category} Department,",
        f"To the {category} Department,",
        f"Respected {category} Department,",
        f"Dear Sir/Madam of {category} Department,",
        f"To Whom It May Concern,"
    ]
    
    # Different urgency expressions
    urgency_variations = [
        "requires immediate attention",
        "needs urgent intervention",
        "demands prompt action",
        "calls for immediate resolution",
        "requires your immediate attention"
    ]
    
    # Different impact statements
    impact_variations = [
        "This issue is affecting the daily lives of residents in our area and requires prompt action from your department.",
        "The situation is causing significant inconvenience to the local community and needs immediate resolution.",
        "This problem is impacting the quality of life for residents and requires urgent attention.",
        "The issue is creating difficulties for the neighborhood and needs prompt intervention.",
        "This matter is affecting public welfare and requires immediate action from your department."
    ]
    
    # Different closing statements
    closing_variations = [
        "I kindly request you to investigate this matter and take necessary steps to resolve it at the earliest.",
        "I would appreciate if you could look into this issue and take appropriate action as soon as possible.",
        "Please consider this matter urgent and take the necessary steps to address it promptly.",
        "I hope you will give this issue the attention it deserves and resolve it quickly.",
        "I trust you will investigate this matter thoroughly and implement a solution without delay."
    ]
    
    # Different thank you messages
    thank_you_variations = [
        "Thank you for your attention to this issue.",
        "I appreciate your time and consideration in this matter.",
        "Thank you for taking the time to address this concern.",
        "I look forward to your response and action on this matter.",
        "Thank you for your cooperation in resolving this issue."
    ]
    
    # Different sign-off variations
    sign_off_variations = [
        "Best regards,",
        "Sincerely,",
        "Yours faithfully,",
        "Respectfully yours,",
        "Thank you,"
    ]
    
    # Randomly select variations
    subject = random.choice(subject_variations)
    opening = random.choice(opening_variations)
    urgency = random.choice(urgency_variations)
    impact = random.choice(impact_variations)
    closing = random.choice(closing_variations)
    thank_you = random.choice(thank_you_variations)
    sign_off = random.choice(sign_off_variations)
    
    # Generate different body content based on category
    body_content = ""
    if category.lower() in ['water', 'sanitation', 'sewage']:
        body_content = f"I am writing to bring to your attention a {category.lower()} issue that {urgency} in our area.\n\n"
    elif category.lower() in ['electricity', 'power']:
        body_content = f"I am writing to report a {category.lower()} problem that {urgency} in our locality.\n\n"
    elif category.lower() in ['roads', 'transport']:
        body_content = f"I am writing to bring to your notice a {category.lower()} issue that {urgency} in our area.\n\n"
    elif category.lower() in ['garbage', 'waste']:
        body_content = f"I am writing to report a {category.lower()} management issue that {urgency} in our neighborhood.\n\n"
    else:
        body_content = f"I am writing to bring to your attention a {category.lower()} issue that {urgency} in our area.\n\n"
    
    draft = f"""Subject: {subject}

{opening}

{body_content}Issue Details:
- Category: {category}
- Description: {issue_description}
- Location: {address.get('houseNo', '')}, {address.get('addressLine1', '')}, {address.get('addressLine2', '')}, PIN: {address.get('pinCode', '')}
- Region: {region}

Personal Information:
- Name: {user_info.get('fullName', '')}
- Contact: {user_info.get('mobile', '')}
- Email: {user_info.get('email', '')}

{impact} {closing}

{thank_you}

{sign_off}
{user_info.get('fullName', '')}
{user_info.get('mobile', '')}"""
    
    return draft

def send_feedback_email(feedback_data):
    """
    Send feedback email to JANAI team with AI-generated content
    """
    try:
        # Generate AI-powered email content
        email_body = generate_feedback_email_with_gemini(feedback_data)
        
        # Check if AI generation failed
        if email_body.startswith("Error generating AI content:"):
            return {
                'success': False,
                'message': email_body
            }
        
        # Prepare email
        msg = Message(
            subject="🚀 New User Feedback - JANAI Civic Platform",
            recipients=['deepanshichoudhary03@gmail.com'],  # JANAI email
            body=email_body
        )

        current_app.mail.send(msg)

        # Save to email logs
        email_log = {
            'id': f"email_{random.randint(1000, 9999)}",
            'complaint_id': "FEEDBACK",
            'to': 'deepanshichoudhary03@gmail.com',
            'subject': msg.subject,
            'body': msg.body,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent',
            'type': 'feedback'
        }
        save_email_log(email_log)

        return {
            'success': True,
            'message': 'Feedback email sent successfully',
            'email_id': email_log['id']
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send feedback email: {str(e)}'
        }
