from flask import Blueprint, request, jsonify
from models.user import connection

user = Blueprint("user", __name__)

@user.route("/save-profile", methods=["POST"])
def save_profile():

    try:

        data = request.get_json()

        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE phone=?
        """,

        (data["phone"],)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.execute("""

            UPDATE users

            SET
            name=?,
            birthday=?,
            age=?,
            gender=?,
            weight=?,
            height=?

            WHERE phone=?

            """,

            (
            data["name"],
            data["birthday"],
            data["age"],
            data["gender"],
            data["weight"],
            data["height"],
            data["phone"]
            )
            )

        else:

            cursor.execute("""

            INSERT INTO users
            (
            name,
            phone,
            birthday,
            age,
            gender,
            weight,
            height
            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (
            data["name"],
            data["phone"],
            data["birthday"],
            data["age"],
            data["gender"],
            data["weight"],
            data["height"]
            )
            )

        connection.commit()

        return jsonify({
            "success":True  
        })

    except Exception as e:

        return jsonify({
            "success":False,
            "error":str(e)
        })