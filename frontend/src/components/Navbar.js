import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ user, onLogout, onToggleSidebar }) => {
  const [showDropdown, setShowDropdown] = useState(false);

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <button 
            className="navbar-menu-button"
            onClick={onToggleSidebar}
            aria-label="Toggle sidebar"
          >
            ☰
          </button>
          <Link to="/" className="navbar-logo">
            JanAI
          </Link>
        </div>
        
        <div className="navbar-right">
          <div className="navbar-profile">
            <button 
              className="profile-button"
              onClick={toggleDropdown}
              aria-label="User profile menu"
            >
              <div className="profile-avatar">
                {user ? user.fullName.charAt(0).toUpperCase() : 'U'}
              </div>
            </button>
            
            {showDropdown && (
              <div className="profile-dropdown">
                {user ? (
                  <>
                    <div className="dropdown-header">
                      <div className="user-info">
                        <div className="user-name">{user.fullName}</div>
                        <div className="user-email">{user.email}</div>
                      </div>
                    </div>
                    <div className="dropdown-divider"></div>
                    <Link to="/" className="dropdown-item">
                      Dashboard
                    </Link>
                    <button 
                      className="dropdown-item"
                      onClick={onLogout}
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link to="/login" className="dropdown-item">
                      Login
                    </Link>
                    <Link to="/register" className="dropdown-item">
                      Register
                    </Link>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Backdrop for dropdown */}
      {showDropdown && (
        <div 
          className="dropdown-backdrop"
          onClick={() => setShowDropdown(false)}
        />
      )}
    </nav>
  );
};

export default Navbar; 