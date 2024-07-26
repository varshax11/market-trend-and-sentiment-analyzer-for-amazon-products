# market-analysis
Market trend analysis and feature recommendation for product based startups


Amazon Product Review Scraper and Recommender

This project is a Python-based tool for scraping product reviews from Amazon and providing recommendations based on sentiment analysis. The tool uses Selenium for web scraping, BeautifulSoup for HTML parsing, and NLTK for natural language processing and sentiment analysis.

Features:

Scrapes product information (description, price, rating, review count, reviews) from Amazon.
Analyzes reviews to extract positive and negative features.
Provides recommendations based on extracted features.
Displays recommendations in a simple UI using Tkinter.
Saves product details and recommendations to a CSV file.

Requirements:

Python 3.6 or higher
Google Chrome browser
ChromeDriver (compatible with your version of Chrome)

Libraries:

The following libraries are required to run this project:

selenium
beautifulsoup4
nltk
tkinter (standard with Python installations)

You can install the required libraries using pip:

pip install selenium beautifulsoup4 nltk

Installation:

Download ChromeDriver:

Download the ChromeDriver from here and ensure it matches your version of Chrome. Place it in a directory and note the path.

Clone the Repository:

git clone https://github.com/yourusername/amazon-product-review-scraper.git
cd amazon-product-review-scraper

Install Python Libraries:

pip install -r requirements.txt

Set Up NLTK:

Run the following in a Python interpreter to download required NLTK data:

import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')

Usage:

Run the Script:

python amazon_scraper.py

Enter the Product Category:

The script will prompt you to enter the product category you want to search for (e.g., "ipad").

View Recommendations:

The UI will display the recommendations for the products found in the specified category.

CSV Output:

Product details and recommendations will be saved to a CSV file in the format category_name_dd-mm-yyyy.csv.

Code Overview:

AmazonProductScraper Class

Methods:
open_browser(): Opens the Chrome browser.
get_category_url(category_name): Constructs the search URL for the specified category.
extract_webpage_information(): Extracts product information from the search results page.
extract_product_information(page_results): Extracts details for each product.
navigate_to_other_pages(category_url): Navigates through the search result pages and collects product information.
product_information_spreadsheet(records): Writes product details and recommendations to a CSV file.
clean_review_text(text): Cleans and tokenizes review text.
extract_unique_features(reviews, sentiment): Extracts features from reviews based on sentiment.
transform_negative_features(negative_features, positive_features): Transforms negative features into recommendations.
get_recommendations(records): Compiles recommendations for products.
run_ui() Function
Sets up a simple Tkinter UI for entering the product category and displaying recommendations.

Contributing:

Feel free to open issues or submit pull requests for any improvements or bug fixes.

License:

This project is licensed under the MIT License.
