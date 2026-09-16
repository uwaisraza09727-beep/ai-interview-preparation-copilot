import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Landing() {
  const [backendStatus, setBackendStatus] = useState("Checking backend...");

  useEffect(() => {
    api
      .get("/")
      .then((response) => {
        setBackendStatus(
          response.data?.message || "Backend is connected"
        );
      })
      .catch(() => {
        setBackendStatus("Backend connection unavailable");
      });
  }, []);

  return (
    <main className="landing-page">
      <section className="landing-hero">
        <div className="landing-content">
          <span className="landing-badge">AI-Powered Interview Preparation</span>

          <h1>
            Prepare smarter.
            <br />
            <span>Interview with confidence.</span>
          </h1>

          <p>
            Upload your resume and job description, generate personalized
            interview questions, practice your answers, and get AI-powered
            feedback.
          </p>

          <div className="landing-actions">
            <Link to="/register" className="btn btn-primary">
              Get Started
            </Link>

            <Link to="/login" className="btn btn-secondary">
              Login
            </Link>
          </div>

          <div className="backend-status">
            <span className="status-dot"></span>
            {backendStatus}
          </div>
        </div>
      </section>

      <section className="landing-features page-container">
        <div className="landing-feature card">
          <h3>Resume Analysis</h3>
          <p>
            Upload your resume and prepare based on your actual skills and
            experience.
          </p>
        </div>

        <div className="landing-feature card">
          <h3>AI Interview Questions</h3>
          <p>
            Generate personalized technical and interview questions using AI.
          </p>
        </div>

        <div className="landing-feature card">
          <h3>Answer Evaluation</h3>
          <p>
            Practice answers and receive AI-powered feedback and suggestions.
          </p>
        </div>
      </section>
    </main>
  );
}