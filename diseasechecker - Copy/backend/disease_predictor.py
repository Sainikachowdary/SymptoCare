"""
Disease Predictor with Precautions and Confidence Scores
"""

import json
import os
from ml_model import ml_model

class DiseasePredictor:
    def __init__(self):
        self.model = ml_model
        self.precaution_data = self.load_precautions()
        
    def load_precautions(self):
        """Load disease precautions"""
        default_precautions = {
            "Fungal infection": [
                "Keep affected area dry and clean",
                "Use antifungal cream as prescribed",
                "Avoid sharing towels or clothes",
                "Wear loose-fitting cotton clothes"
            ],
            "Allergy": [
                "Avoid known allergens",
                "Take antihistamines if prescribed",
                "Keep environment dust-free",
                "Use air purifier if needed"
            ],
            "GERD": [
                "Avoid spicy and fatty foods",
                "Don't lie down immediately after eating",
                "Elevate head while sleeping",
                "Avoid caffeine and alcohol"
            ],
            "Diabetes": [
                "Monitor blood sugar regularly",
                "Follow diabetic diet plan",
                "Exercise regularly",
                "Take medications on time"
            ],
            "Hypertension": [
                "Reduce salt intake",
                "Exercise regularly",
                "Manage stress",
                "Take BP medications regularly"
            ],
            "Migraine": [
                "Avoid triggers (bright lights, loud noises)",
                "Stay hydrated",
                "Get adequate sleep",
                "Practice stress reduction techniques"
            ],
            "COVID-19": [
                "Isolate immediately",
                "Monitor oxygen levels",
                "Stay hydrated",
                "Contact healthcare provider"
            ],
            "Pneumonia": [
                "Complete antibiotic course",
                "Get plenty of rest",
                "Stay hydrated",
                "Use humidifier for breathing"
            ],
            "Common Cold": [
                "Rest and stay hydrated",
                "Use saline nasal drops",
                "Gargle with salt water",
                "Take steam inhalation"
            ],
            "Malaria": [
                "Complete anti-malarial course",
                "Use mosquito nets",
                "Monitor fever pattern",
                "Get blood tests as advised"
            ],
            "Dengue": [
                "Monitor platelet count",
                "Stay hydrated",
                "Take paracetamol for fever",
                "Avoid NSAIDs like ibuprofen"
            ],
            "Arthritis": [
                "Gentle exercise like walking",
                "Apply hot/cold packs",
                "Maintain healthy weight",
                "Take prescribed medications"
            ],
            "Asthma": [
                "Use inhaler as prescribed",
                "Avoid dust and smoke",
                "Identify and avoid triggers",
                "Keep rescue inhaler always"
            ],
            "Urinary Tract Infection": [
                "Drink plenty of water",
                "Complete antibiotic course",
                "Avoid holding urine",
                "Cranberry juice may help"
            ]
        }
        
        # Try to load from file
        try:
            with open("data/disease_precautions.json", "r") as f:
                return json.load(f)
        except:
            # Save default precautions
            os.makedirs("data", exist_ok=True)
            with open("data/disease_precautions.json", "w") as f:
                json.dump(default_precautions, f, indent=2)
            return default_precautions
    
    def get_precautions(self, disease_name):
        """Get precautions for a disease"""
        # Try exact match
        if disease_name in self.precaution_data:
            return self.precaution_data[disease_name]
        
        # Try partial match
        for key in self.precaution_data:
            if disease_name.lower() in key.lower() or key.lower() in disease_name.lower():
                return self.precaution_data[key]
        
        # Default precautions
        return [
            "Consult a healthcare professional",
            "Get adequate rest",
            "Stay hydrated",
            "Follow prescribed treatment"
        ]
    
    def predict_with_precautions(self, symptoms):
        """Get disease prediction with precautions"""
        # Get prediction
        prediction = self.model.predict(symptoms)
        
        # Get precautions
        precautions = self.get_precautions(prediction['disease'])
        
        # Determine severity based on confidence
        if prediction['confidence'] > 80:
            severity = "High confidence - Follow precautions"
        elif prediction['confidence'] > 60:
            severity = "Medium confidence - Consult doctor if symptoms persist"
        else:
            severity = "Low confidence - Please consult a healthcare professional"
        
        return {
            "success": True,
            "symptoms": symptoms,
            "predicted_disease": prediction['disease'],
            "confidence_score": prediction['confidence'],
            "severity_advice": severity,
            "precautions": precautions,
            "alternative_diseases": prediction['top_predictions'][1:],
            "requires_doctor": prediction['confidence'] < 65
        }

# Initialize predictor
predictor = DiseasePredictor()