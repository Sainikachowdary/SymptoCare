"""
Train Complete DiseaseChecker Model with proper symptoms
"""

import pickle
import os
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier

# Complete training data with proper symptoms
training_data = [
    # Respiratory diseases
    (["fever", "cough", "fatigue", "body_ache"], "Influenza"),
    (["fever", "cough", "fatigue", "loss_of_taste", "loss_of_smell"], "COVID-19"),
    (["cough", "shortness_of_breath", "chest_pain", "fever"], "Pneumonia"),
    (["runny_nose", "sneezing", "sore_throat", "mild_cough"], "Common Cold"),
    (["wheezing", "shortness_of_breath", "chest_tightness", "cough"], "Asthma"),
    (["sore_throat", "fever", "swollen_lymph_nodes"], "Strep Throat"),
    
    # Gastrointestinal
    (["vomiting", "diarrhea", "dehydration", "abdominal_pain"], "Gastroenteritis"),
    (["stomach_pain", "acidity", "heartburn", "nausea"], "GERD"),
    (["constipation", "bloating", "abdominal_pain", "gas"], "IBS"),
    
    # Neurological
    (["headache", "nausea", "vomiting", "sensitivity_to_light"], "Migraine"),
    (["fever", "headache", "stiff_neck", "confusion"], "Meningitis"),
    
    # Tropical/Vector-borne
    (["high_fever", "chills", "sweating", "headache", "muscle_pain"], "Malaria"),
    (["high_fever", "severe_headache", "pain_behind_eyes", "joint_pain", "rash"], "Dengue"),
    (["fever", "rash", "joint_pain", "red_eyes"], "Chikungunya"),
    
    # Chronic
    (["frequent_urination", "excessive_thirst", "fatigue", "blurred_vision"], "Diabetes"),
    (["headache", "dizziness", "shortness_of_breath", "chest_pain"], "Hypertension"),
    (["joint_pain", "joint_swelling", "stiffness", "fatigue"], "Arthritis"),
    
    # Skin conditions
    (["skin_rash", "itching", "red_spots", "fever"], "Dengue"),
    (["blistering_rash", "fever", "fatigue", "loss_of_appetite"], "Chickenpox"),
    (["fever", "rash", "cough", "runny_nose", "red_eyes"], "Measles"),
    
    # Other
    (["yellow_skin", "yellow_eyes", "dark_urine", "fatigue"], "Hepatitis"),
    (["cough", "coughing_blood", "night_sweats", "weight_loss"], "Tuberculosis"),
    (["fatigue", "weight_gain", "cold_intolerance", "dry_skin"], "Hypothyroidism"),
    (["palpitations", "dizziness", "chest_pain", "shortness_of_breath"], "Heart Disease"),
]

# Precautions for each disease
precautions = {
    "Influenza": ["Rest and stay hydrated", "Take fever reducers", "Avoid contact with others", "Get flu shot annually"],
    "COVID-19": ["Isolate immediately", "Monitor oxygen levels", "Stay hydrated", "Contact healthcare provider"],
    "Pneumonia": ["Complete antibiotic course", "Get plenty of rest", "Use humidifier", "Stay hydrated"],
    "Common Cold": ["Rest and hydrate", "Use saline drops", "Gargle salt water", "Take steam inhalation"],
    "Asthma": ["Use rescue inhaler", "Avoid triggers", "Keep medication accessible", "Monitor breathing"],
    "Strep Throat": ["Complete antibiotic course", "Gargle salt water", "Rest voice", "Stay hydrated"],
    "Gastroenteritis": ["Stop solid food temporarily", "Take small sips of water", "Rest", "Ease back into eating"],
    "GERD": ["Avoid spicy foods", "Don't lie down after eating", "Elevate head", "Limit caffeine"],
    "IBS": ["Manage stress", "Avoid trigger foods", "Exercise regularly", "Stay hydrated"],
    "Migraine": ["Rest in dark room", "Apply cold compress", "Avoid triggers", "Stay hydrated"],
    "Meningitis": ["Seek immediate medical care", "Complete treatment", "Rest", "Stay hydrated"],
    "Malaria": ["Complete anti-malarial course", "Use mosquito nets", "Monitor fever", "Get blood tests"],
    "Dengue": ["Monitor platelet count", "Stay hydrated", "Take paracetamol", "Avoid NSAIDs"],
    "Chikungunya": ["Rest", "Stay hydrated", "Take pain relievers", "Use mosquito protection"],
    "Diabetes": ["Monitor blood sugar", "Follow diet plan", "Exercise regularly", "Take medications"],
    "Hypertension": ["Reduce salt intake", "Exercise regularly", "Manage stress", "Take BP medication"],
    "Arthritis": ["Gentle exercise", "Apply hot/cold packs", "Maintain healthy weight", "Take medication"],
    "Chickenpox": ["Avoid scratching", "Take oatmeal baths", "Use calamine lotion", "Isolate until blisters crust"],
    "Measles": ["Isolate", "Rest", "Stay hydrated", "Use fever reducers"],
    "Hepatitis": ["Get plenty of rest", "Eat healthy diet", "Avoid alcohol", "Follow medication schedule"],
    "Tuberculosis": ["Complete treatment course", "Isolate during infectious period", "Good ventilation", "Wear mask"],
    "Hypothyroidism": ["Take thyroid medication", "Eat balanced diet", "Exercise", "Regular checkups"],
    "Heart Disease": ["Take medications as prescribed", "Healthy diet", "Exercise", "Stop smoking"],
}

print("="*60)
print("🏥 Training Complete DiseaseChecker Model")
print("="*60)

# Prepare training data
symptoms_list = [item[0] for item in training_data]
diseases_list = [item[1] for item in training_data]

print(f"\n📊 Training data:")
print(f"   - Total samples: {len(training_data)}")
print(f"   - Unique diseases: {len(set(diseases_list))}")

# Create encoder
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(symptoms_list)
y = diseases_list

print(f"   - Unique symptoms: {len(mlb.classes_)}")
print(f"   - Symptom examples: {list(mlb.classes_)[:15]}")

# Train model
print("\n🧠 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    bootstrap=False
)
model.fit(X, y)

accuracy = model.score(X, y) * 100
print(f"✅ Model trained! Accuracy: {accuracy:.1f}%")

# Save model
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
print("🔍 Testing the new model")
print("="*60)

test_cases = [
    ["fever", "cough", "fatigue"],
    ["headache", "nausea", "sensitivity_to_light"],
    ["vomiting", "diarrhea", "dehydration"],
    ["high_fever", "chills", "sweating", "headache"],
    ["joint_pain", "rash", "fever"],
    ["wheezing", "shortness_of_breath", "cough"],
]

for test in test_cases:
    test_encoded = mlb.transform([test])
    pred = model.predict(test_encoded)[0]
    conf = max(model.predict_proba(test_encoded)[0]) * 100
    prec = precautions.get(pred, ["No precautions"])[0]
    
    print(f"\n📋 Symptoms: {', '.join(test)}")
    print(f"   → Disease: {pred}")
    print(f"   → Confidence: {conf:.1f}%")
    print(f"   → Precaution: {prec[:50]}...")

print("\n" + "="*60)
print("🎉 Training complete!")
print("="*60)
print("\nNow run: python working_app.py")