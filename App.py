import streamlit as st
from SataScraper import FootballScraper
from ModelTrainer import MatchPredictor
from Inference import Predictor
from Model_Test import TestMatchPredictor
from Scraping_Test import TestFootballScraper

st.title("🏆 Match Outcome Predictor")

page = st.sidebar.radio("Go to", ["Run All Tests", "Scrape Matches", "Train Model", "Predict Outcome"])

if page == "Run All Tests":
    st.header("🧪 Running All Tests")
    try:
        tester = TestFootballScraper()
        tester.test_selenium_session()
        st.success("✅ test_selenium_session passed.")
    except Exception as e:
        st.error("❌ test_selenium_session failed.")
        st.exception(e)

    try:
        tester.test_season_url()
        st.success("✅ test_season_url passed.")
    except Exception as e:
        st.error("❌ test_season_url failed.")
        st.exception(e)

    try:
        modelTest = TestMatchPredictor()
        modelTest.test_model()
        st.success("✅ test_model passed.")
    except Exception as e:
        st.error("❌ test_model failed.")
        st.exception(e)

    try:
        modelTest.test_prediction()
        st.success("✅ test_prediction passed.")
    except Exception as e:
        st.error("❌ test_prediction failed.")
        st.exception(e)

elif page == "Scrape Matches":
    st.header("Scrape Championship Seasons")
    start = st.number_input("Start Year", min_value=2000, value=2023)
    end = st.number_input("End Year", min_value=start, max_value=2023)
    file = st.text_input("Output CSV Filename", "championship_all.csv")
    if st.button("Start Scraping"):
        scraper = FootballScraper()
        scraper.scrape_seasons(start, end, file)
        st.success(f"Data saved to {file}")

elif page == "Train Model":
    st.header("Train Model")
    trainer = MatchPredictor(data_file="championship_all.csv")
    if st.button("Train/Re-train Model"):
        trainer.train_and_save()
        st.success("Model trained and saved to disk.")

elif page == "Predict Outcome":
    st.header("Predict Match Result")
    model = MatchPredictor().load_or_train()
    predictor = Predictor()

    st.subheader("Enter Stats for 24 players (Team 1)")
    team1_stats = []
    for i in range(1, 25):
        team1_stats += [st.number_input(f"T1 P{i} Wins", 0), st.number_input(f"T1 P{i} Draws", 0), st.number_input(f"T1 P{i} Losses", 0)]

    st.subheader("Enter Stats for 24 players (Team 2)")
    team2_stats = []
    for i in range(1, 25):
        team2_stats += [st.number_input(f"T2 P{i} Wins", 0), st.number_input(f"T2 P{i} Draws", 0), st.number_input(f"T2 P{i} Losses", 0)]

    if st.button("Predict Winner"):
        prediction = predictor.predict(team1_stats, team2_stats)
        st.success(f"🏅 Predicted Winner: {prediction}")
