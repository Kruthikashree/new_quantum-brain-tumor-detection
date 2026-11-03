Quantum Enhanced Deep Learning for Brain Tumor Detection

A hybrid quantum-classical deep learning system for automated brain tumor detection and classification from MRI scans using MobileNetV2, PennyLane, and PyTorch.

The system combines transfer learning and quantum machine learning to classify brain MRI images into four categories while providing explainable AI visualizations through occlusion-based heatmaps. Built as a full-stack web application, it enables secure report generation, doctor referrals, and PDF-based diagnostic reports.

📌 Table of Contents
Overview
Problem Statement
Proposed Solution
Key Features
System Architecture
Classification Pipeline
Technology Stack
Dataset
Model Performance
Application Workflow
Installation
Project Structure
Future Scope
Authors
📖 Overview

Brain tumor detection from MRI scans is challenging due to variations in tumor size, shape, and location. Traditional CNN-based systems often struggle with complex tumor boundaries and may require significant computational resources.

This project introduces a Hybrid Quantum-Classical Deep Learning Framework that combines:

MobileNetV2 Transfer Learning
Quantum Neural Networks
Explainable AI
Secure Web-Based Report Management

The goal is to improve classification accuracy while maintaining interpretability and usability in healthcare environments.

🎯 Problem Statement

Most brain tumor classification systems:

Rely purely on classical deep learning
Provide limited explainability
Lack secure clinical report management
Do not explore quantum-enhanced feature refinement

This project addresses these limitations by integrating a quantum refinement layer into a deep learning pipeline and delivering results through a secure web application.

💡 Proposed Solution

The proposed system:

Accepts Brain MRI scans.
Extracts features using MobileNetV2.
Reduces features using a classical neural network.
Refines features through a 4-qubit quantum circuit built using PennyLane.
Predicts the tumor category.
Generates an explainable heatmap showing influential image regions.
Creates a secure report accessible by assigned doctors through referral codes.
✨ Key Features

✅ Brain MRI Classification

Glioma
Meningioma
Pituitary Tumor
No Tumor

✅ Hybrid Quantum-Classical Deep Learning

✅ Explainable AI Heatmaps

✅ OTP-Based Authentication

✅ Doctor Referral Access System

✅ PDF Report Generation

✅ Role-Based Access Control

✅ Report History & Dashboard Analytics

✅ Email Notifications with Referral Codes

🏗️ System Architecture
Plain Text
React Frontend
│
▼
Flask Backend
│
┌─────────┴─────────┐
▼ ▼
MongoDB AI Pipeline
│
MobileNetV2 Feature Extractor
│
Feature Reduction
│
Quantum Layer
│
Classification Head
│
Prediction
│
Explainability Module
🧠 Classification Pipeline
Plain Text
MRI Scan
│
▼
Image Validation
│
▼
Preprocessing
│
▼
MobileNetV2 Feature Extraction
│
▼
Classical Feature Reduction
│
▼
4-Qubit Quantum Refinement Layer
│
▼
Classification Head
│
▼
Prediction
│
▼
Heatmap Generation
🧰 Technology Stack
Frontend
React
JavaScript
HTML
CSS
Vite
Backend
Flask
Python
Database
MongoDB
Deep Learning
TensorFlow / Keras
PyTorch
MobileNetV2
Quantum Computing
PennyLane
Lightning Qubit Simulator
Other Tools
Pillow
ReportLab
JWT
bcrypt
SMTP Email Services

📊 Dataset

Brain Tumor MRI Dataset (Kaggle)

Classes:

Glioma
Meningioma
Pituitary Tumor
No Tumor

Dataset Size:

Type	ImagesTraining	5,600
Testing	1,600

Images are resized to 224×224 before classification.

📈 Model Performance
Model	Validation AccuracyCNN (From Scratch)	65.94%
MobileNetV2	88.81%
MobileNetV2 + Quantum Layer	92.81%

The hybrid model achieved the highest classification accuracy among all tested approaches.

🔄 Application Workflow
Plain Text
User Registration
│
▼
Email OTP Verification
│
▼
Login
│
▼
Patient & Doctor Details
│
▼
MRI Upload
│
▼
AI Analysis
│
▼
Prediction + Heatmap
│
▼
Report Generation
│
▼
Referral Code Email
│
▼
Doctor Access & PDF Download
⚙️ Installation
Clone Repository
Shell
git clone https://github.com/your-username/quantum-brain-tumor-detection.git
cd quantum-brain-tumor-detection
Backend
Shell
cd backend
pip install -r requirements.txt
python app.py

Backend:

Plain Text
http://127.0.0.1:5000
Frontend
Shell
cd frontend
npm install
npm run dev

Frontend:

Plain Text
http://localhost:5173
📁 Project Structure
Plain Text
quantum-brain-tumor-detection
│
├── backend/
│ ├── app.py
│ ├── routes/
│ ├── models/
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ ├── public/
│ └── package.json
│
├── trained_models/
├── dataset/
└── README.md
🔮 Future Scope
Independent clinical validation
Tumor segmentation
Larger MRI datasets
Multilingual reports
PACS integration
Cloud deployment
Enhanced explainability methods

👨‍💻 Authors
Kruthikashree T
Manya C
Poojashree S

Guide: Mr. Kamleshwar Kumar Yadav

Department of Computer Science & Engineering
 Global Academy of Technology, Bengaluru.

⚠️ Disclaimer

This project is developed for academic and research purposes only and should not be used as a substitute for professional medical diagnosis.

🚀 Hybrid AI + Quantum Computing for Smarter Brain Tumor Detection 🧠⚛️

This style looks professional on GitHub, is concise, and is similar in structure to the Smart Campus README without being unnecessarily long.
