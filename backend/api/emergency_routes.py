from flask import Blueprint, request, jsonify
import json
import os
import google.generativeai as genai

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/process-emergency', methods=['POST'])
def process_emergency():
    """
    Comprehensive emergency voice processing with multi-language support.
    Detects language, state, emergency type, and returns relevant helpline numbers.
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        input_language = data.get('inputLanguage', 'hi-IN')
        
        if not text:
            return jsonify({
                'success': False,
                'message': 'No text provided for processing'
            }), 400
        
        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            # Fallback to basic processing without AI
            return process_without_ai(text, input_language)
        
        # Temporarily use smart fallback instead of AI due to network issues
        # This provides instant, reliable responses with intelligent keyword analysis
        return process_without_ai(text, input_language)
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Gemini configuration error: {str(e)}")
            return process_without_ai(text, input_language)
        
        # Comprehensive analysis prompt
        prompt = f"""
        You are an Indian emergency helpline assistant. Analyze this emergency text: "{text}"

        Use your knowledge of Indian emergency services to provide the most relevant helpline numbers based on the emergency type.

        Return JSON format:
        {{
            "detectedLanguage": "language name",
            "detectedState": "Indian state or All India", 
            "emergencyType": "police/medical/fire/women/child/accident/general",
            "urgencyLevel": "high/medium/low",
            "helplineNumbers": [
                {{
                    "number": "helpline number",
                    "name": "service name", 
                    "type": "category",
                    "description": "what this helpline does",
                    "availability": "24/7",
                    "state": "All India or specific state"
                }}
            ],
            "translatedResponse": "helpful response in the input language"
        }}

        Critical Rules:
        1. CHILD emergencies (child help, kid emergency, child abuse, missing child): 
           - MUST include 1098 (Child Helpline) as FIRST priority
        2. WATER emergencies (pani, water supply, sewerage, drainage):
           - Include 1916 (Water Supply Helpline) as FIRST priority
        3. ELECTRICITY emergencies (bijli, power, outage, current):
           - Include 1912 (Power Grid Emergency) as FIRST priority
        4. TRANSPORT emergencies (train, bus, travel, road):
           - Include 139 (Railway), 1033 (Tourist Helpline) as priorities
        5. Medical: 108/102 (Ambulance), 112 (All emergencies)
        6. Police: 100, 112 (All emergencies) 
        7. Fire: 101, 112 (All emergencies)
        8. Women: 1091 (Women Helpline), 181 (Women Distress), 112 (All emergencies)
           - Keywords: women, mulgi, girl, lady, harassment, domestic violence
        9. ALWAYS include 112 (All emergencies) in every response
        10. Use your vast knowledge of Indian utility and emergency services
        """
        
        # Get AI analysis with timeout
        try:
            import threading
            import time
            
            # Use threading for timeout on Windows
            result = {'response': None, 'error': None}
            
            def ai_request():
                try:
                    result['response'] = model.generate_content(prompt)
                except Exception as e:
                    result['error'] = str(e)
            
            # Start AI request in separate thread
            thread = threading.Thread(target=ai_request)
            thread.daemon = True
            thread.start()
            
            # Wait for 60 seconds (increased timeout)
            thread.join(timeout=60)
            
            if thread.is_alive():
                # Thread is still running, timeout occurred
                print("Gemini AI request timed out after 60 seconds")
                return process_without_ai(text, input_language)
            
            if result['error']:
                print(f"Gemini AI error: {result['error']}")
                return process_without_ai(text, input_language)
            
            if not result['response']:
                print("No response from Gemini AI")
                return process_without_ai(text, input_language)
                
            ai_response = result['response'].text
            
        except Exception as e:
            print(f"Gemini AI timeout or error: {str(e)}")
            return process_without_ai(text, input_language)
        
        # Parse AI response
        try:
            import json
            import re
            
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                ai_data = json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in AI response")
            
            # Validate and ensure required fields
            detected_language = ai_data.get('detectedLanguage', 'Hindi')
            detected_state = ai_data.get('detectedState', 'All India')
            emergency_type = ai_data.get('emergencyType', 'general')
            helpline_numbers = ai_data.get('helplineNumbers', [])
            
            # Comprehensive national emergency numbers
            basic_helplines = [
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "100",
                    "name": "Police",
                    "type": "police",
                    "description": "Police assistance and law enforcement",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "108",
                    "name": "Ambulance Service",
                    "type": "medical",
                    "description": "Medical emergency and ambulance service",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "102",
                    "name": "Ambulance (Free Service)",
                    "type": "medical",
                    "description": "Free ambulance service for pregnant women and children",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "101",
                    "name": "Fire Brigade",
                    "type": "fire",
                    "description": "Fire emergency and rescue services",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1091",
                    "name": "Women Helpline",
                    "type": "women",
                    "description": "Women in distress and domestic violence",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1098",
                    "name": "Child Helpline",
                    "type": "child",
                    "description": "Child protection and assistance",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1930",
                    "name": "Cyber Crime Helpline",
                    "type": "police",
                    "description": "Cyber crime and online fraud reporting",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "14567",
                    "name": "Senior Citizen Helpline",
                    "type": "general",
                    "description": "Elder helpline for senior citizens",
                    "availability": "24/7",
                    "state": "All India"
                }
            ]
            
            # Only add state-specific numbers if a specific state was detected (not "All India")
            if detected_state != 'All India':
                state_specific_helplines = get_state_specific_helplines(detected_state, emergency_type)
                # Combine and deduplicate helplines
                all_helplines = basic_helplines + helpline_numbers + state_specific_helplines
            else:
                # Only show national helplines
                all_helplines = basic_helplines + helpline_numbers
            seen_numbers = set()
            unique_helplines = []
            
            for helpline in all_helplines:
                if helpline['number'] not in seen_numbers:
                    seen_numbers.add(helpline['number'])
                    unique_helplines.append(helpline)
            
            # Sort by priority (emergency type relevance)
            priority_order = ['general', emergency_type.lower(), 'medical', 'police', 'fire']
            unique_helplines.sort(key=lambda x: priority_order.index(x['type']) if x['type'] in priority_order else 999)
            
            return jsonify({
                'success': True,
                'detectedLanguage': detected_language,
                'detectedState': detected_state,
                'emergencyType': emergency_type,
                'urgencyLevel': ai_data.get('urgencyLevel', 'high'),
                'confidence': ai_data.get('confidence', 0.8),
                'helplineNumbers': unique_helplines[:8],  # Limit to top 8 most relevant
                'translatedResponse': ai_data.get('translatedResponse', 'Emergency detected. Help is on the way.'),
                'originalLanguageInstructions': ai_data.get('originalLanguageInstructions', 'Please stay calm and wait for assistance.')
            })
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback response if AI parsing fails
            return jsonify({
                'success': True,
                'detectedLanguage': 'Hindi',
                'detectedState': 'All India',
                'emergencyType': 'general',
                'urgencyLevel': 'high',
                'confidence': 0.6,
                'helplineNumbers': [
                    {
                        "number": "112",
                        "name": "Emergency Response Support System",
                        "type": "general",
                        "description": "All types of emergencies",
                        "availability": "24/7",
                        "state": "All India"
                    },
                    {
                        "number": "100",
                        "name": "Police",
                        "type": "police",
                        "description": "Police assistance",
                        "availability": "24/7",
                        "state": "All India"
                    },
                    {
                        "number": "108",
                        "name": "Ambulance",
                        "type": "medical",
                        "description": "Medical emergency",
                        "availability": "24/7",
                        "state": "All India"
                    }
                ],
                'translatedResponse': 'आपातकाल का पता चला है। सहायता आ रही है।',
                'originalLanguageInstructions': 'कृपया शांत रहें और सहायता का इंतजार करें।'
            })
            
    except Exception as e:
        print(f"Emergency processing error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to process emergency request. Please try again.'
        }), 500

def get_state_specific_helplines(state, emergency_type):
    """Get state-specific helpline numbers based on detected state and emergency type"""
    
    state_helplines = {
        'Uttar Pradesh': [
            {"number": "1076", "name": "UP CM Helpline", "type": "general", "description": "Chief Minister Helpline", "availability": "24/7", "state": "Uttar Pradesh"},
            {"number": "1090", "name": "UP Women Helpline", "type": "women", "description": "Women safety and assistance", "availability": "24/7", "state": "Uttar Pradesh"}
        ],
        'Maharashtra': [
            {"number": "1916", "name": "Maharashtra Sarkar Call Center", "type": "general", "description": "State government helpline", "availability": "24/7", "state": "Maharashtra"},
            {"number": "103", "name": "Maharashtra Emergency Health", "type": "medical", "description": "Health emergency services", "availability": "24/7", "state": "Maharashtra"}
        ],
        'Delhi': [
            {"number": "1031", "name": "Delhi Police Control Room", "type": "police", "description": "Delhi Police assistance", "availability": "24/7", "state": "Delhi"},
            {"number": "1077", "name": "Delhi Fire Service", "type": "fire", "description": "Fire emergency services", "availability": "24/7", "state": "Delhi"}
        ],
        'Karnataka': [
            {"number": "1090", "name": "Karnataka Women Helpline", "type": "women", "description": "Women safety helpline", "availability": "24/7", "state": "Karnataka"},
            {"number": "104", "name": "Karnataka Health Helpline", "type": "medical", "description": "Health services helpline", "availability": "24/7", "state": "Karnataka"}
        ],
        'Tamil Nadu': [
            {"number": "1077", "name": "Tamil Nadu Fire Service", "type": "fire", "description": "Fire and rescue services", "availability": "24/7", "state": "Tamil Nadu"},
            {"number": "104", "name": "Tamil Nadu Health Helpline", "type": "medical", "description": "Health emergency services", "availability": "24/7", "state": "Tamil Nadu"}
        ],
        'Gujarat': [
            {"number": "181", "name": "Gujarat Women Helpline", "type": "women", "description": "Women safety and support", "availability": "24/7", "state": "Gujarat"},
            {"number": "104", "name": "Gujarat Health Helpline", "type": "medical", "description": "Medical assistance", "availability": "24/7", "state": "Gujarat"}
        ],
        'West Bengal': [
            {"number": "1098", "name": "West Bengal Child Helpline", "type": "child", "description": "Child safety and protection", "availability": "24/7", "state": "West Bengal"},
            {"number": "1515", "name": "West Bengal Disaster Management", "type": "disaster", "description": "Disaster response", "availability": "24/7", "state": "West Bengal"}
        ],
        'Andhra Pradesh': [
            {"number": "1100", "name": "AP Emergency Services", "type": "general", "description": "State emergency services", "availability": "24/7", "state": "Andhra Pradesh"},
            {"number": "104", "name": "AP Health Services", "type": "medical", "description": "Health emergency", "availability": "24/7", "state": "Andhra Pradesh"}
        ],
        'Telangana': [
            {"number": "1100", "name": "Telangana Emergency", "type": "general", "description": "State emergency services", "availability": "24/7", "state": "Telangana"},
            
            # Electricity
            {"number": "1912", "name": "TSSPDCL/TPGPDCL", "type": "electricity", "description": "Electricity complaints and outages", "availability": "24/7", "state": "Telangana"},
            
            # Water Supply
            {"number": "155313", "name": "HMWSSB Water Supply", "type": "water", "description": "Hyderabad water supply and sewerage", "availability": "24/7", "state": "Telangana"},
            {"number": "040-23300114", "name": "HMWSSB Support", "type": "water", "description": "Water supply additional support", "availability": "24/7", "state": "Telangana"},
            {"number": "9281097233", "name": "Ground Water Department", "type": "water", "description": "Groundwater assistance and issues", "availability": "Office Hours", "state": "Telangana"},
            
            # Child Help
            {"number": "1098", "name": "Childline Telangana", "type": "child", "description": "Child protection and assistance", "availability": "24/7", "state": "Telangana"},
            
            # Women Helpline
            {"number": "181", "name": "Women Helpline", "type": "women", "description": "Domestic abuse and women safety", "availability": "24/7", "state": "Telangana"},
            {"number": "9059693448", "name": "Women's Protection Cell", "type": "women", "description": "Women protection and safety", "availability": "24/7", "state": "Telangana"},
            {"number": "040-27852355", "name": "Bharosa Hyderabad", "type": "women", "description": "Women and children support center", "availability": "Office Hours", "state": "Telangana"},
            {"number": "155209", "name": "Anganwadi Helpline", "type": "women", "description": "Women and child welfare services", "availability": "24/7", "state": "Telangana"},
            {"number": "14567", "name": "Elderly Helpline", "type": "general", "description": "Senior citizen assistance", "availability": "24/7", "state": "Telangana"},
            {"number": "1800-599-12345", "name": "Pregnant Women Helpline", "type": "women", "description": "Pregnancy and maternity support", "availability": "24/7", "state": "Telangana"},
            
            # Health
            {"number": "14416", "name": "Tele-Mental Health", "type": "medical", "description": "Mental health support and counseling", "availability": "24/7", "state": "Telangana"},
            {"number": "104", "name": "Medical Advice EMRI", "type": "medical", "description": "State health advice service", "availability": "24/7", "state": "Telangana"},
            
            # Transport
            {"number": "040-23370081", "name": "Transport Department", "type": "transport", "description": "Transport grievances and citizen support", "availability": "10 AM-6 PM (Working Days)", "state": "Telangana"},
            {"number": "1800-425-1110", "name": "T App Folio Support", "type": "transport", "description": "Transport app and services support", "availability": "24/7", "state": "Telangana"}
        ],
        'Kerala': [
            {"number": "1077", "name": "Kerala Fire Service", "type": "fire", "description": "Fire and rescue", "availability": "24/7", "state": "Kerala"},
            {"number": "104", "name": "Kerala Health Helpline", "type": "medical", "description": "Medical emergency", "availability": "24/7", "state": "Kerala"}
        ]
    }
    
    return state_helplines.get(state, [])

def process_without_ai(text, input_language):
    """
    Advanced intelligent processing when AI is unavailable.
    Uses comprehensive keyword analysis and smart reasoning like AI.
    """
    try:
        # Simple language detection based on language code
        language_map = {
            'hi-IN': 'Hindi',
            'ta-IN': 'Tamil', 
            'te-IN': 'Telugu',
            'bn-IN': 'Bengali',
            'mr-IN': 'Marathi',
            'gu-IN': 'Gujarati',
            'kn-IN': 'Kannada',
            'ml-IN': 'Malayalam',
            'pa-IN': 'Punjabi',
            'ur-IN': 'Urdu',
            'en-IN': 'English',
            'or-IN': 'Odia'
        }
        
        detected_language = language_map.get(input_language, 'Hindi')
        
        # State detection only if explicitly mentioned in text
        detected_state = 'All India'  # Default to national helplines
        text_lower = text.lower()  # Define text_lower first
        
        # Check if user explicitly mentioned a state
        state_keywords = {
            'Telangana': ['telangana', 'hyderabad', 'tsspdcl', 'tpgpdcl', 'hmwssb', 'secunderabad'],
            'Maharashtra': ['maharashtra', 'mumbai', 'pune', 'nagpur', 'msedcl'],
            'Tamil Nadu': ['tamil nadu', 'chennai', 'madurai', 'coimbatore'],
            'Karnataka': ['karnataka', 'bangalore', 'bengaluru', 'mysore'],
            'Delhi': ['delhi', 'new delhi', 'ncr'],
            'Uttar Pradesh': ['uttar pradesh', 'lucknow', 'kanpur', 'agra', 'uppcl'],
            'Gujarat': ['gujarat', 'ahmedabad', 'surat', 'vadodara'],
            'West Bengal': ['west bengal', 'kolkata', 'calcutta'],
            'Andhra Pradesh': ['andhra pradesh', 'vijayawada', 'visakhapatnam'],
            'Kerala': ['kerala', 'thiruvananthapuram', 'kochi', 'kozhikode'],
            'Punjab': ['punjab', 'chandigarh', 'ludhiana', 'pspcl']
        }
        
        for state, keywords in state_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_state = state
                break
        
        # Simple emergency type detection using keywords
        emergency_type = 'general'
        
        # Comprehensive multilingual keyword detection
        police_keywords = [
            # English
            'police', 'theft', 'crime', 'robbery', 'assault',
            # Hindi
            'पुलिस', 'चोरी', 'अपराध', 'लूट', 'हमला',
            # Tamil
            'காவல்துறை', 'திருட்டு', 'குற்றம்',
            # Telugu
            'పోలీసు', 'దొంగతనం', 'నేరం',
            # Marathi
            'पोलीस', 'चोरी', 'गुन्हा',
            # Bengali
            'পুলিশ', 'চুরি', 'অপরাধ',
            # Gujarati
            'પોલીસ', 'ચોરી', 'ગુનો',
            # Kannada
            'ಪೊಲೀಸ್', 'ಕಳ್ಳತನ', 'ಅಪರಾಧ',
            # Malayalam
            'പോലീസ്', 'മോഷണം', 'കുറ്റം',
            # Punjabi
            'ਪੁਲਿਸ', 'ਚੋਰੀ', 'ਅਪਰਾਧ'
        ]
        
        medical_keywords = [
            # English
            'ambulance', 'medical', 'hospital', 'doctor', 'health', 'emergency', 'injury',
            # Hindi
            'एम्बुलेंस', 'अस्पताल', 'डॉक्टर', 'स्वास्थ्य', 'चिकित्सा', 'घायल',
            # Tamil
            'ஆம்புலன்ஸ்', 'மருத்துவமனை', 'மருத்துவர்', 'உடல்நலம்',
            # Telugu
            'అంబులెన్స్', 'ఆసుపత్రి', 'వైద్యుడు', 'ఆరోగ్యం',
            # Marathi
            'रुग्णालय', 'डॉक्टर', 'आरोग्य',
            # Bengali
            'অ্যাম্বুলেন্স', 'হাসপাতাল', 'ডাক্তার', 'স্বাস্থ্য',
            # Gujarati
            'એમ્બ્યુલન્સ', 'હોસ્પિટલ', 'ડૉક્ટર', 'આરોગ્য',
            # Kannada
            'ಆಂಬ್ಯುಲೆನ್ಸ್', 'ಆಸ್ಪತ್ರೆ', 'ವೈದ್ಯ', 'ಆರೋಗ್ಯ',
            # Malayalam
            'ആംബുലൻസ്', 'ആശുപത്രി', 'ഡോക്ടർ', 'ആരോഗ്യം',
            # Punjabi
            'ਐਂਬੂਲੈਂਸ', 'ਹਸਪਤਾਲ', 'ਡਾਕਟਰ', 'ਸਿਹਤ'
        ]
        
        fire_keywords = [
            # English
            'fire', 'burning', 'smoke', 'flame',
            # Hindi
            'आग', 'जल रहा', 'धुआं', 'लपटें',
            # Tamil
            'தீ', 'எரியும்', 'புகை',
            # Telugu
            'అగ్ని', 'మంటలు', 'పొగ',
            # Marathi
            'आग', 'जळत', 'धूर',
            # Bengali
            'আগুন', 'জ্বলছে', 'ধোঁয়া',
            # Gujarati
            'આગ', 'બળતું', 'ધુમાડો',
            # Kannada
            'ಬೆಂಕಿ', 'ಸುಡುತ್ತಿದೆ', 'ಹೊಗೆ',
            # Malayalam
            'തീ', 'കത്തുന്നു', 'പുക',
            # Punjabi
            'ਅੱਗ', 'ਸੜਦਾ', 'ਧੂੰਆਂ'
        ]
        
        women_keywords = [
            # English
            'women', 'lady', 'female', 'harassment', 'domestic violence', 'domestic', 'teasing', 'molesting', 'stalking', 'eve-teasing', 'assault', 'threatening', 'bothering', 'troubling', 'women abuse', 'woman being',
            # Hindi
            'महिला', 'लड़की', 'स्त्री', 'औरत', 'परेशानी', 'छेड़छाड़', 'तंग', 'दिक्कत', 'परेशान', 'सताना',
            # Tamil
            'பெண்', 'பெண்கள்', 'துன்புறுத்தல்', 'தொல்லை', 'கவலைப்படுத்தல்',
            # Telugu
            'మహిళ', 'అమ్మాయి', 'స్త్రీ', 'వేధింపులు', 'ఇబ్బంది', 'ఇరుక్కు',
            # Marathi
            'महिला', 'मुलगी', 'स्त्री', 'छळवणूक', 'त्रास', 'चिडवणूक',
            # Bengali
            'মহিলা', 'মেয়ে', 'নারী', 'হয়রানি', 'যন্ত্রণা', 'বিরক্ত',
            # Gujarati
            'મહિલા', 'છોકરી', 'સ્ત્રી', 'છેડતી', 'તકલીફ', 'પરેશાન',
            # Kannada
            'ಮಹಿಳೆ', 'ಹುಡುಗಿ', 'ಸ್ತ್ರೀ', 'ಕಿರುಕುಳ', 'ತೊಂದರೆ', 'ಬೇಸರ',
            # Malayalam
            'സ്ത്രീ', 'പെൺകുട്ടി', 'ഉപദ്രവം', 'ശല്യം', 'ബുദ്ധിമുട്ട്',
            # Punjabi
            'ਔਰਤ', 'ਕੁੜੀ', 'ਤੰਗ', 'ਪਰੇਸ਼ਾਨ', 'ਦਿੱਕਤ'
        ]
        
        child_keywords = [
            # English
            'child', 'children', 'kid', 'kids', 'baby', 'infant', 'minor', 'child abuse', 'child being', 'child is', 'kid abuse', 'baby abuse', 'child safety', 'child protection', 'missing child', 'lost child', 'child kidnap', 'child trafficking', 'child labor', 'child labour', 'boy', 'girl working', 'minor working', 'underage work',
            # Hindi
            'बच्चा', 'बच्चे', 'बच्ची', 'शिशु', 'नाबालिग', 'बच्चों का', 'बाल', 'बच्चे को', 'बच्चे का', 'बच्चा गुम', 'बच्चा खो गया', 'बाल मजदूरी', 'बाल श्रम', 'लड़का', 'लड़की', 'बच्चों से काम', 'नाबालिग से काम',
            # Tamil
            'குழந்தை', 'குழந்தைகள்', 'சிறுவன்', 'சிறுமி', 'குழந்தை துன்புறுத்தல்', 'குழந்தை பாதுகாப்பு',
            # Telugu
            'పిల్లలు', 'పిల్లవాడు', 'పిల్లవాళ్ళు', 'శిశువు', 'పిల్లల వేధింపులు', 'పిల్లల భద్రత',
            # Marathi
            'मूल', 'मुलगा', 'मुलगी', 'मुला', 'मुली', 'लहान', 'मुलांचा', 'मुलाचा', 'मुलांची', 'मुल हरवले', 'मुलाला', 'मुलांना', 'बाल मजदूरी', 'मुलांचे शोषण',
            # Bengali
            'শিশু', 'বাচ্চা', 'ছেলে', 'মেয়ে', 'শিশু নির্যাতন', 'শিশু সুরক্ষা', 'হারিয়ে গেছে',
            # Gujarati
            'બાળક', 'છોકરો', 'છોકરી', 'નાનું', 'બાળ સુરક્ષા', 'બાળકની સાથે',
            # Kannada
            'ಮಗು', 'ಮಕ್ಕಳು', 'ಹುಡುಗ', 'ಹುಡುಗಿ', 'ಮಕ್ಕಳ ಕಿರುಕುಳ', 'ಮಕ್ಕಳ ಸುರಕ್ಷತೆ',
            # Malayalam
            'കുട്ടി', 'കുട്ടികൾ', 'കുഞ്ഞ്', 'കുട്ടിയുടെ', 'കുട്ടികളുടെ സുരക്ഷ',
            # Punjabi
            'ਬੱਚਾ', 'ਬੱਚੇ', 'ਮੁੰਡਾ', 'ਕੁੜੀ', 'ਬੱਚਿਆਂ ਦੀ', 'ਬੱਚੇ ਦੀ'
        ]
        
        electricity_keywords = [
            # English
            'electricity', 'power', 'outage', 'current', 'voltage', 'transformer',
            # Hindi
            'बिजली', 'करंट', 'पावर', 'ट्रांसफार्मर', 'बत्ती',
            # Tamil
            'மின்சாரம்', 'மின்னல்', 'கரெண்ட்',
            # Telugu
            'కరెంట్', 'విద్యుత్', 'పవర్',
            # Marathi
            'वीज', 'करंट', 'पॉवर',
            # Bengali
            'বিদ্যুৎ', 'কারেন্ট', 'পাওয়ার',
            # Gujarati
            'વીજળી', 'કરંટ', 'પાવર',
            # Kannada
            'ವಿದ್ಯುತ್', 'ಕರೆಂಟ್', 'ಪವರ್',
            # Malayalam
            'വൈദ്യുതി', 'കറന്റ്', 'പവർ',
            # Punjabi
            'ਬਿਜਲੀ', 'ਕਰੰਟ', 'ਪਾਵਰ'
        ]
        
        water_keywords = [
            # English
            'water', 'supply', 'sewerage', 'drainage', 'pipeline', 'tap',
            # Hindi
            'पानी', 'जल', 'जल आपूर्ति', 'सीवेज', 'नल',
            # Tamil
            'தண்ணீர்', 'நீர்', 'குழாய்',
            # Telugu
            'నీరు', 'నీటి సరఫరా', 'కుళాయి',
            # Marathi
            'पाणी', 'जल', 'नळ',
            # Bengali
            'পানি', 'জল', 'নল',
            # Gujarati
            'પાણી', 'જળ', 'નળ',
            # Kannada
            'ನೀರು', 'ಜಲ', 'ನಲ್ಲಿ',
            # Malayalam
            'വെള്ളം', 'ജലം', 'കുഴൽ',
            # Punjabi
            'ਪਾਣੀ', 'ਜਲ', 'ਨਲ'
        ]
        
        transport_keywords = [
            # English
            'transport', 'bus', 'train', 'railway', 'taxi', 'auto', 'metro', 'road', 'travel',
            # Hindi
            'परिवहन', 'बस', 'ट्रेन', 'रेलवे', 'टैक्सी', 'ऑटो', 'मेट्रो', 'सड़क', 'यात्रा',
            # Tamil
            'போக்குவரத்து', 'பேருந்து', 'ரயில்', 'டாக்ஸி', 'ஆட்டோ',
            # Telugu
            'రవాణా', 'బస్సు', 'రైలు', 'టాక్సీ', 'ఆటో',
            # Marathi
            'वाहतूक', 'बस', 'ट्रेन', 'टॅक्सी', 'ऑटो',
            # Bengali
            'পরিবহন', 'বাস', 'ট্রেন', 'ট্যাক্সি', 'অটো',
            # Gujarati
            'પરિવહન', 'બસ', 'ટ્રેન', 'ટેક્સી', 'ઓટો',
            # Kannada
            'ಸಾರಿಗೆ', 'ಬಸ್', 'ರೈಲು', 'ಟ್ಯಾಕ್ಸಿ', 'ಆಟೋ',
            # Malayalam
            'ഗതാഗതം', 'ബസ്', 'ട്രെയിൻ', 'ടാക്സി', 'ഓട്ടോ',
            # Punjabi
            'ਆਵਾਜਾਈ', 'ਬੱਸ', 'ਰੇਲ', 'ਟੈਕਸੀ', 'ਆਟੋ'
        ]
        
        # Smart context-based emergency detection (most specific first)
        
        # CHILD emergencies - highest priority for child safety
        if any(word in text_lower for word in child_keywords):
            emergency_type = 'child'
        # WOMEN emergencies - but only if not child-related
        elif any(word in text_lower for word in women_keywords) and not any(word in text_lower for word in child_keywords):
            emergency_type = 'women'
        # POLICE emergencies
        elif any(word in text_lower for word in police_keywords):
            emergency_type = 'police'
        # MEDICAL emergencies  
        elif any(word in text_lower for word in medical_keywords):
            emergency_type = 'medical'
        # FIRE emergencies
        elif any(word in text_lower for word in fire_keywords):
            emergency_type = 'fire'
        # UTILITY emergencies
        elif any(word in text_lower for word in electricity_keywords):
            emergency_type = 'electricity'
        elif any(word in text_lower for word in water_keywords):
            emergency_type = 'water'
        elif any(word in text_lower for word in transport_keywords):
            emergency_type = 'transport'
        
        # Additional context-based detection with smart logic
        # Women safety - only if NOT about children
        if ('woman' in text_lower or 'girl' in text_lower or 'lady' in text_lower) and ('teasing' in text_lower or 'bothering' in text_lower or 'troubling' in text_lower or 'harassing' in text_lower) and not any(word in text_lower for word in ['child', 'children', 'kid', 'baby', 'minor']):
            emergency_type = 'women'
        
        # Smart helpline prioritization based on emergency type (AI-like reasoning)
        if emergency_type == 'child':
            # For child emergencies: Child helpline FIRST
            basic_helplines = [
                {
                    "number": "1098",
                    "name": "Child Helpline",
                    "type": "child",
                    "description": "Child protection and emergency assistance",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            ]
        elif emergency_type == 'water':
            # For water supply issues: Water specific helplines FIRST
            basic_helplines = [
                {
                    "number": "1916",
                    "name": "Water Supply Helpline",
                    "type": "water",
                    "description": "Water supply complaints and emergency repairs",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1800-11-3155",
                    "name": "Jal Shakti Ministry Helpline",
                    "type": "water",
                    "description": "National water resources and quality complaints",
                    "availability": "9 AM - 6 PM",
                    "state": "All India"
                },
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            ]
        elif emergency_type == 'electricity':
            # For power/electricity issues: Power specific helplines FIRST
            basic_helplines = [
                {
                    "number": "1912",
                    "name": "Power Grid Emergency",
                    "type": "electricity",
                    "description": "National power grid emergencies and outages",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1800-11-4004",
                    "name": "Ministry of Power Helpline",
                    "type": "electricity",
                    "description": "Power supply complaints and consumer grievances",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            ]
        elif emergency_type == 'transport':
            # For transport issues: Transport specific helplines FIRST
            basic_helplines = [
                {
                    "number": "139",
                    "name": "Railway Inquiry",
                    "type": "transport",
                    "description": "Railway information and emergency assistance",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1033",
                    "name": "Tourist Helpline",
                    "type": "transport",
                    "description": "Tourist assistance and travel emergency support",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "1800-11-1363",
                    "name": "Road Transport Helpline",
                    "type": "transport",
                    "description": "Road transport complaints and assistance",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            ]
        elif emergency_type == 'women':
            # For women emergencies: Women helplines FIRST
            basic_helplines = [
                {
                    "number": "1091",
                    "name": "Women Helpline",
                    "type": "women",
                    "description": "Women in distress and domestic violence",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "181",
                    "name": "Women in Distress Helpline",
                    "type": "women",
                    "description": "24x7 helpline for women in distress",
                    "availability": "24/7",
                    "state": "All India"
                },
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            ]
        else:
            # Standard priority for other emergencies
            basic_helplines = [
                {
                    "number": "112",
                    "name": "Emergency Response Support System (ERSS)",
                    "type": "general",
                    "description": "All types of emergencies - Single number for all services",
                    "availability": "24/7",
                    "state": "All India"
                },
            {
                "number": "100",
                "name": "Police",
                "type": "police", 
                "description": "Police assistance and law enforcement",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "108",
                "name": "Ambulance Service",
                "type": "medical",
                "description": "Medical emergency and ambulance service",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "102",
                "name": "Ambulance (Free Service)",
                "type": "medical",
                "description": "Free ambulance service for pregnant women and children",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "101",
                "name": "Fire Brigade",
                "type": "fire",
                "description": "Fire emergency and rescue services",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "1091",
                "name": "Women Helpline",
                "type": "women",
                "description": "Women in distress and domestic violence",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "1098",
                "name": "Child Helpline",
                "type": "child",
                "description": "Child protection and assistance",
                "availability": "24/7",
                "state": "All India"
            },
            {
                "number": "1930",
                "name": "Cyber Crime Helpline",
                "type": "police",
                "description": "Cyber crime and online fraud reporting",
                "availability": "24/7",
                "state": "All India"
            }
        ]
        
        # Only add state-specific helplines if a specific state was detected
        if detected_state != 'All India':
            state_specific = get_state_specific_helplines(detected_state, emergency_type)
            all_helplines = basic_helplines + state_specific
        else:
            # Only show national helplines
            all_helplines = basic_helplines
        
        # Filter and prioritize helplines based on emergency type
        if emergency_type != 'general':
            # Get helplines matching the emergency type first
            priority_helplines = [h for h in all_helplines if h.get('type') == emergency_type]
            other_helplines = [h for h in all_helplines if h.get('type') != emergency_type]
            # Put priority helplines first, then others
            all_helplines = priority_helplines + other_helplines
        
        # Generate contextual translated responses based on emergency type
        emergency_responses = {
            'child': {
                'Hindi': 'बच्चों की आपातकाल! चाइल्डलाइन 1098 से तुरंत संपर्क करें।',
                'Tamil': 'குழந்தைகள் அவசரநிலை! உடனே சைல்ட்லைன் 1098 ஐ அழைக்கவும்.',
                'Telugu': 'పిల్లల అత్యవసర పరిస్థితి! వెంటనే చైల్డ్ లైన్ 1098 కు కాల్ చేయండి.',
                'Marathi': 'मुलांची आपत्कालीन परिस्थिती! मुलांच्या संरक्षणासाठी चाइल्डलाइन 1098 वर ताबडतोब कॉल करा.',
                'Bengali': 'শিশুদের জরুরি অবস্থা! অবিলম্বে চাইল্ডলাইন ১০৯৮ এ কল করুন।',
                'English': 'Child emergency! Call Childline 1098 immediately.'
            },
            'women': {
                'Hindi': 'महिला सहायता! महिला हेल्पलाइन 1091 या 181 पर कॉल करें।',
                'Tamil': 'பெண்கள் உதவி! பெண்கள் ஹெல்ப்லைன் 1091 அல்லது 181 ஐ அழைக்கவும்.',
                'Telugu': 'మహిళల సహాయం! మహిళా హెల్ప్‌లైన్ 1091 లేదా 181 కు కాల్ చేయండి.',
                'Marathi': 'महिला मदत! महिला हेल्पलाइन 1091 किंवा 181 वर कॉल करा.',
                'Bengali': 'মহিলা সহায়তা! মহিলা হেল্পলাইন ১০৯১ বা ১৮১ এ কল করুন।',
                'English': 'Women assistance! Call Women Helpline 1091 or 181.'
            },
            'water': {
                'Hindi': 'पानी की समस्या! जल आपूर्ति हेल्पलाইन 1916 पर कॉल करें।',
                'Tamil': 'தண்ணீர் பிரச்சினை! நீர் விநியோக ஹெல்ப்லைன் 1916 ஐ அழைக்கவும்.',
                'Telugu': 'నీటి సమస్య! వాటర్ సప్లై హెల్ప్‌లైన్ 1916 కు కాల్ చేయండి.',
                'Marathi': 'पाण्याची समस्या! वॉटर सप्लाय हेल्पलाइन 1916 वर कॉल करा.',
                'Bengali': 'পানির সমস্যা! ওয়াটার সাপ্লাই হেল্পলাইন ১৯১৬ এ কল করুন।',
                'English': 'Water problem! Call Water Supply Helpline 1916.'
            },
            'electricity': {
                'Hindi': 'बिजली की समस्या! पावर ग्रिड हेल्पलाइन 1912 पर कॉল करें।',
                'Tamil': 'மின்சார பிரச்சினை! பவர் கிரிட் ஹெல்ப்லைன் 1912 ஐ அழைக்கவும்.',
                'Telugu': 'కరెంట్ సమస్య! పవర్ గ్రిడ్ హెల్ప్‌లైన్ 1912 కు కాల్ చేయండి.',
                'Marathi': 'वीजेची समस्या! पॉवर ग्रिड हेल्पलाइन 1912 वर कॉल करा.',
                'Bengali': 'বিদ্যুতের সমস্যা! পাওয়ার গ্রিড হেল্পলাইন ১৯১২ এ কল করুন।',
                'English': 'Electricity problem! Call Power Grid Helpline 1912.'
            },
            'transport': {
                'Hindi': 'यातायात की समस्या! रेलवे पूछताछ 139 या पर्यटक हेल्पलाइन 1033 पर कॉल करें।',
                'Tamil': 'போக்குவரத்து பிரச்சினை! ரயில்வே விசாரணை 139 அல்லது சுற்றுலா ஹெல்ப்லைன் 1033 ஐ அழைக்கவும்.',
                'Telugu': 'రవాణా సమస్య! రైల్వే ఎంక్వైరీ 139 లేదా టూరిస్ట్ హెల్ప్‌లైన్ 1033 కు కాల్ చేయండి.',
                'Marathi': 'वाहतुकीची समस्या! रेल्वे चौकशी 139 किंवा पर्यटक हेल्पलाइन 1033 वर कॉल करा.',
                'Bengali': 'পরিবহন সমস্যা! রেলওয়ে অনুসন্ধান ১৩৯ বা ট্যুরিস্ট হেল্পলাইন ১০৩৩ এ কল করুন।',
                'English': 'Transport problem! Call Railway Inquiry 139 or Tourist Helpline 1033.'
            },
            'general': {
                'Hindi': 'आपातकाल का पता চला है। सहायता आ रही है। कृपया शांत रहें।',
                'Tamil': 'அவசரநிলை கண্டறியப்পட்டது. உதবি வருகிறது. தயবுসெய்து அমैতியாক இருங்கள்.',
                'Telugu': 'అত্যবসর পরিস্থিতি গুর্তించబడింది. সহায়ం বস্তোంది. దયচেসি প্রশাంতগా ఉండండి।',
                'Marathi': 'आপत্কালীন স্থিতি ওळखলি গেলি. মদত येत আহে. কৃপয়া শাંত राহা।',
                'Bengali': 'জরুরি অবস্থা চিহ্নিত হয়েছে। সাহায্য আসছে। অনুগ্রহ করে শান্ত থাকুন।',
                'English': 'Emergency detected. Help is on the way. Please stay calm.'
            }
        }
        
        # Get appropriate response based on emergency type and language
        emergency_type_responses = emergency_responses.get(emergency_type, emergency_responses['general'])
        translated_response = emergency_type_responses.get(detected_language, emergency_type_responses['English'])
        
        return jsonify({
            'success': True,
            'detectedLanguage': detected_language,
            'detectedState': detected_state,
            'emergencyType': emergency_type,
            'urgencyLevel': 'high',
            'confidence': 0.7,
            'helplineNumbers': all_helplines[:6],  # Return top 6
            'translatedResponse': translated_response,
            'originalLanguageInstructions': translated_response,
            'note': 'Using intelligent keyword analysis for instant emergency detection.'
        })
        
    except Exception as e:
        print(f"Fallback processing error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Emergency processing failed. Please call 112 for immediate assistance.'
        }), 500