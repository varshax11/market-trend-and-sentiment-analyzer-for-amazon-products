import time
import csv
import os
import platform
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import ttk

class AmazonProductScraper:
    def __init__(self):
        self.driver = None
        self.category_name = None
        self.formatted_category_name = None
        self.chrome_driver_path = '/Users/muralikrishamurthy/.wdm/drivers/chromedriver/mac64/126.0.6478.126/chromedriver-mac-arm64/chromedriver'
        self.sid = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.issue_map = {
            "poor": "To enhance the overall quality and durability, consider using higher-grade materials and implementing stricter quality control measures.",
            "bad": "Improve performance by addressing common complaints through rigorous testing and incorporating user feedback into design improvements.",
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

    def get_category_url(self, category_name):
        self.category_name = category_name
        self.formatted_category_name = self.category_name.replace(" ", "+")
        category_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss".format(self.formatted_category_name)
        print(">> Category URL: ", category_url)
        self.driver.get(category_url)
        return category_url

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
                            cleaned_review = self.clean_review_text(review_text)
                            sentiment_scores = self.sid.polarity_scores(cleaned_review)
                            if sentiment_scores['compound'] >= 0.05:
                                sentiment_label = 'Positive'
                            elif sentiment_scores['compound'] <= -0.05:
                                sentiment_label = 'Negative'
                            else:
                                sentiment_label = 'Neutral'
                            reviews[idx] = (review_text, sentiment_label)
                        except NoSuchElementException:
                            reviews[idx] = ("N/A", "N/A")
                except NoSuchElementException:
                    reviews = [("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A")]

            product_information = (description, product_price, product_review, review_number, category_url, reviews)
            temp_record.append(product_information)

        return temp_record

    def navigate_to_other_pages(self, category_url):
        records = []
        page_number = 1

        while True:
            print(f">> Extracting page {page_number}")
            page_results = self.extract_webpage_information()
            temp_record = self.extract_product_information(page_results)
            records.extend(temp_record)

            try:
                next_button = self.driver.find_element(By.XPATH, "//li[@class='a-last']/a")
                next_button.click()
                page_number += 1
                time.sleep(3)
            except (NoSuchElementException, ElementClickInterceptedException):
                break

        return records

    def product_information_spreadsheet(self, records):
        today = date.today().strftime("%d-%m-%Y")
        file_name = "{}_{}.csv".format(self.category_name.replace(" ", "_"), today)

        with open(file_name, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Product URL', 'Review 1', 'Sentiment 1', 'Review 2', 'Sentiment 2', 'Review 3', 'Sentiment 3', 'Review 4', 'Sentiment 4', 'Review 5', 'Sentiment 5', 'Positive Features', 'Recommendations'])
            for record in records:
                reviews_info = []
                for review in record[5]:
                    reviews_info.extend(review)

                positive_features = self.extract_unique_features(record[5], sentiment='Positive')
                negative_features = self.extract_unique_features(record[5], sentiment='Negative')
                recommendations = self.transform_negative_features(negative_features, positive_features)

                writer.writerow([record[0], record[1], record[2], record[3], record[4]] + reviews_info + [positive_features, "\n".join(recommendations)])

        print(f">> Information about the product '{self.category_name}' is stored in {file_name}\n")
        try:
            if platform.system() == "Windows":
                os.startfile(file_name)
            elif platform.system() == "Darwin":
                os.system(f"open {file_name}")
            else:
                os.system(f"xdg-open {file_name}")
        except Exception as e:
            print("Failed to open the file automatically. You can find it in the current directory.")

    def close_browser(self):
        self.driver.quit()

    def clean_review_text(self, review_text):
        tokens = word_tokenize(review_text.lower())
        cleaned_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        cleaned_review = ' '.join(cleaned_tokens)
        return cleaned_review

    def extract_unique_features(self, reviews, sentiment):
        feature_set = set()
        for review_text, sentiment_label in reviews:
            if sentiment_label == sentiment:
                tokens = word_tokenize(review_text.lower())
                features = [word for word in tokens if word.isalnum() and word not in self.stop_words]
                feature_set.update(features)
        return ', '.join(feature_set)

    def transform_negative_features(self, negative_features, positive_features):
        recommendations = []
        for feature in negative_features.split(', '):
            if feature in self.issue_map:
                recommendations.append(self.issue_map[feature])
        for feature in positive_features.split(', '):
            if feature in self.positive_feature_map:
                recommendations.append(self.positive_feature_map[feature])
        return recommendations

def main():
    scraper = AmazonProductScraper()
    scraper.open_browser()

    category_name = input("Enter the product category you want to scrape: ")
    category_url = scraper.get_category_url(category_name)
    records = scraper.navigate_to_other_pages(category_url)
    scraper.product_information_spreadsheet(records)
    scraper.close_browser()

if __name__ == "__main__":
    main()
