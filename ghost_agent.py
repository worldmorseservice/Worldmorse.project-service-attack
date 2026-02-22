import asyncio
from playwright.async_api import async_playwright

async def start():
    async with async_playwright() as p:
        print("--- GHOST AGENT STARTING ---")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # あなたのサイトへアクセス
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
            await asyncio.sleep(5)
            
            content = await page.content()
            if "1局" in content:
                print("TARGET FOUND: SENDING MORSE MESSAGE")
                # テキストエリアに入力
                await page.fill('textarea', "CQ DE AI_GHOST")
                # 送信ボタンをクリック
                btn = await page.query_selector('button:has-text("送信")')
                if btn:
                    await btn.click()
                print("MESSAGE SENT SUCCESS")
            else:
                print("TARGET NOT FOUND: IDLE STATUS")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await browser.close()
            print("--- END ---")

if __name__ == "__main__":
    asyncio.run(start())
