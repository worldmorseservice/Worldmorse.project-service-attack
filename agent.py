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
　　　　　
　　　　 # サイトにアクセス
        await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
        
        # 1. ページ全体から「局」という文字が含まれる要素を探す（より柔軟な探し方）
        try:
            # 5秒だけ待ってみる
            element = await page.wait_for_selector("text=/局/", timeout=5000)
            online_status = await element.inner_text()
            print(f"取得したステータス: {online_status}")
        except:
            # もし見つからなければ、一旦「1局」とみなして進む（テスト用）
            print("人数表示が見つかりませんでしたが、続行します。")
            online_status = "1局"
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
