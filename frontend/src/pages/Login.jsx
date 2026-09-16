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

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setMessage("Logging in...");

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

      console.log("Login response:", response.data);

      const accessToken =
        response.data.access_token;

      if (!accessToken) {
        setMessage(
          "Login failed: access token not received"
        );

        return;
      }

      localStorage.setItem(
        "access_token",
        accessToken
      );

      setMessage("Login successful");

      navigate("/dashboard");
    } catch (error) {
      console.error("Login error:", error);

      if (error.response) {
        console.error(
          "Status:",
          error.response.status
        );

        console.error(
          "Response:",
          error.response.data
        );
      }

      setMessage("Login failed");
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-shell">

        {/* Brand Panel */}
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
              Turn your resume and target role into a
              personalized interview preparation experience.
            </p>

            <div className="auth-benefits">

              <div>
                <span>✓</span>
                Personalized interview questions
              </div>

              <div>
                <span>✓</span>
                Practice with AI-powered feedback
              </div>

              <div>
                <span>✓</span>
                Prepare based on your actual skills
              </div>

            </div>

          </div>

        </section>

        {/* Login Panel */}
        <section className="auth-form-panel">

          <div className="auth-form-container">

            <div className="auth-mobile-brand">

              <div className="auth-brand-icon">
                <BrainIcon />
              </div>

              <strong>
                AI Interview Copilot
              </strong>

            </div>

            <div className="auth-heading">

              <h2>
                Welcome back
              </h2>

              <p>
                Sign in to continue your interview
                preparation.
              </p>

            </div>

            <form
              onSubmit={handleLogin}
              className="auth-form"
            >

              <div className="form-group">

                <label htmlFor="loginEmail">
                  Email Address
                </label>

                <input
                  id="loginEmail"
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

                <label htmlFor="loginPassword">
                  Password
                </label>

                <input
                  id="loginPassword"
                  className="input"
                  type="password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  placeholder="Enter your password"
                  required
                />

              </div>

              <button
                className="btn btn-primary auth-submit"
                type="submit"
              >
                Sign In
              </button>

            </form>

            {message && (
              <p className="auth-message">
                {message}
              </p>
            )}

            <div className="auth-switch">

              Don't have an account?

              <Link to="/register">
                Create account
              </Link>

            </div>

          </div>

        </section>

      </div>
    </main>
  );
}