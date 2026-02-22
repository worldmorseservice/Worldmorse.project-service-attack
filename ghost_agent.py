import asyncio
import os
from playwright.async_api import async_playwright

async def start():
async with async_playwright() as p:
print("--- STARTING GHOST AGENT ---")
browser = await p.chromium.launch(headless=True)
page = await browser.new_page()

if name == "main":
asyncio.run(start())
