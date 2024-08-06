# Market Trend and Sentiment Analyzer for Amazon Products

## Overview

The **Market Trend and Sentiment Analyzer for Amazon Products** is a Python-based tool designed to extract and analyze product information from Amazon. It helps users understand market trends and customer feedback for any given product category. The scraper retrieves detailed product data, performs sentiment analysis on reviews, extracts key features, provides actionable recommendations, and visualizes the potential success of implementing these improvements.

## Features

- **Category-Based Scraping:** Allows users to specify a product category to scrape from Amazon.
- **Product Information Extraction:** Retrieves detailed product information including description, price, rating, review count, and reviews.
- **Sentiment Analysis:** Analyzes reviews to classify them as positive, negative, or neutral using Natural Language Processing (NLP).
- **Feature Extraction:** Identifies unique features mentioned in positive and negative reviews to understand user preferences and pain points.
- **Recommendations:** Provides tailored recommendations based on extracted features to enhance the product and address common issues.
- **Success Rate Visualization:** Generates visualizations to represent the potential success rate of adopting suggested improvements and leveraging current market trends.
- **CSV Export:** Saves all extracted information, analysis, and recommendations into a CSV file for easy access and further analysis.

## Requirements

- **Python 3.x**
- **Selenium:** For web scraping and interaction with Amazon pages.
- **BeautifulSoup4:** For parsing HTML content.
- **NLTK:** For sentiment analysis and text processing.
- **Matplotlib:** For visualizing success rates and trends.
- **ChromeDriver:** Required for Selenium to interact with the Chrome browser.

You can install the required Python packages using:

```bash
pip install selenium beautifulsoup4 nltk matplotlib
