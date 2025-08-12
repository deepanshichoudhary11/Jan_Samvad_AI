import React, { useState } from 'react';
import { schemesAPI } from '../services/api';
import './Schemes.css';

const Schemes = ({ user }) => {
  const [formData, setFormData] = useState({
    name: user.fullName,
    age: '',
    gender: '',
    occupation: '',
    occupationOther: '',
    degree: '',
    degreeOther: '',
    yearOfStudy: '',
    collegeName: '',
    annualIncome: ''
  });
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  const occupations = [
    'Student',
    'Farmer',
    'Business Owner',
    'Employee',
    'Self Employed',
    'Homemaker',
    'Retired',
    'Other'
  ];

  const degrees = [
    'B.Tech',
    'M.Tech',
    'B.Sc',
    'M.Sc',
    'B.Com',
    'M.Com',
    'B.A',
    'M.A',
    'MBBS',
    'BDS',
    'Other'
  ];

  const incomeRanges = [
    '< ₹1 Lakh',
    '₹1-5 Lakhs',
    '₹5-10 Lakhs',
    '₹10-25 Lakhs',
    '> ₹25 Lakhs'
  ];



  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await schemesAPI.findSchemes(formData);
      setSchemes(response.schemes);
      setHasSearched(true);
    } catch (error) {
      setError(error.message || 'Failed to find schemes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isStudent = formData.occupation === 'Student';

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Schemes & Scholarships</h1>
        <p className="page-subtitle">Discover relevant government schemes based on your profile</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="schemes-container">
        {/* Search Form */}
        <div className="search-form-section">
          <h2 className="section-title">Find Your Schemes</h2>
          <form onSubmit={handleSubmit} className="schemes-form">
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="name" className="form-label">Full Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="age" className="form-label">Age</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  className="form-input"
                  min="1"
                  max="120"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="gender" className="form-label">Gender</label>
                <select
                  id="gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

               <div className="form-group">
                 <label htmlFor="occupation" className="form-label">Occupation</label>
                 <select
                   id="occupation"
                   name="occupation"
                   value={formData.occupation}
                   onChange={handleInputChange}
                   className="form-select"
                   required
                 >
                   <option value="">Select occupation</option>
                   {occupations.map(occupation => (
                     <option key={occupation} value={occupation}>{occupation}</option>
                   ))}
                 </select>
                 {formData.occupation === 'Other' && (
                   <input
                     type="text"
                     name="occupationOther"
                     value={formData.occupationOther}
                     onChange={handleInputChange}
                     className="form-input"
                     placeholder="Please specify your occupation"
                     required
                     style={{ marginTop: '0.5rem' }}
                   />
                 )}
               </div>

              {/* Student-specific fields */}
              {isStudent && (
                <>
                  <div className="form-group">
                    <label htmlFor="degree" className="form-label">Degree</label>
                    <select
                      id="degree"
                      name="degree"
                      value={formData.degree}
                      onChange={handleInputChange}
                      className="form-select"
                      required
                    >
                      <option value="">Select degree</option>
                      {degrees.map(degree => (
                        <option key={degree} value={degree}>{degree}</option>
                      ))}
                    </select>
                    {formData.degree === 'Other' && (
                      <input
                        type="text"
                        name="degreeOther"
                        value={formData.degreeOther}
                        onChange={handleInputChange}
                        className="form-input"
                        placeholder="Please specify your degree"
                        required
                        style={{ marginTop: '0.5rem' }}
                      />
                    )}
                  </div>

                  <div className="form-group">
                    <label htmlFor="yearOfStudy" className="form-label">Year of Study</label>
                    <select
                      id="yearOfStudy"
                      name="yearOfStudy"
                      value={formData.yearOfStudy}
                      onChange={handleInputChange}
                      className="form-select"
                      required
                    >
                      <option value="">Select year</option>
                      <option value="1st Year">1st Year</option>
                      <option value="2nd Year">2nd Year</option>
                      <option value="3rd Year">3rd Year</option>
                      <option value="4th Year">4th Year</option>
                      <option value="Final Year">Final Year</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="collegeName" className="form-label">College Name</label>
                    <input
                      type="text"
                      id="collegeName"
                      name="collegeName"
                      value={formData.collegeName}
                      onChange={handleInputChange}
                      className="form-input"
                      placeholder="Enter your college name"
                      required
                    />
                  </div>
                </>
              )}

              {/* Non-student income field */}
              {!isStudent && (
                <div className="form-group">
                  <label htmlFor="annualIncome" className="form-label">Annual Income</label>
                  <select
                    id="annualIncome"
                    name="annualIncome"
                    value={formData.annualIncome}
                    onChange={handleInputChange}
                    className="form-select"
                    required
                  >
                    <option value="">Select income range</option>
                    {incomeRanges.map(income => (
                      <option key={income} value={income}>{income}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <button
              type="submit"
              className={`btn btn-primary ${loading ? 'loading' : ''}`}
              disabled={loading}
            >
              {loading ? 'Finding Schemes...' : 'Find Schemes'}
            </button>
          </form>
        </div>

        {/* Results Section */}
        {hasSearched && (
          <div className="results-section">
            <h2 className="section-title">
              {schemes.length > 0 
                ? `Found ${schemes.length} matching scheme(s)` 
                : 'No matching schemes found'
              }
            </h2>

            {schemes.length > 0 ? (
              <div className="schemes-grid">
                {schemes.map((scheme) => (
                  <div key={scheme.schemeName} className="scheme-card">
                                         <div className="scheme-header">
                       <h3 className="scheme-title">{scheme.schemeName}</h3>
                       <div className="scheme-badges">
                         <span className="scheme-category">{scheme.category}</span>
                         <span className={`scheme-level ${scheme.level === 'Central' ? 'central' : 'state'}`}>
                           {scheme.level}
                         </span>
                       </div>
                     </div>
                    
                    <div className="scheme-body">
                      <p className="scheme-description">{scheme.description}</p>
                      
                      <div className="scheme-details">
                        <h4>Scheme Details:</h4>
                        <ul>
                          <li><strong>Category:</strong> {scheme.category}</li>
                          <li><strong>Level:</strong> {scheme.level}</li>
                          {scheme.state && (
                            <li><strong>State:</strong> {scheme.state}</li>
                          )}
                        </ul>
                      </div>
                    </div>

                    <div className="scheme-footer">
                      {scheme.access && scheme.access.length > 0 && (
                        <div className="scheme-access">
                          <h4>How to Apply:</h4>
                          {scheme.access.map((access, index) => (
                            <div key={index} className="access-item">
                              <strong>{access.type}:</strong> 
                              {access.type === 'Portal' || access.type === 'Website' ? (
                                <a 
                                  href={access.value} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="access-link"
                                >
                                  {access.value}
                                </a>
                              ) : access.type === 'Email' ? (
                                <a 
                                  href={`mailto:${access.value}`}
                                  className="access-link"
                                >
                                  {access.value}
                                </a>
                              ) : access.type === 'Helpline' ? (
                                <a 
                                  href={`tel:${access.value}`}
                                  className="access-link"
                                >
                                  {access.value}
                                </a>
                              ) : (
                                <span>{access.value}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">🎓</div>
                <h3 className="empty-title">No matching schemes found</h3>
                <p className="empty-text">
                  Try adjusting your criteria or check back later for new schemes.
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Schemes; 