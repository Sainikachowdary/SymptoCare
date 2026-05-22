from flask import Blueprint,request,jsonify
from models.history import connection

history = Blueprint(
"history",
__name__
)

@history.route(
"/save",
methods=["POST"]
)

def save_history():

    try:

        data=request.get_json()

        cursor=connection.cursor()

        cursor.execute(
        """

        INSERT INTO history
        (
        user_id,
        symptoms,
        prediction,
        confidence,
        date
        )

        VALUES(?,?,?,?,?)

        """,

        (

        data["user_id"],
        data["symptoms"],
        data["prediction"],
        data["confidence"],
        data["date"]

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


@history.route(
"/get/<user_id>",
methods=["GET"]
)

def get_history(user_id):

    cursor=connection.cursor()

    cursor.execute(

    """
    SELECT *
    FROM history
    WHERE user_id=?
    """,

    (user_id,)
    )

    rows=cursor.fetchall()

    history=[]

    for row in rows:

        history.append({

        "id":row[0],
        "symptoms":row[2],
        "prediction":row[3],
        "confidence":row[4],
        "date":row[5]

        })

    return jsonify(
    history
    )