import os
import asyncio
from playwright.async_api import async_playwright

async def start_agent():
    async with async_playwright() as p:
        print("--- 接続開始 ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)
            content = await page.content()
            if "1局" in content:
                print("ターゲット確認：1局。送信を試みます。")
                await page.fill('textarea', "CQ DE AI_GHOST. UR SIG 5NN.")
                # ボタンを探してクリック
                for btn_text in ["送信", "変換"]:
                    btn = await page.query_selector(f'button:has-text("{btn_text}")')
                    if btn:
                        await btn.click()
                        await asyncio.sleep(2)
                print("送信処理完了")
            else:
                print("現在は1局ではないようです。")
        except Exception as e:
            print(f"エラー内容: {e}")
        finally:
            await browser.close()
            print("--- 終了 ---")

if __name__ == "__main__":
    # 関数名を start_agent にしたので、ここも合わせます
    asyncio.run(start_agent())
