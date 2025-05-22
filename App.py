import streamlit as st
from SataScraper import FootballScraper
from ModelTrainer import MatchPredictor
from Inference import Predictor
import pandas as pd

st.title("🏆 Match Outcome Predictor")

page = st.sidebar.radio("Go to", ["Scrape Matches", "Train Model", "Predict Outcome"])

if page == "Scrape Matches":
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
