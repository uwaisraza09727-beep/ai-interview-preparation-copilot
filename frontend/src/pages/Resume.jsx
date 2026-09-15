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
    <div>
      <h1>Resume</h1>

      <h2>Upload Resume</h2>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br />
        <br />

        <button type="submit">Upload Resume</button>
      </form>

      <p>{message}</p>

      <h2>My Resumes</h2>

      {resumes.length === 0 ? (
        <p>No resumes uploaded yet.</p>
      ) : (
        <ul>
          {resumes.map((resume) => (
            <li key={resume.id}>
              {resume.original_filename} — {resume.file_size} bytes
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}