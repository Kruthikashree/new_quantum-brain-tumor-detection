# 🧠 Quantum Enhanced Deep Learning for Brain Tumor Detection

### A Hybrid Quantum-Classical Deep Learning Framework for Brain MRI Classification

An intelligent brain tumor detection system that combines **MobileNetV2, Quantum Machine Learning, and Explainable AI** to classify brain MRI scans into four categories. The system integrates a quantum-enhanced deep learning pipeline with a secure full-stack web application for MRI analysis, report generation, and doctor referrals.

---

## 📌 Table of Contents

1. [Overview](#-overview)
2. [Problem Statement](#-problem-statement)
3. [Proposed Solution](#-proposed-solution)
4. [Key Features](#-key-features)
5. [System Architecture](#-system-architecture)
6. [Classification Pipeline](#-classification-pipeline)
7. [Technology Stack](#-technology-stack)
8. [Dataset](#-dataset)
9. [Model Performance](#-model-performance)
10. [Application Workflow](#-application-workflow)
11. [Installation and Setup](#-installation-and-setup)
12. [Project Structure](#-project-structure)
13. [Future Enhancements](#-future-enhancements)
14. [Authors](#-authors)
15. [Disclaimer](#-disclaimer)

---

## 📖 Overview

Brain tumor detection from Magnetic Resonance Imaging (MRI) scans is a challenging task due to variations in tumor size, shape, texture, and location. Conventional deep learning approaches can identify tumor patterns, but their decision-making processes may be difficult to interpret.

To address these challenges, this project introduces a **Hybrid Quantum-Classical Deep Learning Framework** that combines the feature extraction capabilities of MobileNetV2 with quantum-based feature refinement using PennyLane.

The proposed system also incorporates Explainable AI techniques to generate occlusion-based heatmaps, helping users visualize the image regions that influence the model's predictions.

A full-stack web application provides an integrated platform for MRI classification, secure user authentication, patient report management, and doctor referral access.

## 🎯 Problem Statement

Existing brain tumor classification systems often face several limitations:

- Dependence on conventional classical deep learning architectures.
- Limited interpretability of model predictions.
- Difficulty understanding which image regions influence classification.
- Lack of integrated and secure medical report management.
- Limited exploration of quantum machine learning for feature refinement.

This project aims to address these challenges through a hybrid quantum-classical architecture combined with an explainable and secure web-based application.

## 💡 Proposed Solution

The proposed system follows a hybrid AI pipeline to analyze brain MRI images.

1. Accepts brain MRI images through a web-based interface.
2. Validates and preprocesses the uploaded images.
3. Extracts visual features using MobileNetV2.
4. Reduces the extracted features using a classical neural network.
5. Processes the reduced features through a 4-qubit quantum circuit implemented using PennyLane.
6. Uses a classification head to predict the brain tumor category.
7. Generates occlusion-based heatmaps to explain influential image regions.
8. Generates PDF-based diagnostic reports.
9. Provides secure report access to assigned doctors through referral codes.

## ✨ Key Features

### 🧠 AI-Based Brain Tumor Classification

Classifies brain MRI images into four categories:

- Glioma
- Meningioma
- Pituitary Tumor
- No Tumor

### ⚛️ Hybrid Quantum-Classical Learning

- MobileNetV2-based feature extraction.
- Classical neural network for feature reduction.
- 4-qubit quantum refinement circuit.
- Quantum-enhanced classification pipeline.

### 🔍 Explainable AI

- Occlusion-based heatmap generation.
- Visual representation of influential image regions.
- Improved interpretability of model predictions.

### 🔐 Secure Web Application

- User registration and email OTP verification.
- Secure login and authentication.
- Role-based access control.
- Patient and doctor information management.

### 📄 Report Management

- Automated PDF report generation.
- Report history and dashboard analytics.
- Doctor referral access using unique referral codes.
- Email notifications containing referral information.

## 🏗️ System Architecture

The application follows a modular architecture consisting of a React frontend, Flask backend, MongoDB database, and hybrid AI processing pipeline.

```text
                 React Frontend
                       |
                       v
                  Flask Backend
                       |
          +------------+------------+
          |                         |
          v                         v
      MongoDB                  AI Pipeline
                                    |
                                    v
                         MobileNetV2 Feature
                              Extraction
                                    |
                                    v
                          Classical Feature
                              Reduction
                                    |
                                    v
                           Quantum Layer
                          (4-Qubit Circuit)
                                    |
                                    v
                           Classification
                                  Head
                                    |
                                    v
                               Prediction
                                    |
                                    v
                          Explainability
                              Module
                                    |
                                    v
                          Heatmap Generation
```

## 🧠 Classification Pipeline

The hybrid classification process consists of the following stages:

```text
             Brain MRI Image
                    |
                    v
              Image Upload
                    |
                    v
              Image Validation
                    |
                    v
               Preprocessing
              (224 x 224)
                    |
                    v
          MobileNetV2 Feature Extraction
                    |
                    v
           Classical Feature Reduction
                    |
                    v
          4-Qubit Quantum Refinement
                    |
                    v
             Classification Head
                    |
                    v
             Predicted Category
                    |
                    v
            Explainability Module
                    |
                    v
           Occlusion-Based Heatmap
```

## 🧰 Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, HTML, CSS, Vite |
| Backend | Python, Flask |
| Database | MongoDB |
| Deep Learning | TensorFlow, Keras, PyTorch |
| Feature Extraction | MobileNetV2 |
| Quantum Computing | PennyLane, Lightning Qubit Simulator |
| Explainable AI | Occlusion-Based Heatmaps |
| Authentication | JWT, bcrypt, Email OTP |
| Image Processing | Pillow |
| PDF Generation | ReportLab |
| Communication | SMTP Email Services |

## 📊 Dataset

The project uses a **Brain Tumor MRI Dataset from Kaggle**, containing MRI images belonging to four classification categories.

| Dataset Category | Number of Images |
|---|---:|
| Training | 5,600 |
| Testing | 1,600 |
| **Total** | **7,200** |

### Classification Categories

- Glioma
- Meningioma
- Pituitary Tumor
- No Tumor

All MRI images are resized to **224 × 224 pixels** before being passed to the classification pipeline.

## 📈 Model Performance

Three different approaches were evaluated to compare their validation accuracy.

| Model Architecture | Validation Accuracy |
|---|---:|
| CNN (From Scratch) | 65.94% |
| MobileNetV2 | 88.81% |
| MobileNetV2 + Quantum Layer | **92.81%** |

### Performance Comparison

The MobileNetV2 model enhanced with the quantum refinement layer achieved the highest reported validation accuracy among the evaluated approaches.

This demonstrates the potential of combining classical deep learning with quantum machine learning for brain MRI classification.

## 🔄 Application Workflow

The web application provides an end-to-end workflow for users and doctors.

```text
                 User Registration
                        |
                        v
                Email OTP Verification
                        |
                        v
                       Login
                        |
                        v
             Patient and Doctor Details
                        |
                        v
                   MRI Upload
                        |
                        v
                  AI Analysis
                        |
                        v
              Tumor Classification
                        |
                        v
               Heatmap Generation
                        |
                        v
                PDF Report Creation
                        |
                        v
             Referral Code via Email
                        |
                        v
               Doctor Report Access
                        |
                        v
                 PDF Download
```

## ⚙️ Installation and Setup

Follow the steps below to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Kruthikashree/new_quantum-brain-tumor-detection.git
```

```bash
cd new_quantum-brain-tumor-detection
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

**Windows:**

```bash
python -m venv bt
bt\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask backend:

```bash
python app.py
```

Backend URL:

```text
http://127.0.0.1:5000
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

### 4. Environment Configuration

Configure the required environment variables for services such as MongoDB, email authentication, JWT, and other application settings.

Do not upload passwords, API keys, database credentials, or secret keys to GitHub. Use environment variables and keep sensitive configuration in a `.env` file excluded through `.gitignore`.

## 📁 Project Structure

```text
new_quantum-brain-tumor-detection/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── database/
│   ├── src/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── README.md
└── ...
```

*Note: This is a simplified representation of the main project directories.*

## 🔮 Future Enhancements

The project can be extended through the following improvements:

- Clinical validation using larger and more diverse MRI datasets.
- Integration of tumor segmentation techniques.
- Evaluation across additional quantum circuit architectures.
- Multilingual diagnostic reports.
- Integration with Picture Archiving and Communication Systems (PACS).
- Improved explainability using additional XAI techniques.
- Scalable cloud deployment and performance optimization.

## 👨‍💻 Authors

**Kruthikashree T**  
**Manya C**  
**Poojashree S**

**Project Guide:** Mr. Kamleshwar Kumar Yadav

Department of Computer Science and Engineering  
Global Academy of Technology, Bengaluru.

## ⚠️ Disclaimer

This project is developed strictly for academic and research purposes. The predictions generated by the system are experimental and should not be considered a substitute for professional medical diagnosis, clinical evaluation, or advice from qualified healthcare professionals.

---

<p align="center">
  <b>🚀 Hybrid AI + Quantum Computing for Smarter Brain Tumor Detection 🧠⚛️</b>
</p>

<p align="center">
  <i>Exploring the potential of quantum-enhanced deep learning in medical image analysis.</i>
</p>
