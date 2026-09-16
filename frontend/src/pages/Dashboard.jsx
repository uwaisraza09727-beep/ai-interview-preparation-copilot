import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);

  const [resumes, setResumes] = useState([]);
  const [jobDescriptions, setJobDescriptions] = useState([]);

  const [resumeId, setResumeId] = useState("");
  const [jobDescriptionId, setJobDescriptionId] = useState("");

  const [matchResult, setMatchResult] = useState(null);
  const [matching, setMatching] = useState(false);
  const [matchMessage, setMatchMessage] = useState("");

  const [message, setMessage] = useState("Loading dashboard...");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [dashboardResponse, resumeResponse, jdResponse] =
          await Promise.all([
            api.get("/dashboard"),
            api.get("/resume/my-resumes"),
            api.get("/job-description/my-job-descriptions"),
          ]);

        setData(dashboardResponse.data);
        setResumes(resumeResponse.data);
        setJobDescriptions(jdResponse.data);
        setMessage("");
      } catch (error) {
        console.error("Dashboard error:", error);
        setMessage("Unable to load dashboard");
      }
    };

    loadDashboard();
  }, []);

  const handleMatch = async (e) => {
    e.preventDefault();

    if (!resumeId || !jobDescriptionId) {
      setMatchMessage("Please select a resume and job description.");
      return;
    }

    setMatching(true);
    setMatchMessage("");
    setMatchResult(null);

    try {
      const response = await api.post(
        `/matching/${resumeId}/${jobDescriptionId}`
      );

      setMatchResult(response.data);
      setMatchMessage("Resume and Job Description matched successfully.");
    } catch (error) {
      console.error("Matching error:", error);

      if (error.response?.data?.detail) {
        setMatchMessage(error.response.data.detail);
      } else {
        setMatchMessage("Unable to analyze resume and job description.");
      }
    } finally {
      setMatching(false);
    }
  };

  if (!data) {
    return (
      <main className="page-container">
        <div className="dashboard-loading card">
          <div className="dashboard-loading-icon">AI</div>
          <h1>Dashboard</h1>
          <p>{message}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="page-container">
      <div className="dashboard-page">

        {/* HERO */}
        <section className="dashboard-hero">
          <div>
            <span className="dashboard-eyebrow">
              YOUR AI INTERVIEW COPILOT
            </span>

            <h1>
              Practice smarter.
              <br />
              <span>Land your dream job.</span>
            </h1>

            <p>
              Track your interview preparation, resume activity,
              and job matching progress in one place.
            </p>
          </div>

          <div className="dashboard-hero-badge">
            <div>AI</div>
            <span>Smart preparation</span>
          </div>
        </section>

        {/* OVERVIEW */}
        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <div>
              <h2>Preparation Overview</h2>
              <p>
                A quick look at your current interview preparation activity.
              </p>
            </div>
          </div>

          <div className="dashboard-grid">

            <div className="dashboard-stat card">
              <div className="stat-icon">▤</div>
              <span className="stat-label">Resumes</span>
              <strong>{data.total_resumes}</strong>
              <small>Uploaded resumes</small>
            </div>

            <div className="dashboard-stat card">
              <div className="stat-icon">▣</div>
              <span className="stat-label">Job Descriptions</span>
              <strong>{data.total_job_descriptions}</strong>
              <small>Saved job descriptions</small>
            </div>

            <div className="dashboard-stat card">
              <div className="stat-icon">↗</div>
              <span className="stat-label">Total Matches</span>
              <strong>{data.total_matches}</strong>
              <small>Resume &amp; JD matches</small>
            </div>

            <div className="dashboard-stat card">
              <div className="stat-icon">◌</div>
              <span className="stat-label">Average Score</span>
              <strong>{data.average_match_score}<small>/100</small></strong>
              <small>Average matching score</small>
            </div>

            <div className="dashboard-stat card">
              <div className="stat-icon">★</div>
              <span className="stat-label">Highest Score</span>
              <strong>{data.highest_match_score}<small>/100</small></strong>
              <small>Best matching score</small>
            </div>

          </div>
        </section>

        {/* MATCH ANALYSIS */}
        <section className="dashboard-match-section card">

          <div className="dashboard-match-header">
            <div>
              <span className="dashboard-eyebrow">
                RESUME ANALYSIS
              </span>

              <h2>Resume–Job Description Match</h2>

              <p>
                Compare your resume with a target job description
                and identify matched and missing skills.
              </p>
            </div>

            <div className="dashboard-match-icon">
              AI
            </div>
          </div>

          {/* FORM */}
          <form
            onSubmit={handleMatch}
            className="dashboard-match-form"
          >
            <div className="form-group">
              <label>Resume</label>

              <select
                className="select"
                value={resumeId}
                onChange={(e) => setResumeId(e.target.value)}
                required
              >
                <option value="">Select Resume</option>

                {resumes.map((resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.original_filename}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Job Description</label>

              <select
                className="select"
                value={jobDescriptionId}
                onChange={(e) =>
                  setJobDescriptionId(e.target.value)
                }
                required
              >
                <option value="">Select Job Description</option>

                {jobDescriptions.map((jd) => (
                  <option key={jd.id} value={jd.id}>
                    {jd.original_filename}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="btn btn-primary dashboard-analyze-btn"
              type="submit"
              disabled={matching}
            >
              {matching ? "Analyzing..." : "Analyze Match"}
            </button>
          </form>

          {matchMessage && (
            <div
              className={`dashboard-match-message ${
                matchResult ? "success" : ""
              }`}
            >
              {matchMessage}
            </div>
          )}

          {/* RESULT */}
          {matchResult && (
            <div className="match-result-panel">

              <div className="match-result-top">
                <div>
                  <span className="dashboard-eyebrow">
                    MATCH ANALYSIS
                  </span>

                  <h3>Resume Compatibility</h3>

                  <p>
                    AI analysis of your resume against the selected
                    job description.
                  </p>
                </div>

                <div className="match-result-score">
                  <strong>{matchResult.overall_score}</strong>
                  <span>/100</span>
                </div>
              </div>

              <div className="match-result-grid">

                {/* MATCHED SKILLS */}
                <div className="match-result-item matched">
                  <div className="result-item-heading">
                    <span className="result-dot matched-dot"></span>
                    <strong>Matched Skills</strong>
                  </div>

                  <div className="skill-list">
                    {matchResult.matched_skills?.length > 0 ? (
                      matchResult.matched_skills.map((skill) => (
                        <span key={skill}>{skill}</span>
                      ))
                    ) : (
                      <p>No matched skills found.</p>
                    )}
                  </div>
                </div>

                {/* MISSING SKILLS */}
                <div className="match-result-item missing">
                  <div className="result-item-heading">
                    <span className="result-dot missing-dot"></span>
                    <strong>Missing Skills</strong>
                  </div>

                  <div className="skill-list">
                    {matchResult.missing_skills?.length > 0 ? (
                      matchResult.missing_skills.map((skill) => (
                        <span key={skill}>{skill}</span>
                      ))
                    ) : (
                      <p>No missing skills found.</p>
                    )}
                  </div>
                </div>

                {/* MATCHED KEYWORDS */}
                <div className="match-result-item">
                  <div className="result-item-heading">
                    <span className="result-dot keyword-dot"></span>
                    <strong>Matched Keywords</strong>
                  </div>

                  <div className="skill-list">
                    {matchResult.matched_keywords?.length > 0 ? (
                      matchResult.matched_keywords.map((keyword) => (
                        <span key={keyword}>{keyword}</span>
                      ))
                    ) : (
                      <p>No matched keywords found.</p>
                    )}
                  </div>
                </div>

                {/* MISSING KEYWORDS */}
                <div className="match-result-item">
                  <div className="result-item-heading">
                    <span className="result-dot neutral-dot"></span>
                    <strong>Missing Keywords</strong>
                  </div>

                  <div className="skill-list">
                    {matchResult.missing_keywords?.length > 0 ? (
                      matchResult.missing_keywords.map((keyword) => (
                        <span key={keyword}>{keyword}</span>
                      ))
                    ) : (
                      <p>No missing keywords found.</p>
                    )}
                  </div>
                </div>

              </div>
            </div>
          )}
        </section>

      </div>
    </main>
  );
}