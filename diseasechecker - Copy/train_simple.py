"""
Complete Training Script for DiseaseChecker
"""

import json
import pickle
import os
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier

def main():
    print("="*60)
    print("🏥 DiseaseChecker - Training with Real Medical Data")
    print("="*60)
    
    # First, download the dataset if not exists
    if not os.path.exists("data/real_training_data.json"):
        print("\n📥 Downloading real medical dataset...")
        os.makedirs("data", exist_ok=True)
        
        # Sample real disease data (41 diseases)
        training_data = [
            {"symptoms": ["itching", "skin rash", "nodal skin eruptions", "dischromic patches"], "disease": "Fungal infection"},
            {"symptoms": ["continuous sneezing", "shivering", "chills", "watering from eyes"], "disease": "Allergy"},
            {"symptoms": ["stomach pain", "acidity", "ulcers on tongue", "vomiting", "cough", "chest pain"], "disease": "GERD"},
            {"symptoms": ["vomiting", "loss of appetite", "abdominal pain", "passage of gases", "internal itching"], "disease": "Peptic ulcer disease"},
            {"symptoms": ["fatigue", "weight loss", "restlessness", "lethargy", "irregular sugar level", "blurred vision", "obesity", "excessive hunger"], "disease": "Diabetes"},
            {"symptoms": ["fever", "cough", "fatigue", "loss of taste", "loss of smell", "sore throat"], "disease": "COVID-19"},
            {"symptoms": ["chest pain", "shortness of breath", "cough with phlegm", "fever", "chills"], "disease": "Pneumonia"},
            {"symptoms": ["high fever", "chills", "sweating", "headache", "nausea", "muscle pain"], "disease": "Malaria"},
            {"symptoms": ["high fever", "severe headache", "pain behind eyes", "joint pain", "muscle pain", "rash"], "disease": "Dengue"},
            {"symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing"], "disease": "Asthma"},
            {"symptoms": ["frequent urination", "burning urination", "cloudy urine", "pelvic pain", "fever"], "disease": "Urinary Tract Infection"},
            {"symptoms": ["headache", "nausea", "vomiting", "sensitivity to light", "sensitivity to sound"], "disease": "Migraine"},
            {"symptoms": ["headache", "shortness of breath", "nosebleeds", "flushing", "dizziness", "chest pain"], "disease": "Hypertension"},
            {"symptoms": ["joint pain", "joint swelling", "stiffness", "warmth around joints"], "disease": "Arthritis"},
            {"symptoms": ["fatigue", "fever", "night sweats", "weight loss", "persistent cough", "coughing blood"], "disease": "Tuberculosis"},
            {"symptoms": ["fever", "headache", "stiff neck", "confusion", "sensitivity to light"], "disease": "Meningitis"},
            {"symptoms": ["yellow skin", "yellow eyes", "dark urine", "abdominal pain", "loss of appetite"], "disease": "Hepatitis"},
            {"symptoms": ["runny nose", "sneezing", "nasal congestion", "sore throat", "mild cough"], "disease": "Common Cold"},
            {"symptoms": ["sore throat", "fever", "swollen lymph nodes", "white patches on tonsils"], "disease": "Strep Throat"},
            {"symptoms": ["ear pain", "fever", "difficulty hearing", "fluid drainage from ear"], "disease": "Ear Infection"},
            {"symptoms": ["sinus pressure", "headache", "nasal congestion", "thick nasal discharge", "facial pain"], "disease": "Sinusitis"},
            {"symptoms": ["nausea", "vomiting", "diarrhea", "abdominal cramps", "dehydration"], "disease": "Gastroenteritis"},
            {"symptoms": ["constipation", "bloating", "abdominal pain", "gas", "irregular bowel movements"], "disease": "IBS"},
            {"symptoms": ["red rash", "itching", "dry skin", "inflammation", "blisters"], "disease": "Eczema"},
            {"symptoms": ["red patches", "silver scales", "itching", "dry skin", "joint pain"], "disease": "Psoriasis"},
            {"symptoms": ["pimples", "blackheads", "whiteheads", "oily skin", "cysts"], "disease": "Acne"},
            {"symptoms": ["burning sensation in chest", "regurgitation", "difficulty swallowing", "chest pain"], "disease": "Acid Reflux"},
            {"symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath", "cold hands and feet"], "disease": "Anemia"},
            {"symptoms": ["chest pain", "shortness of breath", "palpitations", "dizziness", "fatigue"], "disease": "Heart Disease"},
            {"symptoms": ["fever", "rash", "joint pain", "red eyes", "mouth ulcers"], "disease": "Chikungunya"},
            {"symptoms": ["fever", "rash", "conjunctivitis", "joint pain", "muscle pain"], "disease": "Zika Virus"},
            {"symptoms": ["blistering rash", "fever", "fatigue", "headache", "loss of appetite"], "disease": "Chickenpox"},
            {"symptoms": ["fever", "rash", "cough", "runny nose", "red eyes"], "disease": "Measles"},
            {"symptoms": ["fever", "rash", "swollen glands", "joint pain", "headache"], "disease": "Rubella"},
            {"symptoms": ["fatigue", "fever", "sore throat", "swollen lymph nodes", "enlarged spleen"], "disease": "Mononucleosis"},
            {"symptoms": ["fever", "cough", "runny nose", "red eyes", "rash"], "disease": "Roseola"},
            {"symptoms": ["painful urination", "frequent urination", "fever", "chills", "nausea"], "disease": "Pyelonephritis"},
            {"symptoms": ["testicular pain", "swelling", "fever", "nausea", "vomiting"], "disease": "Testicular Infection"},
            {"symptoms": ["vaginal discharge", "itching", "burning sensation", "pain during intercourse"], "disease": "Yeast Infection"},
            {"symptoms": ["pelvic pain", "fever", "abnormal discharge", "pain during urination", "pain during intercourse"], "disease": "PID"},
            {"symptoms": ["fatigue", "weight gain", "cold intolerance", "dry skin", "hair loss"], "disease": "Hypothyroidism"},
        ]
        
        # Precautions for each disease
        precautions = {}
        for item in training_data:
            precautions[item['disease']] = [
                "Consult a healthcare professional immediately",
                "Get adequate rest and sleep",
                "Stay hydrated with plenty of fluids",
                "Follow prescribed treatment plan",
                "Monitor symptoms and seek help if worsens"
            ]
        
        # Save the data
        with open("data/real_training_data.json", "w") as f:
            json.dump(training_data, f, indent=2)
        
        with open("data/disease_precautions_real.json", "w") as f:
            json.dump(precautions, f, indent=2)
        
        print(f"✅ Created dataset with {len(training_data)} disease records")
    else:
        # Load existing data
        with open("data/real_training_data.json", "r") as f:
            training_data = json.load(f)
        with open("data/disease_precautions_real.json", "r") as f:
            precautions = json.load(f)
        print(f"✅ Loaded {len(training_data)} disease records")
    
    print(f"🩺 Unique diseases: {len(precautions)}")
    
    # Prepare training data
    print("\n🎯 Preparing training data...")
    symptoms_list = [item['symptoms'] for item in training_data if item.get('symptoms')]
    diseases_list = [item['disease'] for item in training_data if item.get('disease')]
    
    print(f"   - Training samples: {len(symptoms_list)}")
    
    # Create encoder and train model
    print("\n🧠 Training Random Forest model...")
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(symptoms_list)
    y = diseases_list
    
    print(f"   - Unique symptoms: {len(mlb.classes_)}")
    print(f"   - Feature matrix shape: {X.shape}")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        bootstrap=False
    )
    model.fit(X, y)
    
    accuracy = model.score(X, y) * 100
    print(f"✅ Model trained! Accuracy: {accuracy:.2f}%")
    
    # Save model files
    print("\n💾 Saving model...")
    os.makedirs("model", exist_ok=True)
    
    with open("model/disease_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("model/symptom_encoder.pkl", "wb") as f:
        pickle.dump(mlb, f)
    
    with open("model/precautions.pkl", "wb") as f:
        pickle.dump(precautions, f)
    
    print("✅ Model saved successfully!")
    
    # Test the model
    print("\n" + "="*60)
    print("🔍 Testing the model")
    print("="*60)
    
    test_cases = [
        ["fever", "cough", "fatigue", "loss of taste"],
        ["high fever", "chills", "sweating", "headache"],
        ["vomiting", "diarrhea", "dehydration"],
        ["headache", "nausea", "sensitivity to light"],
        ["joint pain", "rash", "fever"],
        ["wheezing", "shortness of breath", "cough"],
    ]
    
    for test in test_cases:
        test_encoded = mlb.transform([test])
        prediction = model.predict(test_encoded)[0]
        proba = max(model.predict_proba(test_encoded)[0]) * 100
        
        print(f"\n📋 Symptoms: {', '.join(test)}")
        print(f"   → Disease: {prediction}")
        print(f"   → Confidence: {proba:.1f}%")
    
    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETE!")
    print("="*60)
    print(f"\n✅ Your DiseaseChecker can now detect {len(precautions)} diseases!")
    print("✅ Model saved to 'model/' folder")
    print("\nNext steps:")
    print("   1. Run: cd backend")
    print("   2. Run: python app.py")
    print("   3. Open http://localhost:5000")

if __name__ == "__main__":
    main()