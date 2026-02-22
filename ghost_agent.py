import asyncio
import re
import time
from playwright.async_api import async_playwright

# --- 設定：AIのアイデンティティ ---
CALLSIGN = "Worldmorse_AI"
OP_NAME = "Gemini_Agent"

# --- 内部状態管理用 ---
state = {
    "last_called_time": 0,    # 最後に呼びかけられた時刻 (UNIXタイム)
    "last_interactor": None,  # 最後に話しかけてきた相手のコールサイン
}

# 監視キーワード
AI_NAMES = ["WORLDMORSE", "worldmorse", "WorldMorse", "Worldmorse"]
NG_PATTERNS = [r"NIGG", r"NIGA", r"N1GA", r"FUCK", r"SHIT", r"BAKA"]

async def monitor_and_respond(page):
    print(f"--- 監視サイクル: {time.strftime('%H:%M:%S')} ---")
    current_time = time.time()
    
    # 1. 画面情報の取得
    content = await page.content()
    messages = await page.query_selector_all('div.message-item')
    
    latest_msg_text = ""
    latest_msg_sender = ""
    
    if messages:
        # 最新のメッセージと送信者を取得 (サイトの構造に合わせた想定)
        full_text = await messages[-1].inner_text()
        # 例: "JA1ABC: HELLO" という形式を想定
        if ":" in full_text:
            latest_msg_sender, latest_msg_text = full_text.split(":", 1)
            latest_msg_sender = latest_msg_sender.strip()
            latest_msg_text = latest_msg_text.strip()
        else:
            latest_msg_text = full_text.strip()

    # 2. オンライン局数の確認
    online_count = 1
    online_match = re.search(r"オンライン局: (\d+)局", content)
    if online_match:
        online_count = int(online_match.group(1))

    # --- 判定ロジック ---

    # A. NGワードチェック (即座に注意)
    for pattern in NG_PATTERNS:
        if re.search(pattern, latest_msg_text, re.IGNORECASE):
            await send_message(page, f"DE {CALLSIGN} STOP. PSE KEEP MANNER.")
            return

    # B. AIへの呼びかけ検知 (5分間のフラグを立てる)
    is_called = any(name in latest_msg_text for name in AI_NAMES)
    if is_called:
        print(f"呼びかけ検知: {latest_msg_sender} さん")
        state["last_called_time"] = current_time
        state["last_interactor"] = latest_msg_sender
        await send_message(page, f"QRZ? {latest_msg_sender} DE {CALLSIGN} GA UR 599 BK")
        return

    # C. 呼びかけから5分以内のチャットへの反応
    if current_time - state["last_called_time"] < 300: # 300秒 = 5分
        if latest_msg_text and latest_msg_sender != CALLSIGN:
            print(f"対話継続中: {latest_msg_sender}")
            # 相手の内容に応じた簡単な返事 (定型)
            await send_message(page, f"R FB {state['last_interactor']} DE {CALLSIGN} TU 73")
            # 返事をしたので一旦タイマーを少し進めて連投を防ぐ工夫なども可能
            return

    # D. 他に局がいない時の「CQ CQ CQ」への反応
    # 自分以外の1局（相手）がCQを出している場合
    if online_count == 2 and "CQ CQ CQ" in latest_msg_text and latest_msg_sender != CALLSIGN:
        print("CQへの応答")
        await send_message(page, f"{latest_msg_sender} DE {CALLSIGN} GE UR 599 K")
        state["last_called_time"] = current_time # 会話モードへ
        state["last_interactor"] = latest_msg_sender
        return

    # E. 完全に一人きりの時
    if online_count == 1:
        # たまにCQを出して存在を示す
        if int(current_time) % 120 < 30: # 2分に1回、30秒間隔のタイミングで
            await send_message(page, f"CQ CQ CQ DE {CALLSIGN} K")

async def send_message(page, text):
    textarea = await page.query_selector('textarea')
    if textarea:
        await textarea.fill(text)
        await page.click('button:has-text("この内容を送信")')
        print(f">>> 送信: {text}")
        await asyncio.sleep(2)

async def start():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://worldmorse-project.onrender.com", wait_until="networkidle")
            # ログイン・保存
            await page.fill('input[placeholder*="例: JA1ABC"]', CALLSIGN)
            await page.fill('input[placeholder*="例: Taro"]', OP_NAME)
            await page.click('button:has-text("保存")')
            await asyncio.sleep(5)

            # GitHub Actionsの制限(約6時間)内でループ
            # 30秒×20回 = 約10分間監視して終了（これをcronで5分おきに回すのが効率的）
            for _ in range(20):
                await monitor_and_respond(page)
                await asyncio.sleep(30)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(start())
