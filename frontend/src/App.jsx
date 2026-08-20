import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import About from "./pages/About";
import Login from "./pages/Login";

import ProtectedRoute from "./components/ProtectedRoute";

import {
  Routes,
  Route,
  useLocation
} from "react-router-dom";

import "./styles/app.css";

function App() {

  const location =
    useLocation();

  return (

    <div className="app">

      {

        location.pathname !== "/login"

        &&

        <Sidebar />

      }

      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />


        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          }
        />

        <Route
          path="/about"
          element={
            <ProtectedRoute>
              <About />
            </ProtectedRoute>
          }
        />

      </Routes>

    </div>

  );

}

export default App;