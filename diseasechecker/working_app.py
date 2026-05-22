"""
DiseaseChecker - Complete Working Web Application
"""

from flask import Flask, request, jsonify, render_template_string
import pickle
import os

app = Flask(__name__)

# Load model
print("="*60)
print("🏥 Loading DiseaseChecker Model...")
print("="*60)

try:
    with open("model/disease_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/symptom_encoder.pkl", "rb") as f:
        mlb = pickle.load(f)
    with open("model/precautions.pkl", "rb") as f:
        precautions = pickle.load(f)
    
    print(f"✅ Model loaded successfully!")
    print(f"🩺 Can detect {len(model.classes_)} diseases")
    print(f"🔬 Recognizes {len(mlb.classes_)} symptoms")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Please run: python train_complete_model.py first")
    exit(1)

# HTML Template
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiseaseChecker - AI Symptom Checker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        h1 { font-size: 36px; margin-bottom: 10px; }
        .subtitle { opacity: 0.9; }
        main { padding: 30px; }
        .input-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        h3 { margin-bottom: 15px; color: #333; }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        .btn-predict {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 18px;
            padding: 15px;
            margin-top: 15px;
        }
        .btn-predict:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102,126,234,0.3);
        }
        .btn-predict:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .symptoms-container {
            background: white;
            border-radius: 10px;
            padding: 15px;
            min-height: 80px;
            border: 2px dashed #e0e0e0;
            margin-bottom: 20px;
        }
        .symptom-tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 6px 12px;
            margin: 5px;
            border-radius: 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .symptom-tag:hover {
            background: #e53e3e;
            transform: scale(1.05);
        }
        .symptom-tag::after {
            content: " ×";
            font-weight: bold;
            margin-left: 5px;
        }
        .placeholder {
            color: #999;
            text-align: center;
        }
        .result-card {
            margin-top: 20px;
            padding: 25px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: none;
        }
        .disease-name {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: #f0f4ff;
            border-radius: 10px;
        }
        .confidence-section {
            margin: 20px 0;
        }
        .confidence-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .progress-bar {
            background: #e0e0e0;
            height: 35px;
            border-radius: 17px;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, #48bb78, #38a169);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.5s ease;
        }
        .precautions-list {
            list-style: none;
            padding: 0;
            margin-top: 15px;
        }
        .precautions-list li {
            padding: 12px;
            margin: 10px 0;
            background: #f0fdf4;
            border-left: 4px solid #48bb78;
            border-radius: 8px;
        }
        .warning {
            background: #fee2e2;
            border-left: 4px solid #e53e3e;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
        .stats {
            text-align: center;
            padding: 10px;
            background: #e8f5e9;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 DiseaseChecker</h1>
            <p class="subtitle">AI-Powered Medical Symptom Checker</p>
        </header>
        <main>
            <div class="stats">
                ✅ System can detect <strong>{{ diseases_count }}</strong> medical conditions
            </div>
            
            <div class="input-section">
                <h3>📝 Enter Your Symptoms</h3>
                <div class="input-group">
                    <input type="text" id="symptomInput" placeholder="e.g., fever, cough, headache, fatigue" list="symptomList">
                    <datalist id="symptomList"></datalist>
                    <button class="btn-primary" onclick="addSymptom()">+ Add Symptom</button>
                </div>
                <div class="symptoms-container" id="symptomsContainer">
                    <p class="placeholder">No symptoms added yet. Type symptoms above.</p>
                </div>
                <button class="btn-predict" id="predictBtn" onclick="predictDisease()" disabled>🔍 Check Disease</button>
            </div>
            
            <div id="result" class="result-card"></div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing your symptoms...</p>
            </div>
        </main>
        <footer>
            <p>⚠️ This is an AI prediction based on medical data. Always consult a healthcare professional for accurate diagnosis.</p>
        </footer>
    </div>

    <script>
        let symptoms = new Set();
        
        function addSymptom() {
            const input = document.getElementById('symptomInput');
            const symptom = input.value.trim().toLowerCase();
            if (symptom && !symptoms.has(symptom)) {
                symptoms.add(symptom);
                updateSymptoms();
                input.value = '';
                document.getElementById('predictBtn').disabled = false;
            }
        }
        
        function removeSymptom(symptom) {
            symptoms.delete(symptom);
            updateSymptoms();
            document.getElementById('predictBtn').disabled = symptoms.size === 0;
        }
        
        function updateSymptoms() {
            const container = document.getElementById('symptomsContainer');
            if (symptoms.size === 0) {
                container.innerHTML = '<p class="placeholder">No symptoms added yet. Type symptoms above.</p>';
                return;
            }
            let html = '';
            symptoms.forEach(s => {
                html += `<span class="symptom-tag" onclick="removeSymptom('${s}')">${s}</span>`;
            });
            container.innerHTML = html;
        }
        
        async function predictDisease() {
            if (symptoms.size === 0) return;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ symptoms: Array.from(symptoms) })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const resultDiv = document.getElementById('result');
            const confidence = data.confidence;
            const disease = data.disease;
            const precautions = data.precautions;
            const needsDoctor = confidence < 65;
            
            let confidenceColor = '#48bb78';
            if (confidence < 60) confidenceColor = '#f56565';
            else if (confidence < 80) confidenceColor = '#f6ad55';
            
            resultDiv.innerHTML = `
                <h3>🩺 Diagnosis Result</h3>
                <div class="disease-name">${disease}</div>
                <div class="confidence-section">
                    <div class="confidence-label">
                        <span>Confidence Score</span>
                        <span><strong>${confidence}%</strong></span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${confidence}%; background: ${confidenceColor}">${confidence}%</div>
                    </div>
                </div>
                <h4>📋 Precautions & Recommendations</h4>
                <ul class="precautions-list">
                    ${precautions.map(p => `<li>✓ ${p}</li>`).join('')}
                </ul>
                ${needsDoctor ? `
                <div class="warning">
                    <strong>⚠️ Medical Disclaimer:</strong> Low confidence prediction. Please consult a healthcare professional.
                </div>
                ` : ''}
            `;
            resultDiv.style.display = 'block';
            resultDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Load symptom suggestions
        fetch('/symptoms')
            .then(r => r.json())
            .then(data => {
                if (data.symptoms) {
                    const datalist = document.getElementById('symptomList');
                    data.symptoms.forEach(symptom => {
                        const option = document.createElement('option');
                        option.value = symptom;
                        datalist.appendChild(option);
                    });
                }
            });
        
        // Enter key support
        document.getElementById('symptomInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') addSymptom();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, diseases_count=len(model.classes_))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms', [])
    
    if not symptoms:
        return jsonify({"error": "No symptoms"}), 400
    
    # Transform symptoms
    symptoms_encoded = mlb.transform([symptoms])
    
    # Predict
    disease = model.predict(symptoms_encoded)[0]
    confidence = max(model.predict_proba(symptoms_encoded)[0]) * 100
    
    # Get precautions
    prec = precautions.get(disease, [
        "Consult a healthcare professional",
        "Get adequate rest",
        "Stay hydrated",
        "Monitor your symptoms",
        "Seek medical help if symptoms worsen"
    ])
    
    return jsonify({
        "disease": disease,
        "confidence": round(confidence, 2),
        "precautions": prec
    })

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify({"symptoms": sorted(list(mlb.classes_))[:50]})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 DiseaseChecker is running!")
    print("="*60)
    print(f"\n✅ Model loaded: {len(model.classes_)} diseases, {len(mlb.classes_)} symptoms")
    print(f"✅ Open your browser to: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)