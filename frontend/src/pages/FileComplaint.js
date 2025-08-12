import React, { useState, useRef } from 'react';
import { complaintAPI, aiAPI } from '../services/api';
import './FileComplaint.css';

const FileComplaint = ({ user }) => {
  const [formData, setFormData] = useState({
    address: {
      houseNo: '',
      addressLine1: '',
      addressLine2: '',
      pinCode: ''
    },
    issueDescription: '',
    category: '',
    categoryOther: '',
    region: '',
    regionOther: ''
  });
  
  const [voiceInput, setVoiceInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [voiceLanguage, setVoiceLanguage] = useState(() => {
    // Auto-detect language based on browser settings
    const browserLang = navigator.language || navigator.userLanguage;
    if (browserLang.startsWith('hi')) return 'hi-IN';
    if (browserLang.startsWith('en')) return 'en-IN';
    if (browserLang.startsWith('gu')) return 'gu-IN';
    if (browserLang.startsWith('bn')) return 'bn-IN';
    if (browserLang.startsWith('ta')) return 'ta-IN';
    if (browserLang.startsWith('te')) return 'te-IN';
    if (browserLang.startsWith('mr')) return 'mr-IN';
    if (browserLang.startsWith('pa')) return 'pa-IN';
    if (browserLang.startsWith('kn')) return 'kn-IN';
    return 'hi-IN'; // Default to Hindi
  });
  const [selectedImages, setSelectedImages] = useState([]);
  const [aiDraft, setAiDraft] = useState(null);
  const [isGeneratingDraft, setIsGeneratingDraft] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reviewConfirmed, setReviewConfirmed] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState('');
  const [isEditingDraft, setIsEditingDraft] = useState(false);
  const [editedDraft, setEditedDraft] = useState('');
  const [editedAuthorityEmail, setEditedAuthorityEmail] = useState('');

  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);

  // Check browser compatibility
  const isSpeechRecognitionSupported = () => {
    return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  };

  // Initialize speech recognition
  const initializeSpeechRecognition = () => {
    if (!recognitionRef.current) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      console.log('Speech Recognition available:', !!SpeechRecognition);
      
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        
        // Set language based on user selection
        const languageCode = voiceLanguage === 'hi-IN-haryanvi' ? 'hi-IN' : voiceLanguage;
        recognitionRef.current.lang = languageCode;
        console.log('Setting language to:', languageCode);
        
        recognitionRef.current.onresult = (event) => {
          console.log('Speech recognition result:', event);
          let finalTranscript = '';
          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            }
          }
          if (finalTranscript) {
            console.log('Final transcript:', finalTranscript);
            setVoiceInput(finalTranscript);
            setFormData(prev => ({
              ...prev,
              issueDescription: prev.issueDescription + ' ' + finalTranscript
            }));
          }
        };

        recognitionRef.current.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setError(`Voice recognition failed: ${event.error}. Please try again.`);
          setIsRecording(false);
        };

        recognitionRef.current.onend = () => {
          console.log('Speech recognition ended');
          setIsRecording(false);
        };

        recognitionRef.current.onstart = () => {
          console.log('Speech recognition started');
        };
      } else {
        console.log('Speech recognition not supported');
        setError('Speech recognition is not supported in this browser.');
      }
    } else {
      // Update language if recognition already exists
      const languageCode = voiceLanguage === 'hi-IN-haryanvi' ? 'hi-IN' : voiceLanguage;
      recognitionRef.current.lang = languageCode;
      console.log('Updated language to:', languageCode);
    }
  };

  const categories = [
    'Sanitation',
    'Water',
    'Electricity',
    'Roads',
    'Street Lights',
    'Sewage',
    'Garbage',
    'Traffic',
    'Other'
  ];

  const regions = [
    'Maharashtra',
    'Uttar Pradesh',
    'Delhi',
    'Karnataka',
    'Tamil Nadu',
    'Gujarat',
    'West Bengal',
    'Andhra Pradesh',
    'Telangana',
    'Kerala',
    'Other'
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleVoiceRecording = async () => {
    if (isRecording) {
      // Stop recording
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
    } else {
      // Start recording
      try {
        // Check microphone permission first
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
          } catch (permissionError) {
            setError('Microphone permission denied. Please allow microphone access and try again.');
            return;
          }
        }

        initializeSpeechRecognition();
        if (recognitionRef.current) {
          // Clear any previous error
          setError('');
          setVoiceInput('');
          
          // Start recording
          recognitionRef.current.start();
          setIsRecording(true);
          console.log('Started voice recording with language:', voiceLanguage);
        } else {
          // Fallback to simulated transcription
          setError('Speech recognition not available. Using simulated transcription.');
          setIsRecording(true);
          setTimeout(async () => {
            try {
              const result = await aiAPI.transcribeAudio();
              setVoiceInput(result.text);
              setFormData(prev => ({
                ...prev,
                issueDescription: prev.issueDescription + ' ' + result.text
              }));
            } catch (error) {
              setError('Voice transcription failed. Please try again.');
            } finally {
              setIsRecording(false);
            }
          }, 3000);
        }
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setError(`Failed to start voice recording: ${error.message}. Please try again.`);
        setIsRecording(false);
      }
    }
  };

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    const newImages = files.map(file => ({
      file,
      preview: URL.createObjectURL(file),
      analysis: null
    }));
    setSelectedImages(prev => [...prev, ...newImages]);
    
    // Simulate image analysis
    files.forEach((file, index) => {
      setTimeout(async () => {
        try {
          const analysis = await aiAPI.analyzeImage(file);
          setSelectedImages(prev => 
            prev.map((img, i) => 
              i === prev.length - files.length + index 
                ? { ...img, analysis }
                : img
            )
          );
        } catch (error) {
          console.error('Image analysis failed:', error);
        }
      }, 1000 + index * 500);
    });
  };

  const removeImage = (index) => {
    setSelectedImages(prev => {
      const newImages = prev.filter((_, i) => i !== index);
      return newImages;
    });
  };

  const generateDraft = async () => {
    if (!formData.category || !formData.issueDescription) {
      setError('Please fill in category and issue description first.');
      return;
    }

    setIsGeneratingDraft(true);
    setError('');

    try {
      const draft = await aiAPI.generateComplaintDraft({
        userInfo: user,
        address: formData.address,
        issueDescription: formData.issueDescription,
        category: formData.category,
        region: formData.region
      });
      setAiDraft(draft);
      setEditedDraft(draft.draft);
      setEditedAuthorityEmail(draft.authority.email);
      setIsEditingDraft(false);
    } catch (error) {
      setError('Failed to generate complaint draft. Please try again.');
    } finally {
      setIsGeneratingDraft(false);
    }
  };

  const handleEditDraft = () => {
    setIsEditingDraft(true);
    setEditedDraft(aiDraft.draft);
    setEditedAuthorityEmail(aiDraft.authority.email);
  };

  const handleSaveDraft = () => {
    setAiDraft(prev => ({
      ...prev,
      draft: editedDraft,
      authority: {
        ...prev.authority,
        email: editedAuthorityEmail
      }
    }));
    setIsEditingDraft(false);
  };

  const handleCancelEdit = () => {
    setIsEditingDraft(false);
    setEditedDraft(aiDraft.draft);
    setEditedAuthorityEmail(aiDraft.authority.email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!reviewConfirmed) {
      setError('Please review and confirm the complaint details.');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const complaintData = {
        userId: user.id,
        userInfo: user,
        ...formData
      };
      
      // Add AI draft if available
      if (aiDraft) {
        complaintData.aiDraft = aiDraft;
      }
      
      // Add edited authority email if draft was edited and email was changed
      console.log('DEBUG: aiDraft exists:', !!aiDraft);
      console.log('DEBUG: editedAuthorityEmail:', editedAuthorityEmail);
      console.log('DEBUG: aiDraft.authority.email:', aiDraft?.authority?.email);
      
      // Use the current aiDraft authority email (which gets updated when saved)
      const currentAuthorityEmail = aiDraft?.authority?.email;
      console.log('DEBUG: currentAuthorityEmail:', currentAuthorityEmail);
      console.log('DEBUG: emails are different:', editedAuthorityEmail !== currentAuthorityEmail);
      
      // Check if the current email is different from the auto-generated one
      const autoGeneratedEmail = `${formData.category.toLowerCase().replace(' ', '.')}@examplecity.gov.in`;
      console.log('DEBUG: autoGeneratedEmail:', autoGeneratedEmail);
      
      if (aiDraft && currentAuthorityEmail && currentAuthorityEmail !== autoGeneratedEmail) {
        complaintData.editedAuthorityEmail = currentAuthorityEmail;
        console.log('✅ Sending edited authority email:', currentAuthorityEmail);
      } else {
        console.log('❌ NOT sending edited authority email. Using default.');
      }
      
      console.log('DEBUG: Final complaintData being sent:', complaintData);
      const response = await complaintAPI.fileComplaint(complaintData);
      setSuccess(response);
      // Reset form
      setFormData({
        address: { houseNo: '', addressLine1: '', addressLine2: '', pinCode: '' },
        issueDescription: '',
        category: '',
        region: ''
      });
      setVoiceInput('');
      setSelectedImages([]);
      setAiDraft(null);
      setReviewConfirmed(false);
    } catch (error) {
      setError(error.message || 'Failed to submit complaint. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">File a Complaint</h1>
        <p className="page-subtitle">Report civic issues with AI-powered assistance</p>
      </div>

      {success && (
        <div className="alert alert-success">
          <h3>Complaint Submitted Successfully!</h3>
          <p>Your tracking ID is: <strong>{success.trackingId}</strong></p>
          
          {success.emailStatus && (
            <div className="email-status">
              <h4>Email Status:</h4>
              <div className="email-status-item">
                <strong>Authority Email:</strong> 
                {success.emailStatus.authority.success ? 
                  <span className="success">✅ Sent to {success.complaint.authority.email}</span> : 
                  <span className="error">❌ Failed: {success.emailStatus.authority.message}</span>
                }
              </div>
              <div className="email-status-item">
                <strong>Confirmation Email:</strong> 
                {success.emailStatus.user.success ? 
                  <span className="success">✅ Sent to {user.email}</span> : 
                  <span className="error">❌ Failed: {success.emailStatus.user.message}</span>
                }
              </div>
            </div>
          )}
          
          <button 
            className="btn btn-secondary"
            onClick={() => setSuccess(null)}
          >
            File Another Complaint
          </button>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="complaint-form-container animate-fade-in">
        <form onSubmit={handleSubmit} className="complaint-form animate-slide-in-left">
          {/* Address Section */}
          <div className="form-section">
            <h3 className="section-title">Address Details</h3>
            <div className="address-grid">
              <div className="form-group">
                <label htmlFor="houseNo" className="form-label">House No.</label>
                <input
                  type="text"
                  id="houseNo"
                  name="address.houseNo"
                  value={formData.address.houseNo}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Enter house number"
                />
              </div>
              <div className="form-group">
                <label htmlFor="addressLine1" className="form-label">Address Line 1</label>
                <input
                  type="text"
                  id="addressLine1"
                  name="address.addressLine1"
                  value={formData.address.addressLine1}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Street address"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="addressLine2" className="form-label">Address Line 2</label>
                <input
                  type="text"
                  id="addressLine2"
                  name="address.addressLine2"
                  value={formData.address.addressLine2}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Landmark or area"
                />
              </div>
              <div className="form-group">
                <label htmlFor="pinCode" className="form-label">PIN Code</label>
                <input
                  type="text"
                  id="pinCode"
                  name="address.pinCode"
                  value={formData.address.pinCode}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="6-digit PIN code"
                  required
                />
              </div>
            </div>
          </div>

          {/* Issue Description Section */}
          <div className="form-section">
            <h3 className="section-title">Issue Description</h3>
            <div className="form-group">
              <label htmlFor="issueDescription" className="form-label">
                Describe the issue (Text)
              </label>
              <textarea
                id="issueDescription"
                name="issueDescription"
                value={formData.issueDescription}
                onChange={handleInputChange}
                className="form-input"
                rows="4"
                placeholder="Describe the civic issue in detail..."
                required
              />
            </div>

            {/* Voice Input */}
            <div className="voice-input-section">
              <label className="form-label">Voice Input</label>
              <div className="voice-controls">
                <div className="voice-language-selector">
                  <label htmlFor="voiceLanguage" className="form-label">Language:</label>
                                     <select
                     id="voiceLanguage"
                     value={voiceLanguage}
                     onChange={(e) => setVoiceLanguage(e.target.value)}
                     className="form-select"
                     disabled={isRecording}
                   >
                     <option value="hi-IN">Hindi (हिंदी)</option>
                     <option value="en-IN">English (India)</option>
                     <option value="en-US">English (US)</option>
                     <option value="gu-IN">Gujarati (ગુજરાતી)</option>
                     <option value="bn-IN">Bengali (বাংলা)</option>
                     <option value="ta-IN">Tamil (தமிழ்)</option>
                     <option value="te-IN">Telugu (తెలుగు)</option>
                     <option value="mr-IN">Marathi (मराठी)</option>
                     <option value="pa-IN">Punjabi (ਪੰਜਾਬੀ)</option>
                     <option value="kn-IN">Kannada (ಕನ್ನಡ)</option>
                     <option value="hi-IN-haryanvi">Haryanvi (हरियाणवी)</option>
                   </select>
                </div>
                <button
                  type="button"
                  className={`btn ${isRecording ? 'btn-danger' : 'btn-secondary'}`}
                  onClick={handleVoiceRecording}
                >
                  {isRecording ? '🛑 Stop Recording' : '🎤 Start Recording'}
                </button>
                                 {isRecording && (
                   <div className="recording-indicator">
                     <span className="recording-dot"></span>
                     Recording... Speak clearly in {voiceLanguage === 'hi-IN' ? 'Hindi' : 
                       voiceLanguage === 'en-IN' || voiceLanguage === 'en-US' ? 'English' :
                       voiceLanguage === 'gu-IN' ? 'Gujarati' :
                       voiceLanguage === 'bn-IN' ? 'Bengali' :
                       voiceLanguage === 'ta-IN' ? 'Tamil' :
                       voiceLanguage === 'te-IN' ? 'Telugu' :
                       voiceLanguage === 'mr-IN' ? 'Marathi' :
                       voiceLanguage === 'pa-IN' ? 'Punjabi' :
                       voiceLanguage === 'kn-IN' ? 'Kannada' :
                       voiceLanguage === 'hi-IN-haryanvi' ? 'Haryanvi' : 'Hindi'}
                   </div>
                 )}
                {voiceInput && (
                  <div className="voice-transcription">
                    <div className="transcription-header">
                      <strong>Transcribed:</strong>
                      <button
                        type="button"
                        className="clear-transcription-btn"
                        onClick={() => {
                          setVoiceInput('');
                          setFormData(prev => ({
                            ...prev,
                            issueDescription: prev.issueDescription.replace(voiceInput, '').trim()
                          }));
                        }}
                      >
                        ✕ Clear
                      </button>
                    </div>
                    <div className="transcription-text">{voiceInput}</div>
                  </div>
                )}
                                 <div className="voice-instructions">
                   <small>💡 Tip: Speak clearly in your selected language for better recognition</small>
                   <br />
                   <small>🌐 Browser Support: {isSpeechRecognitionSupported() ? '✅ Supported' : '❌ Not Supported'} - Chrome, Edge, Safari (HTTPS required)</small>
                 </div>
              </div>
            </div>

            {/* Image Upload */}
            <div className="image-upload-section">
              <label className="form-label">Upload Images</label>
              <div className="image-upload-controls">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => fileInputRef.current.click()}
                >
                  📷 Upload Images
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{ display: 'none' }}
                />
              </div>
              
              {selectedImages.length > 0 && (
                <div className="image-preview-grid">
                  {selectedImages.map((image, index) => (
                    <div key={index} className="image-preview-card">
                      <img 
                        src={image.preview} 
                        alt={`Upload ${index + 1}`}
                        className="image-preview"
                      />
                      <button
                        type="button"
                        className="remove-image-btn"
                        onClick={() => removeImage(index)}
                      >
                        ✕
                      </button>
                      {image.analysis && (
                        <div className="image-analysis">
                          <strong>AI Analysis:</strong> {image.analysis.description}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Category and Region */}
          <div className="form-section">
            <h3 className="section-title">Additional Details</h3>
            <div className="details-grid">
              <div className="form-group">
                <label htmlFor="category" className="form-label">Issue Category</label>
                <select
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select category</option>
                  {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
                {formData.category === 'Other' && (
                  <input
                    type="text"
                    name="categoryOther"
                    value={formData.categoryOther}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Please specify the issue category"
                    required
                    style={{ marginTop: '0.5rem' }}
                  />
                )}
              </div>
              <div className="form-group">
                <label htmlFor="region" className="form-label">State/Region</label>
                <select
                  id="region"
                  name="region"
                  value={formData.region}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select state</option>
                  {regions.map(region => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </select>
                {formData.region === 'Other' && (
                  <input
                    type="text"
                    name="regionOther"
                    value={formData.regionOther}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Please specify your state/region"
                    required
                    style={{ marginTop: '0.5rem' }}
                  />
                )}
              </div>
            </div>
          </div>

          {/* AI Draft Generation */}
          <div className="form-section">
            <h3 className="section-title">AI-Powered Draft</h3>
            <button
              type="button"
              className={`btn btn-primary ${isGeneratingDraft ? 'loading' : ''}`}
              onClick={generateDraft}
              disabled={isGeneratingDraft || !formData.category || !formData.issueDescription}
            >
              {isGeneratingDraft ? 'Generating Draft...' : 'Generate AI Draft'}
            </button>

            {aiDraft && (
              <div className="ai-draft-section">
                <div className="draft-header">
                  <h4>Generated Complaint Draft:</h4>
                  <div className="draft-actions">
                    {!isEditingDraft ? (
                      <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleEditDraft}
                      >
                        ✏️ Edit Draft
                      </button>
                    ) : (
                      <div className="edit-actions">
                        <button
                          type="button"
                          className="btn btn-success"
                          onClick={handleSaveDraft}
                        >
                          💾 Save Changes
                        </button>
                        <button
                          type="button"
                          className="btn btn-secondary"
                          onClick={handleCancelEdit}
                        >
                          ❌ Cancel
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {!isEditingDraft ? (
                  <div className="draft-preview">
                    <pre className="draft-content">{aiDraft.draft}</pre>
                  </div>
                ) : (
                  <div className="draft-edit">
                    <div className="form-group">
                      <label htmlFor="editedDraft" className="form-label">Edit Complaint Draft:</label>
                      <textarea
                        id="editedDraft"
                        value={editedDraft}
                        onChange={(e) => setEditedDraft(e.target.value)}
                        className="form-input"
                        rows="8"
                        placeholder="Edit the complaint draft..."
                      />
                    </div>
                  </div>
                )}

                <div className="authority-info">
                  <h4>Concerned Authority:</h4>
                  <p><strong>Name:</strong> {aiDraft.authority.name}</p>
                  {!isEditingDraft ? (
                    <p><strong>Email:</strong> {aiDraft.authority.email}</p>
                  ) : (
                    <div className="form-group">
                      <label htmlFor="editedAuthorityEmail" className="form-label">Authority Email:</label>
                      <input
                        type="email"
                        id="editedAuthorityEmail"
                        value={editedAuthorityEmail}
                        onChange={(e) => setEditedAuthorityEmail(e.target.value)}
                        className="form-input"
                        placeholder="Enter authority email"
                      />
                    </div>
                  )}
                  <p><strong>Phone:</strong> {aiDraft.authority.phone}</p>
                </div>
              </div>
            )}
          </div>

          {/* Review and Submit */}
          <div className="form-section">
            <h3 className="section-title">Review & Submit</h3>
            <div className="review-checkbox">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={reviewConfirmed}
                  onChange={(e) => setReviewConfirmed(e.target.checked)}
                  className="checkbox-input"
                />
                <span className="checkbox-text">
                  I have reviewed the complaint and confirm the details are correct
                </span>
              </label>
            </div>

            <button
              type="submit"
              className={`btn btn-success w-full ${isSubmitting ? 'loading' : ''}`}
              disabled={isSubmitting || !reviewConfirmed}
            >
              {isSubmitting ? 'Submitting Complaint...' : 'Submit Complaint'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FileComplaint; 