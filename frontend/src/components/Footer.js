import React, { useState } from 'react';
import { complaintAPI } from '../services/api';
import './Footer.css';

const Footer = () => {
  const [feedback, setFeedback] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleFeedbackChange = (e) => {
    const { name, value } = e.target;
    setFeedback(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState('');

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('');

    try {
      const response = await complaintAPI.submitFeedback(feedback);
      
      if (response.emailStatus && response.emailStatus.success) {
        setSubmitStatus('success');
        setFeedback({ name: '', email: '', message: '' });
      } else {
        setSubmitStatus('error');
      }
    } catch (error) {
      console.error('Feedback submission error:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const authors = [
    {
      name: 'Deepanshi Choudhary',
      email: 'iec2022013@iiita.ac.in',
      phone: '+91-7906853153'
    },
    {
      name: 'Dimple Bhondekar',
      email: 'iit2022022@iiita.ac.in',
      phone: '+91-7972920270'
    },
    {
      name: 'Poonam Gate',
      email: 'iec2022087@iiita.ac.in',
      phone: '+91-8824699335'
    }
  ];

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          {/* Authors Section */}
          <div className="footer-section">
            <h3 className="footer-title">Authors</h3>
            <div className="authors-list">
              {authors.map((author, index) => (
                <div key={index} className="author-card">
                  <h4 className="author-name">{author.name}</h4>
                  <div className="author-contact">
                    <p className="author-email">
                      <span className="contact-icon">📧</span>
                      {author.email}
                    </p>
                    <p className="author-phone">
                      <span className="contact-icon">📞</span>
                      {author.phone}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Form */}
          <div className="footer-section">
            <h3 className="footer-title">Get in Touch</h3>
            <form className="feedback-form" onSubmit={handleFeedbackSubmit}>
              <div className="form-group">
                <label htmlFor="name" className="form-label">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={feedback.name}
                  onChange={handleFeedbackChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={feedback.email}
                  onChange={handleFeedbackChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="message" className="form-label">Message</label>
                <textarea
                  id="message"
                  name="message"
                  value={feedback.message}
                  onChange={handleFeedbackChange}
                  className="form-input"
                  rows="4"
                  required
                />
              </div>
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Sending...' : 'Send Feedback'}
              </button>
              
              {submitStatus === 'success' && (
                <div className="feedback-success">
                  ✅ Thank you for your feedback! We will get back to you soon.
                </div>
              )}
              
              {submitStatus === 'error' && (
                <div className="feedback-error">
                  ❌ Failed to send feedback. Please try again.
                </div>
              )}
            </form>
          </div>

          {/* Contact Information */}
          <div className="footer-section">
            <h3 className="footer-title">Contact Information</h3>
            <div className="contact-info">
              <div className="contact-item">
                <span className="contact-icon">📧</span>
                <div className="contact-details">
                  <h4>General Inquiries</h4>
                  <p>contact@janai.example.com</p>
                </div>
              </div>
              <div className="contact-item">
                <span className="contact-icon">🌐</span>
                <div className="contact-details">
                  <h4>Website</h4>
                  <p>www.janai.example.com</p>
                </div>
              </div>
                             <div className="contact-item">
                 <span className="contact-icon">📍</span>
                 <div className="contact-details">
                   <h4>Address</h4>
                   <p>IIITA, Prayagraj, Uttar Pradesh, India</p>
                 </div>
               </div>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="footer-bottom">
          <p className="copyright">
            © 2024 JanAI - India's Hyperlocal Civic Agent. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 