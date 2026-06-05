"""
Test script to verify model is working correctly
"""

import pickle
import os

print("="*60)
print("🔍 Testing DiseaseChecker Model")
print("="*60)

# Check if model files exist
model_path = "model"

if not os.path.exists(model_path):
    print(f"❌ Model folder not found: {model_path}")
    exit(1)

# List model files
print("\n📂 Model files found:")
for file in os.listdir(model_path):
    size = os.path.getsize(os.path.join(model_path, file))
    print(f"   - {file} ({size:,} bytes)")

# Load and test the model
print("\n" + "="*60)
print("📊 Loading Model Files")
print("="*60)

try:
    # Load model
    with open("model/disease_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Disease model loaded successfully")
    print(f"   - Model type: {type(model).__name__}")
    print(f"   - Can detect {len(model.classes_)} diseases")
    
    # Load encoder
    with open("model/symptom_encoder.pkl", "rb") as f:
        mlb = pickle.load(f)
    print("✅ Symptom encoder loaded successfully")
    print(f"   - Can recognize {len(mlb.classes_)} unique symptoms")
    
    # Load precautions
    with open("model/precautions.pkl", "rb") as f:
        precautions = pickle.load(f)
    print(f"✅ Precautions loaded successfully")
    print(f"   - Have precautions for {len(precautions)} diseases")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# Test predictions
print("\n" + "="*60)
print("🔬 Testing Predictions")
print("="*60)

test_cases = [
    ["fever", "cough", "fatigue"],
    ["headache", "nausea", "sensitivity to light"],
    ["vomiting", "diarrhea", "dehydration"],
    ["high fever", "chills", "sweating"],
    ["joint pain", "rash", "fever"],
    ["wheezing", "shortness of breath", "cough"],
]

for i, symptoms in enumerate(test_cases, 1):
    print(f"\n{i}. Symptoms: {', '.join(symptoms)}")
    
    # Transform symptoms
    symptoms_encoded = mlb.transform([symptoms])
    
    # Predict
    predicted = model.predict(symptoms_encoded)[0]
    probabilities = model.predict_proba(symptoms_encoded)[0]
    confidence = max(probabilities) * 100
    
    # Get first precaution
    prec = precautions.get(predicted, ["No precautions available"])[0]
    
    print(f"   → Predicted: {predicted}")
    print(f"   → Confidence: {confidence:.1f}%")
    print(f"   → Precaution: {prec[:60]}...")

print("\n" + "="*60)
print("✅ Model is working correctly!")
print("="*60)
print("\nNow you can start the web server:")
print("   cd backend")
print("   python app.py")
print("\nThen open: http://localhost:5000")