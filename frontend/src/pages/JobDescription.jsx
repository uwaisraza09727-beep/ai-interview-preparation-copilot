import { useEffect, useState } from "react";
import api from "../services/api";

export default function JobDescription() {
  const [title, setTitle] = useState("");
  const [jdText, setJdText] = useState("");
  const [file, setFile] = useState(null);

  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [message, setMessage] = useState("");

  const loadJobDescriptions = async () => {
    try {
      const response = await api.get(
        "/job-description/my-job-descriptions"
      );

      setJobDescriptions(response.data);
    } catch (error) {
      console.error("Load job descriptions error:", error);
      setMessage("Unable to load job descriptions");
    }
  };

  useEffect(() => {
    loadJobDescriptions();
  }, []);

  const handleTextSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim() || !jdText.trim()) {
      setMessage("Please enter title and job description");
      return;
    }

    if (jdText.trim().length < 20) {
      setMessage("Job description must be at least 20 characters");
      return;
    }

    setMessage("Saving job description...");

    try {
      await api.post("/job-description/text", {
        title,
        jd_text: jdText,
      });

      setTitle("");
      setJdText("");
      setMessage("Job description saved successfully");

      await loadJobDescriptions();
    } catch (error) {
      console.error("Job description error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);
      }

      setMessage("Failed to save job description");
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a JD file");
      return;
    }

    setMessage("Uploading job description...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      await api.post("/job-description/upload", formData);

      setFile(null);
      setMessage("Job description uploaded successfully");

      await loadJobDescriptions();
    } catch (error) {
      console.error("JD upload error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);
      }

      setMessage("Job description upload failed");
    }
  };

  return (
    <main className="page-container">
      <div className="page-heading">
        <h1>Job Description</h1>
        <p>Add a job description by pasting the text or uploading a file.</p>
      </div>

      <section className="card">
        <h2>Paste Job Description</h2>
        <p className="section-description">
          Add the job details you want to use for interview preparation.
        </p>

        <form onSubmit={handleTextSubmit} className="form-stack">
          <div className="form-group">
            <label>Title</label>
            <input
              className="input"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Python Backend Developer"
            />
          </div>

          <div className="form-group">
            <label>Job Description</label>
            <textarea
              className="textarea jd-textarea"
              rows="12"
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste the complete job description here..."
            />
          </div>

          <button className="btn btn-primary" type="submit">
            Save Job Description
          </button>
        </form>
      </section>

      <section className="card upload-card">
        <h2>Upload Job Description File</h2>
        <p className="section-description">
          Supported formats: PDF, DOC, DOCX, TXT
        </p>

        <form onSubmit={handleFileUpload} className="upload-form">
          <input
            className="input"
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button className="btn btn-secondary" type="submit">
            Upload JD
          </button>
        </form>

        {message && <p className="form-message">{message}</p>}
      </section>

      <section className="content-section">
        <div className="section-heading">
          <h2>My Job Descriptions</h2>
          <span className="count-badge">{jobDescriptions.length}</span>
        </div>

        {jobDescriptions.length === 0 ? (
          <div className="card empty-state">
            <h3>No job descriptions added yet</h3>
            <p>Add a job description to start interview preparation.</p>
          </div>
        ) : (
          <div className="resume-list">
            {jobDescriptions.map((jd) => (
              <div className="card resume-item" key={jd.id}>
                <div>
                  <h3>{jd.original_filename}</h3>
                  <p>{jd.file_type}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}