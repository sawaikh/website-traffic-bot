import asyncio
import random
import time
import requests
from playwright.async_api import async_playwright

PANEL_IP = "YOUR_PANEL_IP"  # Auto injected from GitHub, don't change manually

async def visit_website(task):
    url = task["url"]
    duration = int(task["duration"])
    click_ads = task["click_ads"]

    user_agents = [
        # Mix of mobile and desktop
        "Mozilla/5.0 (Linux; Android 10) Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    ]
    user_agent = random.choice(user_agents)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=user_agent, locale="en-US")
        page = await context.new_page()

        try:
            await page.goto(url, timeout=60000)
            start = time.time()

            while time.time() - start < duration:
                await page.mouse.wheel(0, random.randint(200, 800))
                await asyncio.sleep(random.randint(3, 6))

            if click_ads == "yes":
                ads = await page.query_selector_all("iframe, a[href*='ad']")
                if ads:
                    await ads[0].click()

        except Exception as e:
            print("Bot error:", e)
        await browser.close()

def get_task():
    try:
        res = requests.get(f"http://{PANEL_IP}:8000/run_task")
        return res.json()
    except:
        return None

async def main():
    ip = requests.get("https://api.ipify.org").text
    try:
        requests.post(f"http://{PANEL_IP}:8000/register_vps", json={"ip": ip})
    except:
        pass

    while True:
        task = get_task()
        if task:
            await visit_website(task)
        await asyncio.sleep(10)

asyncio.run(main())
