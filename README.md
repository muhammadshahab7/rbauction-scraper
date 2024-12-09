# Product Information Scraper for rbauction.com

## Overview
This project is a Python-based web scraper designed to extract product information (titles, descriptions, pricing, and image URLs) from `rbauction.com`. The scraper avoids using headless browsers like Selenium or Playwright, ensuring lightweight and efficient scraping.

## Features
- **Data Extraction**:
  - Product Title
  - Product Description
  - Pricing Data
  - Image URLs
- **Anti-blocking Measures**:
  - Rotating User Agents
  - Random Delays Between Requests
- **Concurrency**:
  - Multi-threading using `ThreadPoolExecutor` for faster performance.
- **Error Handling**:
  - Robust error handling for network and parsing issues.

## Requirements
- Python 3.7 or higher
- Dependencies:
  - `requests`
  - `beautifulsoup4`

Install the dependencies using:
```bash
pip install requests beautifulsoup4
```
## How to Use
- **Clone the repository:**

```bash
git clone https://github.com/your-username/rbauction-scraper.git
cd rbauction-scraper
```
Update the urls list in scraper.py with the product page URLs you want to scrape.

## Run the script:

```bash
python scraper.py
```
The script will print the scraped product information (title, description, price, and image URLs) to the console.

Example Output
```json
{
    "title": "Boom Truck Example",
    "description": "A powerful boom truck for heavy lifting.",
    "price": "$25,000",
    "images": [
        "https://www.rbauction.com/images/product1.jpg",
        "https://www.rbauction.com/images/product2.jpg"
    ]
}
```
## Notes
- **Blocking Prevention**: Ensure you don't make too many rapid requests to avoid being blocked by the site.
- **Customization**: Update the parsing logic in scrape_product if the site's structure changes.