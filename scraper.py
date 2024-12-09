import requests
from bs4 import BeautifulSoup
import random
import time
from concurrent.futures import ThreadPoolExecutor

# List of user agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

# Headers for requests
def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

# Scraping function
def scrape_product(url):
    """
    Scrapes product details from a given URL.
    
    Args:
        url (str): URL of the product page.
        
    Returns:
        dict: A dictionary containing title, description, price, and images of the product.
    """
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract product details
        title = soup.find("h1", {"class": "item-title"}).get_text(strip=True) if soup.find("h1", {"class": "item-title"}) else "N/A"
        description = soup.find("div", {"class": "item-description"}).get_text(strip=True) if soup.find("div", {"class": "item-description"}) else "N/A"
        price = soup.find("span", {"class": "item-price"}).get_text(strip=True) if soup.find("span", {"class": "item-price"}) else "N/A"
        
        # Extract images
        images = [img['src'] for img in soup.find_all("img", {"class": "item-image"}) if 'src' in img.attrs]
        
        return {
            "title": title,
            "description": description,
            "price": price,
            "images": images
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Main function to scrape multiple URLs
def scrape_urls(urls):
    """
    Scrapes multiple product URLs concurrently.
    
    Args:
        urls (list): List of product page URLs.
        
    Returns:
        list: A list of dictionaries containing product information.
    """
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(scrape_product, url): url for url in urls}
        for future in future_to_url:
            result = future.result()
            if result:
                results.append(result)
            time.sleep(random.uniform(1, 3))  # Random delay to avoid blocks
    return results

# Example usage
if __name__ == "__main__":
    # Replace with actual URLs
    urls = [
        "https://www.rbauction.com/cp/boom-truck",
    ]
    
    data = scrape_urls(urls)
    for item in data:
        print(item)
