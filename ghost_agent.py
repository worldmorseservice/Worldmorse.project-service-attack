import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT STARTING ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # サイトへ接続
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)
            
            # ポップアップをEscキーで消す
            await page.keyboard.press("Escape")
            await asyncio.sleep(2)
            
            # フォントが効いているか確認のための撮影
            await page.screenshot(path="font_check.png")

            # 文字が読めなくても、入力欄（textarea）があれば書き込む
            textarea = await page.query_selector('textarea')
            if textarea:
                print("Textarea found! Injecting message...")
                await textarea.fill("CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
                await asyncio.sleep(3)
                await page.screenshot(path="after_send.png")
            else:
                print("Textarea not found. Trying another way...")
                
        except Exception as e:
            print(f"ERROR: {e}")
            await page.screenshot(path="error.png")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
