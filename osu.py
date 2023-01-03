import requests
import time

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

token = get_token(client_id, client_secret)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}

params = {
    'mode': 'osu',
    'limit': 1
}

# Getting initial stats
user_ids = ['7562902', '11367222', '6447454', '9269034', '4504101', '7525949', '7512553', '5339515', '6304246', '2291265'] # users to check (used top 10 players as example)
old_pps = []
old_ranks = []
for i in range(len(user_ids)):
    response = requests.get(f'{API_URL}/users/{user_ids[i]}/', params = params, headers = headers)
    old_pps.append(response.json().get('statistics').get('pp'))
    old_ranks.append(str(response.json().get('statistics').get('global_rank')))

while True:
    new_pps = []
    new_ranks = []
    changed = False
    for i in range(len(user_ids)):
        t = ''
        response = requests.get(f'{API_URL}/users/{user_ids[i]}/', params = params, headers = headers)
        pp = response.json().get('statistics').get('pp')
        username = response.json().get('username')
        rank = response.json().get('statistics').get('global_rank')
        diff = float(pp) - float(old_pps[i])
        d = int(old_ranks[i]) - int(rank)
        if diff > 0.0:
            t += username + ' has gained +' + "{:.2f}".format(diff) + ' pp. New total: ' + "{:,}".format(float(pp)) + ' pp. '
            if d > 0:
                t += 'New rank: #' + "{:,}".format(int(rank)) + ' (+' + "{:,}".format(d) + ').\n'
            elif d == 0:
                t += 'Didn\'t gain any ranks (#' + "{:,}".format(int(old_ranks[i])) + ').\n'
            else:
                t += 'New rank: #' + "{:,}".format(int(rank)) + ' (' + "{:,}".format(d) + ').\n'
            changed = True
        elif diff < 0.0:
            t += username + ' has lost ' + "{:.2f}".format(diff) + ' pp. New total: ' + "{:,}".format(float(pp)) + ' pp. '
            if d > 0:
                t += 'New rank: #' + "{:,}".format(int(rank)) + ' (+' + "{:,}".format(d) + ').\n'
            elif d == 0:
                t += 'Didn\'t gain any ranks (#' + "{:,}".format(int(old_ranks[i])) + ').\n'
            else:
                t += 'New rank: #' + "{:,}".format(int(rank)) + ' (' + "{:,}".format(d) + ').\n'
            changed = True
        if(t != ""):
            print(t)
        new_pps.append(pp)
        new_ranks.append(str(rank))
        if old_ranks[i] != new_ranks[i] or old_pps[i] != new_pps[i]:
            old_ranks[i] = new_ranks[i]
            old_pps[i] = new_pps[i]
    if changed == False:
        print('No changes.') # Making sure it works, instead of staring at blank screen
    time.sleep(15) # wait 15s before checking again
