import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Phone, KeyRound, RefreshCw, ArrowLeft } from 'lucide-react';
import '../ForgotPassword.css';

export default function ForgotPassword() {
  const [phone, setPhone] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const navigate = useNavigate();

  const handleReset = (e) => {
    e.preventDefault();
    const savedUser = JSON.parse(localStorage.getItem("user"));

    if (!savedUser) {
      alert("No user found. Please Register first.");
      return;
    }

    if (phone !== savedUser.phone) {
      alert("Phone number does not match!");
      return;
    }

    const updatedUser = {
      ...savedUser,
      password: newPassword,
    };

    localStorage.setItem("user", JSON.stringify(updatedUser));
    alert("Password Reset Successful! Now Login.");
    navigate("/"); // Navigate to the login route
  };

  return (
    <div className="forgot-page-wrapper">
      <div className="forgot-card">
        <div className="forgot-header">
          <div className="forgot-icon">🔒</div>
          <h1>Reset Password</h1>
          <p>Enter your details to recover access</p>
        </div>

        <form onSubmit={handleReset} className="forgot-form">
          <div className="input-group">
            <Phone className="input-icon" size={18} />
            <input
              type="text"
              placeholder="Registered Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <KeyRound className="input-icon" size={18} />
            <input
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="reset-btn">
            Update Password <RefreshCw size={18} />
          </button>

          <div className="forgot-footer">
            <Link to="/" className="back-link">
              <ArrowLeft size={16} /> Back to Login
            </Link>
          </div>
        </form>
      </div>

      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>
    </div>
  );
}