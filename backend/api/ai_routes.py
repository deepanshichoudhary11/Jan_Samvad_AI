from flask import Blueprint, request, jsonify
import json
import re
import os

ai_bp = Blueprint('ai', __name__)

def get_state_emergency_numbers(state):
    """
    Get state-specific emergency numbers based on the state
    """
    state_lower = state.lower()
    
    # State-specific emergency numbers
    state_numbers = {
        'uttar pradesh': [
            'Call 108 for ambulance (UP specific)',
            'Call 100 for police (UP)',
            'Call 101 for fire (UP)'
        ],
        'maharashtra': [
            'Call 108 for ambulance (Maharashtra)',
            'Call 104 for fire/medical (Maharashtra)',
            'Call 100 for police (Maharashtra)'
        ],
        'karnataka': [
            'Call 104 for medical advice (Arogyavani)',
            'Call 108 for ambulance (Karnataka)',
            'Call 100 for police (Karnataka)'
        ],
        'delhi': [
            'Call 102 for ambulance (Delhi)',
            'Call 100 for police (Delhi)',
            'Call 101 for fire (Delhi)'
        ],
        'tamil nadu': [
            'Call 108 for ambulance (Tamil Nadu)',
            'Call 100 for police (Tamil Nadu)',
            'Call 101 for fire (Tamil Nadu)'
        ],
        'gujarat': [
            'Call 108 for ambulance (Gujarat)',
            'Call 100 for police (Gujarat)',
            'Call 101 for fire (Gujarat)'
        ],
        'west bengal': [
            'Call 108 for ambulance (West Bengal)',
            'Call 100 for police (West Bengal)',
            'Call 101 for fire (West Bengal)'
        ],
        'andhra pradesh': [
            'Call 108 for ambulance (Andhra Pradesh)',
            'Call 100 for police (Andhra Pradesh)',
            'Call 101 for fire (Andhra Pradesh)'
        ],
        'telangana': [
            'Call 108 for ambulance (Telangana)',
            'Call 100 for police (Telangana)',
            'Call 101 for fire (Telangana)'
        ],
        'kerala': [
            'Call 108 for ambulance (Kerala)',
            'Call 100 for police (Kerala)',
            'Call 101 for fire (Kerala)'
        ]
    }
    
    # Return state-specific numbers if available, otherwise return general numbers
    return state_numbers.get(state_lower, [
        'Call 108 for ambulance (state-specific)',
        'Call 100 for police (state-specific)',
        'Call 101 for fire (state-specific)'
    ])

def get_language_specific_helplines(language, state):
    """
    Get language-specific helpline recommendations
    """
    language_lower = language.lower()
    state_lower = state.lower()
    
    # Language-specific helpline messages
    language_messages = {
        'hindi': {
            'delhi': [
                'दिल्ली पुलिस हेल्पलाइन: 100',
                'दिल्ली एम्बुलेंस: 102',
                'दिल्ली फायर ब्रिगेड: 101'
            ],
            'maharashtra': [
                'महाराष्ट्र पुलिस हेल्पलाइन: 100',
                'महाराष्ट्र एम्बुलेंस: 108',
                'महाराष्ट्र फायर ब्रिगेड: 101'
            ],
            'uttar pradesh': [
                'उत्तर प्रदेश पुलिस हेल्पलाइन: 100',
                'उत्तर प्रदेश एम्बुलेंस: 108',
                'उत्तर प्रदेश फायर ब्रिगेड: 101'
            ],
            'general': [
                'आपातकालीन सहायता: 112',
                'पुलिस हेल्पलाइन: 100',
                'एम्बुलेंस: 102/108',
                'फायर ब्रिगेड: 101'
            ]
        },
        'bengali': {
            'west bengal': [
                'পশ্চিমবঙ্গ পুলিশ হেল্পলাইন: 100',
                'পশ্চিমবঙ্গ অ্যাম্বুলেন্স: 108',
                'পশ্চিমবঙ্গ ফায়ার ব্রিগেড: 101'
            ],
            'general': [
                'জরুরি সাহায্য: 112',
                'পুলিশ হেল্পলাইন: 100',
                'অ্যাম্বুলেন্স: 102/108',
                'ফায়ার ব্রিগেড: 101'
            ]
        },
        'tamil': {
            'tamil nadu': [
                'தமிழ்நாடு காவல்துறை ஹெல்ப்லைன்: 100',
                'தமிழ்நாடு ஆம்புலன்ஸ்: 108',
                'தமிழ்நாடு தீயணைப்பு பிரிகேட்: 101'
            ],
            'general': [
                'அவசர உதவி: 112',
                'காவல்துறை ஹெல்ப்லைன்: 100',
                'ஆம்புலன்ஸ்: 102/108',
                'தீயணைப்பு பிரிகேட்: 101'
            ]
        },
        'telugu': {
            'andhra pradesh': [
                'ఆంధ్రప్రదేశ్ పోలీసు హెల్ప్‌లైన్: 100',
                'ఆంధ్రప్రదేశ్ ఆంబులెన్స్: 108',
                'ఆంధ్రప్రదేశ్ అగ్నిమాపక బ్రిగేడ్: 101'
            ],
            'telangana': [
                'తెలంగాణ పోలీసు హెల్ప్‌లైన్: 100',
                'తెలంగాణ ఆంబులెన్స్: 108',
                'తెలంగాణ అగ్నిమాపక బ్రిగేడ్: 101'
            ],
            'general': [
                'విపత్తు సహాయం: 112',
                'పోలీసు హెల్ప్‌లైన్: 100',
                'ఆంబులెన్స్: 102/108',
                'అగ్నిమాపక బ్రిగేడ్: 101'
            ]
        },
        'gujarati': {
            'gujarat': [
                'ગુજરાત પોલીસ હેલ્પલાઈન: 100',
                'ગુજરાત એમ્બ્યુલન્સ: 108',
                'ગુજરાત ફાયર બ્રિગેડ: 101'
            ],
            'general': [
                'કટોકટી સહાય: 112',
                'પોલીસ હેલ્પલાઈન: 100',
                'એમ્બ્યુલન્સ: 102/108',
                'ફાયર બ્રિગેડ: 101'
            ]
        },
        'marathi': {
            'maharashtra': [
                'महाराष्ट्र पोलीस हेल्पलाईन: 100',
                'महाराष्ट्र एम्ब्युलन्स: 108',
                'महाराष्ट्र फायर ब्रिगेड: 101'
            ],
            'general': [
                'आणीबाळ मदत: 112',
                'पोलीस हेल्पलाईन: 100',
                'एम्ब्युलन्स: 102/108',
                'फायर ब्रिगेड: 101'
            ]
        },
        'kannada': {
            'karnataka': [
                'ಕರ್ನಾಟಕ ಪೊಲೀಸ್ ಹೆಲ್ಪ್‌ಲೈನ್: 100',
                'ಕರ್ನಾಟಕ ಆಂಬ್ಯುಲೆನ್ಸ್: 108',
                'ಕರ್ನಾಟಕ ಅಗ್ನಿಮಾಪಕ ಬ್ರಿಗೇಡ್: 101'
            ],
            'general': [
                'ತುರ್ತು ಸಹಾಯ: 112',
                'ಪೊಲೀಸ್ ಹೆಲ್ಪ್‌ಲೈನ್: 100',
                'ಆಂಬ್ಯುಲೆನ್ಸ್: 102/108',
                'ಅಗ್ನಿಮಾಪಕ ಬ್ರಿಗೇಡ್: 101'
            ]
        },
        'malayalam': {
            'kerala': [
                'കേരള പോലീസ് ഹെൽപ്പ്‌ലൈൻ: 100',
                'കേരള ആംബുലൻസ്: 108',
                'കേരള ഫയർ ബ്രിഗേഡ്: 101'
            ],
            'general': [
                'അടിയന്തിര സഹായം: 112',
                'പോലീസ് ഹെൽപ്പ്‌ലൈൻ: 100',
                'ആംബുലൻസ്: 102/108',
                'ഫയർ ബ്രിഗേഡ്: 101'
            ]
        }
    }
    
    # Get language-specific messages
    lang_messages = language_messages.get(language_lower, {})
    
    # Return state-specific messages if available, otherwise return general messages
    return lang_messages.get(state_lower, lang_messages.get('general', []))

def analyze_problem_with_gemini(description, language, state):
    """
    Analyze problem using real Gemini AI with improved error handling and multi-language support
    """
    try:
        import google.generativeai as genai
        import time
        
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model with timeout
        model = genai.GenerativeModel('gemini-pro')
        
        # Create comprehensive prompt for AI analysis with multi-language support
        prompt = f"""
You are an expert helpline assistant for India that understands ALL Indian languages. Analyze the following problem description and provide detailed analysis.

Problem Description: "{description}"
Language: {language}
State: {state}

IMPORTANT: The problem description may be in Hindi, English, Gujarati, Tamil, Telugu, Bengali, Marathi, or any other Indian language. You must:
1. Understand the problem regardless of language
2. Identify key concepts like "child", "woman", "harassment", "health", "transport", etc.
3. Translate the meaning to English for categorization
4. Provide appropriate helpline recommendations

Please analyze this problem and provide a JSON response with the following structure:

{{
    "problemType": "Specific problem category (e.g., Women Safety, Child Protection, Healthcare, Transport, etc.)",
    "suggestedState": "Detected state from description or provided state",
    "suggestedIssue": "Relevant issue category (Women Help, Child Help, Health, Transport, Water, Electricity, Emergency)",
    "priority": "High/Medium/Low/Critical based on urgency",
    "recommendations": [
        "Specific helpline numbers and actions",
        "Contact information",
        "Immediate steps to take"
    ],
    "confidence": 0.95,
    "aiAnalysis": "Detailed AI analysis of the problem",
    "context": "Additional context and insights"
}}

Key Detection Guidelines:
1. CHILD PROTECTION: Look for words like "बच्चा", "child", "kid", "minor", "student" + words like "harassment", "abuse", "मजदूर", "slave", "help", "मदद"
2. WOMEN SAFETY: Look for words like "woman", "women", "female", "girl", "महिला", "स्त्री" + words like "harassment", "molestation", "violence", "हिंसा"
3. HEALTH: Look for words like "health", "medical", "hospital", "doctor", "ambulance", "स्वास्थ्य", "डॉक्टर", "बीमार"
4. TRANSPORT: Look for words like "highway", "road", "petrol", "fuel", "vehicle", "सड़क", "पेट्रोल", "गाड़ी"
5. EMERGENCY: Look for words like "emergency", "urgent", "critical", "आपातकाल", "तत्काल"

Always include 112 for emergencies and provide specific, actionable recommendations.
        """
        
        # Generate response from Gemini with timeout
        start_time = time.time()
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Check if response took too long
        if time.time() - start_time > 30:  # 30 second timeout
            raise Exception("AI response timeout")
        
        # Parse the JSON response
        try:
            # Extract JSON from the response (in case there's extra text)
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            json_str = ai_response[start_idx:end_idx]
            
            analysis_result = json.loads(json_str)
            
            # Ensure all required fields are present
            required_fields = ['problemType', 'suggestedState', 'suggestedIssue', 'priority', 'recommendations']
            for field in required_fields:
                if field not in analysis_result:
                    analysis_result[field] = 'General' if field == 'problemType' else ''
            
            return analysis_result
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                'problemType': 'General',
                'suggestedState': state,
                'suggestedIssue': '',
                'priority': 'Medium',
                'recommendations': ['Contact 112 for emergency assistance'],
                'confidence': 0.7,
                'aiAnalysis': ai_response,
                'context': 'AI analysis provided but JSON parsing failed'
            }
        
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        # Use intelligent fallback analysis based on keywords
        return intelligent_fallback_analysis(description, language, state, str(e))

def intelligent_fallback_analysis(description, language, state, error_msg):
    """
    Intelligent fallback analysis when AI fails
    """
    description_lower = description.lower()
    
    # Women safety analysis - Multi-language support
    women_keywords = [
        'woman', 'women', 'female', 'girl', 'ladies',
        'महिला', 'स्त्री', 'लड़की', 'औरत', 'नारी',
        'பெண்', 'பெண்கள்', 'பெண் குழந்தை',
        'స్త్రీ', 'మహిళ', 'అమ్మాయి',
        'মহিলা', 'নারী', 'মেয়ে',
        'बाई', 'स्त्री', 'महिला'
    ]
    harassment_keywords = [
        'harassment', 'harassing', 'harassed', 'molestation', 'stalking', 'eve teasing',
        'छेड़छाड़', 'परेशानी', 'उत्पीड़न', 'दुर्व्यवहार', 'हिंसा',
        'வேட்டை', 'துன்புறுத்தல்', 'கொடுமை',
        'వేధింపులు', 'అవమానం', 'దుర్వినియోగం',
        'নির্যাতন', 'উৎপীড়ন', 'অত্যাচার'
    ]
    violence_keywords = [
        'violence', 'abuse', 'domestic', 'beating', 'threat', 'intimidation',
        'हिंसा', 'मारपीट', 'धमकी', 'अत्याचार', 'दुर्व्यवहार',
        'வன்முறை', 'அடி', 'மிரட்டல்',
        'హింస', 'చావగొట్టడం', 'ముప్పు',
        'সহিংসতা', 'মারধর', 'ধমক'
    ]
    
    is_woman_mentioned = any(keyword in description_lower for keyword in women_keywords)
    is_harassment_mentioned = any(keyword in description_lower for keyword in harassment_keywords)
    is_violence_mentioned = any(keyword in description_lower for keyword in violence_keywords)
    
    if is_woman_mentioned and (is_harassment_mentioned or is_violence_mentioned):
        return {
            'problemType': 'Women Safety',
            'suggestedState': state,
            'suggestedIssue': 'Women Help',
            'priority': 'High',
            'recommendations': [
                'Contact National Women Helpline (181)',
                'Call 112 for immediate assistance',
                'Contact local women protection cell',
                'Contact Women and Child Protection Unit',
                'File complaint at nearest police station'
            ],
            'confidence': 0.85,
            'aiAnalysis': 'Intelligent analysis detected women safety issue with harassment/violence',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Child protection analysis - Multi-language support
    child_keywords = [
        'child', 'children', 'minor', 'kid', 'boy', 'girl', 'student',
        'बच्चा', 'बच्चे', 'बच्ची', 'लड़का', 'लड़की', 'शिशु', 'बालक', 'बालिका',
        'குழந்தை', 'பிள்ளை', 'மகன்', 'மகள்',
        'పిల్లలు', 'బిడ్డ', 'కుమారుడు', 'కుమార్తె',
        'শিশু', 'ছেলে', 'মেয়ে', 'সন্তান',
        'बालक', 'बालिका', 'मुलगा', 'मुलगी'
    ]
    child_abuse_keywords = [
        'abuse', 'molestation', 'exploitation', 'trafficking', 'neglect', 
        'harassment', 'harassing', 'harassed', 'slave', 'slavery', 
        'mistreatment', 'beating', 'threat',
        'मजदूर', 'शोषण', 'दुर्व्यवहार', 'गुलाम', 'पीटना', 'धमकी', 'अत्याचार',
        'கொடுமை', 'வன்முறை', 'சுரண்டல்', 'அடிமை',
        'దుర్వినియోగం', 'వేధింపులు', 'గులాము', 'చావగొట్టడం',
        'নির্যাতন', 'শোষণ', 'দাসত্ব', 'মারধর'
    ]
    
    is_child_mentioned = any(keyword in description_lower for keyword in child_keywords)
    is_child_abuse_mentioned = any(keyword in description_lower for keyword in child_abuse_keywords)
    
    if is_child_mentioned and is_child_abuse_mentioned:
        return {
            'problemType': 'Child Protection',
            'suggestedState': state,
            'suggestedIssue': 'Child Help',
            'priority': 'High',
            'recommendations': [
                'Contact Childline India (1098)',
                'Report to local police station',
                'Contact child protection unit',
                'Contact National Commission for Protection of Child Rights',
                'Call 112 for immediate assistance'
            ],
            'confidence': 0.9,
            'aiAnalysis': 'Intelligent analysis detected child protection issue with abuse/slavery',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # General child help cases
    if is_child_mentioned and ('help' in description_lower or 'want to help' in description_lower or 'need help' in description_lower or 'मदद' in description_lower or 'सहायता' in description_lower or 'बचाना' in description_lower):
        return {
            'problemType': 'Child Protection',
            'suggestedState': state,
            'suggestedIssue': 'Child Help',
            'priority': 'High',
            'recommendations': [
                'Contact Childline India (1098)',
                'Report to local police station',
                'Contact child protection unit',
                'Contact National Commission for Protection of Child Rights',
                'Contact local child welfare committee'
            ],
            'confidence': 0.8,
            'aiAnalysis': 'Intelligent analysis detected child help request',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Transport analysis - Multi-language support
    transport_keywords = [
        'highway', 'road', 'petrol', 'fuel', 'gas', 'vehicle', 'car', 'bike', 'bus', 'truck', 'transport', 'travel', 'journey', 'trip',
        'सड़क', 'पेट्रोल', 'गाड़ी', 'वाहन', 'यात्रा', 'रास्ता',
        'சாலை', 'பெட்ரோல்', 'வாகனம்', 'பயணம்',
        'రోడ్', 'పెట్రోల్', 'వాహనం', 'ప్రయాణం',
        'সড়ক', 'পেট্রোল', 'গাড়ি', 'যাত্রা'
    ]
    emergency_transport_keywords = [
        'accident', 'breakdown', 'stuck', 'emergency', 'help', 'assistance',
        'एक्सीडेंट', 'दुर्घटना', 'मदद', 'आपातकाल', 'ब्रेकडाउन', 'फंस गया',
        'விபத்து', 'உதவி', 'அவசரம்', 'சிக்கல்',
        'ప్రమాదం', 'సహాయం', 'తక్షణం', 'అడ్డుపడింది',
        'দুর্ঘটনা', 'সাহায্য', 'জরুরি', 'আটকে গেছে'
    ]
    
    is_transport_mentioned = any(keyword in description_lower for keyword in transport_keywords)
    is_emergency_transport = any(keyword in description_lower for keyword in emergency_transport_keywords)
    
    # Check for transport emergency first (accident, breakdown, etc.)
    if is_emergency_transport:
        # State-specific emergency numbers
        state_emergency_numbers = get_state_emergency_numbers(state)
        
        return {
            'problemType': 'Transport Emergency',
            'suggestedState': state,
            'suggestedIssue': 'Transport',
            'priority': 'High',
            'recommendations': [
                'Call 112 for emergency assistance',
                'Call 1099 for specialized trauma assistance',
                'Call 102 for ambulance (free service)',
                'Call 108 for ambulance (state-specific)',
                'Contact Highway Patrol',
                'Call nearest police station',
                'Contact local transport authority',
                'Call National Highway Helpline'
            ] + state_emergency_numbers,
            'confidence': 0.85,
            'aiAnalysis': 'Intelligent analysis detected transport emergency',
            'context': 'Using intelligent analysis due to network issues'
        }
    # Check for general transport issues
    elif is_transport_mentioned:
        return {
            'problemType': 'Transport',
            'suggestedState': state,
            'suggestedIssue': 'Transport',
            'priority': 'Medium',
            'recommendations': [
                'Contact local transport authority',
                'Call nearest petrol pump',
                'Contact highway assistance',
                'Call National Highway Helpline',
                'Contact local police for directions'
            ],
            'confidence': 0.8,
            'aiAnalysis': 'Intelligent analysis detected transport issue',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Healthcare analysis - Multi-language support
    health_keywords = [
        'health', 'medical', 'hospital', 'doctor', 'ambulance', 'covid', 'fever', 'pain', 'sick', 'medicine', 'treatment',
        'स्वास्थ्य', 'मेडिकल', 'हॉस्पिटल', 'डॉक्टर', 'एम्बुलेंस', 'बुखार', 'दर्द', 'बीमार', 'दवा', 'इलाज',
        'சுகாதாரம்', 'மருத்துவம்', 'மருத்துவமனை', 'மருத்துவர்', 'ஆம்புலன்ஸ்', 'காய்ச்சல்', 'வலி', 'நோய்', 'மருந்து', 'சிகிச்சை',
        'ఆరోగ్యం', 'వైద్యం', 'ఆసుపత్రి', 'డాక్టర్', 'ఆంబులెన్స్', 'జ్వరం', 'నొప్పి', 'అనారోగ్యం', 'మందు', 'చికిత్స',
        'স্বাস্থ্য', 'চিকিৎসা', 'হাসপাতাল', 'ডাক্তার', 'অ্যাম্বুলেন্স', 'জ্বর', 'ব্যথা', 'অসুস্থ', 'ঔষধ', 'চিকিৎসা',
        'आरोग्य', 'वैद्यकीय', 'रुग्णालय', 'वैद्य', 'रुग्णवाहिका', 'ताप', 'वेदना', 'आजारी', 'औषध', 'उपचार'
    ]
    emergency_health_keywords = [
        'emergency', 'critical', 'unconscious', 'bleeding', 'heart attack', 'stroke', 'accident', 'injury',
        'आपातकाल', 'गंभीर', 'बेहोश', 'खून बह रहा', 'हार्ट अटैक', 'स्ट्रोक', 'दुर्घटना', 'चोट',
        'அவசரம்', 'கடுமையான', 'உணர்வற்ற', 'இரத்தம்', 'இதய நோய்', 'பக்கவாதம்', 'விபத்து', 'காயம்',
        'తక్షణం', 'క్లిష్టమైన', 'అపస్మారకం', 'రక్తం', 'గుండెపోటు', 'పక్షవాతం', 'ప్రమాదం', 'గాయం',
        'জরুরি', 'গুরুতর', 'অচেতন', 'রক্তপাত', 'হার্ট অ্যাটাক', 'স্ট্রোক', 'দুর্ঘটনা', 'আঘাত',
        'आणीबाळ', 'गंभीर', 'बेशुद्ध', 'रक्तस्त्राव', 'हृदयविकार', 'पक्षघात', 'अपघात', 'जखम'
    ]
    
    is_health_mentioned = any(keyword in description_lower for keyword in health_keywords)
    is_emergency_health = any(keyword in description_lower for keyword in emergency_health_keywords)
    
    if is_health_mentioned:
        if is_emergency_health:
            # State-specific emergency numbers
            state_emergency_numbers = get_state_emergency_numbers(state)
            
            return {
                'problemType': 'Medical Emergency',
                'suggestedState': state,
                'suggestedIssue': 'Health',
                'priority': 'Critical',
                'recommendations': [
                    'Call 112 immediately for medical emergency',
                    'Call 102 for ambulance (free service)',
                    'Call 108 for ambulance (state-specific)',
                    'Call 1099 for specialized trauma assistance',
                    'Contact nearest hospital emergency department',
                    'Call National Health Helpline (1075)'
                ] + state_emergency_numbers,
                'confidence': 0.9,
                'aiAnalysis': 'Intelligent analysis detected medical emergency',
                'context': 'Using intelligent analysis due to network issues'
            }
        else:
            return {
                'problemType': 'Healthcare',
                'suggestedState': state,
                'suggestedIssue': 'Health',
                'priority': 'Medium',
                'recommendations': [
                    'Contact National Health Helpline (1075)',
                    'Contact local hospital',
                    'Contact nearest primary health center'
                ],
                'confidence': 0.7,
                'aiAnalysis': 'Intelligent analysis detected healthcare issue',
                'context': 'Using intelligent analysis due to network issues'
            }
    
    # Water issues - Multi-language support
    water_keywords = [
        'water', 'supply', 'shortage', 'leak', 'pipe', 'drinking', 'tank', 'tap',
        'पानी', 'आपूर्ति', 'कमी', 'रिसाव', 'पाइप', 'पीने का', 'टैंक', 'नल',
        'தண்ணீர்', 'விநியோகம்', 'பற்றாக்குறை', 'கசிவு', 'குழாய்', 'குடிநீர்', 'தொட்டி', 'குழாய்',
        'నీరు', 'సరఫరా', 'పొట్టు', 'రావడం', 'పైపు', 'త్రాగడానికి', 'ట్యాంక్', 'బోరు',
        'জল', 'সরবরাহ', 'স্বল্পতা', 'ফুটো', 'পাইপ', 'পানীয়', 'ট্যাঙ্ক', 'কল',
        'पाणी', 'पुरवठा', 'उणीव', 'गळती', 'पाईप', 'पिण्याचे', 'टाकी', 'नळ'
    ]
    
    # Electricity issues - Multi-language support
    electricity_keywords = [
        'electricity', 'power', 'current', 'voltage', 'wire', 'switch', 'meter', 'bill',
        'बिजली', 'विद्युत', 'करंट', 'वोल्टेज', 'तार', 'स्विच', 'मीटर', 'बिल',
        'மின்சாரம்', 'மின்', 'மின்னோட்டம்', 'மின்னழுத்தம்', 'கம்பி', 'சுவிட்ச்', 'மீட்டர்', 'பில்',
        'విద్యుత్', 'పవర్', 'కరెంట్', 'వోల్టేజ్', 'వైర్', 'స్విచ్', 'మీటర్', 'బిల్లు',
        'বিদ্যুৎ', 'পাওয়ার', 'কারেন্ট', 'ভোল্টেজ', 'তারের', 'সুইচ', 'মিটার', 'বিল',
        'वीज', 'विद्युत', 'प्रवाह', 'व्होल्टेज', 'तार', 'स्विच', 'मीटर', 'बिल'
    ]
    
    # Police issues - Multi-language support
    police_keywords = [
        'police', 'crime', 'theft', 'robbery', 'fraud', 'complaint', 'fir', 'investigation',
        'पुलिस', 'अपराध', 'चोरी', 'डकैती', 'धोखाधड़ी', 'शिकायत', 'एफआईआर', 'जांच',
        'காவல்துறை', 'குற்றம்', 'திருட்டு', 'கொள்ளை', 'மோசடி', 'புகார்', 'எஃப்ஐஆர்', 'விசாரணை',
        'పోలీసు', 'నేరం', 'దొంగతనం', 'దోపిడీ', 'మోసం', 'ఫిర్యాదు', 'ఎఫ్ఐఆర్', 'విచారణ',
        'পুলিশ', 'অপরাধ', 'চুরি', 'ডাকাতি', 'জালিয়াতি', 'অভিযোগ', 'এফআইআর', 'তদন্ত',
        'पोलीस', 'गुन्हा', 'चोरी', 'दरोडा', 'फसवणूक', 'तक्रार', 'एफआयआर', 'चौकशी'
    ]
    
    # Fire emergency - Multi-language support
    fire_keywords = [
        'fire', 'burning', 'smoke', 'flame', 'blaze', 'firefighter', 'rescue',
        'आग', 'जल रहा', 'धुआं', 'लौ', 'ज्वाला', 'अग्निशमक', 'बचाव',
        'தீ', 'எரிகிறது', 'புகை', 'சுடர்', 'சுடர்', 'தீயணைப்பு', 'காப்பாற்றல்',
        'అగ్ని', 'మండుతున్న', 'పొగ', 'జ్వాల', 'జ్వాల', 'అగ్నిమాపక', 'రక్షణ',
        'আগুন', 'জ্বলছে', 'ধোঁয়া', 'শিখা', 'শিখা', 'অগ্নিনির্বাপক', 'উদ্ধার',
        'आग', 'जळत आहे', 'धूर', 'शिखा', 'शिखा', 'अग्निशमन', 'बचाव'
    ]
    
    # Check for water issues
    is_water_mentioned = any(keyword in description_lower for keyword in water_keywords)
    if is_water_mentioned:
        return {
            'problemType': 'Water Supply',
            'suggestedState': state,
            'suggestedIssue': 'Water',
            'priority': 'Medium',
            'recommendations': [
                'Contact local water supply department',
                'Call municipal corporation water helpline',
                'Contact water board office',
                'Report to local authority',
                'Call 112 for emergency water issues'
            ],
            'confidence': 0.8,
            'aiAnalysis': 'Intelligent analysis detected water supply issue',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Check for electricity issues
    is_electricity_mentioned = any(keyword in description_lower for keyword in electricity_keywords)
    if is_electricity_mentioned:
        # Check if Delhi is mentioned for specific Delhi power companies
        delhi_keywords = ['delhi', 'दिल्ली', 'டெல்லி', 'దిల్లీ', 'দিল্লি', 'दिल्ली']
        is_delhi_mentioned = any(keyword in description_lower for keyword in delhi_keywords)
        
        if is_delhi_mentioned or state.lower() == 'delhi':
            return {
                'problemType': 'Electricity - Delhi',
                'suggestedState': 'Delhi',
                'suggestedIssue': 'Electricity',
                'priority': 'Medium',
                'recommendations': [
                    'BSES Rajdhani Power Limited (South & West Delhi): 19123',
                    'BSES Yamuna Power Limited (Central & East Delhi): 19122',
                    'Tata Power Delhi Distribution (North & North-West Delhi): 19124',
                    'Tata Power Toll-Free (Outside Delhi): 1800-208-9124',
                    'Delhi Electricity Regulatory Commission: +91-11-41080417',
                    'Electricity Ombudsman Delhi: 011-26144979',
                    'Call 112 for emergency power issues'
                ],
                'confidence': 0.9,
                'aiAnalysis': 'Intelligent analysis detected Delhi electricity issue',
                'context': 'Using intelligent analysis due to network issues'
            }
        else:
            return {
                'problemType': 'Electricity',
                'suggestedState': state,
                'suggestedIssue': 'Electricity',
                'priority': 'Medium',
                'recommendations': [
                    'Contact local electricity board',
                    'Call power supply helpline',
                    'Contact electricity department',
                    'Report to power distribution company',
                    'Call 112 for emergency power issues'
                ],
                'confidence': 0.8,
                'aiAnalysis': 'Intelligent analysis detected electricity issue',
                'context': 'Using intelligent analysis due to network issues'
            }
    
    # Check for police/crime issues
    is_police_mentioned = any(keyword in description_lower for keyword in police_keywords)
    if is_police_mentioned:
        # State-specific emergency numbers
        state_emergency_numbers = get_state_emergency_numbers(state)
        
        return {
            'problemType': 'Crime/Police',
            'suggestedState': state,
            'suggestedIssue': 'Police',
            'priority': 'High',
            'recommendations': [
                'Call 100 for police assistance',
                'Call 112 for emergency police help',
                'Call 1099 for specialized trauma assistance',
                'Contact nearest police station',
                'File complaint at local police station',
                'Contact crime branch if needed'
            ] + state_emergency_numbers,
            'confidence': 0.85,
            'aiAnalysis': 'Intelligent analysis detected crime/police issue',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Check for fire emergency
    is_fire_mentioned = any(keyword in description_lower for keyword in fire_keywords)
    if is_fire_mentioned:
        # State-specific emergency numbers
        state_emergency_numbers = get_state_emergency_numbers(state)
        
        return {
            'problemType': 'Fire Emergency',
            'suggestedState': state,
            'suggestedIssue': 'Fire',
            'priority': 'Critical',
            'recommendations': [
                'Call 101 for fire emergency',
                'Call 112 for immediate assistance',
                'Call 1099 for specialized trauma assistance',
                'Contact fire brigade',
                'Evacuate the area immediately',
                'Call nearest fire station'
            ] + state_emergency_numbers,
            'confidence': 0.9,
            'aiAnalysis': 'Intelligent analysis detected fire emergency',
            'context': 'Using intelligent analysis due to network issues'
        }
    
    # Default fallback
    return {
        'problemType': 'General',
        'suggestedState': state,
        'suggestedIssue': '',
        'priority': 'Medium',
        'recommendations': ['Contact 112 for emergency assistance'],
        'confidence': 0.5,
        'aiAnalysis': 'Intelligent analysis completed successfully',
        'context': 'Using intelligent analysis due to network issues'
    }

@ai_bp.route('/analyze-problem', methods=['POST'])
def analyze_problem():
    try:
        data = request.get_json()
        description = data.get('description', '')
        language = data.get('language', 'en-IN')
        state = data.get('state', 'India')
        
        # Use real AI analysis
        analysis_result = analyze_problem_with_gemini(description, language, state)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/recommend-schemes', methods=['POST'])
def recommend_schemes():
    """
    AI-powered scheme recommendation based on problem analysis
    """
    try:
        data = request.get_json()
        problem_description = data.get('problemDescription', '')
        user_profile = data.get('userProfile', {})
        language = data.get('language', 'en-IN')
        
        # Load available schemes
        with open('data/schemes.json', 'r') as f:
            schemes_data = json.load(f)
        
        schemes = schemes_data.get('schemes', [])
        
        # Use AI to analyze and recommend schemes
        recommended_schemes = recommend_schemes_with_gemini(
            problem_description, 
            user_profile, 
            schemes, 
            language
        )
        
        return jsonify({
            'recommendedSchemes': recommended_schemes,
            'total': len(recommended_schemes),
            'aiAnalysis': 'AI analyzed your problem and recommended relevant government schemes'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def recommend_schemes_with_gemini(problem_description, user_profile, schemes, language):
    """
    Use Gemini AI to recommend relevant government schemes
    """
    try:
        import google.generativeai as genai
        
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create schemes list for AI
        schemes_list = []
        for scheme in schemes:
            schemes_list.append({
                'name': scheme.get('name', ''),
                'category': scheme.get('category', ''),
                'description': scheme.get('description', ''),
                'eligibility': scheme.get('eligibility', ''),
                'benefits': scheme.get('benefits', '')
            })
        
        # Create comprehensive prompt for AI scheme recommendation
        prompt = f"""
You are an expert government scheme advisor for India. Analyze the following problem and user profile to recommend the most relevant government schemes.

Problem Description: "{problem_description}"
User Profile: {json.dumps(user_profile, indent=2)}
Language: {language}

Available Schemes: {json.dumps(schemes_list, indent=2)}

Please analyze the problem and user profile, then recommend the most relevant government schemes. Return a JSON response with:

{{
    "recommendedSchemes": [
        {{
            "name": "Scheme name",
            "category": "Scheme category",
            "description": "Why this scheme is relevant",
            "eligibility": "Eligibility criteria",
            "benefits": "What benefits you can get",
            "relevanceScore": 0.95,
            "howToApply": "Step-by-step application process"
        }}
    ],
    "aiAnalysis": "Detailed analysis of why these schemes are recommended",
    "priorityOrder": "List schemes in order of priority/relevance"
}}

Guidelines:
1. Focus on schemes that directly address the user's problem
2. Consider user's demographic profile (age, gender, occupation, income)
3. Prioritize schemes with immediate benefits
4. Include both central and state government schemes
5. Provide clear application instructions
6. Consider cultural and regional context
7. Maximum 5-8 most relevant schemes

Analyze thoroughly and provide the most helpful scheme recommendations.
        """
        
        # Generate response from Gemini
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Parse the JSON response
        try:
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            json_str = ai_response[start_idx:end_idx]
            
            recommendation_result = json.loads(json_str)
            
            # Ensure required fields are present
            if 'recommendedSchemes' not in recommendation_result:
                recommendation_result['recommendedSchemes'] = []
            
            return recommendation_result['recommendedSchemes']
            
        except json.JSONDecodeError:
            # Fallback to basic scheme matching
            return schemes[:5]  # Return first 5 schemes as fallback
        
    except Exception as e:
        print(f"Gemini AI Scheme Recommendation Error: {e}")
        # Return fallback recommendations
        return schemes[:5]

@ai_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'AI Analysis'})