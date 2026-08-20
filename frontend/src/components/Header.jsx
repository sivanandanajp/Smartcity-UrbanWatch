import "../styles/header.css";
import { useNavigate } from "react-router-dom";

function Header({

  searchTerm,
  setSearchTerm

}) {

  const navigate =
    useNavigate();

  const logout = () => {

    localStorage.removeItem(
      "isLoggedIn"
    );

    navigate("/login");
  };

  return (

    <div className="header">

      <div>

        <h1>
          Dashboard
        </h1>

        <p>
          Urban Traffic Intelligence System
        </p>

      </div>

      <div className="search-box">

        <input

          type="text"

          placeholder="Search Junction..."

          value={searchTerm}

          onChange={(e) =>
            setSearchTerm(
              e.target.value
            )
          }

        />

        <button
          className="export-btn"
          onClick={logout}
        >
          Logout
        </button>

      </div>

    </div>

  );
}

export default Header;