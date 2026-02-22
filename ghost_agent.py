import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT: FINAL TRANSMISSION ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Connecting to WorldMorse...")
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            # 1. 局情報の設定（コールサインと名前）
            print("Setting Identity...")
            await page.fill('input[placeholder*="例: JA1ABC"]', "Worldmorse_AI")
            await page.fill('input[placeholder*="例: Taro"]', "Gemini_Agent")
            await asyncio.sleep(1)

            # 2. 「保存」ボタンをクリック
            print("Saving profile...")
            save_button = page.get_by_text("保存")
            await save_button.click()
            await asyncio.sleep(3) # 画面切り替え待ち

            # 3. メッセージを入力
            print("Preparing message...")
            textarea = await page.query_selector('textarea')
            if textarea:
                await textarea.fill("CQ DE Worldmorse_AI")
                await asyncio.sleep(1)
                
                # 4. 【重要】緑色の「この内容を送信」ボタンを直接クリック
                print("Clicking TRANSMIT button...")
                # ボタンのテキスト「この内容を送信」を狙い撃ちします
                send_button = page.get_by_text("この内容を送信")
                if await send_button.is_visible():
                    await send_button.click()
                    print("TRANSMITTED SUCCESSFULLY!")
                else:
                    # 見つからない場合はEnterキーを念押し
                    await page.keyboard.press("Enter")
                
                await asyncio.sleep(3)
                await page.screenshot(path="mission_complete.png")
            else:
                print("Textarea not found.")

        except Exception as e:
            print(f"ERROR: {e}")
            await page.screenshot(path="final_debug_error.png")
        finally:
            await browser.close()
            print("--- AGENT OFFLINE ---")

if __name__ == "__main__":
    asyncio.run(start())
