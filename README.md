# Amazon Product Review Analysis and Feature Recommendation System for startups 

## Overview

This project analyzes Amazon product reviews to extract valuable insights and generate recommendations for startups trying to launch similar products , so they can improve their products based on user feedback. The system performs sentiment analysis on product reviews, identifies common issues, and provides actionable recommendations to enhance product performance and user satisfaction.

## Features

- Scrapes Amazon product pages for details and reviews.
- Analyzes reviews for positive and negative sentiments.
- Identifies issues and positive features from reviews.
- Generates recommendations based on identified issues and positive features. 
- Saves the analysis results and recommendations to a CSV file.

## Prerequisites

- Python 3.x
- ChromeDriver (compatible with your version of Google Chrome)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/amazon-product-review-analysis.git
    cd amazon-product-review-analysis
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Update the ChromeDriver path in `amazon_product_scraper.py`:

    ```python
    self.chrome_driver_path = '/path/to/chromedriver'  # Update with your ChromeDriver path
    ```

## Usage

1. Run the script:

    ```bash
    python amazon_product_scraper.py
    ```

2. Enter the product name when prompted.

3. The script will generate a CSV file with the analysis results and print the recommendations to the console.

## Sample Data

A sample data file is included in the `sample_data` directory for reference.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
