import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import socket

# This host's IPv6 route is unreachable and blackholes rather than refusing,
# so outbound DNS lookups must skip AAAA results or the Gemini call hangs
# far past its request timeout waiting on dead IPv6 candidates.
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _ipv4_only_getaddrinfo

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session
import pickle
import numpy as np
import requests
from datetime import datetime

GEMINI_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
label_encoder = model_data['label_encoder']
scaler = model_data['scaler']

# Input validation ranges
INPUT_RANGES = {
    'nitrogen': {'min': 0, 'max': 140, 'unit': 'kg/ha', 'label': 'Nitrogen (N)'},
    'phosphorus': {'min': 5, 'max': 145, 'unit': 'kg/ha', 'label': 'Phosphorus (P)'},
    'potassium': {'min': 5, 'max': 205, 'unit': 'kg/ha', 'label': 'Potassium (K)'},
    'temperature': {'min': 8, 'max': 44, 'unit': '°C', 'label': 'Temperature'},
    'humidity': {'min': 10, 'max': 100, 'unit': '%', 'label': 'Humidity'},
    'ph': {'min': 3.5, 'max': 9.9, 'unit': '', 'label': 'pH Value'},
    'rainfall': {'min': 20, 'max': 300, 'unit': 'mm', 'label': 'Rainfall'},
}

# Crop info database
CROP_INFO = {
    'rice': {'season': 'Kharif', 'water': 'High', 'temp_range': '20-30°C', 'icon': '🌾'},
    'wheat': {'season': 'Rabi', 'water': 'Low-Medium', 'temp_range': '10-25°C', 'icon': '🌾'},
    'maize': {'season': 'Kharif/Rabi', 'water': 'Medium', 'temp_range': '18-32°C', 'icon': '🌽'},
    'cotton': {'season': 'Kharif', 'water': 'Medium', 'temp_range': '25-35°C', 'icon': '☁️'},
    'sugarcane': {'season': 'Annual', 'water': 'High', 'temp_range': '20-40°C', 'icon': '🎋'},
    'jute': {'season': 'Kharif', 'water': 'High', 'temp_range': '25-35°C', 'icon': '🌿'},
    'coffee': {'season': 'Annual', 'water': 'Medium', 'temp_range': '15-28°C', 'icon': '☕'},
    'coconut': {'season': 'Annual', 'water': 'High', 'temp_range': '20-32°C', 'icon': '🥥'},
    'papaya': {'season': 'Annual', 'water': 'Medium', 'temp_range': '22-36°C', 'icon': '🍈'},
    'orange': {'season': 'Annual', 'water': 'Medium', 'temp_range': '15-35°C', 'icon': '🍊'},
    'apple': {'season': 'Rabi', 'water': 'Low-Medium', 'temp_range': '15-25°C', 'icon': '🍎'},
    'muskmelon': {'season': 'Summer', 'water': 'Low', 'temp_range': '25-35°C', 'icon': '🍈'},
    'watermelon': {'season': 'Summer', 'water': 'Medium', 'temp_range': '22-35°C', 'icon': '🍉'},
    'grapes': {'season': 'Annual', 'water': 'Low-Medium', 'temp_range': '15-35°C', 'icon': '🍇'},
    'mango': {'season': 'Summer', 'water': 'Low-Medium', 'temp_range': '24-38°C', 'icon': '🥭'},
    'banana': {'season': 'Annual', 'water': 'High', 'temp_range': '25-35°C', 'icon': '🍌'},
    'pomegranate': {'season': 'Annual', 'water': 'Low', 'temp_range': '15-38°C', 'icon': '🍎'},
    'lentil': {'season': 'Rabi', 'water': 'Low', 'temp_range': '15-25°C', 'icon': '🫘'},
    'blackgram': {'season': 'Kharif/Rabi', 'water': 'Low-Medium', 'temp_range': '25-35°C', 'icon': '🫘'},
    'mungbean': {'season': 'Kharif', 'water': 'Medium', 'temp_range': '25-35°C', 'icon': '🫘'},
    'chickpea': {'season': 'Rabi', 'water': 'Low', 'temp_range': '15-25°C', 'icon': '🫘'},
    'kidneybeans': {'season': 'Kharif', 'water': 'Medium', 'temp_range': '20-30°C', 'icon': '🫘'},
    'pigeonpeas': {'season': 'Kharif', 'water': 'Low-Medium', 'temp_range': '25-35°C', 'icon': '🫘'},
    'mothbeans': {'season': 'Kharif', 'water': 'Low', 'temp_range': '25-35°C', 'icon': '🫘'},
    'gram': {'season': 'Rabi', 'water': 'Low', 'temp_range': '15-25°C', 'icon': '🫘'},
}


def validate_inputs(data):
    """Validate input values against acceptable ranges."""
    errors = []
    for key, rng in INPUT_RANGES.items():
        val = data.get(key)
        if val is None:
            errors.append(f'{rng["label"]} is required')
            continue
        try:
            v = float(val)
            if v < rng['min'] or v > rng['max']:
                errors.append(f'{rng["label"]} should be between {rng["min"]} and {rng["max"]} {rng["unit"]}')
        except (ValueError, TypeError):
            errors.append(f'{rng["label"]} must be a valid number')
    return errors


def get_prediction_with_confidence(features_scaled):
    """Get prediction with confidence scores for all crops."""
    prediction = model.predict(features_scaled)
    predicted_crop = label_encoder.inverse_transform(prediction)[0]

    confidence = {}
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(features_scaled)[0]
        classes = label_encoder.classes_
        for cls, prob in zip(classes, proba):
            confidence[cls] = round(float(prob) * 100, 1)
        confidence = dict(sorted(confidence.items(), key=lambda x: x[1], reverse=True))

    return predicted_crop, confidence


def get_ai_analysis(crop, inputs, confidence):
    """Get AI-powered analysis from Google Gemini."""
    if not GEMINI_API_KEY:
        return None

    prompt = f"""You are an expert agricultural scientist. Analyze this crop recommendation and provide detailed insights.

Crop Recommended: {crop}
ML Model Confidence: {confidence}%

Soil & Climate Data:
- Nitrogen (N): {inputs['nitrogen']} kg/ha
- Phosphorous (P): {inputs['phosphorus']} kg/ha
- Potassium (K): {inputs['potassium']} kg/ha
- pH Value: {inputs['ph']}
- Temperature: {inputs['temperature']}°C
- Humidity: {inputs['humidity']}%
- Rainfall: {inputs['rainfall']} mm

Provide a JSON response with these fields (no markdown, just raw JSON):
{{
    "summary": "2-3 sentence summary of why this crop is recommended",
    "suitability": "one of: Excellent, Good, Moderate, Fair",
    "soil_analysis": "brief analysis of soil conditions based on NPK and pH",
    "climate_analysis": "brief analysis of climate suitability based on temp, humidity, rainfall",
    "tips": ["tip1", "tip2", "tip3"],
    "warnings": ["warning1"] or [],
    "best_practices": ["practice1", "practice2"],
    "expected_yield": "brief estimate of expected yield",
    "market_demand": "brief note on market demand for this crop"
}}"""

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            params={'key': GEMINI_API_KEY},
            json={'contents': [{'parts': [{'text': prompt}]}]},
            timeout=20,
        )
        response.raise_for_status()
        text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()

        # Clean up response - remove markdown code blocks if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
        if text.endswith('```'):
            text = text.rsplit('```', 1)[0]
        text = text.strip()

        import json
        return json.loads(text)
    except Exception as e:
        print(f"AI analysis error: {e}")
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', input_ranges=INPUT_RANGES)


@app.route('/find_your_crop', methods=['GET', 'POST'])
def find_your_crop():
    if request.method == 'POST':
        try:
            data = {
                'nitrogen': request.form.get('nitrogen'),
                'phosphorus': request.form.get('phosphorus'),
                'potassium': request.form.get('potassium'),
                'temperature': request.form.get('temperature'),
                'humidity': request.form.get('humidity'),
                'ph': request.form.get('ph'),
                'rainfall': request.form.get('rainfall'),
                'region': request.form.get('region', 'general'),
            }

            errors = validate_inputs(data)
            if errors:
                return render_template('find_your_crop.html',
                                     error='; '.join(errors),
                                     show_result=False,
                                     input_ranges=INPUT_RANGES,
                                     form_data=data)

            values = [float(data[k]) for k in ['nitrogen', 'phosphorus', 'potassium',
                                                  'temperature', 'humidity', 'ph', 'rainfall']]
            features = np.array([values])
            features_scaled = scaler.transform(features)

            predicted_crop, confidence = get_prediction_with_confidence(features_scaled)
            crop_info = CROP_INFO.get(predicted_crop, {})

            # Get AI analysis
            ai_analysis = get_ai_analysis(predicted_crop, data, confidence.get(predicted_crop, 0))

            # Store in session history
            if 'history' not in session:
                session['history'] = []

            result_entry = {
                'crop': predicted_crop,
                'inputs': data,
                'confidence': confidence.get(predicted_crop, 0),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'crop_info': crop_info,
                'ai_analysis': ai_analysis,
            }
            session['history'].insert(0, result_entry)
            session['history'] = session['history'][:10]
            session.modified = True

            top_alternatives = list(confidence.items())[1:4] if confidence else []

            return render_template('find_your_crop.html',
                                 prediction=predicted_crop,
                                 confidence=confidence.get(predicted_crop, 0),
                                 crop_info=crop_info,
                                 top_alternatives=top_alternatives,
                                 form_data=data,
                                 ai_analysis=ai_analysis,
                                 show_result=True,
                                 input_ranges=INPUT_RANGES)

        except Exception as e:
            return render_template('find_your_crop.html',
                                 error=f'Prediction failed: {str(e)}',
                                 show_result=False,
                                 input_ranges=INPUT_RANGES)

    return render_template('find_your_crop.html', show_result=False, input_ranges=INPUT_RANGES)


@app.route('/history')
def history():
    history = session.get('history', [])
    return render_template('history.html', history=history)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API endpoint for crop prediction with AI analysis."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        errors = validate_inputs(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400

        values = [float(data[k]) for k in ['nitrogen', 'phosphorus', 'potassium',
                                              'temperature', 'humidity', 'ph', 'rainfall']]
        features = np.array([values])
        features_scaled = scaler.transform(features)

        predicted_crop, confidence = get_prediction_with_confidence(features_scaled)
        crop_info = CROP_INFO.get(predicted_crop, {})

        # Get AI analysis
        ai_analysis = get_ai_analysis(predicted_crop, data, confidence.get(predicted_crop, 0))

        return jsonify({
            'success': True,
            'prediction': {
                'crop': predicted_crop,
                'confidence': confidence.get(predicted_crop, 0),
                'crop_info': crop_info,
            },
            'ai_analysis': ai_analysis,
            'all_scores': {k: v for k, v in list(confidence.items())[:10]},
            'input_ranges': {k: {'min': v['min'], 'max': v['max'], 'unit': v['unit']}
                           for k, v in INPUT_RANGES.items()},
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/crops')
def api_crops():
    crops = list(label_encoder.classes_)
    return jsonify({
        'crops': crops,
        'total': len(crops),
        'info': {c: CROP_INFO.get(c, {}) for c in crops}
    })


@app.route('/clear-history')
def clear_history():
    session.pop('history', None)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
