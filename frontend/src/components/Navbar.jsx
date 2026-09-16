import { NavLink, useLocation, useNavigate } from "react-router-dom";

function HomeIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 10.5L12 3l9 7.5" />
      <path d="M5.5 9.5V21h13V9.5" />
      <path d="M9.5 21v-6h5v6" />
    </svg>
  );
}

function InterviewIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M8 9h8" />
      <path d="M8 13h5" />
      <path d="M8 17h3" />
    </svg>
  );
}

function HistoryIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </svg>
  );
}

function ResumeIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 3h9l3 3v15H6z" />
      <path d="M14 3v4h4" />
      <path d="M9 12h6" />
      <path d="M9 16h6" />
    </svg>
  );
}

function JobIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="3" y="7" width="18" height="13" rx="2" />
      <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <path d="M3 12h18" />
    </svg>
  );
}

function LogoutIcon() {
  return (
    <svg
      width="17"
      height="17"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M10 17l5-5-5-5" />
      <path d="M15 12H3" />
      <path d="M21 19V5a2 2 0 0 0-2-2h-6" />
      <path d="M13 21h6a2 2 0 0 0 2-2" />
    </svg>
  );
}

function ChevronDownIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const publicRoutes = ["/", "/login", "/register"];
  const isPublicRoute = publicRoutes.includes(location.pathname);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login", { replace: true });
  };

  if (isPublicRoute) {
    return (
      <nav className="navbar public-navbar">
        <div className="navbar-inner">
          <NavLink to="/" end className="navbar-brand">
            <span className="brand-mark">AI</span>
            <span>AI Interview Copilot</span>
          </NavLink>

          <div className="navbar-links">
            <NavLink to="/" end className="navbar-link">
              Home
            </NavLink>

            <NavLink to="/login" className="navbar-link">
              Login
            </NavLink>

            <NavLink to="/register" className="navbar-link">
              Register
            </NavLink>
          </div>
        </div>
      </nav>
    );
  }

  const linkClass = ({ isActive }) =>
    `sidebar-link ${isActive ? "active" : ""}`;

  return (
    <aside className="app-sidebar">
      <div className="sidebar-top">
        <NavLink to="/dashboard" className="sidebar-brand">
          <span className="sidebar-brand-icon">AI</span>

          <span className="sidebar-brand-text">
            AI Interview
            <br />
            Copilot
          </span>
        </NavLink>

        <nav className="sidebar-navigation">
          <NavLink to="/dashboard" className={linkClass}>
            <HomeIcon />
            <span>Home</span>
          </NavLink>

          <NavLink to="/interview" className={linkClass}>
            <InterviewIcon />
            <span>Interview Preparation</span>
          </NavLink>

          <NavLink to="/history" className={linkClass}>
            <HistoryIcon />
            <span>History</span>
          </NavLink>

          <NavLink to="/resume" className={linkClass}>
            <ResumeIcon />
            <span>Resume</span>
          </NavLink>

          <NavLink to="/job-description" className={linkClass}>
            <JobIcon />
            <span>Job Description</span>
          </NavLink>
        </nav>
      </div>

      <div className="sidebar-bottom">
        <div className="sidebar-profile">
          <div className="profile-avatar">A</div>

          <div className="profile-info">
            <strong>Arhan</strong>
            <span>Student</span>
          </div>

          <ChevronDownIcon />
        </div>

        <button
          type="button"
          className="sidebar-logout"
          onClick={handleLogout}
        >
          <LogoutIcon />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}