from flask import Blueprint, request, jsonify
import json
import random
import string
from datetime import datetime
from .email_service import send_complaint_email, send_confirmation_email, generate_complaint_draft_with_gemini

complaint_bp = Blueprint('complaint', __name__)

def load_complaints():
    try:
        with open('data/complaints.json', 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_complaints(complaints):
    with open('data/complaints.json', 'w') as f:
        json.dump(complaints, f, indent=2)

def generate_tracking_id():
    return f"JANAI-{''.join(random.choices(string.digits, k=5))}"

@complaint_bp.route('/file', methods=['POST'])
def file_complaint():
    data = request.get_json()
    
    # Validation
    required_fields = ['userId', 'address', 'issueDescription', 'category', 'region']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    complaints = load_complaints()
    
    # Generate tracking ID
    tracking_id = generate_tracking_id()
    
    # Check if there's an edited authority email from the draft
    edited_authority_email = data.get('editedAuthorityEmail')
    print(f"DEBUG: Received editedAuthorityEmail: {edited_authority_email}")
    print(f"DEBUG: Category: {data.get('category')}")
    print(f"DEBUG: Auto-generated email would be: {data.get('category', '').lower().replace(' ', '.')}@examplecity.gov.in")
    
    # Create new complaint
    new_complaint = {
        'id': tracking_id,
        'userId': data['userId'],
        'category': data['category'],
        'description': data['issueDescription'],
        'address': data['address'],
        'status': 'Submitted',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'authority': {
            'name': f"Municipal Corporation - {data['category']} Dept.",
            'email': edited_authority_email if edited_authority_email else f"{data['category'].lower().replace(' ', '.')}@examplecity.gov.in",
            'phone': f"+91-22-{random.randint(10000000, 99999999)}"
        }
    }
    
    # Add AI draft if available
    if data.get('aiDraft'):
        new_complaint['aiDraft'] = data['aiDraft']
    
    complaints.append(new_complaint)
    save_complaints(complaints)
    
    # Send emails
    user_email = data.get('userInfo', {}).get('email', 'deepanshichoudhary03@gmail.com')
    email_status = {
        'authority': send_complaint_email(new_complaint, new_complaint['authority']['email']),
        'user': send_confirmation_email(user_email, new_complaint)
    }
    
    return jsonify({
        'message': 'Complaint Sent Successfully!',
        'trackingId': tracking_id,
        'complaint': new_complaint,
        'emailStatus': email_status
    }), 201

@complaint_bp.route('/status', methods=['GET'])
def get_complaint_status():
    user_id = request.args.get('userId')
    
    if not user_id:
        return jsonify({'error': 'userId is required'}), 400
    
    complaints = load_complaints()
    user_complaints = [c for c in complaints if c['userId'] == user_id]
    
    return jsonify({
        'complaints': user_complaints
    }), 200

@complaint_bp.route('/resolve', methods=['POST'])
def resolve_complaint():
    data = request.get_json()
    complaint_id = data.get('complaintId')
    
    if not complaint_id:
        return jsonify({'error': 'complaintId is required'}), 400
    
    complaints = load_complaints()
    
    # Find and update the complaint
    complaint_found = False
    for complaint in complaints:
        if complaint['id'] == complaint_id:
            complaint['status'] = 'Issue Resolved'
            complaint_found = True
            break
    
    if not complaint_found:
        return jsonify({'error': 'Complaint not found'}), 404
    
    # Save updated complaints
    save_complaints(complaints)
    
    return jsonify({
        'message': 'Complaint resolved successfully',
        'complaint_id': complaint_id
    }), 200



@complaint_bp.route('/manual-resolve', methods=['POST'])
def manually_resolve_complaint():
    """Manually resolve a complaint (for testing)"""
    data = request.get_json()
    complaint_id = data.get('complaintId')
    
    if not complaint_id:
        return jsonify({'error': 'complaintId is required'}), 400
    
    try:
        from .email_service import update_complaint_status, send_resolution_notification
        
        success = update_complaint_status(complaint_id, "Issue Resolved")
        if success:
            send_resolution_notification(complaint_id)
            return jsonify({'success': True, 'message': 'Complaint resolved successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to resolve complaint'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@complaint_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        from .email_service import send_feedback_email
        
        # Send feedback email to JANAI email
        email_status = send_feedback_email(data)
        
        return jsonify({
            'message': 'Feedback submitted successfully!',
            'emailStatus': email_status
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to submit feedback: {str(e)}'}), 500

@complaint_bp.route('/generate-draft', methods=['POST'])
def generate_complaint_draft():
    """Generate complaint draft using Gemini AI"""
    data = request.get_json()
    
    # Validation
    required_fields = ['userInfo', 'address', 'issueDescription', 'category', 'region']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        # Generate draft using Gemini AI
        draft_content = generate_complaint_draft_with_gemini(data)
        
        # Create authority information
        authority = {
            'name': f"{data['category']} Department - Municipal Corporation",
            'email': f"{data['category'].lower().replace(' ', '.')}@examplecity.gov.in",
            'phone': f"+91-22-{random.randint(10000000, 99999999)}"
        }
        
        return jsonify({
            'draft': draft_content,
            'authority': authority
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate draft: {str(e)}'}), 500 