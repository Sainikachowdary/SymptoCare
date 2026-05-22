// DiseaseChecker Frontend JavaScript

class DiseaseCheckerUI {
    constructor() {
        this.symptoms = new Set();
        this.init();
    }

    init() {
        this.loadSymptomsList();
        this.setupEventListeners();
        this.updatePredictButton();
    }

    async loadSymptomsList() {
        try {
            const response = await fetch('/api/symptoms');
            const data = await response.json();

            if (data.success) {
                const datalist = document.getElementById('symptomSuggestions');
                data.symptoms.forEach(symptom => {
                    const option = document.createElement('option');
                    option.value = symptom;
                    datalist.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading symptoms:', error);
        }
    }

    setupEventListeners() {
        // Add symptom button
        document.getElementById('addSymptomBtn').addEventListener('click', () => {
            this.addSymptom();
        });

        // Enter key in input
        document.getElementById('symptomInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addSymptom();
            }
        });

        // Predict button
        document.getElementById('predictBtn').addEventListener('click', () => {
            this.predictDisease();
        });
    }

    addSymptom() {
        const input = document.getElementById('symptomInput');
        let symptom = input.value.trim().toLowerCase();

        if (symptom && !this.symptoms.has(symptom)) {
            this.symptoms.add(symptom);
            this.updateSelectedSymptoms();
            input.value = '';
            this.updatePredictButton();
        }
    }

    removeSymptom(symptom) {
        this.symptoms.delete(symptom);
        this.updateSelectedSymptoms();
        this.updatePredictButton();
    }

    updateSelectedSymptoms() {
        const container = document.getElementById('selectedSymptoms');

        if (this.symptoms.size === 0) {
            container.innerHTML = '<p class="placeholder">No symptoms added yet. Type symptoms above.</p>';
            return;
        }

        let html = '';
        this.symptoms.forEach(symptom => {
            html += `<span class="symptom-tag" onclick="ui.removeSymptom('${symptom}')">${symptom}</span>`;
        });
        container.innerHTML = html;
    }

    updatePredictButton() {
        const predictBtn = document.getElementById('predictBtn');
        predictBtn.disabled = this.symptoms.size === 0;
    }

    async predictDisease() {
        if (this.symptoms.size === 0) return;

        // Show loading
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symptoms: Array.from(this.symptoms)
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
        } finally {
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    }

    displayResults(result) {
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';

        // Display predicted disease
        document.getElementById('predictedDisease').textContent = result.predicted_disease;

        // Display confidence score
        const confidence = result.confidence_score;
        document.getElementById('confidenceScore').textContent = `${confidence}%`;

        // Update confidence bar
        const fillBar = document.getElementById('confidenceFill');
        fillBar.style.width = `${confidence}%`;
        fillBar.textContent = `${confidence}%`;

        // Color based on confidence
        if (confidence >= 80) {
            fillBar.style.background = 'linear-gradient(90deg, #48bb78, #38a169)';
        } else if (confidence >= 60) {
            fillBar.style.background = 'linear-gradient(90deg, #f6ad55, #ed8936)';
        } else {
            fillBar.style.background = 'linear-gradient(90deg, #fc8181, #f56565)';
        }

        // Display severity advice
        document.getElementById('severityAdvice').textContent = result.severity_advice;

        // Display precautions
        const precautionsList = document.getElementById('precautionsList');
        precautionsList.innerHTML = '';
        result.precautions.forEach(precaution => {
            const li = document.createElement('li');
            li.textContent = precaution;
            precautionsList.appendChild(li);
        });

        // Display alternative diseases
        const alternativesDiv = document.getElementById('alternativeDiseases');
        if (result.alternative_diseases && result.alternative_diseases.length > 0) {
            let altHtml = '';
            result.alternative_diseases.forEach(alt => {
                altHtml += `
                    <div class="alternative-disease">
                        <span>${alt.disease}</span>
                        <span style="color: #666;">${alt.probability}% probability</span>
                    </div>
                `;
            });
            alternativesDiv.innerHTML = altHtml;
        } else {
            alternativesDiv.innerHTML = '<p>No strong alternatives found</p>';
        }

        // Show doctor warning if needed
        const doctorWarning = document.getElementById('doctorWarning');
        if (result.requires_doctor || confidence < 65) {
            doctorWarning.style.display = 'block';
        } else {
            doctorWarning.style.display = 'none';
        }

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    showError(message) {
        alert('Error: ' + message);
    }
}

// Initialize the app
let ui;
window.addEventListener('DOMContentLoaded', () => {
    ui = new DiseaseCheckerUI();
    window.ui = ui; // Make accessible from HTML
});