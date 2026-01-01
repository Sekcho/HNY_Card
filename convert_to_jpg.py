"""
Convert HTML to JPG using Playwright
"""
import asyncio
from playwright.async_api import async_playwright
import os

async def html_to_jpg():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, 'new-year-card.html')
    output_file = os.path.join(current_dir, 'new-year-card.jpg')

    # Convert to file URL
    html_url = f'file:///{html_file.replace(chr(92), "/")}'

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={'width': 900, 'height': 1400}
        )

        # Navigate to HTML file
        await page.goto(html_url)

        # Wait for fonts and animations to load
        await asyncio.sleep(3)

        # Take screenshot
        await page.screenshot(
            path=output_file,
            type='jpeg',
            quality=95,
            full_page=True
        )

        await browser.close()

    print(f'✓ Successfully converted to: {output_file}')

if __name__ == '__main__':
    asyncio.run(html_to_jpg())
