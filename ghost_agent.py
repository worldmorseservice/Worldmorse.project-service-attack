import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- STARTING GHOST AGENT ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Connecting...")
            # サイトを開く
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            
            # 【重要】ここで写真を撮る命令
            print("Taking screenshot...")
            await page.screenshot(path="evidence.png")
            
            content = await page.content()
            if "1局" in content:
                print("TARGET FOUND")
                await page.fill('textarea', "CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
                # 送信後の写真
                await page.screenshot(path="after_send.png")
            else:
                print("TARGET NOT FOUND")
        except Exception as e:
            print(f"ERROR: {e}")
            # エラー時も写真を撮る
            await page.screenshot(path="error.png")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
