import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  const navItems = [
    {
      path: '/',
      label: 'Dashboard',
      icon: '🏠'
    },
    {
      path: '/file-complaint',
      label: 'File a Complaint',
      icon: '📝'
    },
    {
      path: '/track-status',
      label: 'Track Application Status',
      icon: '📊'
    },
    {
      path: '/schemes',
      label: 'Schemes & Scholarships',
      icon: '🎓'
    },
    {
      path: '/helpline',
      label: 'Helpline Numbers',
      icon: '📞'
    }
  ];

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div 
          className="sidebar-backdrop"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <h2 className="sidebar-title">JanAI</h2>
          <button 
            className="sidebar-close"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            ✕
          </button>
        </div>
        
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`sidebar-nav-item ${isActive(item.path) ? 'active' : ''}`}
              onClick={onClose}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </nav>
        
        <div className="sidebar-footer">
          <div className="sidebar-info">
            <p className="sidebar-subtitle">India's Hyperlocal Civic Agent</p>
            <p className="sidebar-version">Version 1.0.0</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar; 