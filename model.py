import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model():
    # Load dataset
    data = pd.read_csv('healthcare_dataset.csv')
    
    # Feature engineering
    data['Age'] = pd.to_numeric(data['Age'])
    data['Days_Hospitalized'] = (pd.to_datetime(data['Discharge Date']) - 
                                pd.to_datetime(data['Date of Admission'])).dt.days
    
    # Select features and target
    features = ['Age', 'Gender', 'Blood Type', 'Medical Condition', 'Days_Hospitalized']
    target = 'Admission Type'
    
    # Convert categorical variables
    X = pd.get_dummies(data[features], columns=['Gender', 'Blood Type', 'Medical Condition'])
    y = (data[target] == 'Emergency').astype(int)  # Predict emergency readmissions

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Save model and feature columns
    joblib.dump(model, 'patient_readmission_model.pkl')
    joblib.dump(list(X.columns), 'feature_columns.pkl')
    print("Model and feature columns saved")

if __name__ == '__main__':
    train_model()
