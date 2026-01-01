"""
Card generator for creating HTML and converting to JPG
"""
import asyncio
from playwright.async_api import async_playwright
import os
from jinja2 import Template
from config import THEMES, FONTS, FONT_SIZES


class CardGenerator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.template_path = os.path.join(base_dir, 'templates', 'card_template.html')
        self.output_dir = os.path.join(base_dir, 'static', 'generated')

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, data):
        """
        Generate HTML from template with user data

        Args:
            data: Dictionary containing:
                - year_cs: Christian year
                - year_be: Buddhist year
                - wishes: List of wish texts
                - signature: Signature name
                - photo_path: Path to uploaded photo
                - theme: Theme name
                - thai_font: Thai font key
                - english_font: English font key
                - font_sizes: Dictionary of font size settings

        Returns:
            Tuple of (html_content, html_filepath)
        """
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        template = Template(template_content)

        # Get theme colors
        theme = THEMES.get(data.get('theme', 'blue-gold'))

        # Get fonts
        thai_font_key = data.get('thai_font', 'noto-sans-thai')
        english_font_key = data.get('english_font', 'poppins')

        thai_font = FONTS['thai'][thai_font_key]
        english_font = FONTS['english'][english_font_key]

        # Get font sizes
        font_sizes = data.get('font_sizes', {})

        # Convert photo path to absolute path
        photo_path = data.get('photo_path', '')
        if photo_path.startswith('../static/'):
            # Convert relative path to absolute path
            # ../static/uploads/filename.jpg -> D:/2026/Card/static/uploads/filename.jpg
            relative_part = photo_path.replace('../static/', '')
            photo_path = os.path.join(self.base_dir, 'static', relative_part).replace('\\', '/')

        # Prepare template data
        template_data = {
            'year_cs': data.get('year_cs', 2026),
            'year_be': data.get('year_be', 2569),
            'wishes': data.get('wishes', []),
            'signature': data.get('signature', ''),
            'photo_path': photo_path,
            'theme': theme,
            'thai_font': thai_font,
            'english_font': english_font,
            'font_sizes': {
                'year_badge': FONT_SIZES['year-badge'].get(font_sizes.get('year-badge', 'medium'), '36px'),
                'main_title': FONT_SIZES['main-title'].get(font_sizes.get('main-title', 'medium'), '72px'),
                'thai_title': FONT_SIZES['thai-title'].get(font_sizes.get('thai-title', 'medium'), '48px'),
                'wishes': FONT_SIZES['wishes'].get(font_sizes.get('wishes', 'medium'), '20px'),
                'signature': FONT_SIZES['signature'].get(font_sizes.get('signature', 'medium'), '36px'),
            }
        }

        # Render template
        html_content = template.render(**template_data)

        # Save HTML file
        html_filename = f'card_{data.get("year_cs", 2026)}.html'
        html_filepath = os.path.join(self.output_dir, html_filename)

        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_content, html_filepath

    async def convert_to_jpg(self, html_filepath, output_filename=None):
        """
        Convert HTML to JPG using Playwright

        Args:
            html_filepath: Path to HTML file
            output_filename: Optional output filename (without extension)

        Returns:
            Path to generated JPG file
        """
        if output_filename is None:
            output_filename = os.path.splitext(os.path.basename(html_filepath))[0]

        output_path = os.path.join(self.output_dir, f'{output_filename}.jpg')

        # Convert to file URL
        html_url = f'file:///{html_filepath.replace(chr(92), "/")}'

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
                path=output_path,
                type='jpeg',
                quality=95,
                full_page=True
            )

            await browser.close()

        return output_path

    def generate_card(self, data):
        """
        Generate both HTML and JPG for the card

        Args:
            data: Dictionary containing card data

        Returns:
            Tuple of (html_path, jpg_path)
        """
        # Generate HTML
        html_content, html_path = self.generate_html(data)

        # Convert to JPG
        jpg_path = asyncio.run(self.convert_to_jpg(html_path))

        return html_path, jpg_path
