from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://www.rbauction.com"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]


def extract_item_number(url):
    """Extract the product number from the URL."""
    return url.rstrip("/").split("/")[-1]


def setup_driver():
    """Initialize headless Chrome with a random User-Agent."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=chrome")  # More compatible
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    return webdriver.Chrome(options=chrome_options)


def get_product_links(search_url):
    """Scrape product listing URLs from the search results page."""
    driver = setup_driver()
    driver.get(search_url)
    time.sleep(3)

    product_links = []
    try:
        product_anchors = driver.find_elements(
            By.CSS_SELECTOR, "a.MuiTypography-root.MuiLink-root")
        for anchor in product_anchors:
            href = anchor.get_attribute("href")
            if href and "/pdp/" in href:
                product_links.append(href.split("?")[0])
    except Exception as e:
        print(f"Error fetching links: {e}")

    driver.quit()
    return list(set(product_links[:1]))  # Remove duplicates


def scrape_product_with_selenium(url):
    """Scrape product detail data from the given product URL."""
    driver = setup_driver()
    driver.get(url)
    time.sleep(2)

    item_number = extract_item_number(url)
    data = {"url": url}

    try:
        title_elem = driver.find_element(
            By.CSS_SELECTOR, "h1.MuiTypography-h4")
        data["title"] = title_elem.text.strip()
    except NoSuchElementException:
        data["title"] = "N/A"

    try:
        feature_xpath = f"//div[contains(@data-testid, 'item-details-{item_number}-features')]//p[contains(@class, 'MuiTypography-body1')]"
        feature_elems = driver.find_elements(By.XPATH, feature_xpath)
        data["feature"] = feature_elems[-1].text.strip() if feature_elems else "N/A"
    except:
        data["feature"] = "N/A"

    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        image_urls = [
            img.get_attribute("src") for img in images
            if img.get_attribute("src") and any(
                img.get_attribute("src").startswith(domain)
                for domain in ("https://www-ironplanet", "https://cdn.ironpla.net")
            )
        ]
        data["images"] = image_urls
    except:
        data["images"] = []

    driver.quit()
    return data


def scrape_urls_concurrently(urls, max_workers=3):
    """Run scraping tasks in parallel using threads."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(scrape_product_with_selenium, urls))


def main():
    print("🔍 Ritchie Bros Auction Web Scraper (Selenium Edition)")
    query = input(
        "Enter search term (e.g., truck, excavator, loader): ").strip()
    if not query:
        print("❌ Please enter a valid search term.")
        return

    encoded_query = quote_plus(query)
    search_url = f"https://www.rbauction.com/search?freeText={encoded_query}&refreshSearch=true"

    print(f"\n[INFO] Searching for: {query}")
    print("[INFO] Fetching product links...")

    product_urls = get_product_links(search_url)

    if not product_urls:
        print("❌ No products found. Try a different keyword.")
        return

    print(f"[INFO] Found {len(product_urls)} items. Scraping details...\n")

    product_data = scrape_urls_concurrently(product_urls)

    for item in product_data:
        print("=" * 60)
        print(f"URL     : {item['url']}")
        print(f"Title   : {item['title']}")
        print(f"Feature : {item['feature']}")
        print(f"Images  : {item['images']}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
