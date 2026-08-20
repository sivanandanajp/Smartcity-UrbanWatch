import { NavLink } from "react-router-dom";

import "../styles/sidebar.css";

function Sidebar() {

  return (

    <div className="sidebar">

      <h2 className="logo">
        UrbanWatch
      </h2>

      <ul className="menu">

        <li>

          <NavLink
            to="/"
            className={({isActive}) =>
              isActive
              ? "active-link"
              : ""
            }
          >
            Dashboard
          </NavLink>

        </li>

        

        

        

        <li>

          <NavLink
            to="/analytics"
            className={({isActive}) =>
              isActive
              ? "active-link"
              : ""
            }
          >
            Analytics
          </NavLink>

        </li>

        <li>

          <NavLink
            to="/about"
            className={({isActive}) =>
              isActive
              ? "active-link"
              : ""
            }
          >
            About
          </NavLink>

        </li>


      </ul>

    </div>

  );

}

export default Sidebar;