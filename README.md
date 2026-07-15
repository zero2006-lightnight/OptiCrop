# OptiCrop — Smart Agricultural Production Optimization Engine

**OptiCrop** is an AI-driven crop recommendation system that empowers farmers and agricultural stakeholders to make data-informed decisions. The platform integrates a high-accuracy machine learning model with generative AI to deliver crop suitability predictions, soil analysis, and actionable agricultural insights.

## Key Highlights

- **ML Model Accuracy** — Random Forest classifier achieving **99.55%** accuracy across 22 crop types
- **Generative AI Integration** — Google Gemini 2.5 Flash for contextual soil assessment, climate evaluation, and market-oriented recommendations
- **Confidence-Based Predictions** — Every recommendation includes probabilistic confidence scores for all supported crops
- **REST API Support** — Programmatic access via a JSON endpoint for integration with external systems

---

## Repository Structure

```
OptiCrop/
├── code files/                # Application source code
│   ├── app/                   # Flask web application
│   │   ├── app.py             # Application entry point and routes
│   │   ├── model.pkl          # Serialized Random Forest model
│   │   ├── templates/         # Jinja2 HTML templates
│   │   └── static/            # CSS stylesheets and assets
│   ├── dataset/               # Training dataset (2,200 records, 22 crops)
│   ├── notebooks/             # Jupyter notebooks for EDA and model training
│   ├── train_model.py         # Model training and serialization pipeline
│   └── requirements.txt       # Python package dependencies
├── demo video/                # Video walkthrough of application features
└── Documentation/             # Comprehensive project documentation
    ├── 1. Brainstorming & Ideation/
    ├── 2. Requirement Analysis/
    ├── 3. Project Design Phase/
    ├── 4. Project Planning Phase/
    ├── 5. Project Development Phase/
    ├── 6. Project Testing/
    └── 7. Project Demonstration/
```

---

## Getting Started

### Prerequisites

- Python 3.8 or later
- Google Gemini API key (optional — ML predictions work without it; AI analysis features require it)

### Installation

```bash
# Navigate to the application source directory
cd "code files"

# Install required Python packages
pip install -r requirements.txt

# Launch the Flask application
cd app
python app.py
```

The application will be available at **http://localhost:5000**.

### Configuration

To enable generative AI features, set your Google Gemini API key:

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your-api-key"

# Linux / macOS
export GEMINI_API_KEY="your-api-key"

# Alternatively, create a .env file in the project root:
#   GEMINI_API_KEY=your-api-key
```

---

## Features

### Core Prediction Engine
- **Multi-Class Crop Classification** — Random Forest model trained on nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall parameters
- **Probabilistic Confidence Scoring** — Ranked predictions with percentage confidence for all 22 crops
- **Input Validation** — Server-side range checking with descriptive error messaging

### AI-Powered Analysis
- **Soil Assessment** — Detailed evaluation of NPK levels and pH balance
- **Climate Compatibility** — Temperature and humidity suitability analysis
- **Market Demand Insights** — Crop market potential and expected yield estimates
- **Actionable Recommendations** — Practical farming tips tailored to predicted crops

### Application Features
- **Web Interface** — Responsive, earth-tone design with interactive soil gauges
- **Session History** — Persistent prediction history for the last 10 analyses
- **REST API** — JSON-based programmatic access at `/api/predict`
- **Crop Catalog** — Comprehensive list of all supported crops at `/api/crops`

---

## API Reference

### POST `/api/predict`

Submit soil and environmental parameters for crop prediction:

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

**Response:** Predicted crop, confidence scores, crop information, AI analysis, and validation ranges.

### Input Parameters

| Parameter      | Range      | Unit    | Description                  |
|----------------|------------|---------|------------------------------|
| Nitrogen (N)   | 0–140      | kg/ha   | Nitrogen content in soil     |
| Phosphorus (P) | 5–145      | kg/ha   | Phosphorus content in soil   |
| Potassium (K)  | 5–205      | kg/ha   | Potassium content in soil    |
| Temperature    | 8–44       | °C      | Ambient temperature          |
| Humidity       | 10–100     | %       | Relative humidity            |
| pH             | 3.5–9.9    | —       | Soil pH value                |
| Rainfall       | 20–300     | mm      | Rainfall amount              |

---

## Technology Stack

| Layer       | Technologies                                          |
|-------------|-------------------------------------------------------|
| Backend     | Python, Flask, Scikit-learn, NumPy, Joblib            |
| AI / ML     | Google Gemini 2.5 Flash, Random Forest Classifier     |
| Frontend    | HTML5, CSS3, Jinja2 Templates, Google Fonts           |
| Data        | CSV (2,200 records, 22 crop classes)                  |

## Model Performance

| Model               | Accuracy |
|---------------------|----------|
| Random Forest       | 99.55%   |
| K-Nearest Neighbors | 97.95%   |
| Decision Tree       | 97.95%   |
| Logistic Regression | 97.27%   |

---

## Documentation

The `Documentation/` directory contains the complete project lifecycle documentation across seven phases:

1. **Brainstorming & Ideation** — Problem definition, empathy mapping, idea prioritization
2. **Requirement Analysis** — Customer journey mapping, data flow diagrams, technology stack
3. **Project Design** — Solution architecture, problem-solution fit, proposed solutions
4. **Project Planning** — Timeline, milestones, resource allocation
5. **Development** — Full application source code and implementation details
6. **Testing** — Performance testing and validation results
7. **Demonstration** — Demo planning, communication strategy, future roadmap

---

## License

This project is developed as part of the SmartBridge AI/ML internship program.
