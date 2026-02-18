# Gmaps-Lead-Extractor
A professional Google Maps scraper built with Python &amp; Selenium, featuring automated emoji cleaning and direct Excel export for clean lead generation.
#  Google Maps Lead Extractor & Cleaner

A professional Python tool built with **Selenium** to scrape business data from Google Maps. It features an automated **data cleaning layer** that removes emojis and special characters (like 🚀, 💣, 💥), ensuring the Excel output is clean and ready for professional use.

---

##  Main Features
- **Smart Data Cleaning:** Automatically filters out emojis and symbols from business names.
- **Lead Generation:** Extracts Name, Address, and Phone Number.
- **Dynamic Scrolling:** Handles infinite scroll and slow-loading maps.
- **Excel Export:** Saves data directly into organized `.xlsx` files.
- **Headless Mode:** Option to run the browser in the background.

##  Project Structure
- `main.py`: The entry point to run the scraper.
- `scraper.py`: Contains the `GoogleMapsScraper` class and scraping logic.
- `config.py`: Configuration for search terms, wait times, and headless mode.
- `requirements.txt`: Project dependencies.

##  License
This project is for educational purposes. Please adhere to Google Maps' Terms of Service.

---

##  How to Run (طريقة التشغيل)
To start extracting data, follow these steps in your terminal:
```bash
git clone https://github.com
pip install selenium pandas openpyxl
# Update keywords in config.py then run:
python main.py


   ```bash
   git clone https://github.com
