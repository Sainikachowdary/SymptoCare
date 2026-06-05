from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integration_api import DiseaseCheckerAPI

app = Flask(__name__)
CORS(app)

# Initialize the API
api = DiseaseCheckerAPI()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DiseaseChecker - AI Symptom Checker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        h1 { font-size: 32px; margin-bottom: 10px; }
        main { padding: 30px; }
        .input-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-predict {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            padding: 15px;
            font-size: 18px;
            margin-top: 15px;
        }
        .btn-predict:disabled { opacity: 0.5; cursor: not-allowed; }
        .selected-symptoms {
            background: white;
            border-radius: 10px;
            padding: 15px;
            min-height: 80px;
            border: 2px dashed #ddd;
        }
        .symptom-tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            margin: 5px;
            cursor: pointer;
        }
        .symptom-tag:hover { background: #e53e3e; }
        .symptom-tag::after { content: " ×"; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .prediction-disease {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            margin: 15px 0;
        }
        .progress-bar {
            background: #e0e0e0;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            background: linear-gradient(90deg, #48bb78, #38a169);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.5s;
        }
        .precautions-list li {
            padding: 10px;
            margin: 8px 0;
            background: #f0fdf4;
            border-left: 4px solid #48bb78;
            list-style: none;
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
            margin: 0 auto;
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
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 DiseaseChecker</h1>
            <p>AI-Powered Medical Symptom Checker</p>
        </header>
        <main>
            <div class="input-section">
                <h3>📝 Enter Your Symptoms</h3>
                <div class="input-group">
                    <input type="text" id="symptomInput" placeholder="e.g., fever, cough, headache">
                    <button class="btn-primary" onclick="addSymptom()">+ Add</button>
                </div>
                <div class="selected-symptoms" id="selectedSymptoms">
                    <p style="color:#999;text-align:center">No symptoms added</p>
                </div>
                <button class="btn-predict" id="predictBtn" onclick="predictDisease()" disabled>🔍 Check Disease</button>
            </div>
            <div id="results" style="display:none"></div>
            <div class="loading" id="loading"><div class="spinner"></div><p>Analyzing symptoms...</p></div>
        </main>
        <footer>
            <p>⚠️ This is an AI prediction. Always consult a healthcare professional.</p>
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
            const container = document.getElementById('selectedSymptoms');
            if (symptoms.size === 0) {
                container.innerHTML = '<p style="color:#999;text-align:center">No symptoms added</p>';
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
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/api/predict', {
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
            const resultsDiv = document.getElementById('results');
            const confidence = data.confidence_score || data.confidence;
            
            resultsDiv.innerHTML = `
                <div class="card">
                    <h3>🩺 Diagnosis Result</h3>
                    <div class="prediction-disease">${data.predicted_disease || data.disease}</div>
                    <div>Confidence Score: ${confidence}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${confidence}%">${confidence}%</div>
                    </div>
                </div>
                <div class="card">
                    <h3>📋 Precautions</h3>
                    <ul class="precautions-list">
                        ${(data.precautions || []).map(p => `<li>${p}</li>`).join('')}
                    </ul>
                </div>
                ${data.needs_doctor ? `<div class="warning">⚠️ <strong>Medical Disclaimer:</strong> Low confidence prediction. Please consult a doctor.</div>` : ''}
            `;
            resultsDiv.style.display = 'block';
        }
        
        document.getElementById('symptomInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') addSymptom();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400
        
        # Try to get prediction with precautions
        if hasattr(api, 'diagnose_with_precautions'):
            result = api.diagnose_with_precautions(symptoms)
        else:
            result = api.check_disease(symptoms)
            result['predicted_disease'] = result.get('disease', 'Unknown')
            result['precautions'] = api.get_precautions_for_disease(result.get('disease', ''))
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": api.model is not None})

if __name__ == '__main__':
    print("="*60)
    print("🏥 DiseaseChecker Server Starting...")
    print("="*60)
    print("\n🌐 Open: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)