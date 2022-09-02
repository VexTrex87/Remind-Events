EVENTS_FILE = 'events.json'
EVENTS_REGION = 'Vriginia'
EVENTS_SEASON = 173

import requests
import json
import os
import dotenv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

dotenv.load_dotenv('.env')

email_username = os.getenv('EMAIL_USERNAME')
email_password = os.getenv('EMAIL_PASSWORD')
robot_events_token = os.getenv('ROBOT_EVENTS_TOKEN')

send_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
send_server.ehlo()
send_server.starttls()
send_server.login(email_username, email_password)

class Event():
    def __init__(self, raw_event):
        self.sku = raw_event['sku']
        self.name = raw_event['name']
        self.start = raw_event['start']
        self.location = raw_event['location']
        self.season = {'id': raw_event['season']['id'], 'name': raw_event['season']['name']}
        self.program = raw_event['program']['code']
        self.city = raw_event['location']['city']
        self.region = raw_event['location']['region']
        self.url = f'https://www.robotevents.com/robot-competitions/vex-robotics-competition/{self.sku}.html#general-info'

def send_email(text):
    formatted_text = MIMEText(text, 'plain')

    message = MIMEMultipart('alternative')
    message['To'] = email_username
    message['Subject'] = 'New Robotics Competition(s)'
    message.attach(formatted_text)
    formatted_message = message.as_string()

    send_server.sendmail(email_username, [email_username], formatted_message)

def get_events(region, season):
    events = []

    next_page_url = 'https://www.robotevents.com/api/v2/events?page=1'
    while True:
        response = requests.get(url=next_page_url, params={'season': season}, headers={'Authorization': f'Bearer {robot_events_token}'}).json()
        for raw_event in response['data']:
            event = Event(raw_event)
            if event.region == region:
                events.append(event)

        next_page_url = response['meta']['next_page_url']
        if not next_page_url:
            break

    return events

def __main__():
    print('Checking for new events...')
    events = get_events(region=EVENTS_REGION, season=EVENTS_SEASON)

    new_events = []
    with open(EVENTS_FILE, 'r') as file:
        file = json.load(file)
        for event in events:
            if not event.name in file:
                new_events.append(f'{event.name} @ {event.city} - {event.url}')
                file.append(event.name)

        with open(EVENTS_FILE, 'w') as file_2:
            json.dump(file, file_2)

    if len(new_events) > 0:
        email_message = '\n'.join(new_events)
        send_email(email_message)

if __name__ == '__main__':
    __main__()
