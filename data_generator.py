import pandas as pd
import numpy as np

def generate_patient_data(num_patients=10000):
    np.random.seed(42)
    
    # Base distributions
    age = np.random.normal(loc=55, scale=15, size=num_patients).astype(int)
    age = np.clip(age, 18, 90)
    
    bmi = np.random.normal(loc=26, scale=4, size=num_patients)
    bmi = np.clip(bmi, 18, 40)
    
    # Correlated features
    blood_pressure = 90 + (bmi - 18) * 0.8 + np.random.normal(0, 5, num_patients)
    blood_pressure = np.clip(blood_pressure, 90, 180)
    
    cholesterol = 150 + (age - 40) * 0.5 + np.random.normal(0, 15, num_patients)
    cholesterol = np.clip(cholesterol, 150, 300)
    
    glucose = 80 + (age - 40) * 0.3 + np.random.normal(0, 10, num_patients)
    glucose = np.clip(glucose, 70, 200)
    
    heart_rate = np.random.normal(loc=72, scale=8, size=num_patients)
    heart_rate = np.clip(heart_rate, 50, 100)
    
    # Calculate readmission risk (higher for multiple risk factors)
    risk_factors = (
        (age > 65).astype(int) + 
        (bmi > 30).astype(int) + 
        (blood_pressure > 140).astype(int) + 
        (cholesterol > 240).astype(int) + 
        (glucose > 126).astype(int)
    )
    readmitted = (risk_factors >= 2) & (np.random.random(num_patients) > 0.3)
    readmitted = readmitted.astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'age': age,
        'bmi': bmi.round(1),
        'blood_pressure': blood_pressure.round(0),
        'cholesterol': cholesterol.round(0),
        'glucose': glucose.round(0),
        'heart_rate': heart_rate.round(0),
        'readmitted': readmitted
    })
    
    return data

if __name__ == '__main__':
    df = generate_patient_data()
    df.to_csv('patient_data.csv', index=False, sep=',')
    print("Generated patient_data.csv with", len(df), "records")
