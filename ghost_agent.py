import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT: SETTING CALLSIGN & SENDING ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Connecting...")
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # 1. 最初に表示される設定窓（コールサイン設定）を操作
            print("Setting Callsign...")
            # 1つ目の入力欄（コールサイン）に「AI_GHOST」と入力
            # ページ内の最初の入力欄(input)を狙います
            await page.fill('input[type="text"]', "AI_GHOST")
            await asyncio.sleep(1)

            # 2. 保存ボタン（フロッピーのアイコンなど）をクリック
            # 画像から、黄色い「保存」ボタン（button）を探してクリックします
            print("Clicking Save button...")
            save_button = await page.query_selector('button:has-text("保存"), button:has-child(i)')
            if save_button:
                await save_button.click()
            else:
                # ボタンが見つからない場合はEnterで代用
                await page.keyboard.press("Enter")
            
            await asyncio.sleep(3)
            print("Callsign set. Now sending message...")

            # 3. メッセージ入力欄（textarea）を探して書き込む
            textarea = await page.query_selector('textarea')
            if textarea:
                await textarea.fill("CQ DE AI_GHOST")
                await page.keyboard.press("Enter")
                await asyncio.sleep(3)
                print("Message sent!")
                await page.screenshot(path="final_verified_send.png")
            else:
                print("Textarea not found.")

        except Exception as e:
            print(f"ERROR: {e}")
            await page.screenshot(path="error_step.png")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
