import asyncio
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- STARTING GHOST AGENT ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
            await asyncio.sleep(5)
            content = await page.content()
            if "1局" in content:
                print("TARGET FOUND: SENDING MESSAGE")
                await page.fill('textarea', "CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
            else:
                print("TARGET NOT FOUND: IDLE")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
