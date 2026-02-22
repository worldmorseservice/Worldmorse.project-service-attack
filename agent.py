import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # ブラウザを起動
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # サイトにアクセス
        await page.goto("https://worldmorse-project.onrender.com")
        await asyncio.sleep(5) # 読み込み待ち

        # オンライン局の人数を確認
        # 画面上の「0局」や「1局」というテキストを探す
        online_status = await page.inner_text('.online-count-selector') # セレクタは必要に応じて調整

        if "1局" in online_status:
            print("管理者が1人でログイン中。メッセージを送信します。")
            
            # メッセージ入力（例として固定。OpenAI API連携も可能）
            message = "CQ DE AI_GHOST. UR SIG 5NN. 73 K"
            
            # 翻訳機を操作
            await page.fill('textarea[placeholder="テキストを入力..."]', message)
            await page.click('button:has-text("テキスト → モールス")')
            await asyncio.sleep(2)
            await page.click('button:has-text("この内容を送信")')
            print(f"送信完了: {message}")
        else:
            print(f"現在の状況: {online_status}。出番ではありません。")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
