import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signup, verifySignup, resendCode } from "../services/api";
import "./Auth.css";

function Signup() {
  const navigate = useNavigate();

  const [step, setStep] = useState("form"); // "form" or "verify"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("lab");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [cooldown, setCooldown] = useState(0);

  // Countdown for the "Resend code" button
  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown(cooldown - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const getError = (err, fallback) =>
    err.response?.data?.error || fallback;

  // Step 1: send the code
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await signup(name, email, password, role);
      setStep("verify");
      setCooldown(30);
      setSuccess(`We sent a 6-digit code to ${email}`);
    } catch (err) {
      setError(getError(err, "Signup failed. Please try again."));
    } finally {
      setLoading(false);
    }
  };

  // Step 2: check the code
  const handleVerify = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await verifySignup(email, code);
      setSuccess("Email verified! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(getError(err, "Verification failed. Please try again."));
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError("");
    setSuccess("");
    try {
      await resendCode(email);
      setCooldown(30);
      setCode("");
      setSuccess("A new code has been sent.");
    } catch (err) {
      setError(getError(err, "Could not resend the code."));
    }
  };

  // ---------- Verify screen ----------
  if (step === "verify") {
    return (
      <div className="auth-page">
        <form className="auth-card" onSubmit={handleVerify}>
          <h1>Verify Your Email</h1>
          <p className="auth-subtitle">
            Enter the 6-digit code we sent to {email}
          </p>

          {error && <div className="auth-error">{error}</div>}
          {success && <div className="auth-success">{success}</div>}

          <label>Verification Code</label>
          <input
            className="otp-input"
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={6}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
            placeholder="123456"
            required
          />

          <button
            type="submit"
            className="auth-btn"
            disabled={loading || code.length !== 6}
          >
            {loading ? "Verifying..." : "Verify & Create Account"}
          </button>

          <p className="auth-switch">
            Didn't get it?{" "}
            {cooldown > 0 ? (
              <span>Resend in {cooldown}s</span>
            ) : (
              <button
                type="button"
                className="link-btn"
                onClick={handleResend}
              >
                Resend code
              </button>
            )}
          </p>

          <p className="auth-switch">
            <button
              type="button"
              className="link-btn"
              onClick={() => {
                setStep("form");
                setError("");
                setSuccess("");
                setCode("");
              }}
            >
              Use a different email
            </button>
          </p>
        </form>
      </div>
    );
  }

  // ---------- Signup form ----------
  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <p className="auth-subtitle">Sign up to get started</p>

        {error && <div className="auth-error">{error}</div>}

        <label>I am a</label>
        <div className="role-toggle">
          <button
            type="button"
            className={`role-option ${role === "lab" ? "active" : ""}`}
            onClick={() => setRole("lab")}
          >
            Laboratory Staff
          </button>
          <button
            type="button"
            className={`role-option ${role === "doctor" ? "active" : ""}`}
            onClick={() => setRole("doctor")}
          >
            Doctor
          </button>
        </div>

        <label>Full Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Jane Doe"
          required
        />

        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          minLength={6}
          required
        />

        <button type="submit" className="auth-btn" disabled={loading}>
          {loading ? "Sending code..." : "Sign Up"}
        </button>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </form>
    </div>
  );
}

export default Signup;