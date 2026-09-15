import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

const api = axios.create({
  baseURL: API_BASE_URL,
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

export default api;
