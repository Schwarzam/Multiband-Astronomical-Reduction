from mar_functions import *
import requests

import json

import datetime


token = login("t80team", "asdflkjh")
header = getHeader(token)

START_DATE = "2022-01-01"
END_DATE = "2022-07-20"

IP = 'http://10.180.0.140:3001'

def search_in_database(date):
    # Implement your database search code to retrieve observations for the given date
    # Replace the code below with your actual implementation
    observations = []  # Placeholder for retrieving observations from the database
   
    startDate = datetime.datetime.strptime(date, "%Y-%m-%d")
    endDate = startDate + datetime.timedelta(days=1)
    startDate = startDate.strftime("%Y-%m-%d")
    endDate = endDate.strftime("%Y-%m-%d")

    data = {
        "type": "get",
        "startDate": startDate,
        "endDate": endDate,
    }

    res = requests.post(f"{IP}/reduction/individualfile", data=json.dumps(data), headers=header)
    for file in res.json()['msg']:
        if file['file_type'] == "BIAS":
            observations.append(file['file_name'])

    return observations

def search_observations(start_date, end_date):
    current_date = start_date
    block_dates = []
    observations = []

    while current_date <= end_date:
        # Perform database search for observations on the current date
        observations += search_in_database(current_date.strftime("%Y-%m-%d"))

        if len(observations) > 80:
            print("Block found: " + start_date.strftime("%Y-%m-%d") + " - " + current_date.strftime("%Y-%m-%d"))
            block_dates.append({"start": start_date.strftime("%Y-%m-%d"), "end": current_date.strftime("%Y-%m-%d"), "observations": len(observations)})
            observations = []
            start_date = current_date + datetime.timedelta(days=1)
        
        current_date += datetime.timedelta(days=1)
    
    return block_dates


def create_bias_block(startDate, endDate):
    data = {
        "type": "create",
        "startDate": startDate,
        "endDate": endDate
    }
    res = requests.post(f"{IP}/reduction/biasblock", data=json.dumps(data), headers=header)
    print(res.json())

def process(block_id):
    data = {
        "type": "process",
        "id": block_id
        }
    res = requests.post(f"{IP}/reduction/biasblock", data=json.dumps(data), headers=header)
    print(res.json())

blocks = search_observations(datetime.datetime.strptime(START_DATE, "%Y-%m-%d"), datetime.datetime.strptime(END_DATE, "%Y-%m-%d")) 

for block in blocks:
    create_bias_block(block['start'], block['end'])

def get_blocks():
    data = {
        "type": "get",
        "startDate": START_DATE,
        "endDate": END_DATE
    }
    res = requests.post(f"{IP}/reduction/biasblock", data=json.dumps(data), headers=header)
    return (res.json()['msg'])

blocks = get_blocks()

for block in blocks:
    process(block['id'])
    




