import os
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # ブラウザを起動（ヘッドレスモード）
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # サイトへ移動（読み込み完了まで待機）
        print("WorldMorseに接続中...")
        await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
        
        # 5秒待機して画面を安定させる
        await asyncio.sleep(5)

        # 画面上に「1局」という文字があるかチェック
        content = await page.content()
        if "1局" in content:
            print("ターゲット確認：管理者が1人で待機中。出動します。")
            
            # メッセージを入力して送信
            message = "CQ DE AI_GHOST. UR SIG 5NN. 73 K"
            
            # セレクタを使わず、入力欄を探して入力
            await page.fill('textarea', message)
            # 送信ボタン（モールス変換ボタンなど）を特定してクリック
            # サイトの仕様に合わせて「送信」や「変換」ボタンを狙い撃ち
            try:
                await page.click('button:has-text("送信")')
                print(f"送信成功: {message}")
            except:
                print("ボタンクリックに失敗しましたが、入力は試みました。")
        else:
            print("現在は1局ではありません。出番を待ちます。")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
if __name__ == "__main__":
    asyncio.run(main())
