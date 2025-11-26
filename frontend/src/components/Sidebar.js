import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ user, onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: '📊' },
    { name: 'Resume Upload', path: '/resume-upload', icon: '📄' },
    { name: 'Job Matching', path: '/job-matching', icon: '💼' },
    { name: 'Career Path', path: '/career-path', icon: '📈' },
    { name: 'Future Skills', path: '/future-skills', icon: '🔮' },
    { name: 'Bias Checker', path: '/bias-checker', icon: '✅' },
    { name: 'AI Mentor Chat', path: '/ai-mentor', icon: '🤖' },
    { name: 'Portfolio Generator', path: '/portfolio-generator', icon: '📁' },
    { name: 'Interview Practice', path: '/interview-practice', icon: '💬' },
    { name: 'Profile', path: '/profile', icon: '👤' },
  ];

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>AI Career Platform</h2>
      </div>
      
      <nav className="sidebar-nav">
        <ul>
          {menuItems.map((item) => (
            <li key={item.path}>
              <button
                className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
                onClick={() => navigate(item.path)}
              >
                <span className="sidebar-icon">{item.icon}</span>
                <span className="sidebar-text">{item.name}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
      
      <div className="sidebar-user">
        <div className="user-info">
          <div className="user-avatar">
            {user?.name?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          <div className="user-details">
            <div className="user-name">{user?.name || 'User'}</div>
            <div className="user-email">{user?.email || 'user@example.com'}</div>
          </div>
        </div>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;