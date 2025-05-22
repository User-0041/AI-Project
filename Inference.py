import joblib
import pandas as pd

class Predictor:
    def __init__(self, model_path="model.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, team1_stats, team2_stats):
        input_data = pd.DataFrame([team1_stats + team2_stats])
        return self.model.predict(input_data)[0]