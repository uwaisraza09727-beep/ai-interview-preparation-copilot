import { useEffect, useState } from "react";
import api from "../services/api";

export default function History() {
  const [answers, setAnswers] = useState([]);
  const [message, setMessage] = useState("Loading history...");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await api.get(
          "/interview/answers/my"
        );

        setAnswers(response.data);
        setMessage("");
      } catch (error) {
        console.error(
          "Interview history loading error:",
          error
        );

        if (error.response?.data?.detail) {
          setMessage(error.response.data.detail);
        } else {
          setMessage(
            "Unable to load interview history"
          );
        }
      }
    };

    loadHistory();
  }, []);

  return (
    <div>
      <h1>Interview History</h1>

      {message && <p>{message}</p>}

      {answers.length === 0 && !message ? (
        <p>No evaluated answers found.</p>
      ) : (
        <ol>
          {answers.map((item) => (
            <li key={item.id}>
              <p>
                <strong>Your Answer:</strong>
              </p>

              <p>{item.answer}</p>

              <p>
                <strong>Score:</strong>{" "}
                {item.score}/10
              </p>

              <p>
                <strong>Feedback:</strong>{" "}
                {item.feedback}
              </p>

              <p>
                <strong>Strengths:</strong>{" "}
                {item.strengths}
              </p>

              <p>
                <strong>Improvements:</strong>{" "}
                {item.improvements}
              </p>

              <p>
                <strong>Overall Result:</strong>{" "}
                {item.overall_result}
              </p>

              <hr />
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}