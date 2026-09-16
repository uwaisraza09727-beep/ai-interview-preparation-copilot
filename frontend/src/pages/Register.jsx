import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function BrainIcon() {
  return (
    <svg
      width="28"
      height="28"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9.5 4.5A3 3 0 0 0 6 7.4 3.2 3.2 0 0 0 6.5 13a3 3 0 0 0 3 5.5" />
      <path d="M14.5 4.5A3 3 0 0 1 18 7.4a3.2 3.2 0 0 1-.5 5.6 3 3 0 0 1-3 5.5" />
      <path d="M9 8h6" />
      <path d="M9 12h6" />
      <path d="M9.5 16h5" />
      <path d="M12 4v16" />
    </svg>
  );
}

export default function Register() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      setMessage("Creating your account...");

      await api.post("/auth/register", {
        full_name: fullName,
        email,
        password,
      });

      setMessage("Registration successful");

      navigate("/login");
    } catch (error) {
      console.error(error);
      setMessage("Registration failed");
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-shell">

        <section className="auth-brand-panel">
          <div className="auth-brand">
            <div className="auth-brand-icon">
              <BrainIcon />
            </div>

            <div>
              <strong>AI Interview</strong>
              <span>Copilot</span>
            </div>
          </div>

          <div className="auth-brand-content">
            <span className="auth-eyebrow">
              AI-Powered Preparation
            </span>

            <h1>
              Prepare smarter.
              <br />
              <span>Interview with confidence.</span>
            </h1>

            <p>
              Build your interview skills with personalized questions,
              practice sessions, and AI-powered feedback.
            </p>

            <div className="auth-benefits">
              <div>
                <span>✓</span>
                Personalized interview questions
              </div>

              <div>
                <span>✓</span>
                Practice with AI feedback
              </div>

              <div>
                <span>✓</span>
                Track your preparation progress
              </div>
            </div>
          </div>
        </section>

        <section className="auth-form-panel">

          <div className="auth-form-container">

            <div className="auth-mobile-brand">
              <div className="auth-brand-icon">
                <BrainIcon />
              </div>

              <strong>AI Interview Copilot</strong>
            </div>

            <div className="auth-heading">
              <h2>Create your account</h2>

              <p>
                Start preparing for your next interview today.
              </p>
            </div>

            <form
              onSubmit={handleRegister}
              className="auth-form"
            >

              <div className="form-group">
                <label htmlFor="fullName">
                  Full Name
                </label>

                <input
                  id="fullName"
                  className="input"
                  type="text"
                  value={fullName}
                  onChange={(e) =>
                    setFullName(e.target.value)
                  }
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="registerEmail">
                  Email Address
                </label>

                <input
                  id="registerEmail"
                  className="input"
                  type="email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  placeholder="you@example.com"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="registerPassword">
                  Password
                </label>

                <input
                  id="registerPassword"
                  className="input"
                  type="password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  placeholder="Create a password"
                  required
                />
              </div>

              <button
                className="btn btn-primary auth-submit"
                type="submit"
              >
                Create Account
              </button>

            </form>

            {message && (
              <p className="auth-message">
                {message}
              </p>
            )}

            <div className="auth-switch">
              Already have an account?
              <Link to="/login">
                Sign in
              </Link>
            </div>

          </div>

        </section>

      </div>
    </main>
  );
}