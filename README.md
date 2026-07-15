# OptiCrop

Smart Agricultural Production Optimization Engine — an AI-powered crop recommendation system that helps farmers make data-driven decisions.

Combines a **Random Forest model (99.55% accuracy)** with **Google Gemini 2.5 Flash** for detailed agricultural analysis, confidence scoring, and actionable insights.

## Repository Structure

```
OptiCrop/
├── code files/           # Application source code
│   ├── app/              # Flask web application
│   ├── dataset/          # Training data (Crop_recommendation.csv)
│   ├── notebooks/        # EDA & model training notebooks
│   ├── train_model.py    # Model training script
│   └── requirements.txt  # Python dependencies
├── demo video/           # Project demo walkthrough
└── Documentation/        # Full project documentation
    ├── 1. Brainstorming & Ideation/
    ├── 2. Requirement Analysis/
    ├── 3. Project Design Phase/
    ├── 4. Project Planning Phase/
    ├── 5. Project Development Phase/
    ├── 6. Project Testing/
    └── 7. Project Demonstration/
```

## Quick Start

```bash
cd "code files"
pip install -r requirements.txt
cd app
python app.py
```

Open **http://localhost:5000**

Set `GEMINI_API_KEY` environment variable (or `.env` file) for AI-powered analysis features.

## Features

- **ML Crop Prediction** — Random Forest model (99.55% accuracy) trained on 22 crops
- **Google Gemini AI Analysis** — Soil assessment, climate analysis, market demand insights
- **Confidence Scoring** — Every prediction includes % confidence for all alternatives
- **REST API** — JSON endpoint at `/api/predict`
- **Prediction History** — Session-based history (last 10 analyses)
- **Soil Gauges** — Visual NPK and pH level indicators

## Technologies

**Backend:** Python, Flask, Scikit-learn, NumPy, Joblib
**AI:** Google Gemini 2.5 Flash
**Frontend:** Custom CSS, Jinja2 templates
**ML Model:** Random Forest Classifier

## Documentation

The `Documentation/` folder contains 7 phases covering the full project lifecycle — from brainstorming and requirements through design, development, testing, and demonstration.
