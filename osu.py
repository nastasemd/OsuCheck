import requests
from urllib.request import Request

# Keeping tokens hidden in a separate file
# file has 2 lines (on the first there's the client id and on the second the client secret)
file = open("C:/osuKey.txt", "r")
tokens = file.readlines()
client_id = tokens[0].strip()
client_secret = tokens[1].strip()
file.close()

# API follows OATH 2 protocols
API_URL ='https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

def get_token(client_id, client_secret):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'public'
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json().get('access_token')