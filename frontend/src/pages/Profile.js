import React, { useState, useEffect } from 'react';
import './Profile.css';

const Profile = ({ user }) => {
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    joinDate: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [editedData, setEditedData] = useState({});

  useEffect(() => {
    if (user) {
      setProfileData({
        name: user.name || '',
        email: user.email || '',
        joinDate: new Date().toLocaleDateString()
      });
      setEditedData({
        name: user.name || '',
        email: user.email || ''
      });
    }
  }, [user]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    // In a real app, you would send this data to the backend
    setProfileData({
      ...profileData,
      ...editedData
    });
    setIsEditing(false);
    
    // Update localStorage as well
    const updatedUser = {
      ...user,
      name: editedData.name,
      email: editedData.email
    };
    localStorage.setItem('user', JSON.stringify(updatedUser));
  };

  const handleCancel = () => {
    setEditedData({
      name: profileData.name,
      email: profileData.email
    });
    setIsEditing(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedData({
      ...editedData,
      [name]: value
    });
  };

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>User Profile</h1>
        {!isEditing ? (
          <button className="edit-button" onClick={handleEdit}>
            Edit Profile
          </button>
        ) : (
          <div className="edit-actions">
            <button className="save-button" onClick={handleSave}>
              Save
            </button>
            <button className="cancel-button" onClick={handleCancel}>
              Cancel
            </button>
          </div>
        )}
      </div>

      <div className="profile-content">
        <div className="profile-avatar">
          <div className="avatar-circle">
            {profileData.name?.charAt(0)?.toUpperCase() || 'U'}
          </div>
        </div>

        <div className="profile-details">
          {isEditing ? (
            <div className="edit-form">
              <div className="form-group">
                <label htmlFor="name">Full Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={editedData.name}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={editedData.email}
                  onChange={handleChange}
                />
              </div>
            </div>
          ) : (
            <div className="profile-info">
              <div className="info-item">
                <label>Full Name</label>
                <div className="info-value">{profileData.name}</div>
              </div>
              <div className="info-item">
                <label>Email Address</label>
                <div className="info-value">{profileData.email}</div>
              </div>
              <div className="info-item">
                <label>Member Since</label>
                <div className="info-value">{profileData.joinDate}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;