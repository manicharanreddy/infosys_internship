import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/globals.css';
import './Auth.css';

const Register = ({ updateUser }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [error, setError] = useState('');
  const [nameError, setNameError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');

  const navigate = useNavigate();

  // ----------- VALIDATIONS --------------

  const validateName = (value) => {
    if (!value.trim()) return setNameError("Name is required");
    if (value.length < 3) return setNameError("Name must be at least 3 characters");
    if (!/^[A-Za-z\s]+$/.test(value)) return setNameError("Name should contain only letters");
    setNameError('');
  };

  const validateEmail = (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!value) return setEmailError("Email is required");
    if (!pattern.test(value)) return setEmailError("Enter a valid email");
    setEmailError('');
  };

  const validatePassword = (value) => {
    if (!value) return setPasswordError("Password is required");
    if (value.length < 6) return setPasswordError("Password must be at least 6 characters");
    setPasswordError('');
  };

  const validateConfirmPassword = (value) => {
    if (!value) return setConfirmPasswordError("Confirm your password");
    if (value !== password) return setConfirmPasswordError("Passwords do not match");
    setConfirmPasswordError('');
  };

  // ----------- HANDLE SUBMIT --------------

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (nameError || emailError || passwordError || confirmPasswordError) {
      setError("Please fix the errors before submitting");
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);

        const userData = {
          _id: data._id,
          name: data.name,
          email: data.email
        };

        localStorage.setItem('user', JSON.stringify(userData));

        if (updateUser) updateUser(userData);

        navigate('/dashboard');

      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError('Server error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Create an Account</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          
          {/* Name */}
          <div className="form-group">
            <label htmlFor="name">Full Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                validateName(e.target.value);
              }}
              required
            />
            {nameError && <p className="input-error">{nameError}</p>}
          </div>

          {/* Email */}
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                validateEmail(e.target.value);
              }}
              required
            />
            {emailError && <p className="input-error">{emailError}</p>}
          </div>

          {/* Password */}
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                validatePassword(e.target.value);
              }}
              required
            />
            {passwordError && <p className="input-error">{passwordError}</p>}
          </div>

          {/* Confirm Password */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => {
                setConfirmPassword(e.target.value);
                validateConfirmPassword(e.target.value);
              }}
              required
            />
            {confirmPasswordError && <p className="input-error">{confirmPasswordError}</p>}
          </div>

          <button
            type="submit"
            className="auth-button"
            disabled={
              nameError || emailError || passwordError || confirmPasswordError
            }
          >
            Register
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account?
            <button onClick={() => navigate('/login')} className="link-button">
              Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
