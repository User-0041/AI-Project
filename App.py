import streamlit as st
from SataScraper import FootballScraper
from ModelTrainer import MatchPredictor
from Inference import Predictor
import pandas as pd
from PreProsses import Preprocess
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
    df = pd.read_csv("championship_all.csv")

    team_names = sorted(set(df["Team 1"]).union(set(df["Team 2"])))

    team1 = st.selectbox("Select Team 1", team_names)
    team2 = st.selectbox("Select Team 2", team_names)

    if team1 == team2:
        st.warning("Please choose two different teams.")
    else:
        if st.button("Predict Winner"):

            latest_match = df[((df["Team 1"] == team1) & (df["Team 2"] == team2)) |
                              ((df["Team 1"] == team2) & (df["Team 2"] == team1))].iloc[-1:]

            if latest_match.empty:
                st.error("No past match data found for these teams.")
            else:

                score = latest_match["Score"].values[0]
                st.info(f"Last recorded match score: {score}")


                team1_stats = []
                team2_stats = []

                for i in range(1, 25):  
                    for stat in ["Wins", "Draws", "Losses"]:
                        team1_stats.append(latest_match[f"Team 1 Player {i} {stat}"].values[0])
                        team2_stats.append(latest_match[f"Team 2 Player {i} {stat}"].values[0])
                print(team1_stats,team2_stats)
                
                predictor = Predictor()
                predicted_winner = predictor.predict(team1_stats, team2_stats)
                winner_name =""
                if predicted_winner == 0:
                    winner_name = team1
                elif predicted_winner == 1:
                    winner_name = team2

                st.success(f"🏅 Predicted Winner: **{winner_name}**")