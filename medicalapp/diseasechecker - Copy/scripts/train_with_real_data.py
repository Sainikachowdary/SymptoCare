"""
Train DiseaseChecker with REAL medical dataset
Uses disease-symptoms-precautions data from Hugging Face
"""

import sys
sys.path.append('..')

import json
import pandas as pd
from integration_api import DiseaseCheckerAPI

class RealDataTrainer:
    def __init__(self):
        self.training_data = []
        self.precautions = {}
    
    def load_data(self):
        """Load the real medical dataset"""
        
        print("="*60)
        print("🏥 Loading REAL Medical Dataset")
        print("="*60)
        
        # Try to load from JSON first
        try:
            with open("data/real_training_data.json", "r") as f:
                self.training_data = json.load(f)
            
            with open("data/disease_precautions_real.json", "r") as f:
                self.precautions = json.load(f)
            
            print(f"✅ Loaded {len(self.training_data)} disease records")
            print(f"🩺 {len(self.precautions)} unique diseases with precautions")
            
        except FileNotFoundError:
            print("❌ Dataset not found. Run download_real_dataset.py first")
            return False
        
        return True
    
    def train_model(self):
        """Train the model with real data"""
        
        print("\n" + "="*60)
        print("🎯 Training Model with REAL Medical Data")
        print("="*60)
        
        # Initialize DiseaseChecker
        checker = DiseaseCheckerAPI(confidence_threshold=0.65)
        
        # Train with real data
        print(f"\n📊 Training on {len(self.training_data)} real disease records...")
        checker.train_from_list(self.training_data)
        
        print(f"✅ Model trained successfully!")
        print(f"🩺 Can detect {len(checker.disease_checker.model.classes_)} diseases")
        
        # Save the precautions mapping for later use
        checker.precautions = self.precautions
        
        return checker
    
    def test_predictions(self, checker):
        """Test the model with real symptom inputs"""
        
        print("\n" + "="*60)
        print("🔍 Testing with REAL Symptom Combinations")
        print("="*60)
        
        test_cases = [
            ["vomiting", "sunken eyes", "dehydration", "diarrhoea"],
            ["chills", "high fever", "sweating", "headache", "muscle pain"],
            ["itching", "skin rash", "fatigue", "high fever", "red spots"],
            ["continuous sneezing", "shivering", "chills", "watering from eyes"],
            ["fatigue", "weight loss", "irregular sugar level", "blurred vision"],
            ["cough", "shortness of breath", "chest pain", "high fever"],
            ["headache", "nausea", "sensitivity to light", "visual disturbances"],
        ]
        
        for i, symptoms in enumerate(test_cases, 1):
            result = checker.check_disease(symptoms)
            
            print(f"\n{i}. Symptoms: {', '.join(symptoms[:5])}")
            print(f"   → Predicted: {result['disease']}")
            print(f"   → Confidence: {result['confidence']*100}%")
            
            # Show precautions if available
            if result['disease'] in self.precautions:
                prec = self.precautions[result['disease']]
                print(f"   → Precautions: {prec[0][:50]}...")
    
    def export_for_integration(self, checker):
        """Export everything for integration"""
        
        # Save model with precautions
        import pickle
        
        model_data = {
            "model": checker.disease_checker.model,
            "encoder": checker.disease_checker.mlb,
            "precautions": self.precautions,
            "disease_list": list(self.precautions.keys()),
            "confidence_threshold": checker.disease_checker.confidence_threshold
        }
        
        with open("model/diseasechecker_complete.pkl", "wb") as f:
            pickle.dump(model_data, f)
        
        print(f"\n💾 Saved complete model to: model/diseasechecker_complete.pkl")
        
        # Also export as JSON for easy access
        export_data = {
            "diseases": list(self.precautions.keys()),
            "total_diseases": len(self.precautions),
            "precautions": self.precautions
        }
        
        with open("model/disease_info.json", "w") as f:
            json.dump(export_data, f, indent=2)
        
        print(f"💾 Saved disease info to: model/disease_info.json")
        
        return model_data

def main():
    trainer = RealDataTrainer()
    
    # Step 1: Load real data
    if not trainer.load_data():
        print("\n❌ Please run: python scripts/download_real_dataset.py")
        return
    
    # Step 2: Train model
    checker = trainer.train_model()
    
    # Step 3: Test predictions
    trainer.test_predictions(checker)
    
    # Step 4: Export for integration
    trainer.export_for_integration(checker)
    
    print("\n" + "="*60)
    print("🎉 DISEASECHECKER WITH REAL MEDICAL DATA - READY!")
    print("="*60)
    print(f"\n✅ Model trained on {len(trainer.training_data)} real disease records")
    print(f"🩺 Can detect {len(trainer.precautions)} diseases")
    print(f"📋 Each disease has 4+ precautions from medical sources")
    print("\n📦 Integration ready! Use:")
    print("   from integration_api import DiseaseCheckerAPI")
    print("   checker = DiseaseCheckerAPI()")
    print("   result = checker.check_disease(['fever', 'cough'])")

if __name__ == "__main__":
    main()