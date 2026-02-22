import asyncio
from playwright.async_api import async_playwright

async def run_ghost():
    async with async_playwright() as p:
        print("--- START ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
            await asyncio.sleep(3)
            content = await page.content()
            
            if "1局" in content:
                print("TARGET: 1 STATION. SENDING...")
                await page.fill('textarea', "CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
                print("DONE")
            else:
                print(f"STATUS: {content[:50]}...") # 最初の50文字だけ表示
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(run_ghost())
