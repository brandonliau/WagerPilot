# Third party imports
import requests
# Local imports
import wagerpilot.config as con

def sportsAPI() -> dict:
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={oddsAPIKey}'
    response = requests.request("GET", url)
    return(response.json())

def eventsAPI(sportKey: str) -> dict:
    oddsAPIKey = next(con.oddsAPIKeyCycle)
    url = f'https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?apiKey={oddsAPIKey}&regions={con.regions}&markets=h2h&oddsFormat=decimal'
    response = requests.request("GET", url)
    return(response.json())

