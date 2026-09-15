import { useEffect, useState } from "react";
import api from "../services/api";

export default function Landing() {
  const [backendStatus, setBackendStatus] = useState("Checking backend...");

  useEffect(() => {
    console.log("Testing backend connection...");
    console.log("Backend URL:", "http://localhost:8000/");

    api
      .get("/")
      .then((response) => {
        console.log("BACKEND RESPONSE:", response);
        console.log("BACKEND STATUS:", response.status);
        console.log("BACKEND DATA:", response.data);

        setBackendStatus(
          `Backend connected: ${
            response.data?.message || "API is working"
          }`
        );
      })
      .catch((error) => {
        console.error("========== BACKEND ERROR ==========");
        console.error("ERROR:", error);
        console.error("MESSAGE:", error.message);
        console.error("CODE:", error.code);
        console.error("RESPONSE:", error.response);
        console.error("REQUEST:", error.request);
        console.error("===================================");

        setBackendStatus(
          `Backend connection failed: ${error.message}`
        );
      });
  }, []);

  return (
    <div>
      <h1>Landing Page</h1>
      <p>{backendStatus}</p>
    </div>
  );
}