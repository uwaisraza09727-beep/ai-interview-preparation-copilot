import { useEffect, useState } from "react";
import api from "../services/api";

export default function Interview() {
  const [resumes, setResumes] = useState([]);
  const [jobDescriptions, setJobDescriptions] = useState([]);

  const [resumeId, setResumeId] = useState("");
  const [jobDescriptionId, setJobDescriptionId] = useState("");

  const [category, setCategory] = useState("technical");
  const [difficulty, setDifficulty] = useState("medium");
  const [questionCount, setQuestionCount] = useState(5);

  const [questions, setQuestions] = useState([]);
  const [message, setMessage] = useState("");

  const [answers, setAnswers] = useState({});
  const [evaluations, setEvaluations] = useState({});
  const [evaluationErrors, setEvaluationErrors] = useState({});
  const [evaluating, setEvaluating] = useState({});

  useEffect(() => {
    const loadData = async () => {
      try {
        const [resumeResponse, jdResponse] = await Promise.all([
          api.get("/resume/my-resumes"),
          api.get("/job-description/my-job-descriptions"),
        ]);

        setResumes(resumeResponse.data);
        setJobDescriptions(jdResponse.data);
      } catch (error) {
        console.error("Interview data loading error:", error);
        setMessage("Unable to load resumes or job descriptions");
      }
    };

    loadData();
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();

    if (!resumeId || !jobDescriptionId) {
      setMessage("Please select a resume and job description");
      return;
    }

    setMessage("Generating questions...");
    setQuestions([]);
    setAnswers({});
    setEvaluations({});
    setEvaluationErrors({});
    setEvaluating({});

    try {
      const response = await api.post(
        "/interview/questions/generate",
        {
          resume_id: resumeId,
          job_description_id: jobDescriptionId,
          category,
          difficulty,
          question_count: Number(questionCount),
        }
      );

      setQuestions(response.data);

      setMessage(
        `${response.data.length} questions generated successfully`
      );
    } catch (error) {
      console.error("Question generation error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);
      }

      setMessage("Failed to generate questions");
    }
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswers((previousAnswers) => ({
      ...previousAnswers,
      [questionId]: value,
    }));

    setEvaluationErrors((previousErrors) => ({
      ...previousErrors,
      [questionId]: "",
    }));
  };

  const handleEvaluate = async (questionId) => {
    const answer = (answers[questionId] || "").trim();

    if (answer.length < 10) {
      setEvaluationErrors((previousErrors) => ({
        ...previousErrors,
        [questionId]: "Answer must be at least 10 characters long.",
      }));

      return;
    }

    setEvaluationErrors((previousErrors) => ({
      ...previousErrors,
      [questionId]: "",
    }));

    setEvaluating((previousEvaluating) => ({
      ...previousEvaluating,
      [questionId]: true,
    }));

    try {
      const response = await api.post(
        "/interview/answers/evaluate",
        {
          interview_question_id: questionId,
          answer,
        }
      );

      setEvaluations((previousEvaluations) => ({
        ...previousEvaluations,
        [questionId]: response.data,
      }));
    } catch (error) {
      console.error("Answer evaluation error:", error);

      let errorMessage = "Failed to evaluate answer";

      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;

        if (typeof detail === "string") {
          errorMessage = detail;
        } else if (Array.isArray(detail)) {
          errorMessage = detail
            .map((item) => item.msg || "Validation error")
            .join(", ");
        }
      }

      setEvaluationErrors((previousErrors) => ({
        ...previousErrors,
        [questionId]: errorMessage,
      }));
    } finally {
      setEvaluating((previousEvaluating) => ({
        ...previousEvaluating,
        [questionId]: false,
      }));
    }
  };

  return (
    <main className="page-container">
      <div className="interview-page">

        <section className="interview-hero">
          <div>
            <span className="interview-eyebrow">
              AI INTERVIEW COPILOT
            </span>

            <h1>
              Practice smarter.
              <br />
              <span>Interview with confidence.</span>
            </h1>

            <p>
              Generate personalized interview questions from your resume
              and target job description, then get AI-powered feedback
              on your answers.
            </p>
          </div>

          <div className="interview-hero-icon">
            <div className="ai-circle">
              AI
            </div>

            <span>Smart Practice</span>
          </div>
        </section>

        <section className="interview-workspace card">

          <div className="workspace-header">
            <div className="workspace-title">
              <div className="workspace-icon">
                ✦
              </div>

              <div>
                <h2>Interview Preparation</h2>
                <p>
                  Configure your practice session and generate
                  personalized questions.
                </p>
              </div>
            </div>

            <div className="workspace-status">
              AI Powered
            </div>
          </div>

          <div className="generator-content">

            <div className="generator-title">
              <h3>Generate Interview Questions</h3>

              <p>
                Choose your resume, job description, category,
                difficulty and number of questions.
              </p>
            </div>

            <form
              onSubmit={handleGenerate}
              className="interview-form"
            >

              <div className="interview-form-row">

                <div className="form-group">
                  <label>Resume</label>

                  <select
                    className="select"
                    value={resumeId}
                    onChange={(e) =>
                      setResumeId(e.target.value)
                    }
                    required
                  >
                    <option value="">
                      Select Resume
                    </option>

                    {resumes.map((resume) => (
                      <option
                        key={resume.id}
                        value={resume.id}
                      >
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
                    <option value="">
                      Select Job Description
                    </option>

                    {jobDescriptions.map((jd) => (
                      <option
                        key={jd.id}
                        value={jd.id}
                      >
                        {jd.original_filename}
                      </option>
                    ))}
                  </select>
                </div>

              </div>

              <div className="interview-form-row options-row">

                <div className="form-group">
                  <label>Category</label>

                  <select
                    className="select"
                    value={category}
                    onChange={(e) =>
                      setCategory(e.target.value)
                    }
                  >
                    <option value="technical">
                      Technical
                    </option>

                    <option value="project">
                      Project
                    </option>

                    <option value="behavioral">
                      Behavioral
                    </option>

                    <option value="situational">
                      Situational
                    </option>

                    <option value="conceptual">
                      Conceptual
                    </option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Difficulty</label>

                  <select
                    className="select"
                    value={difficulty}
                    onChange={(e) =>
                      setDifficulty(e.target.value)
                    }
                  >
                    <option value="easy">
                      Easy
                    </option>

                    <option value="medium">
                      Medium
                    </option>

                    <option value="hard">
                      Hard
                    </option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Question Count</label>

                  <input
                    className="input"
                    type="number"
                    min="1"
                    max="20"
                    value={questionCount}
                    onChange={(e) =>
                      setQuestionCount(e.target.value)
                    }
                  />
                </div>

              </div>

              <button
                className="btn btn-primary generate-btn"
                type="submit"
              >
                ✦ Generate Questions
              </button>

            </form>

            {message && (
              <div className="interview-message">
                <span>✓</span>
                {message}
              </div>
            )}

          </div>
        </section>

        <section className="generated-section">

          <div className="generated-heading">

            <div>
              <h2>Generated Questions</h2>

              <p>
                Practice each question and receive personalized
                AI feedback.
              </p>
            </div>

            {questions.length > 0 && (
              <span className="questions-count">
                {questions.length} Questions
              </span>
            )}

          </div>

          {questions.length === 0 ? (

            <div className="card empty-interview-state">

              <div className="empty-icon">
                ✦
              </div>

              <h3>No questions generated yet</h3>

              <p>
                Select a resume and job description above to
                start your interview practice session.
              </p>

            </div>

          ) : (

            <div className="question-list">

              {questions.map((item, index) => {

                const evaluation = evaluations[item.id];
                const isEvaluating = evaluating[item.id];
                const evaluationError =
                  evaluationErrors[item.id];

                return (
                  <article
                    className="question-card card"
                    key={item.id}
                  >

                    <div className="question-top">

                      <div className="question-number-badge">
                        {index + 1}
                      </div>

                      <div className="question-heading">

                        <span>
                          Question {index + 1}
                        </span>

                        <div className="question-meta">
                          <span>
                            {item.category}
                          </span>

                          <span>
                            {item.difficulty}
                          </span>

                          <span>
                            {item.question_type}
                          </span>
                        </div>

                      </div>

                    </div>

                    <h3 className="question-text">
                      {item.question}
                    </h3>

                    <div className="answer-area">

                      <label>Your Answer</label>

                      <textarea
                        className="textarea answer-textarea"
                        rows="6"
                        value={answers[item.id] || ""}
                        onChange={(e) =>
                          handleAnswerChange(
                            item.id,
                            e.target.value
                          )
                        }
                        placeholder="Write your answer here..."
                      />

                    </div>

                    <div className="question-actions">

                      <button
                        className="btn btn-primary"
                        type="button"
                        onClick={() =>
                          handleEvaluate(item.id)
                        }
                        disabled={isEvaluating}
                      >
                        {isEvaluating
                          ? "Evaluating..."
                          : "Evaluate Answer"}
                      </button>

                    </div>

                    {evaluationError && (
                      <div className="evaluation-error">
                        <strong>Error:</strong>{" "}
                        {evaluationError}
                      </div>
                    )}

                    {evaluation && (
                      <div className="evaluation-card">

                        <div className="evaluation-header">
                          <div>
                            <span>AI FEEDBACK</span>
                            <h3>Answer Evaluation</h3>
                          </div>

                          <div className="evaluation-score">
                            <strong>
                              {evaluation.score}
                            </strong>
                            <span>/10</span>
                          </div>
                        </div>

                        <div className="evaluation-grid">

                          <div className="evaluation-item">
                            <strong>Feedback</strong>
                            <p>
                              {evaluation.feedback}
                            </p>
                          </div>

                          <div className="evaluation-item">
                            <strong>Strengths</strong>
                            <p>
                              {evaluation.strengths}
                            </p>
                          </div>

                          <div className="evaluation-item">
                            <strong>Improvements</strong>
                            <p>
                              {evaluation.improvements}
                            </p>
                          </div>

                          <div className="evaluation-item">
                            <strong>Overall Result</strong>
                            <p>
                              {evaluation.overall_result}
                            </p>
                          </div>

                        </div>

                      </div>
                    )}

                  </article>
                );
              })}

            </div>
          )}

        </section>

      </div>
    </main>
  );
}