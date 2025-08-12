import React, { useState, useRef, useEffect, useCallback } from 'react';
import { voiceAPI } from '../services/api';
import './VoiceToText.css';

const VoiceToText = ({ onVoiceResult, userState, userLanguage }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [voiceText, setVoiceText] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [helplineNumbers, setHelplineNumbers] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [supportedLanguages, setSupportedLanguages] = useState([]);
  const [recognition, setRecognition] = useState(null);
  const [showHelplines, setShowHelplines] = useState(false);

  const initializeSpeechRecognition = useCallback(() => {
    if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
      setError('Speech recognition is not supported in this browser');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognitionInstance = new SpeechRecognition();
    
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = selectedLanguage || 'hi-IN';
    
    recognitionInstance.onstart = () => {
      setIsRecording(true);
      setError('');
    };

    recognitionInstance.onresult = (event) => {
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        }
      }

      if (finalTranscript) {
        setVoiceText(finalTranscript);
        processVoiceInput(finalTranscript);
      }
    };

    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setError(`Voice recognition error: ${event.error}`);
      setIsRecording(false);
    };

    recognitionInstance.onend = () => {
      setIsRecording(false);
    };

    setRecognition(recognitionInstance);
  }, [selectedLanguage]);

  useEffect(() => {
    // Load supported languages
    loadSupportedLanguages();
    
    // Initialize speech recognition
    initializeSpeechRecognition();
  }, [initializeSpeechRecognition]);

  const loadSupportedLanguages = async () => {
    try {
      const response = await voiceAPI.getLanguageSupport();
      if (response.success) {
        setSupportedLanguages(response.supported_languages);
      }
    } catch (error) {
      console.error('Error loading supported languages:', error);
      // Fallback to default languages if API fails
      setSupportedLanguages([
        { language_code: 'hi-IN', native_name: 'हिंदी', language: 'Hindi' },
        { language_code: 'mr-IN', native_name: 'मराठी', language: 'Marathi' },
        { language_code: 'ta-IN', native_name: 'தமிழ்', language: 'Tamil' },
        { language_code: 'te-IN', native_name: 'తెలుగు', language: 'Telugu' },
        { language_code: 'gu-IN', native_name: 'ગુજરાતી', language: 'Gujarati' },
        { language_code: 'bn-IN', native_name: 'বাংলা', language: 'Bengali' },
        { language_code: 'ml-IN', native_name: 'മലയാളം', language: 'Malayalam' },
        { language_code: 'ur-IN', native_name: 'اردو', language: 'Urdu' },
        { language_code: 'pa-IN', native_name: 'ਪੰਜਾਬੀ', language: 'Punjabi' },
        { language_code: 'kn-IN', native_name: 'ಕನ್ನಡ', language: 'Kannada' }
      ]);
    }
  };

  const startRecording = () => {
    if (!recognition) {
      setError('Speech recognition not initialized');
      return;
    }

    setVoiceText('');
    setHelplineNumbers([]);
    setError('');
    setShowHelplines(false);

    try {
      recognition.start();
    } catch (error) {
      setError('Failed to start recording. Please try again.');
    }
  };

  const stopRecording = () => {
    if (recognition) {
      recognition.stop();
    }
  };

  const processVoiceInput = async (text) => {
    if (!text.trim()) return;

    setIsProcessing(true);
    setError('');

    try {
      const response = await voiceAPI.voiceToText({
        text: text,
        state: userState,
        language: selectedLanguage
      });

      if (response.success) {
        setHelplineNumbers(response.state_helplines);
        setShowHelplines(true);
        
        // Call parent callback with results
        if (onVoiceResult) {
          onVoiceResult({
            text: text,
            selectedLanguage: selectedLanguage,
            helplineNumbers: response.state_helplines,
            aiAnalysis: response.ai_analysis,
            multilingualResponse: response.multilingual_response
          });
        }
      }
    } catch (error) {
      setError('Failed to process voice input. Please try again.');
      console.error('Voice processing error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const analyzeWithGemini = async () => {
    if (!voiceText.trim()) {
      setError('Please record some voice input first before analyzing.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const response = await voiceAPI.analyzeWithGemini({
        text: voiceText,
        state: userState,
        language: selectedLanguage
      });

      if (response.success) {
        setHelplineNumbers(response.state_helplines);
        setShowHelplines(true);
        
        // Call parent callback with results
        if (onVoiceResult) {
          onVoiceResult({
            text: voiceText,
            selectedLanguage: selectedLanguage,
            helplineNumbers: response.state_helplines,
            aiAnalysis: response.ai_analysis,
            multilingualResponse: response.multilingual_response
          });
        }
      }
    } catch (error) {
      setError('Failed to analyze with Gemini. Please try again.');
      console.error('Gemini analysis error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleLanguageChange = (e) => {
    const newLanguage = e.target.value;
    setSelectedLanguage(newLanguage);
    
    if (recognition) {
      recognition.lang = newLanguage || 'hi-IN';
    }
  };



  const formatHelplineNumber = (service, number) => {
    const serviceNames = {
      'emergency': 'Emergency',
      'ambulance': 'Ambulance',
      'police': 'Police',
      'fire': 'Fire',
      'women_helpline': 'Women Helpline',
      'cm_helpline': 'CM Helpline',
      'electricity': 'Electricity',
      'transport': 'Transport',
      'food_supply': 'Food Supply',
      'water_supply': 'Water Supply'
    };
    
    return {
      service: serviceNames[service] || service.replace('_', ' ').toUpperCase(),
      number: number
    };
  };

  const getRegionFromLanguage = (languageCode) => {
    const languageRegionMap = {
      'hi-IN': 'Uttar Pradesh',
      'mr-IN': 'Maharashtra',
      'ta-IN': 'Tamil Nadu',
      'te-IN': 'Andhra Pradesh',
      'gu-IN': 'Gujarat',
      'bn-IN': 'West Bengal',
      'ml-IN': 'Kerala',
      'ur-IN': 'Delhi',
      'pa-IN': 'Punjab',
      'kn-IN': 'Karnataka'
    };
    return languageRegionMap[languageCode] || 'India';
  };

  return (
    <div className="voice-to-text-container">
      <div className="voice-controls">
        <div className="language-selector">
          <label htmlFor="language-select">Choose Your Language:</label>
                     <select 
             id="language-select" 
             value={selectedLanguage} 
             onChange={handleLanguageChange}
             disabled={isRecording}
           >
             <option value="">Select a language...</option>
             {supportedLanguages.map((lang) => (
               <option key={lang.language_code} value={lang.language_code}>
                 {lang.native_name} ({lang.language})
               </option>
             ))}
           </select>
          
        </div>

        <div className="recording-controls">
          <button
            className={`record-button ${isRecording ? 'recording' : ''}`}
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
          >
            {isRecording ? (
              <>
                <span className="recording-indicator"></span>
                Stop Recording
              </>
            ) : (
              <>
                <span className="microphone-icon">🎤</span>
                Start Recording
              </>
            )}
          </button>
          
          {voiceText && (
            <button
              className="analyze-button"
              onClick={analyzeWithGemini}
              disabled={isProcessing}
            >
              <span className="ai-icon">🤖</span>
              Analyze with Gemini
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {isProcessing && (
        <div className="processing-message">
          Processing voice input...
        </div>
      )}

      {voiceText && (
        <div className="voice-results">
          <div className="voice-text-section">
            <h3>Voice Input:</h3>
            <p className="voice-text">{voiceText}</p>
          </div>

          {showHelplines && helplineNumbers && Object.keys(helplineNumbers).length > 0 && (
            <div className="helpline-section">
              <h3>Helpline Numbers for {getRegionFromLanguage(selectedLanguage)}:</h3>
              <div className="helpline-grid">
                {Object.entries(helplineNumbers).map(([service, number]) => {
                  const formatted = formatHelplineNumber(service, number);
                  return (
                    <div key={service} className="helpline-item">
                      <div className="helpline-service">{formatted.service}</div>
                      <div className="helpline-number">{formatted.number}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}


    </div>
  );
};

export default VoiceToText;