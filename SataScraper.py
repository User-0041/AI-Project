import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class FootballScraper:
    def __init__(self):
        self.driver = None

    def start_selenium_session(self):
        if self.driver is None:
            print("Starting Selenium session...")
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def close_selenium_session(self):
        if self.driver:
            print("Closing Selenium session...")
            self.driver.quit()
            self.driver = None

    def season_url(self, year_start):
        year_end = str(year_start + 1)[-2:]
        return f"https://www.bdfutbol.com/en/t/t{year_start}-{year_end}aCHA.html"

    def get_player_stats(self, player_url):
        try:
            self.start_selenium_session()
            self.driver.get(player_url)
            time.sleep(3)

            wins = self.driver.find_element(By.ID, 'valpgs').text
            draws = self.driver.find_element(By.ID, 'valpes').text
            losses = self.driver.find_element(By.ID, 'valpps').text

            wins = int(wins) if wins.isdigit() else 0
            draws = int(draws) if draws.isdigit() else 0
            losses = int(losses) if losses.isdigit() else 0

            return wins, draws, losses

        except Exception as e:
            print(f"Error fetching player stats from {player_url}: {e}")
            return 0, 0, 0

    def get_team_formations(self, match_url):
        try:
            print(f"Fetching formation from: {match_url}")
            response = requests.get(match_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            team1_formation, team2_formation = [], []
            tables = soup.select("table.taula_estil.text-left")

            for index, table in enumerate(tables):
                rows = table.find_all("tr")
                current_formation = []

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) > 3:
                        player_link_tag = cols[3].find("a")
                        if player_link_tag:
                            player_link = player_link_tag.get("href")
                            player_url = f"https://www.bdfutbol.com/en/{player_link}"
                            wins, draws, losses = self.get_player_stats(player_url)
                            current_formation.extend([wins, draws, losses])

                while len(current_formation) < 72:
                    current_formation.extend([0, 0, 0])

                if index % 2 == 0:
                    team1_formation.extend(current_formation)
                else:
                    team2_formation.extend(current_formation)

            return team1_formation[:72], team2_formation[:72]

        except Exception as e:
            print(f"Error fetching team formations: {e}")
            return [0] * 72, [0] * 72

    def parse_and_save_matches(self, html, writer):
        soup = BeautifulSoup(html, "html.parser")
        table_rows = soup.select("table tr.cha")

        for row in table_rows:
            cols = row.find_all("td")
            if len(cols) < 7:
                continue

            team1 = cols[2].get_text(strip=True)
            team2 = cols[6].get_text(strip=True)
            score_cells = cols[4].find_all("div", class_="resultat-gols")

            if len(score_cells) != 2:
                continue

            score1 = int(score_cells[0].text.strip())
            score2 = int(score_cells[1].text.strip())
            score = f"{score1}-{score2}"

            winner = team1 if score1 > score2 else team2 if score2 > score1 else "Draw"

            try:
                team1_link = cols[2].find("a")["href"]
                match_url = f"https://www.bdfutbol.com/en/{team1_link}"
                team1_formation, team2_formation = self.get_team_formations(match_url)
            except Exception as e:
                print(f"Error retrieving team URLs: {e}")
                team1_formation, team2_formation = [0] * 72, [0] * 72

            row_data = [team1, team2, score, winner] + team1_formation + team2_formation
            writer.writerow(row_data)
            print(f"Match saved: {team1} vs {team2}")

    def scrape_seasons(self, from_year, to_year, output_file="all_championship_data.csv"):
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["Team 1", "Team 2", "Score", "Winner"]
            for i in range(1, 25):
                header.extend([f"Team 1 Player {i} Wins", f"Team 1 Player {i} Draws", f"Team 1 Player {i} Losses"])
                header.extend([f"Team 2 Player {i} Wins", f"Team 2 Player {i} Draws", f"Team 2 Player {i} Losses"])
            writer.writerow(header)

            for year in range(from_year, to_year + 1):
                url = self.season_url(year)
                print(f"\nStarting scraping for season {year}-{str(year+1)[-2:]}: {url}")
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        self.parse_and_save_matches(response.text, writer)
                        print(f"Season {year}-{str(year+1)[-2:]} completed.")
                    else:
                        print(f"Failed to fetch {url}: Status code {response.status_code}")
                except Exception as e:
                    print(f"Error fetching {url}: {e}")

