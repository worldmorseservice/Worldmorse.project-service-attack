import asyncio
import os
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT: FORCING TRANSMISSION ---")
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
            
            # 保存ボタンをクリック
            save_button = page.get_by_text("保存")
            await save_button.click()
            await asyncio.sleep(3)

            # 2. メッセージを入力
            print("Typing message...")
            await page.fill('textarea', "CQ DE Worldmorse_AI")
            await asyncio.sleep(1)

            # 3. 【最重要】「この内容を送信」ボタンを強制クリック
            print("Locating TRANSMIT button...")
            # ボタン要素を直接指定してクリックします
            send_button = page.locator('button:has-text("この内容を送信")')
            
            if await send_button.count() > 0:
                print("Clicking the green button now...")
                await send_button.click()
                # クリックが反映されるまで少し待つ
                await asyncio.sleep(2)
                print("TRANSMISSION COMPLETE!")
            else:
                print("Button not found by text, trying fallback Enter key...")
                await page.keyboard.press("Enter")
            
            # 最終確認の撮影
            await page.screenshot(path="after_click_verification.png")

        except Exception as e:
            print(f"ERROR: {e}")
            await page.screenshot(path="final_debug.png")
        finally:
            await browser.close()
            print("--- AGENT OFFLINE ---")

if __name__ == "__main__":
    asyncio.run(start())
