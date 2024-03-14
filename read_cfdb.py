import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

base_url = 'https://api.collegefootballdata.com'
endpoint = '/teams/fbs'
params = {'year': '2023'}
headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

response = requests.get(base_url + endpoint, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    for team in data:
        print("School:", team["school"])
        print("Conference:", team["conference"])
        print()
else:
    print('Error:', response.status_code)