import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [message, setMessage] = useState("Loading dashboard...");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const response = await api.get("/dashboard");

        setData(response.data);
        setMessage("");
      } catch (error) {
        console.error("Dashboard error:", error);
        setMessage("Unable to load dashboard");
      }
    };

    loadDashboard();
  }, []);

  if (!data) {
    return (
      <div>
        <h1>Dashboard</h1>
        <p>{message}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Dashboard</h1>

      <p>Welcome to your interview preparation dashboard.</p>

      <div>
        <h2>Overview</h2>

        <p>
          <strong>Total Resumes:</strong> {data.total_resumes}
        </p>

        <p>
          <strong>Total Job Descriptions:</strong>{" "}
          {data.total_job_descriptions}
        </p>

        <p>
          <strong>Total Matches:</strong> {data.total_matches}
        </p>

        <p>
          <strong>Average Match Score:</strong>{" "}
          {data.average_match_score}
        </p>

        <p>
          <strong>Highest Match Score:</strong>{" "}
          {data.highest_match_score}
        </p>
      </div>
    </div>
  );
}