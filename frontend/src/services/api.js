import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Attach the login token to every request
api.interceptors.request.use((config) => {
  const stored = localStorage.getItem("user");
  if (stored) {
    try {
      const { token } = JSON.parse(stored);
      if (token) config.headers.Authorization = `Bearer ${token}`;
    } catch (e) {
      // ignore a corrupted value
    }
  }
  return config;
});

export const signup = async (name, email, password, role) => {
  const response = await api.post("/signup", { name, email, password, role });
  return response.data;
};

export const login = async (email, password) => {
  const response = await api.post("/login", { email, password });
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("user");
};

export const getCurrentUser = () => {
  const stored = localStorage.getItem("user");
  return stored ? JSON.parse(stored) : null;
};

export const saveCurrentUser = (userData) => {
  localStorage.setItem("user", JSON.stringify(userData));
};

export const predictImage = async (imageFile) => {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await api.post("/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const createPatient = async ({ patientName, patientAge, patientGender, labNotes, imageFile }) => {
  const formData = new FormData();
  formData.append("patient_name", patientName);
  formData.append("patient_age", patientAge);
  formData.append("patient_gender", patientGender);
  formData.append("lab_notes", labNotes || "");
  formData.append("image", imageFile);

  const response = await api.post("/patients", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getPatientByCode = async (accessCode) => {
  const response = await api.get(`/patients/code/${accessCode}`);
  return response.data;
};

export const generateResult = async (accessCode) => {
  const response = await api.post(`/patients/code/${accessCode}/generate-result`);
  return response.data;
};

export const listPatients = async () => {
  const response = await api.get("/patients");
  return response.data;
};

export const verifySignup = async (email, code) => {
  const response = await api.post("/verify-signup", { email, code });
  return response.data;
};

export const resendCode = async (email) => {
  const response = await api.post("/resend-code", { email });
  return response.data;
};

export const createReport = async (formData, onUploadProgress) => {
  const response = await api.post("/reports", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress,
  });
  return response.data;
};

export const listReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

export const getReport = async (id) => {
  const response = await api.get(`/reports/${id}`);
  return response.data;
};

export const lookupReport = async (code) => {
  const response = await api.post("/reports/lookup", { code });
  return response.data;
};

export const downloadReportPdf = async (id) => {
  const response = await api.get(`/reports/${id}/pdf`, { responseType: "blob" });
  return response.data;
};

export const resendReportEmails = async (id) => {
  const response = await api.post(`/reports/${id}/resend`);
  return response.data;
};

// If the session expired or is invalid, go back to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || "";
    if (error.response?.status === 401 && !url.includes("/login")) {
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
); 
export const forgotPassword = async (email) => {
  const response = await api.post("/forgot-password", { email });
  return response.data;
};

export const resetPassword = async (email, code, newPassword) => {
  const response = await api.post("/reset-password", {
    email,
    code,
    new_password: newPassword,
  });
  return response.data;
};
export const generateReportResult = async (id) => {
  const response = await api.post(`/reports/${id}/generate-result`);
  return response.data;
};
export default api;