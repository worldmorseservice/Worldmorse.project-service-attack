import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("--- エージェント起動 ---")
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5)

            content = await page.content()
            if "1局" in content:
                print("ターゲット確認：1局のみです。送信準備に入ります。")
                # ここに送信処理...
            else:
                print("現在は1局ではありません。終了します。")
        except Exception as e:
            print(f"エラー発生: {e}")
        finally:
            await browser.close()
            print("--- エージェント終了 ---")

if __name__ == "__main__":
    # ここがエラーの元です。必ず 'main' という名前であることを確認してください。
    asyncio.run(main())
