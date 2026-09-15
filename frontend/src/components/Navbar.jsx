import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <NavLink to="/" end>
        Home
      </NavLink>

      {" | "}

      <NavLink to="/login">
        Login
      </NavLink>

      {" | "}

      <NavLink to="/register">
        Register
      </NavLink>

      {" | "}

      <NavLink to="/dashboard">
        Dashboard
      </NavLink>

      {" | "}

      <NavLink to="/resume">
        Resume
      </NavLink>

      {" | "}

      <NavLink to="/job-description">
        Job Description
      </NavLink>

      {" | "}

      <NavLink to="/interview">
        Interview
      </NavLink>

      {" | "}

      <NavLink to="/history">
        History
      </NavLink>
    </nav>
  );
}