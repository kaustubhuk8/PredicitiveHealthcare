from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('../patient_readmission_model.pkl')

# Expected features from the model
REQUIRED_FEATURES = ['Age', 'Gender', 'Blood_Type', 'Medical_Condition', 'Days_Hospitalized']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate base features
        if not all(feature in data for feature in REQUIRED_FEATURES):
            return jsonify({'error': 'Missing required features'}), 400

        # Create feature DataFrame with same structure as training data
        input_df = pd.DataFrame([{
            'Age': data['Age'],
            'Gender': data['Gender'],
            'Blood Type': data['Blood_Type'],
            'Medical Condition': data['Medical_Condition'],
            'Days_Hospitalized': data['Days_Hospitalized']
        }])
        
        # Apply same one-hot encoding used in training
        input_data = pd.get_dummies(input_df, 
                      columns=['Gender', 'Blood Type', 'Medical Condition'])
        
        # Make sure all expected columns are present (fill missing with 0)
        training_columns = joblib.load('/home/hbutsuak/Desktop/Predictive Health Care analysis/feature_columns.pkl')
        for col in training_columns:
            if col not in input_data:
                input_data[col] = 0
        input_data = input_data[training_columns]
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            'readmission_prediction': int(prediction),
            'probability': float(model.predict_proba(input_data)[0][1])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
