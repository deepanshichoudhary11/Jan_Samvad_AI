import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import FileComplaint from './pages/FileComplaint';
import TrackStatus from './pages/TrackStatus';
import Schemes from './pages/Schemes';
import Helpline from './pages/Helpline';
import Login from './pages/Login';
import Register from './pages/Register';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Check for stored user on app load
  React.useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <Router>
      <div className="app">
        <Navbar 
          user={user} 
          onLogout={handleLogout}
          onToggleSidebar={toggleSidebar}
        />
        <Sidebar 
          isOpen={sidebarOpen} 
          onClose={() => setSidebarOpen(false)}
        />
        <main className="main-content">
          <Routes>
            <Route 
              path="/" 
              element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/file-complaint" 
              element={user ? <FileComplaint user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/track-status" 
              element={user ? <TrackStatus user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/schemes" 
              element={user ? <Schemes user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/helpline" 
              element={user ? <Helpline user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/login" 
              element={user ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/register" 
              element={user ? <Navigate to="/" /> : <Register onLogin={handleLogin} />} 
            />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App; 