import os
import requests
from dotenv import load_dotenv


def read_db(endpoint, params):
    return requests.get('https://api.collegefootballdata.com' + endpoint,
                        params=params,
                        headers={'accept': 'application/json',
                                 'Authorization': 'Bearer {}'.format(os.getenv('API_KEY'))})


class CFDB:
    def __init__(self):
        load_dotenv()
        self.conferences = ['ACC', 'Big Ten', 'Big 12', 'Pac-12', 'SEC']
        self.teams = [{'school': team['school'],
                       'conference': team['conference']}
                      for team in read_db('/teams/fbs', {'year': '2023'}).json()
                      if team['conference'] in self.conferences]
