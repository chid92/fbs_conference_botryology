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
                                 'Authorization': 'Bearer {}'.format(os.getenv('API_KEY'))})


class CFDB:
    def __init__(self):
        load_dotenv()
        self.conferences = ['ACC', 'Big Ten', 'Big 12', 'Pac-12', 'SEC']
        self.teams = [{'school': team['school'],
                       'conference': team['conference']}
                      for team in read_db('/teams/fbs', {'year': '2023'}).json()
                      if team['conference'] in self.conferences]
        for team in read_db('/teams/fbs', {'year': '2023'}).json():
            print(team['conference'])
        self.teams.append({'school': 'Notre Dame',
                           'conference': 'FBS Independents'})
        self.teams.append({'school': 'Connecticut',
                           'conference': 'FBS Independents'})
        self.teams.append({'school': 'SMU',
                           'conference': 'American Athletic'})

    def write_matchups_csv(self, filename):
        if os.path.exists(filename):
            return

        progress_bar = tqdm(total=math.comb(len(self.teams), 2), desc="Reading matchups")

        df_data = []
        for i in range(len(self.teams) - 1):
            for j in range(i + 1, len(self.teams)):
                team1 = self.teams[i]['school']
                team2 = self.teams[j]['school']
                data = read_db('/teams/matchup', {'team1': team1,
                                                  'team2': team2,
                                                  'minYear': '1869',
                                                  'maxYear': '2069'}).json()
                games = data['team1Wins'] + data['team2Wins'] + data['ties']
                df_data.append({'team1': team1, 'team2': team2, 'games': games})
                progress_bar.update(1)

        pd.DataFrame(df_data).to_csv(filename)
