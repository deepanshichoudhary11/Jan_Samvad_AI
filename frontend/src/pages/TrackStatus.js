import React, { useState, useEffect } from 'react';
import { complaintAPI } from '../services/api';
import './TrackStatus.css';

const TrackStatus = ({ user }) => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    category: '',
    status: ''
  });

  useEffect(() => {
    fetchComplaints();
  }, [user.id]);

  const fetchComplaints = async () => {
    try {
      const response = await complaintAPI.getComplaintStatus(user.id);
      setComplaints(response.complaints);
    } catch (error) {
      setError('Failed to fetch complaints. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResolveComplaint = async (complaintId) => {
    try {
      // Update the complaint status locally first for immediate UI feedback
      setComplaints(prev => 
        prev.map(complaint => 
          complaint.id === complaintId 
            ? { ...complaint, status: 'Issue Resolved' }
            : complaint
        )
      );

      // Call the backend to update the status
      await complaintAPI.resolveComplaint(complaintId);
      
      // Show success message
      setError(''); // Clear any previous errors
    } catch (error) {
      // Revert the local change if backend call fails
      setComplaints(prev => 
        prev.map(complaint => 
          complaint.id === complaintId 
            ? { ...complaint, status: 'Submitted' } // Revert to original status
            : complaint
        )
      );
      setError('Failed to resolve complaint. Please try again.');
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getFilteredComplaints = () => {
    return complaints.filter(complaint => {
      const categoryMatch = !filters.category || complaint.category === filters.category;
      const statusMatch = !filters.status || complaint.status === filters.status;
      return categoryMatch && statusMatch;
    });
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'submitted':
        return 'status-submitted';
      case 'pending':
        return 'status-pending';
      case 'issue resolved':
        return 'status-resolved';
      default:
        return 'status-submitted';
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
  const statuses = [
    'Submitted',
    'Pending',
    'Issue Resolved'
  ];

  if (loading) {
    return (
      <div className="container">
        <div className="page-header">
          <h1 className="page-title">Track Application Status</h1>
          <p className="page-subtitle">Monitor your complaint resolution progress</p>
        </div>
        <div className="loading-state">
          <p>Loading your complaints...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Track Application Status</h1>
        <p className="page-subtitle">Monitor your complaint resolution progress</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {/* Summary Section */}
      {complaints.length > 0 && (
        <div className="summary-section">
          <h3 className="summary-title">📊 Complaint Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-number">{complaints.length}</span>
              <span className="summary-label">Total Complaints</span>
            </div>
            <div className="summary-item">
              <span className="summary-number">
                {complaints.filter(c => c.status === 'Issue Resolved').length}
              </span>
              <span className="summary-label">✅ Resolved</span>
            </div>
            <div className="summary-item">
              <span className="summary-number">
                {complaints.filter(c => c.status === 'Pending').length}
              </span>
              <span className="summary-label">⏳ Pending</span>
            </div>
            <div className="summary-item">
              <span className="summary-number">
                {complaints.filter(c => c.status === 'Submitted').length}
              </span>
              <span className="summary-label">📝 Submitted</span>
            </div>
            <div className="summary-item">
              <span className="summary-number">
                {Math.round((complaints.filter(c => c.status === 'Issue Resolved').length / complaints.length) * 100)}%
              </span>
              <span className="summary-label">Resolution Rate</span>
            </div>
          </div>
          
          {/* Recent Activity */}
          <div className="recent-activity">
            <h4>🕒 Recent Activity</h4>
            <div className="activity-list">
              {complaints.slice(0, 3).map((complaint, index) => (
                <div key={complaint.id} className="activity-item">
                  <span className="activity-icon">📋</span>
                  <div className="activity-content">
                    <strong>{complaint.category}</strong> - {complaint.status}
                    <small>{complaint.date}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="filters-section">
        <div className="filters-grid">
          <div className="form-group">
            <label htmlFor="category" className="form-label">Filter by Category</label>
            <select
              id="category"
              name="category"
              value={filters.category}
              onChange={handleFilterChange}
              className="form-select"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="status" className="form-label">Filter by Status</label>
            <select
              id="status"
              name="status"
              value={filters.status}
              onChange={handleFilterChange}
              className="form-select"
            >
              <option value="">All Statuses</option>
              {statuses.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Complaints List */}
      <div className="complaints-section">
        {getFilteredComplaints().length > 0 ? (
          <div className="complaints-grid">
            {getFilteredComplaints().map((complaint) => (
              <div key={complaint.id} className="complaint-card">
                <div className="complaint-header">
                  <div className="complaint-info">
                    <h3 className="complaint-title">{complaint.category}</h3>
                    <p className="complaint-id">{complaint.id}</p>
                  </div>
                  <span className={`status-badge ${getStatusColor(complaint.status)}`}>
                    {complaint.status}
                  </span>
                </div>
                
                <div className="complaint-body">
                  <p className="complaint-description">{complaint.description}</p>
                  
                  <div className="complaint-details">
                    <div className="detail-item">
                      <strong>Date:</strong> {complaint.date}
                    </div>
                    <div className="detail-item">
                      <strong>Address:</strong> {complaint.address.houseNo}, {complaint.address.addressLine1}
                    </div>
                    {complaint.address.addressLine2 && (
                      <div className="detail-item">
                        <strong>Landmark:</strong> {complaint.address.addressLine2}
                      </div>
                    )}
                    <div className="detail-item">
                      <strong>PIN Code:</strong> {complaint.address.pinCode}
                    </div>
                  </div>
                </div>

                                 <div className="complaint-footer">
                   <div className="authority-info">
                     <h4>Concerned Authority</h4>
                     <p><strong>Name:</strong> {complaint.authority.name}</p>
                     <p><strong>Email:</strong> {complaint.authority.email}</p>
                     <p><strong>Phone:</strong> {complaint.authority.phone}</p>
                   </div>
                   
                   {/* Resolve Button - Only show for non-resolved complaints */}
                   {complaint.status !== 'Issue Resolved' && (
                     <div className="complaint-actions">
                       <button
                         className="btn btn-success resolve-btn"
                         onClick={() => handleResolveComplaint(complaint.id)}
                       >
                         ✅ Mark as Resolved
                       </button>
                     </div>
                   )}
                 </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📊</div>
            <h3 className="empty-title">
              {complaints.length === 0 ? 'No complaints found' : 'No complaints match your filters'}
            </h3>
            <p className="empty-text">
              {complaints.length === 0 
                ? 'Start by filing your first complaint to track civic issues.'
                : 'Try adjusting your filters to see more results.'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrackStatus; 