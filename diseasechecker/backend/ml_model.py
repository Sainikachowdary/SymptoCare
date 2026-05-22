"""
Trained ML Model for Disease Prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import json

class DiseaseMLModel:
    def __init__(self):
        self.model = None
        self.mlb = MultiLabelBinarizer()
        self.symptom_list = []
        self.disease_list = []
        
    def train(self, training_data_path="data/disease_data.csv"):
        """Train the ML model"""
        print("📊 Training ML Model...")
        
        # Load data
        df = pd.read_csv(training_data_path)
        
        # Prepare training data
        training_data = []
        for _, row in df.iterrows():
            symptoms = [s.strip() for s in row['symptoms'].split(',')]
            disease = row['disease']
            training_data.append({"symptoms": symptoms, "disease": disease})
        
        # Transform symptoms
        X = self.mlb.fit_transform([d["symptoms"] for d in training_data])
        y = [d["disease"] for d in training_data]
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=15,
            random_state=42,
            bootstrap=False  # Deterministic
        )
        self.model.fit(X, y)
        
        self.disease_list = self.model.classes_
        self.symptom_list = self.mlb.classes_
        
        # Save model
        os.makedirs("model", exist_ok=True)
        with open("model/disease_model.pkl", "wb") as f:
            pickle.dump(self.model, f)
        with open("model/symptom_encoder.pkl", "wb") as f:
            pickle.dump(self.mlb, f)
        
        print(f"✅ Model trained on {len(training_data)} samples")
        print(f"🩺 Can predict {len(self.disease_list)} diseases")
        print(f"🔬 Using {len(self.symptom_list)} symptoms")
        
        return self.model
    
    def load_model(self):
        """Load trained model"""
        try:
            with open("model/disease_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open("model/symptom_encoder.pkl", "rb") as f:
                self.mlb = pickle.load(f)
            self.disease_list = self.model.classes_
            self.symptom_list = self.mlb.classes_
            print("✅ Model loaded successfully")
            return True
        except:
            print("⚠️ No model found. Training new model...")
            self.train()
            return True
    
    def predict(self, symptoms):
        """Predict disease from symptoms"""
        # Transform symptoms
        symptoms_encoded = self.mlb.transform([symptoms])
        
        # Predict
        disease = self.model.predict(symptoms_encoded)[0]
        probabilities = self.model.predict_proba(symptoms_encoded)[0]
        confidence = max(probabilities) * 100
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [
            {
                "disease": self.disease_list[idx],
                "probability": round(probabilities[idx] * 100, 2)
            }
            for idx in top_indices
        ]
        
        return {
            "disease": disease,
            "confidence": round(confidence, 2),
            "top_predictions": top_predictions,
            "symptoms_analyzed": symptoms
        }

# Initialize global model
ml_model = DiseaseMLModel()
ml_model.load_model()