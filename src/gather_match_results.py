import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.skysports.com/premier-league-results"
RESULTS_PATH = 'data/match_results.csv'

# Names in article form corresponding to match result names
result_name_mapping = {
    "Liverpool": "Liverpool", 
    "Manchester United": "United", 
    "Aston Villa": "Villa", 
    "Brentford": "Brentford", 
    "West Ham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves", 
    "Arsenal": "Arsenal", 
    "Brighton and Hove Albion": "Brighton", 
    "Burnley": "Burnley", 
    "Everton": "Everton", 
    "Manchester City": "City",
    "Crystal Palace": "Palace", 
    "Newcastle United": "Newcastle", 
    "Fulham": "Fulham", 
    "Chelsea": "Chelsea", 
    "Sheffield United": "Sheffield",
    "Nottingham Forest": "Forest", 
    "Tottenham Hotspur": "Spurs", 
    "Luton Town": "Luton", 
    "Bournemouth": "Bournemouth"
}

def extract_results(match_results):
    """Scrape and add match results (team names and team scores) to list of match results

    Arguments:
        match_results: The list of match results 
    """
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all("div", class_="fixres__item")
        for result in results:
            home_team = result.find("span", class_="matches__participant--side1").get_text(strip=True)
            away_team = result.find("span", class_="matches__participant--side2").get_text(strip=True)

            scores = result.find("span", class_="matches__teamscores").find_all("span", class_="matches__teamscores-side")
            home_score = scores[0].get_text(strip=True)
            away_score = scores[1].get_text(strip=True)
            
            temp_dict = {"Home_Team": result_name_mapping[home_team], "Home_Score": home_score, "Away_Team": result_name_mapping[away_team], "Away_Score": away_score}
            match_results.append(temp_dict)
        # only matches up until end of gameweek 17
        del match_results[:-169]
    else:
        print("Extraction of match results failed\n")

def create_csv(match_results):
    """Save list of match results as a .csv file

    Arguments:
        match_reports: The list of match reports 
    """
    field_names = ["Home_Team", "Home_Score", "Away_Team", "Away_Score"]
    with open(RESULTS_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(match_results)

match_results = []
extract_results(match_results)
create_csv(match_results)