
# 🛠️ Ritchie Bros Auction Scraper (RBAuction.com) 🚜

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup%2C%20Selenium-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Overview

This project provides a **powerful and flexible scraper** for extracting product details from [Ritchie Bros Auction (rbauction.com)](https://www.rbauction.com), a global auction site for heavy equipment and trucks.  
Built with three different scraping strategies to suit your needs:

- 🥣 `BeautifulSoup` – Fast & lightweight (for static pages)
- 🦾 `Selenium` – Reliable for JavaScript-rendered content

---

## 🚀 Features

- ✅ Extract product **title**, **features**, and **images**
- ✅ Smart image filtering (cdn / www-ironplanet based)
- ✅ Works on dynamic & static content
- ✅ Modular & customizable for batch scraping

---

## 📁 Project Structure

```
📦 rbauction_scraper/
├── beautifulsoup_scraper.py      # Static scraper using requests + BeautifulSoup
├── selenium_scraper.py           # Dynamic scraper using Selenium (headless Chrome)
├── LICENSE                       # MIT Licencse File
└── README.md                     # This file
```

---

## ⚙️ Installation

### 📦 Dependencies

```bash
pip install requests beautifulsoup4 selenium
```

### ✅ ChromeDriver for Selenium

Make sure you have the ChromeDriver that matches your Chrome version.  
Download: https://chromedriver.chromium.org/downloads

---

## 💻 Usage

### 1. 🔎 BeautifulSoup (Static Scraping)

```bash
python beautifulsoup_scraper.py
```

> ⚠️ Use only if product content is visible in raw HTML source.

---

## 📸 Screenshot
<img width="1346" height="297" alt="Screenshot 2025-07-31 000114" src="https://github.com/user-attachments/assets/b9dd29cd-580a-4db0-b743-0084105b19ae" />

---

### 2. 🦿 Selenium (Dynamic Scraping)

```bash
python selenium_scraper.py
```

> Uses `headless Chrome` to render and extract content.  
> Suitable for most cases where JS is required to load product details.

---

## 📸 Screenshot
<img width="1433" height="299" alt="Screenshot 2025-07-31 001812" src="https://github.com/user-attachments/assets/4f566334-f1cd-428c-8fb8-96fd595f4670" />

---
## 📸 Output Json Example

```json
{
  "url": "https://www.rbauction.com/xyz123",
  "title": "2022 CAT 320 GC Track Excavator",
  "feature": "Air Conditioner, Boom Check Valve, 24 in Triple Grouser Track Shoes",
  "images": [
    "https://cdn.ironpla.net/image1.jpg",
    "https://www-ironplanet.com/image2.jpg"
  ]
}
```

---

## 🎯 Domain Filtering Logic

To avoid unrelated or low-resolution images, the scraper **only includes image URLs** that start with:

- `https://www-ironplanet`
- `https://cdn.ironpla.net`

This ensures high-quality, relevant images only.

---

## 📘 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Muhammad Shahab**  
_Python developer & web scraping enthusiast._

---

## 🌐 Connect

- 💼 [LinkedIn](https://www.linkedin.com/in/muhammad-shahab07/)
- 🐙 [GitHub](https://github.com/muhammadshahab7)

---

> ⭐ If you found this project helpful, please give it a star!
