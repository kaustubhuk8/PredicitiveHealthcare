# Predictive Healthcare Analytics System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-61DAFB.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A machine learning system for predicting patient readmission risks and healthcare outcomes.

## Features

- **Machine Learning Model**: Predicts patient readmission risks using clinical data
- **REST API Backend**: Flask-based API for model serving
- **React Frontend**: Interactive dashboard for visualization
- **Data Pipeline**: Tools for data preprocessing and feature engineering

## System Architecture

```mermaid
graph TD
    A[Frontend - React] -->|API Calls| B[Backend - Flask]
    B -->|Predictions| C[Machine Learning Model]
    C --> D[Training Data]
    D --> E[Data Preprocessing]
```

## Installation

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Usage

1. Start backend server:
```bash
cd backend
flask run --port=5000
```

2. Start frontend development server:
```bash
cd frontend
npm start
```

3. Access the application at: `http://localhost:3000`

## Project Structure

```
Predictive-Health-Care-analysis/
├── backend/               # Flask API and model serving
│   ├── app.py            # Main application
│   ├── requirements.txt  # Python dependencies
├── frontend/             # React dashboard
│   ├── public/           # Static assets
│   ├── src/              # React components
├── model.py              # ML model training code
├── data_generator.py     # Data preprocessing
└── README.md             # Project documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
