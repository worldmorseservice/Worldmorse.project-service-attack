import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # ブラウザを起動（ヘッドレスモード）
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # サイトへ移動
        print("WorldMorseに接続中...")
        await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
        
        # 画面が安定するまで少し待つ
        await asyncio.sleep(5)

        # 画面の全テキストを取得して人数を確認
        content = await page.content()
        if "1局" in content:
            print("ターゲット確認：管理者が1人で待機中。出動します。")
            
            # 送信するメッセージ
            message = "CQ DE AI_GHOST. UR SIG 5NN. 73 K"
            
            # メッセージを入力欄（textarea）に書き込む
            try:
                await page.fill('textarea', message)
                # 送信に関わるボタン（変換や送信）を順にクリック
                # サイトのボタン名に合わせて調整していますが、まずはテキストで探します
                if await page.query_selector('button:has-text("変換")'):
                    await page.click('button:has-text("変換")')
                    await asyncio.sleep(1)
                
                await page.click('button:has-text("送信")')
                print(f"送信処理を完了しました: {message}")
            except Exception as e:
                print(f"入力または送信中にエラーが発生しましたが、続行しました: {e}")
        else:
            print("現在は1局ではありません。出番を待ちます。")

        await browser.close()

if __name__ == "__main__":
    # ここを main() に修正しました
    asyncio.run(main())
