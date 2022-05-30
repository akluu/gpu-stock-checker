import os
import requests
import asyncio
from datetime import datetime

BASE_URL = "https://api.bestbuy.com/v1/products(sku in(6429440))"
API_KEY = "?apiKey=" + os.environ.get("BBKEY")
OPTIONS = "&sort=onlineAvailability.asc&show=onlineAvailability,addToCartUrl&format=json"
full_link = BASE_URL + API_KEY + OPTIONS

# print(os.environ.get("BBKEY"))
# response = requests.get(full_link)
# print(response.status_code)
# print(response.json())

async def getResponse():
    while True:
        response = requests.get(full_link)
        if response.status_code != 200:
            await asyncio.sleep(60)
            continue
        else:
            return response

async def main():
        in_stock = False
        attempts = 0
        while(not in_stock):
            try:
                task = asyncio.create_task(getResponse())
                response = await asyncio.wait_for(task, timeout = 60*60*24)
                in_stock = response.json()['products'][0]['onlineAvailability']
                if(not in_stock):
                        print('Time=' + str(datetime.now()) + '- Attempt=' + str(attempts))
                        attempts += 1
                await asyncio.sleep(3)
            except asyncio.TimeoutError:
                print("Bad Status Code")
                continue

asyncio.run(main())

