from SataScraper import FootballScraper  # Adjust this import to match your filename

class TestFootballScraper:
    def __init__(self):
        self.scraper = FootballScraper()

    def test_selenium_session(self):
        """Test that the Selenium session starts and closes correctly."""
        try:
            print("🔄 Starting Selenium session test...")
            self.scraper.start_selenium_session()
            assert self.scraper.driver is not None, "❌ Selenium driver was not initialized."
            print("✅ Selenium driver started successfully.")
        finally:
            self.scraper.close_selenium_session()
            assert self.scraper.driver is None, "❌ Selenium driver did not close."
            print("✅ Selenium driver closed successfully.")

    def test_season_url(self):
        """Test that the season_url method returns the correct formatted URL."""
        print("🔄 Testing season URL formatting...")
        url = self.scraper.season_url(2023)
        expected_url = "https://www.bdfutbol.com/en/t/t2023-24aCHA.html"
        assert url == expected_url, f"❌ Expected {expected_url}, but got {url}"
        print(f"✅ Season URL is correct: {url}")


# Run tests
if __name__ == "__main__":
    tester = TestFootballScraper()
    tester.test_selenium_session()
    tester.test_season_url()
