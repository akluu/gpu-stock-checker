import os
import requests
import asyncio
import boto3
from datetime import datetime

BASE_URL = "https://api.bestbuy.com/v1/products(sku in(6429440))"
API_KEY = "?apiKey=" + os.environ.get("BBKEY")
OPTIONS = "&sort=onlineAvailability.asc&show=onlineAvailability,addToCartUrl,onlineAvailabilityUpdateDate&format=json"
full_link = BASE_URL + API_KEY + OPTIONS

async def getResponse():
    while True:
        response = requests.get(full_link)
        if response.status_code != 200:
            await asyncio.sleep(60)
            continue
        else:
            return response

def publishStock(url):
    arn = 'arn:aws:sns:us-west-2:729495428235:stock_alert'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=os.environ.get("AWSAK"),
        aws_secret_access_key=os.environ.get("AWSSAK"),
        region_name='us-west-2'
    )
    response = sns_client.publish(
        TopicArn=arn, Message="GPUS in Stock! Link: " + url)

def publishError():
    arn = 'arn:aws:sns:us-west-2:729495428235:code_broken_alert'
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=os.environ.get("AWSAK"),
        aws_secret_access_key=os.environ.get("AWSSAK"),
        region_name='us-west-2'
    )
    response = sns_client.publish(
        TopicArn=arn, Message="Code caught an error.")

async def main():
        in_stock = False
        attempts = 0
        while(not in_stock):
            try:
                task = asyncio.create_task(getResponse())
                response = await asyncio.wait_for(task, timeout = 60*60*24)
                in_stock = response.json()['products'][0]['onlineAvailability']
                last_time_in_stock = response.json()['products'][0]['onlineAvailabilityUpdateDate']
                url = response.json()['products'][0]['addToCartUrl']
                if(not in_stock):
                        print('Time=' + str(datetime.now()) + '- Attempt=' + str(attempts) + '- LastTimeInStock=' + str(last_time_in_stock))
                        attempts += 1
                else:
                    publishStock(url)
                await asyncio.sleep(3)
            except asyncio.TimeoutError:
                print("Bad Status Code")
                publishError()
                continue

asyncio.run(main())

