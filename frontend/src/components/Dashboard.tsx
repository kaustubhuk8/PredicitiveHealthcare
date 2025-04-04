import React, { useState } from 'react';
import axios from 'axios';
import { Chart } from 'react-chartjs-2';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend,
  ChartData,
  ChartOptions,
  DoughnutController
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  DoughnutController
);

interface PredictionResult {
  readmission_prediction: number;
  probability: number;
}

interface FormData {
  Age: number;
  Gender: string;
  Blood_Type: string;
  Medical_Condition: string;
  Days_Hospitalized: number;
}

const Dashboard = () => {
  const [formData, setFormData] = useState<FormData>({
    Age: 50,
    Gender: 'Male',
    Blood_Type: 'A+',
    Medical_Condition: 'Diabetes',
    Days_Hospitalized: 3
  });
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'Age' || name === 'Days_Hospitalized' 
        ? parseFloat(value) 
        : value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
        const response = await axios.post<PredictionResult>(
        'http://localhost:5001/predict', 
        formData
      );
      setPrediction(response.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          console.error('Server responded with error:', error.response.data);
        } else if (error.request) {
          console.error('No response received:', error.request);
        } else {
          console.error('Request setup error:', error.message);
        }
      } else {
        console.error('Unexpected error:', error);
      }
      alert('Failed to get prediction. Please check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const chartData: ChartData<'doughnut'> = prediction ? {
    labels: ['Low Risk', 'High Risk'],
    datasets: [{
      data: [1 - prediction.probability, prediction.probability],
      backgroundColor: ['#4CAF50', '#F44336'],
      borderWidth: 1
    }]
  } : {
    labels: [],
    datasets: []
  };

  const chartOptions: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: false
  };

  return (
    <div className="dashboard">
      <h1>Patient Readmission Risk Assessment</h1>
      
      <div className="dashboard-content">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Age:
              <input
                type="number"
                name="Age"
                value={formData.Age}
                onChange={handleChange}
                min={0}
              />
            </label>
          </div>

          <div className="form-group">
            <label>Gender:
              <select name="Gender" value={formData.Gender} onChange={handleChange}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label>Blood Type:
              <select name="Blood_Type" value={formData.Blood_Type} onChange={handleChange}>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label>Medical Condition:
              <select name="Medical_Condition" value={formData.Medical_Condition} onChange={handleChange}>
                <option value="Diabetes">Diabetes</option>
                <option value="Hypertension">Hypertension</option>
                <option value="Asthma">Asthma</option>
                <option value="Obesity">Obesity</option>
                <option value="Arthritis">Arthritis</option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label>Days Hospitalized:
              <input
                type="number"
                name="Days_Hospitalized"
                value={formData.Days_Hospitalized}
                onChange={handleChange}
                min={0}
              />
            </label>
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Predicting...' : 'Assess Risk'}
          </button>
        </form>

        {prediction && (
          <div className="results">
            <h2>Results</h2>
            <p>
              Readmission Risk: {prediction.readmission_prediction ? 'High' : 'Low'}
              <br />
              Probability: {(prediction.probability * 100).toFixed(2)}%
            </p>
            
            <div className="chart-container">
              <Chart
                type="doughnut"
                data={chartData}
                options={chartOptions}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
