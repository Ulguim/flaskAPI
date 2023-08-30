import requests
import os


from dotenv import load_dotenv
load_dotenv()

def twit_auth():
    print(os.environ.get('TWITCH_SECRET'))
    url = f"https://id.twitch.tv/oauth2/token?client_id={os.environ.get('TWITCH_CLIENT_ID')}&client_secret={os.environ.get('TWITCH_SECRET')}&grant_type=client_credentials"
    response = requests.post(url)
    app.logger.info(response.json())
    return response.json()

# def handle_request(endpoint, params):
#     baseURL = 'https://api.igdb.com/v4'
#     response = requests.post(endpoint, data=)