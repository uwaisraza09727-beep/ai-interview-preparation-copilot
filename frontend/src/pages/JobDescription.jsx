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
    <div>
      <h1>Job Description</h1>

      <h2>Paste Job Description</h2>

      <form onSubmit={handleTextSubmit}>
        <div>
          <label>Title</label>
          <br />

          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Python Backend Developer"
          />
        </div>

        <br />

        <div>
          <label>Job Description</label>
          <br />

          <textarea
            rows="12"
            cols="60"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the complete job description here..."
          />
        </div>

        <br />

        <button type="submit">
          Save Job Description
        </button>
      </form>

      <hr />

      <h2>Upload Job Description File</h2>

      <form onSubmit={handleFileUpload}>
        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br />
        <br />

        <button type="submit">
          Upload JD
        </button>
      </form>

      <p>{message}</p>

      <hr />

      <h2>My Job Descriptions</h2>

      {jobDescriptions.length === 0 ? (
        <p>No job descriptions added yet.</p>
      ) : (
        <ul>
          {jobDescriptions.map((jd) => (
            <li key={jd.id}>
              <strong>{jd.original_filename}</strong>
              {" — "}
              {jd.file_type}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}