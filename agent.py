import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # ブラウザを起動
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("WorldMorseに接続中...")
            # タイムアウトを長めに設定
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle", timeout=60000)
            
            # 画面が安定するまで待機
            await asyncio.sleep(5)

            # ページ全体のテキストを取得
            content = await page.content()
            
            # 「1局」という文字があるか判定
            if "1局" in content:
                print("ターゲット確認：管理者が1人で待機中。出動します。")
                message = "CQ DE AI_GHOST. UR SIG 5NN. 73 K"
                
                # 入力と送信の試行
                await page.fill('textarea', message)
                
                # ボタンを探してクリック（変換ボタンがあれば押す）
                convert_btn = await page.query_selector('button:has-text("変換")')
                if convert_btn:
                    await convert_btn.click()
                    await asyncio.sleep(1)
                
                # 送信ボタンを押す
                send_btn = await page.query_selector('button:has-text("送信")')
                if send_btn:
                    await send_btn.click()
                    print(f"送信完了: {message}")
                else:
                    # ボタン名が違う可能性を考慮して「送信」を含むものを探す
                    await page.click('button:get-by-text("送信")')
            else:
                print("現在は1局ではありません。出番を待ちます。")

        except Exception as e:
            print(f"実行中にエラーが発生しました: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    # ここで確実に main() を呼び出します
    asyncio.run(main())
