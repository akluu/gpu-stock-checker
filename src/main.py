import requests
import asyncio
from publish import publishError, publishStock
from get import get_key
from datetime import datetime

BASE_URL = "https://api.bestbuy.com/v1/products(sku in(6429440))"
API_KEY = "?apiKey=" + get_key("BEST_BUY_KEY")
OPTIONS = "&sort=onlineAvailability.asc&show=onlineAvailability,addToCartUrl,onlineAvailabilityUpdateDate&format=json"
full_link = BASE_URL + API_KEY + OPTIONS

async def getResponse():
    while True:
        response = requests.get(full_link)
        if response.status_code != 200:
            await asyncio.sleep(60*5)
            continue
        else:
            return response

async def main():
        in_stock = False
        attempts = 0
        while(not in_stock):
            try:
                task = asyncio.create_task(getResponse())
                response = await asyncio.wait_for(task, timeout = 60*60)
                in_stock = response.json()['products'][0]['onlineAvailability']
                last_time_in_stock = response.json()['products'][0]['onlineAvailabilityUpdateDate']
                url = response.json()['products'][0]['addToCartUrl']
                if(not in_stock):
                        print('Time=' + str(datetime.utcnow()) + '- Attempt=' + str(attempts) + '- LastTimeInStock=' + str(last_time_in_stock))
                        attempts += 1
                else:
                    publishStock(url)
                await asyncio.sleep(15)
            except Exception as e:
                print(e)
                publishError()
                asyncio.sleep(60*60)
                continue

asyncio.run(main())

