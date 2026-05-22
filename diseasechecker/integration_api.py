"""
Main Integration API for DiseaseChecker
"""

import pickle
import os
import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier

class DiseaseCheckerAPI:
    def __init__(self, confidence_threshold=0.6):
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.mlb = None
        self.precautions = {}
        self.disease_list = []
        self.load_model()
    
    def train_from_list(self, training_data):
        symptoms_list = [item['symptoms'] for item in training_data]
        diseases_list = [item['disease'] for item in training_data]
        
        self.mlb = MultiLabelBinarizer()
        X = self.mlb.fit_transform(symptoms_list)
        y = diseases_list
        
        self.model = RandomForestClassifier(n_estimators=150, max_depth=15, random_state=42, bootstrap=False)
        self.model.fit(X, y)
        self.disease_list = self.model.classes_
        
        os.makedirs("model", exist_ok=True)
        with open("model/disease_model.pkl", "wb") as f:
            pickle.dump(self.model, f)
        with open("model/symptom_encoder.pkl", "wb") as f:
            pickle.dump(self.mlb, f)
        
        print(f"✅ Model trained! Can detect {len(self.disease_list)} diseases")
        return True
    
    def load_model(self):
        try:
            with open("model/disease_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open("model/symptom_encoder.pkl", "rb") as f:
                self.mlb = pickle.load(f)
            try:
                with open("data/disease_precautions_real.json", "r") as f:
                    self.precautions = json.load(f)
            except:
                pass
            self.disease_list = self.model.classes_
            print(f"✅ Model loaded! Can detect {len(self.disease_list)} diseases")
            return True
        except Exception as e:
            print(f"⚠️ No model found: {e}")
            return False
    
    def check_disease(self, symptoms):
        if self.model is None or self.mlb is None:
            return {"disease": "Unknown", "confidence": 0, "error": "Model not loaded"}
        
        symptoms_encoded = self.mlb.transform([symptoms])
        predicted_disease = self.model.predict(symptoms_encoded)[0]
        probabilities = self.model.predict_proba(symptoms_encoded)[0]
        confidence = max(probabilities) * 100
        
        return {
            "disease": predicted_disease,
            "confidence": round(confidence, 2),
            "needs_more_info": confidence < self.confidence_threshold
        }
    
    def diagnose_with_precautions(self, symptoms):
        result = self.check_disease(symptoms)
        if "error" in result:
            return result
        
        precautions = self.get_precautions_for_disease(result['disease'])
        return {
            "disease": result['disease'],
            "confidence": result['confidence'],
            "needs_doctor": result['confidence'] < 65,
            "precautions": precautions,
            "symptoms_analyzed": symptoms
        }
    
    def get_precautions_for_disease(self, disease_name):
        if disease_name in self.precautions:
            return self.precautions[disease_name]
        for key in self.precautions:
            if disease_name.lower() in key.lower() or key.lower() in disease_name.lower():
                return self.precautions[key]
        return ["Consult a healthcare professional", "Get adequate rest", "Stay hydrated", "Follow prescribed treatment"]