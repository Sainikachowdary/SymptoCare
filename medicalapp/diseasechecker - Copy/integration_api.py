import pickle
import os
import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


class DiseaseCheckerAPI:

    def __init__(self, confidence_threshold=0.6):

        self.confidence_threshold = confidence_threshold
        self.model = None
        self.mlb = None
        self.precautions = {}
        self.disease_list = []

        self.load_model()


    def train_from_list(self, training_data):

        symptoms_list = [
            item['symptoms']
            for item in training_data
        ]

        diseases_list = [
            item['disease']
            for item in training_data
        ]

        self.mlb = MultiLabelBinarizer()

        X = self.mlb.fit_transform(
            symptoms_list
        )

        y = diseases_list

        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=15,
            random_state=42,
            bootstrap=False
        )

        self.model.fit(X, y)

        self.disease_list = self.model.classes_

        os.makedirs(
            MODEL_DIR,
            exist_ok=True
        )

        with open(
            os.path.join(
                MODEL_DIR,
                "disease_model.pkl"
            ),
            "wb"
        ) as f:

            pickle.dump(
                self.model,
                f
            )

        with open(
            os.path.join(
                MODEL_DIR,
                "symptom_encoder.pkl"
            ),
            "wb"
        ) as f:

            pickle.dump(
                self.mlb,
                f
            )

        return True


    def load_model(self):

        try:

            with open(
                os.path.join(
                    MODEL_DIR,
                    "disease_model.pkl"
                ),
                "rb"
            ) as f:

                self.model = pickle.load(f)


            with open(
                os.path.join(
                    MODEL_DIR,
                    "symptom_encoder.pkl"
                ),
                "rb"
            ) as f:

                self.mlb = pickle.load(f)


            try:

                with open(
                    os.path.join(
                        DATA_DIR,
                        "disease_precautions_real.json"
                    ),
                    "r"
                ) as f:

                    self.precautions = json.load(f)

            except:
                pass


            self.disease_list = self.model.classes_

            print(
                f"✅ Model loaded! Can detect {len(self.disease_list)} diseases"
            )

            return True


        except Exception as e:

            print(
                f"⚠️ No model found: {e}"
            )

            return False


    def check_disease(self, symptoms):

        symptoms_encoded = self.mlb.transform(
            [symptoms]
        )

        predicted = self.model.predict(
            symptoms_encoded
        )[0]

        probabilities = self.model.predict_proba(
            symptoms_encoded
        )[0]

        confidence = max(
            probabilities
        )*100

        return {

            "disease":predicted,

            "confidence":
            round(
                confidence,
                2
            )

        }