import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { User, Lock, Phone, ShieldCheck, UserPlus } from 'lucide-react';
import '../Register.css';

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [role, setRole] = useState("engineer");

  const navigate = useNavigate();

  const handleRegister = (e) => {
    e.preventDefault();
    if (!username || !password || !phone) {
      alert("All fields are required");
      return;
    }
    const user = { username, password, phone, role };
    localStorage.setItem("user", JSON.stringify(user));
    alert("Registration Successful! Now Login.");
    navigate("/");
  };

  return (
    <div className="register-page-wrapper">
      <div className="register-card">
        <div className="register-header">
          <div className="register-icon">✨</div>
          <h1>Create Account</h1>
          <p>Join the CivicFix internal team</p>
        </div>

        <form onSubmit={handleRegister} className="register-form">
          <div className="input-group">
            <User className="input-icon" size={18} />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <Lock className="input-icon" size={18} />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <Phone className="input-icon" size={18} />
            <input
              type="text"
              placeholder="Phone Number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <ShieldCheck className="input-icon" size={18} />
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="role-select"
            >
              <option value="engineer">Engineer</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button type="submit" className="register-btn">
            Register <UserPlus size={18} />
          </button>

          <p className="register-footer">
            Already have an account? <Link to="/" className="footer-link">Login</Link>
          </p>
        </form>
      </div>

      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>
    </div>
  );
};

export default Register;