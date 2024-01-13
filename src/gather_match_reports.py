import requests
from bs4 import BeautifulSoup
import csv

API_KEY = "27d8f06a-e47c-4d80-8404-992ec25523f2"
BASE_URL = "https://content.guardianapis.com/search"
START_DATE = "2023-08-11" # Start of gameweek 1 
END_DATE = "2023-12-17" # End of gameweek 17
REPORTS_PATH = 'data/match_reports.csv'

# All of the teams in the URL format 
teams_url = [
    "liverpool", "manchester-united", 
    "aston-villa", "brentford", 
    "west-ham", "wolves", 
    "arsenal", "brighton", 
    "burnley", "everton", 
    "manchester-city", "crystal-palace",
    "newcastle", "fulham", 
    "chelsea", "sheffield-united", 
    "nottingham-forest", "tottenham", 
    "luton", "bournemouth"
]

# Names in article form corresponding to the url names
url_names_mapping = {
    "liverpool": "Liverpool", 
    "manchester-united": "United", 
    "aston-villa": "Villa", 
    "brentford": "Brentford", 
    "west-ham": "West Ham",
    "wolves": "Wolves", 
    "arsenal": "Arsenal", 
    "brighton": "Brighton", 
    "burnley": "Burnley", 
    "everton": "Everton", 
    "manchester-city": "City",
    "crystal-palace": "Palace", 
    "newcastle": "Newcastle", 
    "fulham": "Fulham", 
    "chelsea": "Chelsea", 
    "sheffield-united": "Sheffield",
    "nottingham-forest": "Forest", 
    "tottenham": "Spurs", 
    "luton": "Luton", 
    "bournemouth": "Bournemouth"
}

# The manually extracted match reports that were missing in the guardian API
match_reports = [
                {"Team_1": "Burnley", "Team_2": "Brighton", "Headline": "Burnley and Trafford withstand Brighton onslaught to earn point", "URL": "https://www.theguardian.com/football/2023/dec/09/brighton-burnley-premier-league-match-report", "Date": "2023-12-09", "Article": ""},
                {"Team_1": "Brighton", "Team_2": "Sheffield","Headline": "‘I don’t like 80% of referees’ claims Roberto De Zerbi as Brighton are held", "URL": "https://www.theguardian.com/football/2023/nov/12/brighton-sheffield-united-premier-league-match-report", "Date": "2023-11-12", "Article": ""},
                {"Team_1": "Sheffield", "Team_2": "Bournemouth","Headline": "Fans turn on Sheffield United as Marcus Tavernier double lifts Bournemouth", "URL": "https://www.theguardian.com/football/2023/nov/25/sheffield-united-bournemouth-premier-league-match-report", "Date": "2023-11-25", "Article": ""},
                {"Team_1": "Bournemouth", "Team_2": "Burnley","Headline": "Billing wonder strike sinks Burnley to give Iraola first Bournemouth win", "URL": "https://www.theguardian.com/football/2023/oct/28/bournemouth-burnley-premier-league-match-report", "Date": "2023-10-28", "Article": ""},
                {"Team_1": "Forest", "Team_2": "Luton","Headline": "Elijah Adebayo strikes to complete late Luton comeback and deny Forest", "URL": "https://www.theguardian.com/football/2023/oct/21/nottingham-forest-luton-premier-league-match-report", "Date": "2023-10-21", "Article": ""},
                {"Team_1": "Burnley", "Team_2": "Sheffield","Headline": "Sheffield United fans turn on manager Heckingbottom after Burnley thrashing", "URL": "https://www.theguardian.com/football/2023/dec/02/burnley-sheffield-united-premier-league-match-report", "Date": "2023-12-02", "Article": ""},
                {"Team_1": "Burnley", "Team_2": "Palace","Headline": "Crystal Palace’s win leaves struggling Burnley with unwanted record", "URL": "https://www.theguardian.com/football/2023/nov/04/burnley-crystal-palace-premier-league-match-report", "Date": "2023-11-04", "Article": ""},
                {"Team_1": "Brentford", "Team_2": "Palace","Headline": "Joachim Andersen rescues draw for Crystal Palace to deny Brentford", "URL": "https://www.theguardian.com/football/2023/aug/26/brentford-crystal-palace-premier-league-match-report", "Date": "2023-08-26", "Article": ""},
                {"Team_1": "City", "Team_2": "Liverpool","Headline": "Trent Alexander-Arnold strikes to earn Liverpool vital point at Manchester City", "URL": "https://www.theguardian.com/football/2023/nov/25/manchester-city-liverpool-premier-league-match-report", "Date": "2023-11-25", "Article": ""}
                ]

def fetch_articles_data(match_reports):
    """Fetch and add match reports data (Headline, URL & Date) from the guardian API to list of match reports

    Arguments:
        match_reports: The list of match reports 
    """
    current_page = 1
    total_pages = 1 # Placeholder
    while current_page <= total_pages:
        params = {
            "api-key": API_KEY,
            "section": "football",
            "tag": "football/premierleague,tone/matchreports",
            "from-date": START_DATE,
            "to-date": END_DATE,
            "page": current_page
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()['response']
            for result in data['results']:
                url = result['webUrl']
                current_teams = [team for team in teams_url if team in url]
                match_report_data = {"Team_1": url_names_mapping[current_teams[0]], "Team_2": url_names_mapping[current_teams[1]], 
                                     "Headline": result['webTitle'], "URL": url, "Date": result['webPublicationDate'][:10], "Article": ""}
                match_reports.append(match_report_data)
            total_pages = data['pages']
            current_page += 1
        else:
            print("Fetch of articles data failed\n")

def extract_articles(match_reports):
    """Scrape and add match report article text to list of match reports

    Arguments:
        match_reports: The list of match reports 
    """
    for row in match_reports:
        response = requests.get(row['URL'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            article_paragraphs = soup.find_all('p', class_='dcr-1dpfw7k')
            article_text = ' '.join(paragraph.get_text() for paragraph in article_paragraphs)

            row['Article'] = article_text
        else:
            print("Extraction of article failed\n")
            break

def create_csv(match_reports):
    """Save list of match reports as a .csv file

    Arguments:
        match_reports: The list of match reports 
    """
    field_names = ["Team_1", "Team_2", "Headline", "URL", "Date", "Article"]
    with open(REPORTS_PATH, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(match_reports)

fetch_articles_data(match_reports)
match_reports.sort(key=lambda x:x['Date'], reverse=True) # Sort them with newest report first
extract_articles(match_reports)
create_csv(match_reports)

