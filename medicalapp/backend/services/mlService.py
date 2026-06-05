import sys

sys.path.append(
    r"C:\Users\Korlapati Meghana\symptocare\SymptoCare\medicalapp\backend"
)

from integration_api import DiseaseCheckerAPI
api = DiseaseCheckerAPI()

precautions_data = {

"Dengue":[
"Monitor platelet count",
"Stay hydrated",
"Take paracetamol",
"Avoid NSAIDs"
],

"Pneumonia":[
"Get enough rest",
"Drink fluids",
"Take medicines on time",
"Consult doctor"
],

"Tuberculosis":[
"Wear mask",
"Take prescribed medicines",
"Drink enough water",
"Consult doctor"
],

"Influenza":[
"Rest well",
"Drink fluids",
"Avoid close contact",
"Take medicines if prescribed"
],

"IBS":[
"Manage stress",
"Avoid trigger foods",
"Exercise regularly",
"Stay hydrated"
]

}

def predict_disease(symptoms):

    result = api.check_disease(symptoms)

    disease = result["disease"]

    precautions = precautions_data.get(
        disease,
        [
            "Consult healthcare professional",
            "Get enough rest",
            "Stay hydrated",
            "Follow medical advice"
        ]
    )

    return {
        "disease": disease,
        "confidence": result["confidence"],
        "precautions": precautions
    }