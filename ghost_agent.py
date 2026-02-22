import asyncio
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT STARTING ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
            await asyncio.sleep(5)
            
            # ★ 証拠写真を撮る
            await page.screenshot(path="evidence.png")
            print("SCREENSHOT TAKEN: evidence.png")
            
            content = await page.content()
            if "1局" in content:
                print("TARGET FOUND")
                await page.fill('textarea', "CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
                # 送信後の様子も撮っておく
                await asyncio.sleep(2)
                await page.screenshot(path="after_send.png")
            else:
                print("TARGET NOT FOUND")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
