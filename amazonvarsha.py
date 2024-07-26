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
            "poor": "Improve the overall quality and durability by using better materials.",
            "bad": "Enhance the performance by addressing common complaints and incorporating feedback.",
            "expensive": "Consider offering more competitive pricing or additional features.",
            "slow": "Optimize speed and efficiency by improving software or hardware components.",
            "difficult": "Simplify usage and improve the user interface with better design.",
            "complex": "Make it more user-friendly by streamlining features.",
            "uncomfortable": "Increase comfort through ergonomic design.",
            "weak": "Strengthen durability by reinforcing critical components.",
            "break": "Ensure better build quality to avoid breakages.",
            "noisy": "Reduce noise levels by improving insulation or using quieter components.",
            "battery": "Extend battery life by optimizing power management.",
            "small": "Consider offering larger or more versatile sizes.",
            "large": "Offer more compact versions for convenience.",
            "heavy": "Make it lighter and easier to handle with lighter materials."
        }
        self.positive_feature_map = {
            "quality": "Ensure high-quality materials and craftsmanship.",
            "display": "Provide a clear and vibrant display.",
            "price": "Offer good value for the price.",
            "performance": "Focus on high performance and efficiency.",
            "battery": "Extend battery life for longer usage.",
            "storage": "Offer ample storage space.",
            "speed": "Focus on fast speed and responsiveness.",
            "build": "Ensure a sturdy and durable build.",
            "ease": "Design for ease of use and intuitive operation.",
            "compatibility": "Optimize for compatibility with major systems like iOS."
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

    def clean_review_text(self, text):
        tokens = word_tokenize(text)
        cleaned_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in self.stop_words]
        return " ".join(cleaned_tokens)

    def extract_unique_features(self, reviews, sentiment='Positive'):
        features = []
        if sentiment == 'Positive':
            selected_reviews = [review[0] for review in reviews if review[1] == 'Positive']
            print(f"Positive Reviews: {selected_reviews}")  # Debug print
            for review in selected_reviews:
                for feature, suggestion in self.positive_feature_map.items():
                    if feature in review.lower():
                        features.append(suggestion)
        else:
            selected_reviews = [review[0] for review in reviews if review[1] == 'Negative']
            print(f"Negative Reviews: {selected_reviews}")  # Debug print
            for review in selected_reviews:
                for issue, solution in self.issue_map.items():
                    if issue in review.lower():
                        features.append(solution)
        print(f"Extracted Features: {features}")  # Debug print
        return list(set(features))  # Remove duplicates

    def transform_negative_features(self, negative_features, positive_features):
        transformed_features = [self.issue_map.get(issue, issue) for issue in negative_features]
        return transformed_features + [feature for feature in positive_features if feature not in transformed_features]

    def get_recommendations_csv(self, records):
        today = date.today().strftime("%d-%m-%Y")
        file_name = "{}_recommendations_{}.csv".format(self.category_name.replace(" ", "_"), today)
        
        recommendations_set = set()
        for record in records:
            positive_features = self.extract_unique_features(record[5], sentiment='Positive')
            negative_features = self.extract_unique_features(record[5], sentiment='Negative')
            recommendations = self.transform_negative_features(negative_features, positive_features)
            recommendations_set.update(recommendations)
        
        with open(file_name, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Recommendations'])
            for rec in recommendations_set:
                writer.writerow([rec])
        
        print(f">> Recommendations are stored in {file_name}\n")
        try:
            if platform.system() == "Windows":
                os.startfile(file_name)
            elif platform.system() == "Darwin":
                os.system(f"open {file_name}")
            else:
                os.system(f"xdg-open {file_name}")
        except Exception as e:
            print("Failed to open the file automatically. You can find it in the current directory.")

# Function to get product info and display recommendations only
def get_product_info():
    category_name = entry.get()
    scraper = AmazonProductScraper()
    scraper.open_browser()
    category_url = scraper.get_category_url(category_name)
    records = scraper.navigate_to_other_pages(category_url)
    scraper.close_browser()
    
    # Save recommendations to CSV
    scraper.get_recommendations_csv(records)
    
    # Generate recommendations for UI
    recommendations_set = set()  # Use a set to avoid duplicates
    for record in records:
        positive_features = scraper.extract_unique_features(record[5], sentiment='Positive')
        negative_features = scraper.extract_unique_features(record[5], sentiment='Negative')
        recommendations = scraper.transform_negative_features(negative_features, positive_features)
        recommendations_set.update(recommendations)
    
    recommendations_text = "\n".join(recommendations_set)
    
    # Update UI with recommendations only
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, recommendations_text)

# Set up the Tkinter UI
root = tk.Tk()
root.title("Amazon Product Scraper")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

entry_label = ttk.Label(frame, text="Enter product category:")
entry_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

entry = ttk.Entry(frame, width=50)
entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(frame, text="Get Recommendations", command=get_product_info)
search_button.grid(row=0, column=2, padx=5, pady=5)

result_text = tk.Text(frame, wrap=tk.WORD, height=20, width=80)
result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()




