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

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/amazon-product-review-analysis.git
    ```

2. **Navigate to the project directory:**

    ```sh
    cd amazon-product-review-analysis
    ```

3. **Install the required dependencies:**

    Create a `requirements.txt` file with the following content:

    ```txt
    pandas
    selenium
    beautifulsoup4
    nltk
    matplotlib
    ```

    Install the dependencies using:

    ```sh
    pip install -r requirements.txt
    ```

4. **Ensure ChromeDriver is installed and its path is set in the script.**

## Usage

1. **Run the main script:**

    ```sh
    python amazon_product_scraper.py
    ```

2. **When prompted, enter the product category you wish to scrape (e.g., "iPad", "laptop").**

    The script will:

    - Extract product information from Amazon.
    - Perform sentiment analysis on product reviews.
    - Extract positive and negative features from reviews.
    - Generate recommendations for product improvements and development.
    - Visualize the potential success rate based on the recommendations.
    - Save the results and visualizations into a CSV file named based on the category and the current date.
    - Open the CSV file automatically after creation, or find it in the current directory.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
