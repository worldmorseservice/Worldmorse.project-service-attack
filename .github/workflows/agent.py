import os
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Cookie保存用のファイルがあれば読み込む
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json" if os.path.exists("auth.json") else None)
        page = await context.new_page()
        
        await page.goto(os.getenv("TARGET_URL"))

        # 1. 人数チェック (セレクタは実際のサイトに合わせて調整が必要)
        online_text = await page.inner_text(".online-status-selector") 
        
        if "1局" in online_text:
            # 2. 翻訳機にメッセージを入力
            # ChatGPT連携部分は一旦固定文字でテスト
            message = "CQ DE AI_GHOST. KONBANWA." 
            
            await page.fill('textarea[placeholder="テキストを入力..."]', message)
            await page.click('button:has-text("テキスト → モールス")')
            await asyncio.sleep(2) # 変換待ち
            await page.click('button:has-text("この内容を送信")')
            
            # Cookie（アカウント状態）を保存
            await context.storage_state(path="auth.json")
            print("送信完了しました！")
        
        await browser.close()

asyncio.run(run())import os
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Cookie保存用のファイルがあれば読み込む
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="auth.json" if os.path.exists("auth.json") else None)
        page = await context.new_page()
        
        await page.goto(os.getenv("TARGET_URL"))

        # 1. 人数チェック (セレクタは実際のサイトに合わせて調整が必要)
        online_text = await page.inner_text(".online-status-selector") 
        
        if "1局" in online_text:
            # 2. 翻訳機にメッセージを入力
            # ChatGPT連携部分は一旦固定文字でテスト
            message = "CQ DE AI_GHOST. KONBANWA." 
            
            await page.fill('textarea[placeholder="テキストを入力..."]', message)
            await page.click('button:has-text("テキスト → モールス")')
            await asyncio.sleep(2) # 変換待ち
            await page.click('button:has-text("この内容を送信")')
            
            # Cookie（アカウント状態）を保存
            await context.storage_state(path="auth.json")
            print("送信完了しました！")
        
        await browser.close()

asyncio.run(run())
