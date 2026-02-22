import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT: INITIAL SETUP & SENDING ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Connecting to WorldMorse...")
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # 1. コールサインの入力
            print("Setting up identity...")
            # 「例: JA1ABC」と書かれた欄にコールサインを入力
            await page.fill('input[placeholder*="例: JA1ABC"]', "Worldmorse_AI") # ←ここを好きな英数字に変えられます
            
            # 2. オペレーター名の入力（任意ですが入れておくと確実です）
            # 「例: Taro」と書かれた欄に名前を入力
            await page.fill('input[placeholder*="例: Taro"]', "worldmorse_AI") # ←ここを好きな名前に変えられます
            await asyncio.sleep(1)

            # 3. 黄色い「保存」ボタンをクリック
            print("Clicking 'Save' button...")
            save_button = page.get_by_text("保存")
            await save_button.click()
            
            # 画面が切り替わるのを待つ
            print("Settings saved. Ready to communicate.")
            await asyncio.sleep(3)
            
            # 保存後の状態を念のため撮影
            await page.screenshot(path="after_save_check.png")

            # 4. ついにメッセージ送信
            print("Attempting to send Morse message...")
            textarea = await page.query_selector('textarea')
            if textarea:
                await textarea.fill("CQ DE Worldmorse_AI")
                await page.keyboard.press("Enter")
                await asyncio.sleep(3)
                print("SUCCESS: Message sent to the world!")
                await page.screenshot(path="final_verified_send.png")
            else:
                print("Textarea not found. The popup might still be open.")
                await page.screenshot(path="failed_popup_issue.png")

        except Exception as e:
            print(f"ERROR: {e}")
            await page.screenshot(path="final_error_log.png")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
