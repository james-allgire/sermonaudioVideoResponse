import urllib.parse
import urllib.request
import json
import time
from fake_useragent import UserAgent
import requests
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#gmail account used to send text messages
email = "fbcmonitoring@gmail.com"
pas = "pifsuw-Kagwuz-4jicqa"

sms_gateway = '13174373889@tmomail.net'
# The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
# and port is also provided by the email provider.
smtp = "smtp.gmail.com" 
port = 587

#fake user agent so sermon audio don't block our api request
ua = UserAgent()

#url key and api key log in info to pull sermon info
url = 'https://api.sermonaudio.com/v1/node/webcasts_in_progress'
api_key = '0F7F0BC2-0B9F-47C8-B7AA-F2FEF0AEF81D'
#combines url log in info with a chrome user agent so we can later get the json payload to check if our steam is up 
hdr = {'X-Api-Key' : api_key,'User-Agent':str(ua.chrome)}
req = urllib.request.Request(url, headers=hdr)

timeout = time.time() + 60#*5   # 5 minutes from now
while True:
    test = 0
    if test == 5 or time.time() > timeout:
        break
    test = test - 1
    with urllib.request.urlopen(req) as response:
        if response.getcode() == 200:
            source = response.read()
            the_page = json.loads(source)
            json_results = json.dumps(the_page)
            try:
                video_results = the_page['results'][0]['hasVideo']
                if video_results == True:
                    print("Video Stream is UP") 
                    time.sleep(10)
            except (IndexError):
                video_results = print("Video Stream is OFFLINE!")
                # This will start our email server
                server = smtplib.SMTP(smtp,port)
                # Starting the server
                server.starttls()
                # Now we need to login
                server.login(email,pas)

                # Now we use the MIME module to structure our message.
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = sms_gateway
                # Make sure you add a new line in the subject
                msg['Subject'] = "Video Stream Offline!\n"
                # Make sure you also add new lines to your body
                body = "Please check the video stream.\n"
                # and then attach that body furthermore you can also send html content.
                msg.attach(MIMEText(body, 'plain'))

                sms = msg.as_string()

                server.sendmail(email,sms_gateway,sms)

                # lastly quit the server
                server.quit()
                time.sleep(50)#(240)
            #print(json.dumps(the_page, indent = 4, sort_keys=True)) #Uncommenting will print out the full json payload
            #print(video_results) Print single result if video is online
            
        else:
            print('An error occurred while attempting to retrieve data from the API.')
else:
    exit()
