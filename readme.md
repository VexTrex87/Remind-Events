# Robot Events

## Description

It's nice to know when a new competition has been posted on robotevents.com so teams can plan to register and compete in them.

This project checks when there has been a new event posted in a specific region and season. It emails a user the new events.

## Usage

````
python __main__.py
````

## Settings

In `__main__.py`, you can change the following settings
- `EVENTS_FILE`
- `EVENTS_REGION`
- `EVENTS_SEASON`

## Secrets

Create a file called `.env` with the variables
- `ROBOT_EVENTS_TOKEN`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`

