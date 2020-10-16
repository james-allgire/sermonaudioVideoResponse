import urllib.parse
import urllib.request
import json

from fake_useragent import UserAgent
import requests


ua = UserAgent()

url = 'https://api.sermonaudio.com/v1/node/webcasts_in_progress'
api_key = 'xxxxxxxxxxxx'

hdr = {'X-Api-Key' : api_key,'User-Agent':str(ua.chrome)}
req = urllib.request.Request(url, headers=hdr)

with urllib.request.urlopen(req) as response:
    if response.getcode() == 200:
        source = response.read()
        the_page = json.loads(source)
        print(json.dumps(the_page, indent = 4, sort_keys=True))
    else:
        print('An error occurred while attempting to retrieve data from the API.')








