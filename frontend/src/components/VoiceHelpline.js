import React, { useState, useEffect, useCallback } from 'react';
import './VoiceHelpline.css';

const VoiceHelpline = ({ onHelplineResult }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [voiceText, setVoiceText] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [detectedState, setDetectedState] = useState('');
  const [emergencyType, setEmergencyType] = useState('');
  const [helplineNumbers, setHelplineNumbers] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');

  // Supported Indian languages
  const supportedLanguages = [
    { code: 'hi-IN', name: 'हिंदी (Hindi)', region: 'North India' },
    { code: 'en-IN', name: 'English (India)', region: 'All India' },
    { code: 'ta-IN', name: 'தமிழ் (Tamil)', region: 'Tamil Nadu' },
    { code: 'te-IN', name: 'తెలుగు (Telugu)', region: 'Andhra Pradesh/Telangana' },
    { code: 'mr-IN', name: 'मराठी (Marathi)', region: 'Maharashtra' },
    { code: 'gu-IN', name: 'ગુજરાતી (Gujarati)', region: 'Gujarat' },
    { code: 'bn-IN', name: 'বাংলা (Bengali)', region: 'West Bengal' },
    { code: 'kn-IN', name: 'ಕನ್ನಡ (Kannada)', region: 'Karnataka' },
    { code: 'ml-IN', name: 'മലയാളം (Malayalam)', region: 'Kerala' },
    { code: 'pa-IN', name: 'ਪੰਜਾਬੀ (Punjabi)', region: 'Punjab' },
    { code: 'ur-IN', name: 'اردو (Urdu)', region: 'Delhi/UP' },
    { code: 'or-IN', name: 'ଓଡ଼ିଆ (Odia)', region: 'Odisha' }
  ];

  const processVoiceInput = useCallback(async (text) => {
    if (!text.trim()) {
      setError('No text detected. Please try speaking again.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      // Call the backend API to process the voice input
      const response = await fetch('http://localhost:5000/api/emergency/process-emergency', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          inputLanguage: selectedLanguage
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to process voice input');
      }

      const data = await response.json();
      
      if (data.success) {
        setDetectedLanguage(data.detectedLanguage);
        setDetectedState(data.detectedState);
        setEmergencyType(data.emergencyType);
        setHelplineNumbers(data.helplineNumbers);

        // Show fallback message if AI was unavailable
        if (data.note) {
          console.log('Fallback mode:', data.note);
        }

        // Call parent callback if provided
        if (onHelplineResult) {
          onHelplineResult({
            originalText: text,
            detectedLanguage: data.detectedLanguage,
            detectedState: data.detectedState,
            emergencyType: data.emergencyType,
            helplineNumbers: data.helplineNumbers,
            translatedResponse: data.translatedResponse,
            fallbackMode: !!data.note
          });
        }
      } else {
        setError(data.message || 'Failed to process voice input');
      }
    } catch (error) {
      console.error('Voice processing error:', error);
      setError('Failed to process voice input. Please check your internet connection and try again.');
    } finally {
      setIsProcessing(false);
    }
  }, [selectedLanguage, onHelplineResult]);

  // Initialize speech recognition
  const initializeSpeechRecognition = useCallback(() => {
    if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
      setError('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognitionInstance = new SpeechRecognition();
    
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;
    recognitionInstance.lang = selectedLanguage;
    recognitionInstance.maxAlternatives = 1;
    
    recognitionInstance.onstart = () => {
      setIsRecording(true);
      setError('');
      console.log('Speech recognition started');
    };

    recognitionInstance.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log('Voice transcript:', transcript);
      setVoiceText(transcript);
      processVoiceInput(transcript);
    };

    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setError(`Voice recognition error: ${event.error}. Please try again.`);
      setIsRecording(false);
    };

    recognitionInstance.onend = () => {
      setIsRecording(false);
      console.log('Speech recognition ended');
    };

    setRecognition(recognitionInstance);
  }, [selectedLanguage, processVoiceInput]);

  useEffect(() => {
    initializeSpeechRecognition();
  }, [initializeSpeechRecognition]);

  const startRecording = () => {
    if (!recognition) {
      setError('Speech recognition not initialized. Please refresh the page.');
      return;
    }

    setVoiceText('');
    setDetectedLanguage('');
    setDetectedState('');
    setEmergencyType('');
    setHelplineNumbers([]);
    setError('');

    try {
      recognition.start();
    } catch (error) {
      console.error('Failed to start recording:', error);
      setError('Failed to start recording. Please try again.');
    }
  };

  const stopRecording = () => {
    if (recognition && isRecording) {
      recognition.stop();
    }
  };

  const handleLanguageChange = (e) => {
    const newLanguage = e.target.value;
    setSelectedLanguage(newLanguage);
  };

  const getEmergencyIcon = (type) => {
    const icons = {
      'police': '👮‍♂️',
      'medical': '🚑',
      'fire': '🚒',
      'women': '👩‍⚕️',
      'child': '👶',
      'general': '🆘',
      'accident': '🚗',
      'disaster': '⚠️',
      'electricity': '⚡',
      'water': '💧',
      'transport': '🚌',
      'cyber': '💻'
    };
    return icons[type?.toLowerCase()] || '📞';
  };

  const formatHelplineNumber = (helpline) => {
    return (
      <div key={helpline.number} className="helpline-item">
        <div className="helpline-icon">
          {getEmergencyIcon(helpline.type)}
        </div>
        <div className="helpline-details">
          <div className="helpline-name">{helpline.name}</div>
          <div className="helpline-number">{helpline.number}</div>
          {helpline.description && (
            <div className="helpline-description">{helpline.description}</div>
          )}
        </div>
        <div className="helpline-availability">
          {helpline.availability || '24/7'}
        </div>
      </div>
    );
  };

  return (
    <div className="voice-helpline-container">
      <div className="voice-helpline-header">
        <h2>🎤 Voice Emergency Helpline</h2>
        <p>Speak in any Indian language to get emergency helpline numbers</p>
      </div>

      {/* Language Selection */}
      <div className="language-selection">
        <label htmlFor="language-select">Select your preferred language for voice input:</label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={handleLanguageChange}
          disabled={isRecording || isProcessing}
          className="language-selector"
        >
          {supportedLanguages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>

      {/* Voice Controls */}
      <div className="voice-controls">
        <button
          className={`voice-button ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
        >
          {isRecording ? (
            <>
              <span className="recording-pulse">🔴</span>
              Stop Recording
            </>
          ) : (
            <>
              <span className="microphone-icon">🎤</span>
              Start Voice Input
            </>
          )}
        </button>

        {isRecording && (
          <div className="recording-status">
            <span className="recording-indicator">Recording...</span>
            <p>Speak clearly about your emergency in {supportedLanguages.find(lang => lang.code === selectedLanguage)?.name}</p>
          </div>
        )}
      </div>

      {/* Processing Status */}
      {isProcessing && (
        <div className="processing-status">
          <div className="spinner"></div>
          <p>Processing your voice input and analyzing emergency type...</p>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      {/* Voice Input Display */}
      {voiceText && (
        <div className="voice-input-display">
          <h3>🗣️ Your Voice Input:</h3>
          <div className="voice-text">{voiceText}</div>
        </div>
      )}

      {/* Detection Results */}
      {(detectedLanguage || detectedState || emergencyType) && (
        <div className="detection-results">
          <h3>🔍 Detection Results:</h3>
          <div className="detection-grid">
            {detectedLanguage && (
              <div className="detection-item">
                <span className="detection-label">Language:</span>
                <span className="detection-value">{detectedLanguage}</span>
              </div>
            )}
            {detectedState && (
              <div className="detection-item">
                <span className="detection-label">State/Region:</span>
                <span className="detection-value">{detectedState}</span>
              </div>
            )}
            {emergencyType && (
              <div className="detection-item">
                <span className="detection-label">Emergency Type:</span>
                <span className="detection-value">{emergencyType}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Helpline Numbers */}
      {helplineNumbers.length > 0 && (
        <div className="helpline-results">
          <h3>📞 Emergency Helpline Numbers</h3>
          <div className="helpline-list">
            {helplineNumbers.map(formatHelplineNumber)}
          </div>
          
          <div className="emergency-instructions">
            <h4>🚨 Emergency Instructions:</h4>
            <ul>
              <li>Stay calm and speak clearly</li>
              <li>Provide your exact location</li>
              <li>Describe the emergency situation</li>
              <li>Follow the operator's instructions</li>
              <li>Keep the line open until help arrives</li>
            </ul>
          </div>
        </div>
      )}

      {/* Quick Emergency Numbers */}
      <div className="quick-emergency">
        <h4>🆘 Quick Emergency Numbers (All India):</h4>
        <div className="quick-numbers">
          <div className="quick-number">
            <span className="number">112</span>
            <span className="service">All Emergencies</span>
          </div>
          <div className="quick-number">
            <span className="number">100</span>
            <span className="service">Police</span>
          </div>
          <div className="quick-number">
            <span className="number">108</span>
            <span className="service">Ambulance</span>
          </div>
          <div className="quick-number">
            <span className="number">101</span>
            <span className="service">Fire</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceHelpline;