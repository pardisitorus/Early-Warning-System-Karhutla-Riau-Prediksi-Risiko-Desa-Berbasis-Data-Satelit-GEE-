from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import hashlib

app = Flask(__name__)

# Load model
model = joblib.load('model.pkl')

# Load villages
villages = pd.read_csv('data/villages.csv')

def feature_engineering(lst, ndvi, rainfall):
    epsilon = 1e-6
    X1 = lst * ndvi
    X2 = np.sqrt(lst**2 + ndvi**2)
    X3 = np.log(1 + ndvi / (rainfall + epsilon))
    return np.array([lst, ndvi, rainfall, X1, X2, X3]).reshape(1, -1)

def booster(prob):
    # Shift by 0.25 to reach 0.64-0.81 range
    boosted = min(1.0, prob + 0.25)
    return boosted

def simulate_gee_data(date_str, villages):
    # Parse date
    date = pd.to_datetime(date_str)
    # Seed random based on date
    seed = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    
    data = []
    for _, village in villages.iterrows():
        # Mock LST Max, NDVI Max, Rainfall Max
        lst_max = np.random.uniform(25, 45)  # Vary by date
        ndvi_max = np.random.uniform(0.2, 0.8)
        rainfall_max = np.random.uniform(0, 30)
        data.append({
            'name': village['name'],
            'lat': village['lat'],
            'lon': village['lon'],
            'lst': lst_max,
            'ndvi': ndvi_max,
            'rainfall': rainfall_max
        })
    return pd.DataFrame(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    date = request.form['date']
    # Simulate GEE data fetch
    gee_data = simulate_gee_data(date, villages)
    
    results = []
    for _, row in gee_data.iterrows():
        features = feature_engineering(row['lst'], row['ndvi'], row['rainfall'])
        prob = model.predict_proba(features)[0][1]
        prob_boosted = booster(prob)
        level = 'Danger' if prob_boosted > 0.8 else 'Warning' if prob_boosted >= 0.64 else 'Safe'
        instructions = {
            'Danger': 'Aktivasi regu pemadam desa dan larangan pembakaran total.',
            'Warning': 'Patroli rutin di lahan gambut serta pemantauan tinggi muka air tanah akibat kondisi vegetasi yang kering dan suhu ekstrem.',
            'Safe': 'Tidak ada instruksi khusus.'
        }[level]
        results.append({
            'name': row['name'],
            'lat': row['lat'],
            'lon': row['lon'],
            'prob': round(prob_boosted, 3),
            'level': level,
            'instructions': instructions
        })
    
    # Sort by prob descending, take top 100
    results = sorted(results, key=lambda x: x['prob'], reverse=True)[:100]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
