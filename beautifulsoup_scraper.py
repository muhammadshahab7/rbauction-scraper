import requests
from bs4 import BeautifulSoup
import random
import time
from concurrent.futures import ThreadPoolExecutor

# User agents for rotation to mimic human browsing behavior
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

BASE_URL = "https://www.rbauction.com"


def get_headers():
    """Returns randomized headers with a fake User-Agent."""
    return {"User-Agent": random.choice(USER_AGENTS)}


def get_product_links(listing_url):
    """
    Fetches product links from a category/listing page.

    Args:
        listing_url (str): Full URL of the listing/search page.

    Returns:
        list: A list of product detail page URLs.
    """
    try:
        res = requests.get(listing_url, headers=get_headers(), timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        product_links = []
        cards = soup.find_all(
            "li", {"data-testid": lambda x: x and x.startswith("searchResultItemCard-")})
        for card in cards:
            a_tag = card.find("a", href=True)
            if a_tag:
                full_url = BASE_URL + a_tag["href"]
                product_links.append(full_url)
                product_links = product_links

        return product_links

    except Exception as e:
        print(f"[ERROR] Failed to fetch product links: {e}")
        return []


def extract_item_number(url):
    """
    Extracts the last numeric segment from a given Ritchie Bros. auction product URL.

    Parameters:
        url (str): The full product URL (e.g., 
                   'https://www.rbauction.com/pdp/2006-kenworth-t800-8x6-sleeper-rotator-tow-truck/13462026').

    Returns:
        str: The item number extracted from the URL (e.g., '13462026').
    """
    return url.rstrip("/").split("/")[-1]


def scrape_product(url):
    """
    Scrapes product details from a product detail page.

    Args:
        url (str): Product detail page URL.

    Returns:
        dict or None: Scraped data with title, feature, and image URLs.
    """
    try:
        res = requests.get(url, headers=get_headers(), timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        item_number = extract_item_number(url)

        # Title
        title_tag = soup.find(
            "h1", {"class": lambda x: x and "MuiTypography-h4" in x})
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Features
        features = []
        feature_containers = soup.find_all(
            "div", {
                "data-testid": lambda x: x and x.startswith(f"item-details-{str(item_number)}-features")}
        )

        if feature_containers:
            for container in feature_containers:
                p_tags = container.find_all(
                    "p", {"class": lambda x: x and "MuiTypography-body1" in x}
                )
                for p in p_tags:
                    text = p.get_text(strip=True)
                    if text:
                        features.append(text)

        feature = features[-1] if features else "N/A"

        # Image URLs
        allowed_domains = ("https://www-ironplanet", "https://cdn.ironpla.net")

        images = [
            img["src"] for img in soup.find_all("img")
            if img.get("src", "").startswith(allowed_domains)
        ]

        return {
            "url": url,
            "title": title,
            "feature": feature,
            "images": images,
        }

    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None


def scrape_urls_concurrently(urls, max_workers=5):
    """
    Scrapes multiple URLs concurrently.

    Args:
        urls (list): List of product detail URLs.
        max_workers (int): Number of threads to use.

    Returns:
        list: List of scraped product data.
    """
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scrape_product, url): url for url in urls}
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
            time.sleep(random.uniform(1, 2))  # Random delay between requests
    return results


def main():
    print("🔍 Ritchie Bros Auction Web Scraper")
    query = input(
        "Enter search term (e.g., truck, excavator, loader): ").strip()
    if not query:
        print("❌ Please enter a valid search term.")
        return

    listing_url = f"https://www.rbauction.com/search?freeText={query}&refreshSearch=true"
    print(f"\n[INFO] Searching for: {query}")
    print("[INFO] Fetching product links...")

    product_urls = get_product_links(listing_url)

    if not product_urls:
        print("❌ No products found. Try a different keyword.")
        return

    print(f"[INFO] Found {len(product_urls)} items. Scraping details...\n")

    product_data = scrape_urls_concurrently(product_urls)

    for item in product_data:
        print("=" * 60)
        print(f"\n\nURL     : {item['url']}")
        print(f"Title   : {item['title']}")
        print(f"Feature : {item['feature']}")
        print(f"Images  : {item['images']}\n")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
