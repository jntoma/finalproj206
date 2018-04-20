import requests
from bs4 import BeautifulSoup
import json
import secrets
from requests_oauthlib import OAuth1
from operator import itemgetter
import sqlite3
import csv
import base64

spotifybase = "https://accounts.spotify.com/api/token"
spotifyplay = "https://api.spotify.com/v1"

spotify_client = secrets.client_id
spotify_secret = secrets.client_secret
auth = (spotify_client, spotify_secret)
grant_type = {'grant_type':'client_credentials'}

post_request = requests.post(spotifybase, data=grant_type, auth=auth)
response_data = json.loads(post_request.text)
access_token = response_data["access_token"]
print(access_token)

authorization_header = {"Authorization":"Bearer {}".format(access_token)}
print(authorization_header)

new_url = "https://api.spotify.com/v1/search?type=playlist&q={}".format("hi")
new_response = requests.get(new_url, headers = authorization_header)
data = json.loads(new_response.text)
#print(data)
