import { useEffect, useState } from "react";
import api from "../services/api";

export default function History() {
  const [answers, setAnswers] = useState([]);
  const [message, setMessage] = useState("Loading history...");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await api.get("/interview/answers/my");

        setAnswers(response.data);
        setMessage("");
      } catch (error) {
        console.error("Interview history loading error:", error);

        if (error.response?.data?.detail) {
          setMessage(error.response.data.detail);
        } else {
          setMessage("Unable to load interview history");
        }
      }
    };

    loadHistory();
  }, []);

  return (
    <main className="page-container">
      <div className="page-heading">
        <h1>Interview History</h1>
        <p>Review your previous answers and AI evaluation results.</p>
      </div>

      {message && (
        <div className="card history-message">
          <p>{message}</p>
        </div>
      )}

      {!message && answers.length === 0 ? (
        <div className="card empty-state">
          <h3>No evaluated answers found</h3>
          <p>
            Complete an interview practice question to see your evaluation
            history here.
          </p>
        </div>
      ) : (
        <div className="history-list">
          {answers.map((item, index) => (
            <article className="card history-card" key={item.id}>
              <div className="history-header">
                <span className="question-number">
                  Answer {index + 1}
                </span>

                <div className="history-score">
                  {item.score}/100
                </div>
              </div>

              <div className="history-item">
                <strong>Your Answer</strong>
                <p>{item.answer}</p>
              </div>

              <div className="history-item">
                <strong>Feedback</strong>
                <p>{item.feedback}</p>
              </div>

              <div className="history-details">
                <div className="history-item">
                  <strong>Strengths</strong>
                  <p>{item.strengths}</p>
                </div>

                <div className="history-item">
                  <strong>Improvements</strong>
                  <p>{item.improvements}</p>
                </div>
              </div>

              <div className="history-result">
                <strong>Overall Result</strong>
                <p>{item.overall_result}</p>
              </div>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}