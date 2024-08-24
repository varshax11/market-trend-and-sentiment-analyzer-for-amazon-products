import time
import csv
import os
import platform
import nltk
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

class AmazonProductScraper:
    def __init__(self):
        self.driver = None
        self.product_name = None
        self.chrome_driver_path = '/path/to/chromedriver'  # Update with your ChromeDriver path
        self.sid = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.issue_map = {
            "poor": "Improve performance by addressing common complaints through rigorous testing and incorporating user feedback into design improvements.",
            "bad": "Enhance the overall quality by using higher-grade materials and implementing stricter quality control measures.",
            "expensive": "Evaluate pricing strategies and consider offering additional features or bundling options to provide better value for money.",
            "slow": "Optimize the product's speed and efficiency by upgrading software or hardware components and eliminating performance bottlenecks.",
            "difficult": "Simplify usage by improving the user interface design to be more intuitive and user-friendly, based on common user feedback.",
            "complex": "Streamline features and user interfaces to make the product easier to use, ensuring that essential functions are accessible without unnecessary complexity.",
            "uncomfortable": "Increase user comfort by focusing on ergonomic design improvements and incorporating user feedback on comfort and usability.",
            "weak": "Enhance durability by reinforcing critical components and conducting stress tests to identify and address potential weaknesses.",
            "break": "Improve build quality to prevent breakages by using more durable materials and enhancing product design to withstand everyday use.",
            "noisy": "Reduce noise levels by using quieter components or incorporating better sound insulation to minimize disturbances during operation.",
            "battery": "Extend battery life by optimizing power management features and using more efficient battery technology to support longer usage times.",
            "small": "Consider offering larger or more versatile size options to meet diverse customer needs and preferences.",
            "large": "Provide more compact versions of the product to accommodate users who prefer smaller, more portable options.",
            "heavy": "Reduce the product's weight by using lighter materials and optimizing design to improve portability and ease of handling."
        }
        self.positive_feature_map = {
            "quality": "Ensure that the product maintains high standards of material and craftsmanship for enhanced user satisfaction.",
            "display": "Provide a display that is clear, vibrant, and easy to view under various lighting conditions to improve user experience.",
            "price": "Offer the product at a competitive price point to deliver good value for money and attract more customers.",
            "performance": "Focus on high performance and efficiency to meet user expectations and support demanding tasks or applications.",
            "battery": "Extend battery life to allow for longer usage between charges, enhancing convenience and usability.",
            "storage": "Provide ample storage space to accommodate user needs and ensure the product can handle a variety of data or content.",
            "speed": "Ensure fast speed and responsiveness to improve user satisfaction and efficiency in performing tasks.",
            "build": "Ensure the product has a sturdy and durable build to withstand regular use and enhance longevity.",
            "ease": "Design the product for ease of use with an intuitive interface and straightforward operation to enhance user experience.",
            "compatibility": "Optimize the product for compatibility with major systems or platforms to ensure seamless integration and functionality."
        }

    def open_browser(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        url = "https://www.amazon.in/"
        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=opt)
        self.driver.get(url)
        time.sleep(3)

    def get_product_url(self, product_name):
        self.product_name = product_name
        formatted_product_name = self.product_name.replace(" ", "+")
        product_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss".format(formatted_product_name)
        print(">> Product URL: ", product_url)
        self.driver.get(product_url)
        return product_url

    def extract_webpage_information(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        page_results = soup.find_all('div', {'data-component-type': 's-search-result'})
        return page_results

    def extract_product_information(self, page_results):
        temp_record = []
        for item in page_results:
            try:
                description = item.h2.a.text.strip()
            except AttributeError:
                description = "N/A"

            try:
                category_url = "https://www.amazon.in/" + item.h2.a.get('href')
            except AttributeError:
                category_url = "N/A"

            try:
                product_price = item.find('span', 'a-offscreen').text.strip()
            except AttributeError:
                product_price = "N/A"

            try:
                product_review = item.i.text.strip()
            except AttributeError:
                product_review = "N/A"

            try:
                review_number = item.find('span', {'class': 'a-size-base'}).text.strip()
            except AttributeError:
                review_number = "N/A"

            reviews = ["N/A", "N/A", "N/A", "N/A", "N/A"]
            if category_url != "N/A":
                try:
                    self.driver.get(category_url)
                    time.sleep(3)
                    review_elements = self.driver.find_elements(By.XPATH, "//div[@data-hook='review']")
                    for idx, review_element in enumerate(review_elements[:5]):
                        try:
                            review_text = review_element.find_element(By.XPATH, ".//span[@data-hook='review-body']").text.strip()
                            sentiment_scores = self.sid.polarity_scores(review_text)
                            sentiment = 'positive' if sentiment_scores['compound'] >= 0.05 else 'negative'
                            reviews[idx] = review_text
                        except Exception as e:
                            print(f"Error extracting review {idx+1}: {e}")

                except Exception as e:
                    print(f"Error accessing category URL {category_url}: {e}")

            temp_record.append({
                'description': description,
                'price': product_price,
                'review': product_review,
                'review_count': review_number,
                'reviews': reviews
            })

        return temp_record

    def clean_review_text(self, review_text):
        tokens = word_tokenize(review_text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        return ' '.join(filtered_tokens)

    def analyze_reviews(self, records):
        recommendations = set()

        for record in records:
            reviews = record['reviews']
            issues = set()
            positive_features = set()

            for review in reviews:
                cleaned_review = self.clean_review_text(review)
                sentiment_scores = self.sid.polarity_scores(cleaned_review)
                sentiment = 'positive' if sentiment_scores['compound'] >= 0.05 else 'negative'

                if sentiment == 'negative':
                    for issue, recommendation in self.issue_map.items():
                        if issue in cleaned_review:
                            issues.add(issue)
                            recommendations.add(recommendation)
                            break

                if sentiment == 'positive':
                    for feature, recommendation in self.positive_feature_map.items():
                        if feature in cleaned_review:
                            positive_features.add(feature)
                            recommendations.add(recommendation)
                            break

            record['issues'] = list(issues)
            record['positive_features'] = list(positive_features)

        return records, list(recommendations)

    def save_to_csv(self, records, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['description', 'price', 'review_count', 'issues', 'positive_features']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in records:
                writer.writerow({
                    'description': record['description'],
                    'price': record['price'],
                    'review_count': record['review_count'],
                    'issues': ', '.join(record['issues']),
                    'positive_features': ', '.join(record['positive_features'])
                })

    def run(self, product_name):
        self.open_browser()
        product_url = self.get_product_url(product_name)
        page_results = self.extract_webpage_information()
        records = self.extract_product_information(page_results)
        analyzed_records, recommendations = self.analyze_reviews(records)
        self.save_to_csv(analyzed_records, f'{product_name}_review_analysis.csv')
        print("Recommendations:")
        for rec in recommendations:
            print(f"- {rec}")

# Example usage
if __name__ == "__main__":
    scraper = AmazonProductScraper()
    product_name = input("Enter the product name: ")
    scraper.run(product_name)
