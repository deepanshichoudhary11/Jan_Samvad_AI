import React, { useState, useEffect } from 'react';
import { complaintAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [recentComplaints, setRecentComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecentComplaints = async () => {
      try {
        const response = await complaintAPI.getComplaintStatus(user.id);
        setRecentComplaints(response.complaints.slice(0, 3)); // Show only 3 most recent
      } catch (error) {
        console.error('Error fetching complaints:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecentComplaints();
  }, [user.id]);

  return (
    <div className="container animate-fade-in">
      <div className="page-header animate-slide-in-left">
        <h1 className="page-title">Welcome, {user.fullName}!</h1>
        <p className="page-subtitle">Empowering citizens through AI-driven civic engagement</p>
      </div>

      <div className="dashboard-content">
        {/* About Us Section */}
        <div className="content-section animate-slide-in-right">
          <h2 className="section-title">About JanAI</h2>
          <div className="about-grid">
            <div className="about-card hover-lift animate-scale-in">
              <div className="about-icon animate-float">🎯</div>
              <h3 className="about-title">Our Mission</h3>
              <p className="about-text">
                To bridge the gap between citizens and government authorities by providing 
                an AI-powered platform that makes civic issue reporting accessible, 
                transparent, and efficient for all Indians.
              </p>
            </div>
            <div className="about-card hover-lift animate-scale-in" style={{animationDelay: '0.1s'}}>
              <div className="about-icon animate-float">🤖</div>
              <h3 className="about-title">AI-Powered</h3>
              <p className="about-text">
                Leveraging cutting-edge AI technology including speech recognition, 
                image analysis, and natural language processing to make civic 
                engagement more accessible and effective.
              </p>
            </div>
            <div className="about-card hover-lift animate-scale-in" style={{animationDelay: '0.2s'}}>
              <div className="about-icon animate-float">🌍</div>
              <h3 className="about-title">Multilingual</h3>
              <p className="about-text">
                Supporting multiple Indian languages and regional dialects to ensure 
                that every citizen can participate in civic governance regardless 
                of their language preference.
              </p>
            </div>
          </div>
        </div>

        {/* Our Product Section */}
        <div className="content-section animate-slide-in-left">
          <h2 className="section-title">How JanAI Helps You</h2>
          <div className="features-grid">
            <div className="feature-card hover-lift animate-scale-in">
              <div className="feature-icon animate-float">📝</div>
              <h3 className="feature-title">File Complaints</h3>
              <p className="feature-text">
                Report civic issues using text, voice, or images. Our AI helps 
                translate and format your complaint for the appropriate authorities.
              </p>
            </div>
            <div className="feature-card hover-lift animate-scale-in" style={{animationDelay: '0.1s'}}>
              <div className="feature-icon animate-float">📊</div>
              <h3 className="feature-title">Track Progress</h3>
              <p className="feature-text">
                Monitor the status of your complaints in real-time and get 
                updates on resolution progress.
              </p>
            </div>
            <div className="feature-card hover-lift animate-scale-in" style={{animationDelay: '0.2s'}}>
              <div className="feature-icon animate-float">🎓</div>
              <h3 className="feature-title">Discover Schemes</h3>
              <p className="feature-text">
                Find relevant government schemes and scholarships based on your 
                demographics and requirements.
              </p>
            </div>
            <div className="feature-card hover-lift animate-scale-in" style={{animationDelay: '0.3s'}}>
              <div className="feature-icon animate-float">📞</div>
              <h3 className="feature-title">Emergency Contacts</h3>
              <p className="feature-text">
                Access important helpline numbers and emergency contacts 
                specific to your state and region.
              </p>
            </div>
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="content-section">
          <h2 className="section-title">Recent Activity</h2>
          <div className="activity-section">
            {loading ? (
              <div className="loading-state">
                <p>Loading your recent complaints...</p>
              </div>
            ) : recentComplaints.length > 0 ? (
              <div className="complaints-list">
                {recentComplaints.map((complaint) => (
                  <div key={complaint.id} className="complaint-card">
                    <div className="complaint-header">
                      <h4 className="complaint-category">{complaint.category}</h4>
                      <span className={`status-badge status-${complaint.status.toLowerCase()}`}>
                        {complaint.status}
                      </span>
                    </div>
                    <p className="complaint-description">{complaint.description}</p>
                    <div className="complaint-footer">
                      <span className="complaint-date">{complaint.date}</span>
                      <span className="complaint-id">{complaint.id}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">📝</div>
                <h3 className="empty-title">No complaints yet</h3>
                <p className="empty-text">
                  Start by filing your first complaint to track civic issues in your area.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 