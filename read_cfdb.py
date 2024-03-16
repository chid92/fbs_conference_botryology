import math
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm


def read_db(endpoint, params):
    return requests.get('https://api.collegefootballdata.com' + endpoint,
                        params=params,
                        headers={'accept': 'application/json',
                                 'Authorization': f'Bearer {os.getenv("API_KEY")}'})


class CFDB:
    def __init__(self):
        load_dotenv()
        self.conferences = ['ACC', 'Big Ten', 'Big 12', 'Pac-12', 'SEC']
        self.teams = [{'school': team['school'],
                       'conference': team['conference']}
                      for team in read_db('/teams/fbs', {'year': '2023'}).json()
                      if team['conference'] in self.conferences]
        self.teams.extend([
            {'school': 'Notre Dame', 'conference': 'FBS Independents'},
            {'school': 'Connecticut', 'conference': 'FBS Independents'},
            {'school': 'SMU', 'conference': 'American Athletic'},
            {'school': 'Tulane', 'conference': 'American Athletic'}
        ])

    def write_matchups_csv(self, filename):
        if os.path.exists(filename):
            return

        progress_bar = tqdm(total=math.comb(len(self.teams), 2), desc="Reading matchups")

        df_data = []
        for i, team1 in enumerate(self.teams[:-1]):
            for team2 in self.teams[i + 1:]:
                data = read_db('/teams/matchup', {'team1': team1['school'],
                                                  'team2': team2['school'],
                                                  'minYear': '1869',
                                                  'maxYear': '2069'}).json()
                df_data.append({'team1': team1['school'],
                                'team2': team2['school'],
                                'games': data['team1Wins'] + data['team2Wins'] + data['ties']})
                progress_bar.update(1)

        pd.DataFrame(df_data).to_csv(filename)
