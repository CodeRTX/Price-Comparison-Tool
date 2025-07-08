import asyncio
import re
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
import urllib.parse

class ScraperService:
    def __init__(self):
        self.country_domains = {
            'US': 'amazon.com',
            'UK': 'amazon.co.uk',
            'IN': 'amazon.in',
            'CA': 'amazon.ca',
            'DE': 'amazon.de',
            'FR': 'amazon.fr',
            'IT': 'amazon.it',
            'ES': 'amazon.es',
            'JP': 'amazon.co.jp',
            'AU': 'amazon.com.au',
            'BR': 'amazon.com.br',
            'MX': 'amazon.com.mx'
        }
        
        self.currency_map = {
            'US': 'USD',
            'UK': 'GBP',
            'IN': 'INR',
            'CA': 'CAD',
            'DE': 'EUR',
            'FR': 'EUR',
            'IT': 'EUR',
            'ES': 'EUR',
            'JP': 'JPY',
            'AU': 'AUD',
            'BR': 'BRL',
            'MX': 'MXN'
        }

    async def scrape_products(self, country: str, query: str) -> List[Dict[str, Any]]:
        """
        Scrape products from Amazon for the given country and query.
        """
        domain = self.country_domains.get(country.upper())
        if not domain:
            raise ValueError(f"Unsupported country: {country}")
        
        currency = self.currency_map.get(country.upper(), 'USD')
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set user agent to avoid detection
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            try:
                products = await self._scrape_amazon(page, domain, query, currency)
                return products
            finally:
                await browser.close()

    async def _scrape_amazon(self, page: Page, domain: str, query: str, currency: str) -> List[Dict[str, Any]]:
        """
        Scrape Amazon search results for the given query.
        """
        # Construct search URL
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://{domain}/s?k={encoded_query}"
        
        try:
            # Navigate to search page
            await page.goto(search_url, wait_until='networkidle')
            
            # Wait for search results to load
            await page.wait_for_selector('[data-component-type="s-search-result"]', timeout=10000)
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            products = []
            
            # Find all product containers
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for container in product_containers[:10]:  # Limit to first 10 results
                try:
                    product = self._extract_product_info(container, domain, currency)
                    if product:
                        products.append(product)
                except Exception as e:
                    print(f"Error extracting product: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return []

    def _extract_product_info(self, container, domain: str, currency: str) -> Optional[Dict[str, Any]]:
        """
        Extract product information from a search result container.
        """
        try:
            # Extract product name
            title_element = container.find('h2', class_='a-size-mini')
            if not title_element:
                title_element = container.find('span', class_='a-size-medium')
            if not title_element:
                title_element = container.find('span', class_='a-size-base-plus')
            
            if not title_element:
                return None
            
            product_name = title_element.get_text(strip=True)
            
            # Extract price
            price_element = container.find('span', class_='a-price-whole')
            if not price_element:
                price_element = container.find('span', class_='a-offscreen')
            
            if not price_element:
                return None
            
            price_text = price_element.get_text(strip=True)
            # Clean price text and extract numeric value
            price = self._clean_price(price_text)
            
            if not price:
                return None
            
            # Extract product link
            link_element = container.find('h2').find('a') if container.find('h2') else None
            if not link_element:
                return None
            
            relative_link = link_element.get('href')
            full_link = f"https://{domain}{relative_link}" if relative_link.startswith('/') else relative_link
            
            # Extract rating if available
            rating_element = container.find('span', class_='a-icon-alt')
            rating = None
            if rating_element:
                rating_text = rating_element.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    rating = rating_match.group(1)
            
            # Extract number of reviews if available
            reviews_element = container.find('a', class_='a-link-normal')
            reviews_count = None
            if reviews_element:
                reviews_text = reviews_element.get_text(strip=True)
                reviews_match = re.search(r'([\d,]+)', reviews_text)
                if reviews_match:
                    reviews_count = reviews_match.group(1).replace(',', '')
            
            return {
                'link': full_link,
                'price': price,
                'currency': currency,
                'productName': product_name,
                'rating': rating,
                'reviewsCount': reviews_count,
                'source': 'Amazon'
            }
            
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None

    def _clean_price(self, price_text: str) -> Optional[str]:
        """
        Clean and extract numeric price from price text.
        """
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_match = re.search(r'([\d,]+\.?\d*)', price_text.replace(',', ''))
        if price_match:
            return price_match.group(1).replace(',', '')
        
        return None

