import os
import requests
from dotenv import load_dotenv


def read_db(endpoint, params):
    load_dotenv()
    return requests.get('https://api.collegefootballdata.com' + endpoint,
                        params=params,
                        headers={'accept': 'application/json',
                                 'Authorization': 'Bearer {}'.format(os.getenv('API_KEY'))})


class CFDB:
    def __init__(self):
        endpoint = '/teams/fbs'
        params = {'year': '2023'}
        response = read_db(endpoint, params)

        if response.status_code == 200:
            data = response.json()
            for team in data:
                print("School:", team["school"])
                print("Conference:", team["conference"])
                print()
        else:
            print('Error:', response.status_code)


if __name__ == "__main__":
    CFDB()
