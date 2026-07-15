# OptiCrop — Smart Agricultural Production Optimization Engine

**OptiCrop** is a machine learning-powered crop recommendation system that analyzes soil composition and environmental conditions to recommend the most suitable crop for cultivation. The platform combines a high-accuracy Random Forest classifier with Google Gemini 2.5 Flash for generative AI analysis, delivering probabilistic confidence scores, crop-specific insights, and actionable farming recommendations.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [ML Pipeline](#ml-pipeline)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Application Routes](#application-routes)
- [Design System](#design-system)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Documentation](#documentation)

---

## Problem Statement

Farmers face significant challenges in determining the most suitable crop for their land based on soil nutrients and climatic conditions, leading to suboptimal yields and financial losses. OptiCrop addresses this by providing data-driven, AI-powered crop recommendations using seven key environmental parameters: nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall.

### Expected Outcomes

1. Recommend the most suitable crop for given soil and environmental conditions
2. Maximize yields and resource efficiency through data-driven decisions
3. Support sustainable agricultural practices
4. Provide intelligent recommendations accessible to farmers without technical expertise

---

## System Architecture

### Prediction Engine

The core prediction pipeline processes seven soil and climate parameters through a trained Random Forest classifier:

```
Input Parameters → StandardScaler → Random Forest Model → Label Decoding → Prediction + Confidence Scores
```

**Input Features:**
| Parameter      | Range      | Unit    |
|----------------|------------|---------|
| Nitrogen (N)   | 0–140      | kg/ha   |
| Phosphorus (P) | 5–145      | kg/ha   |
| Potassium (K)  | 5–205      | kg/ha   |
| Temperature    | 8–44       | °C      |
| Humidity       | 10–100     | %       |
| pH             | 3.5–9.9    | —       |
| Rainfall       | 20–300     | mm      |

### AI Analysis Layer

When a Google Gemini API key is configured, the system augments ML predictions with generative AI analysis including:
- **Soil Assessment** — Detailed evaluation of NPK levels and pH balance
- **Climate Evaluation** — Temperature, humidity, and rainfall suitability analysis
- **Market Demand Insights** — Crop market potential assessment
- **Actionable Recommendations** — Practical farming tips and best practices

---

## ML Pipeline

### Dataset

The model is trained on the [Crop Recommendation Dataset](https://www.kaggle.com/) containing 2,200 records across 22 crop classes with 7 feature dimensions.

### Supported Crops

Rice, Wheat, Maize, Cotton, Sugarcane, Jute, Coffee, Coconut, Papaya, Orange, Apple, Muskmelon, Watermelon, Grapes, Mango, Banana, Pomegranate, Lentil, Blackgram, Mungbean, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Gram

### Model Training

Four classifiers were evaluated using stratified train-test split (80:20) with standard scaling:

| Model               | Accuracy |
|---------------------|----------|
| **Random Forest**   | **99.55%** |
| K-Nearest Neighbors | 97.95%   |
| Decision Tree       | 97.95%   |
| Logistic Regression | 97.27%   |

The Random Forest classifier (n_estimators=100) was selected as the production model. The complete training pipeline includes label encoding, feature scaling, and model serialization via joblib.

### Prediction Output

Each prediction returns:
1. **Primary Recommendation** — The most likely crop with confidence percentage
2. **Confidence Distribution** — Probabilistic scores for all 22 crops
3. **Top Alternatives** — Next-best crop options with scores
4. **Crop Information** — Growing season, water requirements, optimal temperature range

---

## Installation

### Prerequisites

- Python 3.8 or later
- Pip package manager

### Setup

```bash
# Navigate to the application directory
cd "code files"

# Install dependencies
pip install -r requirements.txt

# Launch the application
cd app
python app.py
```

The server starts at `http://localhost:5000`.

---

## Configuration

### Google Gemini Integration (Optional)

ML-based predictions function without configuration. For AI-powered analysis features, set your Gemini API key:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key"

# Linux / macOS
export GEMINI_API_KEY="your-api-key"

# Or create a .env file in the app directory:
#   GEMINI_API_KEY=your-api-key
```

---

## Usage

### Web Interface

Navigate to `http://localhost:5000` and use the **Find Your Crop** form to input soil parameters:

1. Enter Nitrogen (N), Phosphorus (P), Potassium (K) levels in kg/ha
2. Input ambient temperature (°C) and relative humidity (%)
3. Provide soil pH value and rainfall (mm)
4. Select optional region/crop type filter
5. Submit for analysis

Results display the recommended crop, confidence score, alternative crop options, crop-specific growing information, and (when configured) AI-generated soil and climate analysis with visual NPK gauges.

### Prediction History

Session-based history retains the last 10 analyses, accessible via the **History** page. Each entry includes input parameters, predicted crop, confidence score, and AI analysis summary.

---

## API Reference

### POST `/api/predict`

Submit soil parameters and receive a complete prediction response.

**Request:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200
  }'
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "crop": "rice",
    "confidence": 98.5,
    "crop_info": {
      "season": "Kharif",
      "water": "High",
      "temp_range": "20-30°C"
    }
  },
  "ai_analysis": { /* present if Gemini is configured */ },
  "all_scores": { /* top 10 crop probabilities */ },
  "input_ranges": { /* validation constraints */ }
}
```

### GET `/api/crops`

Returns all supported crops with metadata.

```bash
curl http://localhost:5000/api/crops
```

### GET `/clear-history`

Clears the current session prediction history.

---

## Application Routes

| Route               | Method | Description                                |
|---------------------|--------|--------------------------------------------|
| `/`                 | GET    | Home page with hero, statistics, features  |
| `/find_your_crop`   | GET/POST | Soil analysis form and prediction results |
| `/about`            | GET    | Mission, how-it-works, core values         |
| `/history`          | GET    | Session prediction history                 |
| `/api/predict`      | POST   | REST API for crop prediction               |
| `/api/crops`        | GET    | List all supported crops                   |
| `/clear-history`    | GET    | Clear session history                      |

---

## Design System

The user interface employs a custom design system with an earth-tone aesthetic:

- **Color Palette**: Warm beige background (`#f8f6f0`), forest green accents (`#2d5016`), gold highlights (`#c4922a`)
- **Typography**: Fraunces (serif headings), Inter (sans-serif body), JetBrains Mono (code/metrics)
- **Components**: Bento-grid feature cards, animated soil gauges, scroll-triggered reveals, mobile-responsive navigation
- **UX Features**: Loading overlay during analysis, back navigation, empty states, error handling with retry

---

## Technology Stack

| Layer       | Technology                                           |
|-------------|------------------------------------------------------|
| Backend     | Python 3, Flask 3.0, Werkzeug 3.0                   |
| ML/AI       | Scikit-learn 1.5, NumPy 1.26, Google Gemini 2.5 Flash |
| Frontend    | HTML5, CSS3, Jinja2 Templates, JavaScript            |
| Data        | Pandas 2.2 (analysis), Joblib 1.4 (serialization)    |
| Security    | Flask-Talisman, Flask-WTF, Flask-Limiter             |
| Deployment  | Gunicorn 23.0, Flask-CORS                            |

### Dependencies

`flask==3.0.3 scikit-learn==1.5.2 pandas==2.2.2 numpy==1.26.4 joblib==1.4.2 requests==2.32.5 python-dotenv==1.0.1 gunicorn==23.0.0 flask-cors==5.0.0 flask-talisman==1.1.0 flask-wtf==1.2.1 flask-limiter==3.9.2 matplotlib==3.9.2 seaborn==0.13.2`

---

## Project Structure

```
OptiCrop/
├── code files/                    # Application source code
│   ├── app/                       # Flask web application
│   │   ├── app.py                 # Application entry point, routes, ML inference
│   │   ├── model.pkl              # Serialized Random Forest model + encoder + scaler
│   │   ├── templates/             # Jinja2 HTML templates
│   │   │   ├── index.html         # Landing page with hero, stats, features
│   │   │   ├── find_your_crop.html# Prediction form and results page
│   │   │   ├── about.html         # Mission, how-it-works, core values
│   │   │   ├── history.html       # Session prediction history
│   │   │   └── partials/
│   │   │       └── nav.html       # Navigation component
│   │   └── static/
│   │       └── style.css          # Custom CSS design system (475 lines)
│   ├── dataset/
│   │   └── Crop_recommendation.csv# 2,200 records, 22 crops, 7 features
│   ├── notebooks/
│   │   └── OptiCrop_Model.ipynb   # EDA, model comparison, training pipeline
│   ├── train_model.py             # Model training and serialization script
│   ├── integrate_templates.js     # Template integration utility
│   ├── debug_response.json        # API response debugging
│   ├── requirements.txt           # Python package dependencies
│   └── .gitignore                 # Version control exclusions
├── demo video/                    # Application walkthrough
└── Documentation/                 # Project lifecycle documentation
    ├── 1. Brainstorming & Ideation/
    ├── 2. Requirement Analysis/
    ├── 3. Project Design Phase/
    ├── 4. Project Planning Phase/
    ├── 5. Project Development Phase/
    ├── 6. Project Testing/
    └── 7. Project Demonstration/
```

---

## Documentation

The `Documentation/` directory contains the complete project lifecycle artifacts across seven phases, including problem definition, empathy mapping, solution architecture, data flow diagrams, technology stack documentation, project planning, development implementation, performance testing, and demonstration materials.

---

*Developed as part of the SmartBridge AI/ML internship program.*
