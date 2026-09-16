import { useEffect, useState } from "react";
import api from "../services/api";

export default function Resume() {
  const [file, setFile] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [message, setMessage] = useState("");

  const loadResumes = async () => {
    try {
      const response = await api.get("/resume/my-resumes");
      setResumes(response.data);
    } catch (error) {
      console.error("Load resumes error:", error);
      setMessage("Unable to load resumes");
    }
  };

  useEffect(() => {
    loadResumes();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a resume file");
      return;
    }

    setMessage("Uploading...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      await api.post("/resume/upload", formData);

      setMessage("Resume uploaded successfully");
      setFile(null);

      await loadResumes();
    } catch (error) {
      console.error("Resume upload error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);
      }

      setMessage("Resume upload failed");
    }
  };

  return (
    <main className="page-container">
      <div className="page-heading">
        <h1>Resume</h1>
        <p>Upload and manage your resumes for interview preparation.</p>
      </div>

      <section className="card upload-card">
        <h2>Upload Resume</h2>
        <p className="section-description">
          Supported formats: PDF, DOC, DOCX
        </p>

        <form onSubmit={handleUpload} className="upload-form">
          <input
            className="input"
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button className="btn btn-primary" type="submit">
            Upload Resume
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <h2>My Resumes</h2>
          <span className="count-badge">{resumes.length}</span>
        </div>

        {resumes.length === 0 ? (
          <div className="card empty-state">
            <h3>No resumes uploaded yet</h3>
            <p>Upload your resume to start preparing for interviews.</p>
          </div>
        ) : (
          <div className="resume-list">
            {resumes.map((resume) => (
              <div className="card resume-item" key={resume.id}>
                <div>
                  <h3>{resume.original_filename}</h3>
                  <p>{resume.file_size} bytes</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}