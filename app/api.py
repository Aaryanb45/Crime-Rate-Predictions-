from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

app = Flask(__name__)

# Load cleaned data and model
scaler = StandardScaler()
df = pd.read_csv("../data/cleaned_crime_data.csv")
scaled_data = scaler.fit_transform(df)

model = KMeans(n_clusters=4, random_state=42)
model.fit(scaled_data)

@app.route('/')
def home():
    return "Crime Cluster Predictor API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json['features']  # Expecting list of numerical features
        input_array = np.array(input_data).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        cluster = model.predict(input_scaled)[0]
        return jsonify({'cluster': int(cluster)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
