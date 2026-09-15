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

  // Answer evaluation state
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

    // Clear old answer and evaluation data
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

    // Clear previous error when user edits the answer
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
        [questionId]:
          "Answer must be at least 10 characters long.",
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
    <div>
      <h1>Interview Preparation</h1>

      <h2>Generate Interview Questions</h2>

      <form onSubmit={handleGenerate}>
        <div>
          <label>Resume</label>
          <br />

          <select
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

        <br />

        <div>
          <label>Job Description</label>
          <br />

          <select
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

        <br />

        <div>
          <label>Category</label>
          <br />

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="technical">Technical</option>
            <option value="project">Project</option>
            <option value="behavioral">Behavioral</option>
            <option value="situational">Situational</option>
            <option value="conceptual">Conceptual</option>
          </select>
        </div>

        <br />

        <div>
          <label>Difficulty</label>
          <br />

          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <br />

        <div>
          <label>Question Count</label>
          <br />

          <input
            type="number"
            min="1"
            max="20"
            value={questionCount}
            onChange={(e) =>
              setQuestionCount(e.target.value)
            }
          />
        </div>

        <br />

        <button type="submit">
          Generate Questions
        </button>
      </form>

      <p>{message}</p>

      <hr />

      <h2>Generated Questions</h2>

      {questions.length === 0 ? (
        <p>No questions generated yet.</p>
      ) : (
        <ol>
          {questions.map((item) => {
            const evaluation = evaluations[item.id];
            const isEvaluating = evaluating[item.id];
            const evaluationError =
              evaluationErrors[item.id];

            return (
              <li key={item.id}>
                <p>
                  <strong>{item.question}</strong>
                </p>

                <p>
                  Category: {item.category} | Difficulty:{" "}
                  {item.difficulty} | Type:{" "}
                  {item.question_type}
                </p>

                <div>
                  <label>
                    <strong>Your Answer</strong>
                  </label>

                  <br />

                  <textarea
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

                <br />

                <button
                  type="button"
                  onClick={() => handleEvaluate(item.id)}
                  disabled={isEvaluating}
                >
                  {isEvaluating
                    ? "Evaluating..."
                    : "Evaluate Answer"}
                </button>

                {evaluationError && (
                  <p>
                    <strong>Error:</strong>{" "}
                    {evaluationError}
                  </p>
                )}

                {evaluation && (
                  <div>
                    <hr />

                    <h3>Evaluation</h3>

                    <p>
                      <strong>Score:</strong>{" "}
                      {evaluation.score}/10
                    </p>

                    <p>
                      <strong>Feedback:</strong>{" "}
                      {evaluation.feedback}
                    </p>

                    <p>
                      <strong>Strengths:</strong>{" "}
                      {evaluation.strengths}
                    </p>

                    <p>
                      <strong>Improvements:</strong>{" "}
                      {evaluation.improvements}
                    </p>

                    <p>
                      <strong>Overall Result:</strong>{" "}
                      {evaluation.overall_result}
                    </p>
                  </div>
                )}

                <br />
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}