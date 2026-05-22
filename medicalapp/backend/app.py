from flask import Flask
from flask_cors import CORS

from routes.authRoutes import auth
from routes.userRoutes import user
from routes.historyRoutes import history
from routes.mlRoutes import ml

app = Flask(__name__)

CORS(app)

app.register_blueprint(
    auth,
    url_prefix="/auth"
)

app.register_blueprint(
    user,
    url_prefix="/user"
)

app.register_blueprint(
    history,
    url_prefix="/history"
)

app.register_blueprint(
    ml,
    url_prefix="/ml"
)

@app.route("/")
def home():

    return {
        "message":"SymptoCare Backend Running"
    }

if __name__=="__main__":
    app.run(
        debug=True
    )