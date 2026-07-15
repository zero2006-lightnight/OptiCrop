# OptiCrop

Smart Agricultural Production Optimization Engine — an AI-powered crop recommendation system that helps farmers make data-driven decisions.

Combines a **Random Forest model (99.55% accuracy)** with **Google Gemini 2.5 Flash** for detailed agricultural analysis, confidence scoring, and actionable insights.

## Project Structure

```
OptiCrop/
├── dataset/
│   └── Crop_recommendation.csv    # 2200 records, 22 crops
├── notebooks/
│   └── OptiCrop_Model.ipynb       # EDA + Model Training
├── app/
│   ├── app.py                     # Flask application
│   ├── model.pkl                  # Trained Random Forest model
│   ├── templates/
│   │   ├── index.html             # Home page with hero, stats, features
│   │   ├── about.html             # Mission, how-it-works, values
│   │   ├── find_your_crop.html    # Prediction form + results
│   │   ├── history.html           # Prediction history
│   │   └── partials/
│   │       └── nav.html           # Shared navigation component
│   └── static/
│       └── style.css              # Custom CSS design system
├── Demo video/                    # Screenshot walkthrough
├── .env                           # Environment variables (GEMINI_API_KEY)
├── requirements.txt
└── README.md
```

## Setup

1. Clone and install:
```bash
pip install -r requirements.txt
```

2. Set your **Google Gemini API key** (optional — ML predictions work without it, AI analysis features require it):
```bash
# Linux / macOS
export GEMINI_API_KEY="your-api-key"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"

# Or create a .env file in the project root:
#   GEMINI_API_KEY=your-api-key
```

3. Run the app:
```bash
cd app
python app.py
```

4. Open **http://localhost:5000**

## Features

- **ML Crop Prediction** — Random Forest model trained on 22 crops, provides confidence scores for all alternatives
- **Google Gemini AI Analysis** — Detailed soil analysis, climate assessment, practical tips, market demand, and expected yield
- **Confidence Scoring** — Every prediction includes a % confidence score
- **Input Validation** — Server-side range checking with clear error messages
- **Prediction History** — Session-based history of past analyses (last 10)
- **Soil Gauges** — Visual bar charts showing NPK and pH levels
- **REST API** — JSON endpoint at `/api/predict` for programmatic access
- **Custom UI** — Earth-tone design with Fraunces/Inter/JetBrains Mono typography, responsive layout, scroll-triggered animations

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home page with hero, animated stats, feature grid |
| `/find_your_crop` | Soil analysis form and prediction results |
| `/history` | Past prediction history |
| `/about` | Mission, how-it-works, values |
| `/api/predict` | REST API (POST JSON) |
| `/api/crops` | List all supported crops |
| `/clear-history` | Clear session history (JSON) |

## Input Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| Nitrogen (N) | 0–140 | kg/ha | Nitrogen content in soil |
| Phosphorus (P) | 5–145 | kg/ha | Phosphorus content in soil |
| Potassium (K) | 5–205 | kg/ha | Potassium content in soil |
| Temperature | 8–44 | °C | Ambient temperature |
| Humidity | 10–100 | % | Relative humidity |
| pH | 3.5–9.9 | — | Soil pH value |
| Rainfall | 20–300 | mm | Rainfall amount |

## REST API

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 90, "phosphorus": 42, "potassium": 43,
    "temperature": 20, "humidity": 80, "ph": 6.5, "rainfall": 200
  }'
```

Returns prediction, confidence scores, crop info, AI analysis, and validation ranges.

## Technologies

- **Backend:** Python, Flask, Scikit-learn, NumPy, Joblib
- **AI:** Google Gemini 2.5 Flash (google-genai SDK)
- **Frontend:** Custom CSS, Jinja2 templates, Google Fonts
- **ML Model:** Random Forest (99.55% accuracy)

## Model Performance

| Model | Accuracy |
|-------|----------|
| Random Forest | 99.55% |
| KNN | 97.95% |
| Decision Tree | 97.95% |
| Logistic Regression | 97.27% |
