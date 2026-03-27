TikTok Social Listener (Data Scraper)
A Python-based automation tool designed for market research and trend analysis on TikTok. It searches for specific keywords (e.g., food categories), extracts engagement metrics, and bypasses common scraping limitations using advanced HTML parsing.

Key Features
Automated Keyword Discovery: Iterates through a list of categories (like "Diyet Yemekleri" or "Pratik Tarifler") to find trending content.
Hybrid Extraction Logic: Uses Selenium for navigation and Regex (Regular Expressions) to "force-extract" view counts (1.2M, 500K, etc.) directly from the HTML source when standard selectors fail.
Anti-Bot Measures: Includes random sleep intervals and a Manual CAPTCHA Pause system that halts the script to let the user solve verification puzzles before continuing.
Metric Normalization: Automatically converts TikTok's shorthand notation (K, M, B) into raw integers for accurate sorting and analysis.
Data Export: Generates a structured Excel (.xlsx) report sorted by view counts to highlight the most viral content.

Installation
1. Prerequisites
Python 3.x
Google Chrome Browser
ChromeDriver (handled automatically by webdriver-manager)

2. Install Dependencies
Bash
pip install selenium webdriver-manager pandas openpyxl

How to Use
Define Your Keywords: Edit the yemekler list in the script to include the terms you want to track:

Python
yemekler = ["Trendler", "Mutfak Sırları"]

Run the Script:
Bash
python TikTok_dinleme.py
Handle Captchas: If TikTok displays a verification screen, the terminal will prompt you. Solve it in the browser window, then press ENTER in the terminal to resume.

Analyze Results: Check the generated tiktok_final_html.xlsx file to see which videos performed best in each category.

Technical Logic
HTML Regex Parsing: The function html_icinden_izlenme_bul scans the raw page source for patterns like >(\d+(\.\d+)?[KMB])< to ensure data capture even if the UI layout changes.
Sorting Engine: Converts strings like "1.5M" into 1500000 using a custom lambda function to allow numerical sorting in Excel.
Infinite Scroll Support: Includes logic to interact with the page to load more content dynamically.

⚠️ Disclaimer
This tool is intended for personal research and competitive analysis. Automated scraping of TikTok may violate their Terms of Service. Use responsibly and avoid high-frequency requests that could lead to IP rate-limiting.
