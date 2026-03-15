import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Listen for console events
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        
        try:
            print("Navigating to http://localhost:5174/login")
            await page.goto("http://localhost:5174/login", wait_until="networkidle")
            print("Page loaded. Waiting 2 seconds for React to mount...")
            await page.wait_for_timeout(2000)
            print("Done collecting logs.")
        except Exception as e:
            print(f"Failed to navigate: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
