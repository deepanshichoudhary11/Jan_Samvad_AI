from flask import Blueprint, request, jsonify
import json
import os

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Voice Processing'})

@voice_bp.route('/get-language-support', methods=['GET'])
def get_language_support():
    """Get supported languages for voice recognition"""
    supported_languages = [
        {'language_code': 'hi-IN', 'native_name': 'हिंदी', 'language': 'Hindi'},
        {'language_code': 'mr-IN', 'native_name': 'मराठी', 'language': 'Marathi'},
        {'language_code': 'ta-IN', 'native_name': 'தமிழ்', 'language': 'Tamil'},
        {'language_code': 'te-IN', 'native_name': 'తెలుగు', 'language': 'Telugu'},
        {'language_code': 'gu-IN', 'native_name': 'ગુજરાતી', 'language': 'Gujarati'},
        {'language_code': 'bn-IN', 'native_name': 'বাংলা', 'language': 'Bengali'},
        {'language_code': 'ml-IN', 'native_name': 'മലയാളം', 'language': 'Malayalam'},
        {'language_code': 'ur-IN', 'native_name': 'اردو', 'language': 'Urdu'},
        {'language_code': 'pa-IN', 'native_name': 'ਪੰਜਾਬੀ', 'language': 'Punjabi'},
        {'language_code': 'kn-IN', 'native_name': 'ಕನ್ನಡ', 'language': 'Kannada'}
    ]
    
    return jsonify({
        'success': True,
        'supported_languages': supported_languages
    })

@voice_bp.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    """Process voice input and return relevant national helpline numbers using AI analysis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        state = data.get('state', '')
        language = data.get('language', 'hi-IN')
        
        # Import Gemini AI for analysis
        import google.generativeai as genai
        import os
        
        # Configure Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        
        # Create AI prompt for analysis
        prompt = f"""
        Analyze this voice input and determine the most relevant national helpline numbers for India.
        
        Voice Input: "{text}"
        Language: {language}
        
        Available National Helpline Numbers:
        - Emergency: 112
        - Ambulance: 108
        - Police: 100
        - Fire: 101
        - Women Helpline: 1091
        - Child Helpline: 1098
        - Senior Citizen: 14567
        - Mental Health: 1800-599-0019
        - Cyber Crime: 1930
        - Consumer Helpline: 1800-11-4000
        - Farmer Helpline: 1800-180-1551
        - Railway Helpline: 139
        - Health Helpline: 104
        - COVID Helpline: 1075
        
        Please analyze the situation and return ONLY the relevant helpline numbers in JSON format:
        {{
            "relevant_helplines": {{
                "helpline_name": "number",
                ...
            }},
            "analysis": {{
                "problem_type": "description",
                "urgency_level": "high/medium/low",
                "recommendations": ["list of recommendations"]
            }}
        }}
        
        Only include helpline numbers that are directly relevant to the described situation.
        """
        
        # Get AI analysis
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Parse AI response (fallback to basic analysis if parsing fails)
        try:
            import json
            # Extract JSON from AI response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                ai_data = json.loads(ai_response[start_idx:end_idx])
                relevant_helplines = ai_data.get('relevant_helplines', {})
                analysis = ai_data.get('analysis', {})
            else:
                raise ValueError("No JSON found in response")
        except Exception as parse_error:
            print(f"Error parsing AI response: {parse_error}")
            # Fallback to basic emergency numbers
            relevant_helplines = {
                'emergency': '112',
                'ambulance': '108',
                'police': '100'
            }
            analysis = {
                'problem_type': 'Emergency',
                'urgency_level': 'high',
                'recommendations': ['Contact emergency services immediately']
            }
        
        return jsonify({
            'success': True,
            'text': text,
            'language': language,
            'state_helplines': relevant_helplines,
            'ai_analysis': {
                'problem_type': analysis.get('problem_type', 'Emergency'),
                'urgency_level': analysis.get('urgency_level', 'high'),
                'recommendations': analysis.get('recommendations', []),
                'confidence': 0.9
            },
            'multilingual_response': f'AI analysis complete - {analysis.get("problem_type", "Emergency")} detected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@voice_bp.route('/analyze-with-gemini', methods=['POST'])
def analyze_with_gemini():
    """Analyze voice input with Gemini AI and return relevant national helpline numbers"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        state = data.get('state', '')
        language = data.get('language', 'hi-IN')
        
        # Import Gemini AI for analysis
        import google.generativeai as genai
        import os
        
        # Configure Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')
        
        # Create AI prompt for analysis
        prompt = f"""
        Analyze this voice input and determine the most relevant national helpline numbers for India.
        
        Voice Input: "{text}"
        Language: {language}
        
        Available National Helpline Numbers:
        - Emergency: 112
        - Ambulance: 108
        - Police: 100
        - Fire: 101
        - Women Helpline: 1091
        - Child Helpline: 1098
        - Senior Citizen: 14567
        - Mental Health: 1800-599-0019
        - Cyber Crime: 1930
        - Consumer Helpline: 1800-11-4000
        - Farmer Helpline: 1800-180-1551
        - Railway Helpline: 139
        - Health Helpline: 104
        - COVID Helpline: 1075
        
        Please analyze the situation and return ONLY the relevant helpline numbers in JSON format:
        {{
            "relevant_helplines": {{
                "helpline_name": "number",
                ...
            }},
            "analysis": {{
                "problem_type": "description",
                "urgency_level": "high/medium/low",
                "recommendations": ["list of recommendations"]
            }}
        }}
        
        Only include helpline numbers that are directly relevant to the described situation.
        """
        
        # Get AI analysis
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Parse AI response (fallback to basic analysis if parsing fails)
        try:
            import json
            # Extract JSON from AI response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                ai_data = json.loads(ai_response[start_idx:end_idx])
                relevant_helplines = ai_data.get('relevant_helplines', {})
                analysis = ai_data.get('analysis', {})
            else:
                raise ValueError("No JSON found in response")
        except Exception as parse_error:
            print(f"Error parsing AI response: {parse_error}")
            # Fallback to basic emergency numbers
            relevant_helplines = {
                'emergency': '112',
                'ambulance': '108',
                'police': '100'
            }
            analysis = {
                'problem_type': 'Emergency',
                'urgency_level': 'high',
                'recommendations': ['Contact emergency services immediately']
            }
        
        return jsonify({
            'success': True,
            'text': text,
            'language': language,
            'state_helplines': relevant_helplines,
            'ai_analysis': {
                'problem_type': analysis.get('problem_type', 'Emergency'),
                'urgency_level': analysis.get('urgency_level', 'high'),
                'recommendations': analysis.get('recommendations', []),
                'confidence': 0.9
            },
            'multilingual_response': f'AI analysis complete - {analysis.get("problem_type", "Emergency")} detected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
