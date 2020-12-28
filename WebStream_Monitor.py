import urllib.parse
import urllib.request
import json

from fake_useragent import UserAgent
import requests

#Stop sermon monitoring/alerting at 11:40
ua = UserAgent()

url = 'https://api.sermonaudio.com/v1/node/webcasts_in_progress'
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'

hdr = {'X-Api-Key' : api_key,'User-Agent':str(ua.chrome)}
req = urllib.request.Request(url, headers=hdr)

with urllib.request.urlopen(req) as response:
    if response.getcode() == 200:
        source = response.read()
        the_page = json.loads(source)
        json_results = json.dumps(the_page)
        try:
            video_results = the_page['results'][0]['hasVideo']
            if video_results == True:
                print("Video Stream is UP") 
        except (IndexError):
            video_results = print("Video Stream is OFFLINE!")
        #print(json.dumps(the_page, indent = 4, sort_keys=True)) #Uncommenting will print out the full json payload
        #print(video_results) Print single result if video is online
        
    else:
        print('An error occurred while attempting to retrieve data from the API.')
