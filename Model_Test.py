import os
from ModelTrainer import MatchPredictor  # Adjust the import if needed

class TestMatchPredictor:
    def __init__(self):
        self.predictor = MatchPredictor()

    def test_training_and_saving(self):
        """Test model training and saving functionality"""
        print("🔄 Running training and saving test...")
        if not os.path.exists(self.predictor.model_path) or not os.path.exists(self.predictor.encoder_path):
            self.predictor.train_and_save()
            print("✅ Model and encoder saved successfully.")
        else:
            print("✅ Model and encoder already exist, skipping training.")

    def test_prediction(self):
        """Test model prediction with sample input"""
        print("🔄 Running prediction test...")
        self.predictor.load_or_train()

        # Sample stats - must match the model's expected input length/order
        team1_stats = [10, 5, 3]  # Example: Wins, Draws, Losses
        team2_stats = [8, 6, 4]

        try:
            result = self.predictor.predict(team1_stats, team2_stats)
            print(f"✅ Predicted Winner: {result}")
        except Exception as e:
            print(f"❌ Prediction failed: {e}")


# Run tests
if __name__ == "__main__":
    tester = TestMatchPredictor()
    tester.test_training_and_saving()
    tester.test_prediction()
