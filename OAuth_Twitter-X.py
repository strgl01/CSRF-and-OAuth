import requests
import os, base64, hashlib
import urllib.parse
import webbrowser
import json

client_id = 'Replace with Client ID'



# Genearate the code challange as per "code_challenge_method": "S256"
def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode()
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()
    return code_verifier, code_challenge

code_verifier, code_challenge = generate_pkce_pair()

# Generate Authorisation URL
params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": "http://localhost:8000/callback",
    "scope": "tweet.read users.read bookmark.read offline.access",
    "state": "random_string",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256"
}
auth_url = f"https://twitter.com/i/oauth2/authorize?{urllib.parse.urlencode(params)}"
webbrowser.open(auth_url)

# Copy paste the code from redirected url after approval
code = input('send code')

data = {
    "grant_type": "authorization_code",
    "code": code,  # the one you got from redirected url after approval
    "redirect_uri": "http://localhost:8000/callback",
    "client_id": client_id,
    "code_verifier": code_verifier
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post("https://api.twitter.com/2/oauth2/token", data=data, headers=headers)

# authentication token
tokens = response.json()


headers_new = {
    "Authorization": f"Bearer {tokens['access_token']}"
}

# user details API
response1 = requests.get("https://api.twitter.com/2/users/me", headers=headers_new)
id = response1.json()['data']['id']

# Post details API
response2 = requests.get( f"https://api.twitter.com/2/users/{id}/tweets", headers=headers)


# i have hide the real results with '*' just a sample
with open('user.json', 'w') as f:
     json.dump(response1.json(),f, indent = 4)


# i have hide the real results with '*' just a sample
with open('post.json', 'w') as f:
    json.dump(response2.json(),f, indent = 4)