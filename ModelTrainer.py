import os
import joblib
import pandas as pd
from PreProsses import Preprocess 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

class MatchPredictor:
    def __init__(self, model_path="model.pkl", encoder_path="encoder.pkl", data_file="championship_2023_24.csv"):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.data_file = data_file
        self.model = None
        self.encoder = None

    def train_and_save(self):
        df = pd.read_csv(self.data_file)
        df = Preprocess(df).transform()
        feature_cols = [col for col in df.columns if "Wins" in col or "Draws" in col or "Losses" in col]
        X = df[feature_cols]
        y = df["Winner"]

        self.encoder = LabelEncoder()
        y_encoded = self.encoder.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=200, random_state=42)
        self.model.fit(X_train, y_train)

        acc = accuracy_score(y_test, self.model.predict(X_test))
        print(f"✅ Model trained. Accuracy: {acc:.2f}")

        joblib.dump(self.model, self.model_path)
        joblib.dump(self.encoder, self.encoder_path)

    def load(self):
        self.model = joblib.load(self.model_path)
        self.encoder = joblib.load(self.encoder_path)

    def load_or_train(self):
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.load()
        else:
            self.train_and_save()

    def predict(self, team1_stats, team2_stats):
        if self.model is None or self.encoder is None:
            self.load()

        input_data = pd.DataFrame([team1_stats + team2_stats])
        pred_encoded = self.model.predict(input_data)[0]
        pred_label = self.encoder.inverse_transform([pred_encoded])[0]
        return pred_label