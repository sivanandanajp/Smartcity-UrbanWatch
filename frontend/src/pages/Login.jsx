import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const navigate = useNavigate();

  const handleLogin = () => {

    if (
      username === "admin" &&
      password === "urbanwatch123"
    ) {

      localStorage.setItem(
        "isLoggedIn",
        "true"
      );

      navigate("/");
    }

    else {

      alert(
        "Invalid credentials"
      );

    }
  };

  return (
  <div
  style={{
    width: "100vw",
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f2f2f2",
  }}
>
    <div
  style={{
    width: "240px",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  }}
>
      <h1
  style={{
    fontSize: "50px",
    fontWeight: "bold",
    marginBottom: "10px",
    borderBottom: "2px solid #5b5bd6",
    width: "90px",
  }}
>
  Login
</h1>

      <input
        type="text"
        placeholder="👤 Adminname"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{
          border: "none",
          borderBottom: "1px solid #666",
          background: "transparent",
          padding: "8px 0",
          outline: "none",
          fontSize: "14px",
        }}
      />

      <input
        type="password"
        placeholder="🔒 Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{
          border: "none",
          borderBottom: "1px solid #666",
          background: "transparent",
          padding: "8px 0",
          outline: "none",
          fontSize: "14px",
        }}
      />

      <button
        onClick={handleLogin}
        style={{
          background: "#0a0aa8",
          color: "white",
          border: "none",
          padding: "10px",
          borderRadius: "4px",
          cursor: "pointer",
          fontSize: "14px",
          marginTop: "5px",
        }}
      >
        Sign In
      </button>
    </div>
  </div>
);
}

export default Login;