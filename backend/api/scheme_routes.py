from flask import Blueprint, request, jsonify
import json

scheme_bp = Blueprint('schemes', __name__)

def load_schemes():
    with open('data/schemes.json', 'r') as f:
        return json.load(f)

@scheme_bp.route('/find', methods=['POST'])
def find_schemes():
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'age', 'gender', 'occupation']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    schemes_data = load_schemes()
    schemes = schemes_data.get('schemes', [])
    matching_schemes = []
    
    # Show all schemes without filtering by type
    for scheme in schemes:
        # Intelligent matching based on user profile
        if data['occupation'] == 'Student':
            # Students get education and skill development schemes
            if any(keyword in scheme['category'].lower() for keyword in ['education', 'scholarship', 'skill']):
                matching_schemes.append(scheme)
        elif data['occupation'] == 'Farmer':
            # Farmers get agricultural and rural schemes
            if any(keyword in scheme['category'].lower() for keyword in ['agricultural', 'crop', 'rural', 'kisan']):
                matching_schemes.append(scheme)
        elif data['occupation'] == 'Homemaker':
            # Homemakers get women empowerment and family schemes
            if any(keyword in scheme['category'].lower() for keyword in ['women', 'maternity', 'family', 'social security']):
                matching_schemes.append(scheme)
        elif data['occupation'] == 'Employee' or data['occupation'] == 'Self Employed':
            # Working people get skill development and entrepreneurship schemes
            if any(keyword in scheme['category'].lower() for keyword in ['skill', 'entrepreneurship', 'pension']):
                matching_schemes.append(scheme)
        elif data['occupation'] == 'Business Owner':
            # Business owners get entrepreneurship and startup schemes
            if any(keyword in scheme['category'].lower() for keyword in ['entrepreneurship', 'startup', 'skill']):
                matching_schemes.append(scheme)
        elif data['occupation'] == 'Retired':
            # Retired people get pension and health schemes
            if any(keyword in scheme['category'].lower() for keyword in ['pension', 'health', 'social security']):
                matching_schemes.append(scheme)
        else:
            # For other occupations, show relevant schemes based on age and gender
            if data['age'] >= 60:
                # Elderly people get pension and health schemes
                if any(keyword in scheme['category'].lower() for keyword in ['pension', 'health', 'social security']):
                    matching_schemes.append(scheme)
            elif data['gender'] == 'Female':
                # Women get women empowerment schemes
                if any(keyword in scheme['category'].lower() for keyword in ['women', 'maternity', 'girl child']):
                    matching_schemes.append(scheme)
            else:
                # Others get general schemes (limit to 5-10 most relevant)
                if len(matching_schemes) < 8:
                    matching_schemes.append(scheme)
    
    return jsonify({
        'schemes': matching_schemes,
        'total': len(matching_schemes)
    }), 200 