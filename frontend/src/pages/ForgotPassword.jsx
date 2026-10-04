import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { forgotPassword, resetPassword } from "../services/api";
import "./Auth.css";

function ForgotPassword() {
  const navigate = useNavigate();

  const [step, setStep] = useState("request"); // "request" or "reset"
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [cooldown, setCooldown] = useState(0);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown(cooldown - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const getError = (err, fallback) => err.response?.data?.error || fallback;

  const handleRequest = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await forgotPassword(email);
      setStep("reset");
      setCooldown(30);
      setSuccess(data.message);
    } catch (err) {
      setError(getError(err, "Something went wrong. Please try again."));
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError("");
    try {
      const data = await forgotPassword(email);
      setCooldown(30);
      setCode("");
      setSuccess(data.message);
    } catch (err) {
      setError(getError(err, "Could not resend the code."));
    }
  };

  const handleReset = async (e) => {
    e.preventDefault();
    setError("");

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await resetPassword(email, code, newPassword);
      setSuccess("Password reset! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(getError(err, "Could not reset the password."));
    } finally {
      setLoading(false);
    }
  };

  if (step === "reset") {
    return (
      <div className="auth-page">
        <form className="auth-card" onSubmit={handleReset}>
          <h1>Reset Password</h1>
          <p className="auth-subtitle">
            Enter the 6-digit code sent to {email}, then choose a new password
          </p>

          {error && <div className="auth-error">{error}</div>}
          {success && <div className="auth-success">{success}</div>}

          <label>Verification Code</label>
          <input
            className="otp-input"
            type="text"
            inputMode="numeric"
            maxLength={6}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
            placeholder="123456"
            required
          />

          <label>New Password</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="••••••••"
            minLength={6}
            required
          />

          <label>Confirm New Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="••••••••"
            minLength={6}
            required
          />

          <button
            type="submit"
            className="auth-btn"
            disabled={loading || code.length !== 6}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>

          <p className="auth-switch">
            Didn't get it?{" "}
            {cooldown > 0 ? (
              <span>Resend in {cooldown}s</span>
            ) : (
              <button type="button" className="link-btn" onClick={handleResend}>
                Resend code
              </button>
            )}
          </p>

          <p className="auth-switch">
            <button
              type="button"
              className="link-btn"
              onClick={() => {
                setStep("request");
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

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleRequest}>
        <h1>Forgot Password</h1>
        <p className="auth-subtitle">
          Enter your account email and we'll send you a reset code
        </p>

        {error && <div className="auth-error">{error}</div>}

        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />

        <button type="submit" className="auth-btn" disabled={loading}>
          {loading ? "Sending code..." : "Send Reset Code"}
        </button>

        <p className="auth-switch">
          Remembered your password? <Link to="/login">Log in</Link>
        </p>
      </form>
    </div>
  );
}

export default ForgotPassword;