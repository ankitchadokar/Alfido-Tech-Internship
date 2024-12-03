import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

class WebScraper:
    def __init__(self):
        self.data = []

    def fetch_page(self, url):
        """Fetch the HTML content of a page."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.log_error(f"Error fetching {url}: {e}")
            print(Fore.RED + f"Failed to fetch {url}. Check error log.")
            return None

    def log_error(self, message, filename="error_log.txt"):
        """Log errors to a file."""
        with open(filename, 'a') as f:
            f.write(message + '\n')

    def scrape_data(self, url, tag, attribute, attribute_value):
        """Scrape specific data dynamically based on user-defined tag and attribute."""
        print(Fore.BLUE + f"Scraping data from {url}...")

        soup = self.fetch_page(url)
        if not soup:
            return

        self.data = [{tag.capitalize(): element.get_text(strip=True)}
                     for element in soup.find_all(tag, {attribute: attribute_value})]

        print(Fore.GREEN + f"Scraped {len(self.data)} items.")

    def handle_pagination(self, base_url, tag, attribute, attribute_value, page_param="page", max_pages=5):
        """Handle pagination to scrape multiple pages."""
        print(Fore.YELLOW + "Starting pagination...")
        for page in tqdm(range(1, max_pages + 1), desc="Scraping pages"):
            paginated_url = f"{base_url}?{page_param}={page}"
            self.scrape_data(paginated_url, tag, attribute, attribute_value)

    def save_to_csv(self, filename='scraped_data.csv'):
        """Save scraped data to a CSV file."""
        if not self.data:
            print(Fore.RED + "No data to save!")
            return

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(Fore.GREEN + f"Data saved to {filename}")

    def save_to_db(self, db_name='scraped_data.db', table_name='data'):
        """Save scraped data to an SQLite database."""
        if not self.data:
            print(Fore.RED + "No data to save!")
            return

        conn = sqlite3.connect(db_name)
        df = pd.DataFrame(self.data)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(Fore.GREEN + f"Data saved to database {db_name} in table '{table_name}'.")

    def save_to_json(self, filename='scraped_data.json'):
        """Save scraped data to a JSON file."""
        if not self.data:
            print(Fore.RED + "No data to save!")
            return

        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(Fore.GREEN + f"Data saved to {filename}")

# Interactive Menu
if __name__ == "__main__":
    scraper = WebScraper()

    while True:
        print(Style.BRIGHT + "\n--- Web Scraper ---")
        print("1. Scrape a Single Page (Dynamic)")
        print("2. Scrape Multiple Pages (Pagination)")
        print("3. Save Data to CSV")
        print("4. Save Data to SQLite Database")
        print("5. Save Data to JSON")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            url = input("Enter the URL: ")
            tag = input("Enter HTML tag (e.g., h1, span, div): ").lower()
            attribute = input("Enter the attribute (e.g., class, id): ").lower()
            attribute_value = input(f"Enter the value for {attribute} (e.g., product-name): ")
            scraper.scrape_data(url, tag, attribute, attribute_value)
        elif choice == '2':
            base_url = input("Enter the base URL: ")
            tag = input("Enter HTML tag (e.g., h1, span, div): ").lower()
            attribute = input("Enter the attribute (e.g., class, id): ").lower()
            attribute_value = input(f"Enter the value for {attribute} (e.g., product-name): ")
            max_pages = int(input("Enter the number of pages to scrape: "))
            scraper.handle_pagination(base_url, tag, attribute, attribute_value, max_pages=max_pages)
        elif choice == '3':
            filename = input("Enter filename (default: scraped_data.csv): ") or 'scraped_data.csv'
            scraper.save_to_csv(filename)
        elif choice == '4':
            db_name = input("Enter database name (default: scraped_data.db): ") or 'scraped_data.db'
            table_name = input("Enter table name (default: data): ") or 'data'
            scraper.save_to_db(db_name, table_name)
        elif choice == '5':
            filename = input("Enter filename (default: scraped_data.json): ") or 'scraped_data.json'
            scraper.save_to_json(filename)
        elif choice == '6':
            print(Fore.CYAN + "Exiting... Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
