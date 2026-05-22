from flask import Blueprint, request, jsonify
from services.mlService import predict_disease

ml = Blueprint("ml", __name__)

@ml.route("/test")
def test():
    
    result = predict_disease(
        ["fever", "cough"]
    )

    return jsonify(result)


@ml.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    symptoms = data["symptoms"]

    result = predict_disease(
        symptoms
    )

    return jsonify(result)