from flask import Blueprint, request, jsonify
from services.otpService import generate_otp, verify_otp

auth = Blueprint("auth", __name__)

@auth.route("/send-otp", methods=["POST"])
def send_otp():

    data = request.get_json()

    phone = data["phone"]

    otp = generate_otp(phone)

    print("OTP:", otp)

    return jsonify({
        "success": True
    })


@auth.route("/verify-otp", methods=["POST"])
def verify():

    data = request.get_json()

    phone = data["phone"]
    otp = data["otp"]

    result = verify_otp(phone, otp)

    return jsonify({
        "success": result
    })