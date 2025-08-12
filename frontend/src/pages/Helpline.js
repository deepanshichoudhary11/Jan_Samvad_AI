import React, { useState } from 'react';
import { helplineAPI } from '../services/api';
import VoiceHelpline from '../components/VoiceHelpline';
import './Helpline.css';

const Helpline = ({ user }) => {
  const [selectedState, setSelectedState] = useState('');
  const [selectedIssue, setSelectedIssue] = useState('');
  const [helplineData, setHelplineData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const states = [
    'Maharashtra',
    'Uttar Pradesh',
    'Delhi',
    'Karnataka',
    'Tamil Nadu',
    'Gujarat',
    'West Bengal',
    'Andhra Pradesh',
    'Telangana',
    'Kerala'
  ];

  const issues = [
    'Women Help',
    'Child Help',
    'Transport',
    'Water',
    'Electricity',
    'Health'
  ];

  const handleStateChange = async (e) => {
    const state = e.target.value;
    setSelectedState(state);
    
    if (state) {
      setLoading(true);
      setError('');
      
      try {
        const response = await helplineAPI.getHelplineNumbers(state);
        setHelplineData(response);
      } catch (error) {
        setError(error.message || 'Failed to fetch helpline numbers. Please try again.');
      } finally {
        setLoading(false);
      }
    } else {
      setHelplineData(null);
    }
  };

  const handleIssueChange = (e) => {
    setSelectedIssue(e.target.value);
  };

  const filterHelplinesByIssue = (helplines) => {
    if (!selectedIssue) return helplines;
    
    const issueKeywords = {
      'Women Help': ['women', 'woman', 'female', 'domestic', 'harassment', 'violence'],
      'Child Help': ['child', 'children', 'childline', 'minor', 'protection'],
      'Transport': ['transport', 'bus', 'rail', 'railway', 'road', 'upsrtc'],
      'Water': ['water', 'supply', 'phed', 'drinking'],
      'Electricity': ['electricity', 'power', 'msedcl', 'uhbvn', 'pspcl', 'uppcl'],
      'Health': ['health', 'medical', 'hospital', 'ambulance', 'covid', 'vaccination', 'mental']
    };

    const keywords = issueKeywords[selectedIssue] || [];
    return helplines.filter(helpline => {
      const serviceText = helpline.service.toLowerCase();
      const notesText = (helpline.notes || '').toLowerCase();
      return keywords.some(keyword => 
        serviceText.includes(keyword) || notesText.includes(keyword)
      );
    });
  };

  const getHelplineIcon = (service) => {
    const icons = {
      'Emergency Response Support System (ERSS)': '🚨',
      'National Women Helpline': '👩',
      'Childline India': '👶',
      'National Health Helpline': '🏥',
      'National Senior Citizen Helpline (Elder Line)': '👴',
      'KIRAN Mental Health Rehabilitation Helpline': '🧠',
      'National Cyber Crime Reporting Portal': '💻',
      'National Consumer Helpline': '🛒',
      'Kisan Call Centre (for Farmers)': '🌾',
      'CPGRAMS': '📋',
      'Rail Madad': '🚂',
      'Ayushman Bharat (PMJAY)': '🏥',
      'E-SHRAM Portal': '👷',
      'UP CM Helpline (Jansunwai - Samadhan)': '🏛️',
      'Women and Child Power Line (UP Police)': '👮',
      'UP Power Corporation Ltd. (Electricity)': '⚡',
      'UP State Road Transport Corporation (UPSRTC)': '🚌',
      'CM Window (Jan Sahayak)': '🏛️',
      'Electricity (UHBVN)': '⚡',
      'Police / Emergency': '👮',
      'Women Helpline': '👩',
      'Ration / Food Distribution': '🍞',
      'Electricity (MSEDCL)': '⚡',
      'Ration / Food Supply': '🍞',
      'Electricity (PSPCL)': '⚡',
      'Rajasthan Sampark': '🏛️',
      'Water Supply (PHED)': '💧',
      'Women/Child Protection': '👩‍👧‍👦',
      'Emergency': '🚨',
      'Police': '👮',
      'Fire': '🚒',
      'Ambulance': '🚑',
      'Child Helpline': '👶',
      'Highway Assistance': '🛣️',
      'Tourist Helpline': '🏛️',
      'Railway Helpline': '🚂'
    };
    return icons[service] || '📞';
  };



  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Helpline Numbers</h1>
        <p className="page-subtitle">Emergency contact information by state</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="helpline-container">
        {/* Voice Emergency Helpline */}
        <VoiceHelpline 
          onHelplineResult={(result) => {
            console.log('Voice emergency result:', result);
            // Optionally auto-select state based on detection
            if (result.detectedState && result.detectedState !== 'All India') {
              setSelectedState(result.detectedState);
              handleStateChange({ target: { value: result.detectedState } });
            }
          }}
        />

        {/* State and Issue Selection */}
        <div className="selection-section">
          <h2 className="section-title">Select Your State and Issue</h2>
          <div className="selection-grid">
            <div className="state-selector">
              <label htmlFor="state-select">State:</label>
              <select
                id="state-select"
                value={selectedState}
                onChange={handleStateChange}
                className="form-select"
              >
                <option value="">Choose your state</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </div>
            
            <div className="issue-selector">
              <label htmlFor="issue-select">Issue Type:</label>
              <select
                id="issue-select"
                value={selectedIssue}
                onChange={handleIssueChange}
                className="form-select"
              >
                <option value="">All Issues</option>
                {issues.map(issue => (
                  <option key={issue} value={issue}>{issue}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Helpline Numbers */}
        {loading && (
          <div className="loading-state">
            <p>Loading helpline numbers...</p>
          </div>
        )}

        {helplineData && !loading && (
          <div className="helpline-results">
            <h2 className="section-title">
              Helpline Numbers for {selectedState}
            </h2>

            {/* Central Helplines */}
            <div className="helpline-section">
              <h3 className="subsection-title">
                National Helplines
                {selectedIssue && ` - ${selectedIssue}`}
              </h3>
              <div className="helpline-grid">
                {filterHelplinesByIssue(helplineData.helplines.filter(helpline => helpline.level === 'Central')).map((helpline, index) => (
                  <div key={index} className="helpline-card national">
                    <div className="helpline-icon">
                      {getHelplineIcon(helpline.service)}
                    </div>
                    <div className="helpline-info">
                      <h4 className="helpline-category">{helpline.service}</h4>
                      <p className="helpline-number">{helpline.number}</p>
                      {helpline.notes && (
                        <p className="helpline-notes">{helpline.notes}</p>
                      )}
                      <div className="helpline-links">
                        {helpline.website && (
                          <a 
                            href={helpline.website} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="helpline-link"
                          >
                            🌐 Website
                          </a>
                        )}
                        {helpline.email && (
                          <a 
                            href={`mailto:${helpline.email}`}
                            className="helpline-link"
                          >
                            📧 Email
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* State-Specific Helplines */}
            <div className="helpline-section">
              <h3 className="subsection-title">
                State-Specific Helplines
                {selectedIssue && ` - ${selectedIssue}`}
              </h3>
              <div className="helpline-grid">
                {filterHelplinesByIssue(helplineData.helplines.filter(helpline => helpline.level === 'State' && helpline.state === selectedState)).map((helpline, index) => (
                  <div key={index} className="helpline-card state">
                    <div className="helpline-icon">
                      {getHelplineIcon(helpline.service)}
                    </div>
                    <div className="helpline-info">
                      <h4 className="helpline-category">{helpline.service}</h4>
                      <p className="helpline-number">{helpline.number}</p>
                      {helpline.notes && (
                        <p className="helpline-notes">{helpline.notes}</p>
                      )}
                      <div className="helpline-links">
                        {helpline.website && (
                          <a 
                            href={helpline.website} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="helpline-link"
                          >
                            🌐 Website
                          </a>
                        )}
                        {helpline.email && (
                          <a 
                            href={`mailto:${helpline.email}`}
                            className="helpline-link"
                          >
                            📧 Email
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Emergency Tips */}
            <div className="emergency-tips">
              <h3 className="subsection-title">Emergency Tips</h3>
              <div className="tips-grid">
                <div className="tip-card">
                  <div className="tip-icon">📞</div>
                  <h4>Call 112</h4>
                  <p>For any emergency situation, dial 112 for immediate assistance.</p>
                </div>
                <div className="tip-card">
                  <div className="tip-icon">🚨</div>
                  <h4>Stay Calm</h4>
                  <p>Remain calm and provide clear information when calling emergency services.</p>
                </div>
                <div className="tip-card">
                  <div className="tip-icon">📍</div>
                  <h4>Location Details</h4>
                  <p>Always provide your exact location and landmarks when reporting emergencies.</p>
                </div>
                <div className="tip-card">
                  <div className="tip-icon">📱</div>
                  <h4>Save Numbers</h4>
                  <p>Save important emergency numbers in your phone for quick access.</p>
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="disclaimer-section">
              <h3 className="subsection-title">Important Notice</h3>
              <div className="disclaimer-content">
                <p><strong>Disclaimer:</strong> Helpline numbers and web links are subject to change. For the most critical emergencies, please dial <strong>112</strong>. Most helplines listed are toll-free, but please check with your service provider.</p>
                <p>This information is provided for public service and should be used responsibly. Always verify the current status of helpline numbers before use.</p>
              </div>
            </div>
          </div>
        )}

        {!selectedState && !loading && (
          <div className="empty-state">
            <div className="empty-icon">📞</div>
            <h3 className="empty-title">Select a State</h3>
            <p className="empty-text">
              Choose your state and issue type from the dropdowns above to view relevant helpline numbers.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Helpline; 