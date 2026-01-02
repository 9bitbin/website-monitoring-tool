import os
import asyncio
from datetime import datetime

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app = FastAPI(title="Website Monitoring Tool")

monitored_websites = []
website_status = {}
CHECK_INTERVAL = 60  # seconds

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class Website(BaseModel):
    url: str

async def send_discord_alert(message: str):
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json={"content": message})

async def check_website(url: str):
    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        log_file = os.path.join(
            LOG_DIR,
            f"{url.replace('https://','').replace('http://','').replace('/','_')}.log"
        )

        previous_status = website_status.get(url, "UNKNOWN")

        try:
            start = datetime.now()
            response = await client.get(url)
            elapsed = (datetime.now() - start).total_seconds() * 1000
            current_status = "UP"
            message = (
                f"{datetime.now()} | {url} | UP | "
                f"Status: {response.status_code} | Time: {int(elapsed)}ms"
            )
        except httpx.RequestError:
            current_status = "DOWN"
            message = f"{datetime.now()} | {url} | DOWN"

        if previous_status != "UNKNOWN" and previous_status != current_status:
            emoji = "🚨" if current_status == "DOWN" else "✅"
            alert = (
                f"{emoji} **Website Status Change**\n"
                f"URL: {url}\n"
                f"Status: {previous_status} → {current_status}\n"
                f"Time: {datetime.now()}"
            )
            print(alert)
            await send_discord_alert(alert)

        website_status[url] = current_status

        print(message)
        with open(log_file, "a") as f:
            f.write(message + "\n")

async def monitor_loop():
    while True:
        if monitored_websites:
            tasks = [check_website(url) for url in monitored_websites]
            await asyncio.gather(*tasks)
        await asyncio.sleep(CHECK_INTERVAL)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_loop())

@app.post("/monitor")
def add_website(site: Website):
    if site.url not in monitored_websites:
        monitored_websites.append(site.url)
        return {"message": f"{site.url} added for monitoring"}
    return {"message": f"{site.url} already being monitored"}

@app.get("/monitor")
def list_websites():
    return {"monitored_websites": monitored_websites}
