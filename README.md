# Web Scraper

A collection of two scraping tools built by UJ — a Chrome extension for scraping Google Maps business data and a Python desktop app for extracting emails from websites.

---

## Google Maps Scraper

A Chrome extension (Manifest V3) that scrapes business listings from Google Maps search results.

### Data Extracted
- Business name
- Rating & review count
- Phone number
- Industry/category
- Address
- Website URL
- Google Maps link

### Installation
1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked** and select the `google-maps-scraper` folder

### Usage
1. Go to [Google Maps](https://www.google.com/maps/search/) and search for a business type (e.g. "restaurants in New York")
2. Click the extension icon
3. Click **Scrape Google Maps**
4. Optionally enter a file name, then click **Download as CSV**

---

## Email Scraper

A Python desktop application with a Tkinter GUI that extracts email addresses from a list of URLs and exports the results to an Excel file.

### Requirements
- Python 3
- pandas (`pip install -r Email-Scraping-master/requirements.txt`)

### Usage
1. Run the app:
   ```bash
   python "Email-Scraping-master/Email Scraping.py"
   ```
2. Click **Browse** to upload a `.txt` file containing URLs (one per line)
3. Click **Browse** to choose an output `.xlsx` file path
4. Click **Scrape Emails** and wait for the completion message
