import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}