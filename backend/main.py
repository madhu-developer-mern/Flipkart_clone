from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import asyncio
from typing import List
import re
from urllib.parse import urljoin
import json

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: str
    name: str
    price: str
    image_url: str
    rating: str = "N/A"
    reviews: str = "0"

# Cache for scraped products
products_cache = {}

def get_flipkart_headers():
    """Return headers to mimic a real browser"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def scrape_flipkart_search(search_query: str, max_products: int = 20) -> List[Product]:
    """
    Scrape Flipkart search results for given query
    """
    try:
        # Create search URL
        search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
        
        headers = get_flipkart_headers()
        
        # Make request with timeout
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Try to find product containers
        product_containers = soup.find_all('div', {'class': re.compile('col.*')})
        
        for container in product_containers[:max_products]:
            try:
                # Extract product details
                product_link = container.find('a', {'class': re.compile('_+1UQZyc')})
                if not product_link:
                    continue
                
                product_url = product_link.get('href', '')
                
                # Get product name
                name_elem = container.find('a', {'class': re.compile('s1Q50cAgFa')})
                name = name_elem.text.strip() if name_elem else "Unknown Product"
                
                # Get price
                price_elem = container.find('div', {'class': re.compile('_+30jeq3')})
                price = price_elem.text.strip() if price_elem else "N/A"
                
                # Get image
                img_elem = container.find('img')
                image_url = img_elem.get('src', '') if img_elem else ""
                
                # Get rating
                rating_elem = container.find('div', {'class': re.compile('_+1lRcqm')})
                rating = rating_elem.text.strip() if rating_elem else "N/A"
                
                # Get review count
                review_elem = container.find('span', {'class': re.compile('_+1oKavI')})
                reviews = review_elem.text.strip() if review_elem else "0"
                
                if name and image_url:
                    product = Product(
                        id=hash(product_url) % ((2**31) - 1),
                        name=name[:100],
                        price=price,
                        image_url=image_url,
                        rating=rating,
                        reviews=reviews
                    )
                    products.append(product)
                    
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue
        
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        # Return mock data if scraping fails
        return get_mock_products(search_query)

def get_mock_products(search_query: str) -> List[Product]:
    """
    Return mock products when scraping fails
    This includes sample data to demonstrate the application
    """
    mock_data = {
        "electronics": [
            {
                "name": "Samsung Galaxy M31 (Space Black, 4GB RAM, 64GB Storage)",
                "price": "₹9,999",
                "image_url": "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=300",
                "rating": "4.5",
                "reviews": "15.2K"
            },
            {
                "name": "Apple iPhone 12 (Blue, 64GB)",
                "price": "₹54,999",
                "image_url": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=300",
                "rating": "4.7",
                "reviews": "25.8K"
            },
            {
                "name": "OnePlus 9 Pro (Pine Green, 8GB RAM, 128GB)",
                "price": "₹49,999",
                "image_url": "https://images.unsplash.com/photo-1511367461989-f85a1664c5ad?w=300",
                "rating": "4.6",
                "reviews": "12.3K"
            },
            {
                "name": "Redmi Note 10 Pro (Gradient Bronze, 6GB RAM, 64GB)",
                "price": "₹15,999",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300",
                "rating": "4.4",
                "reviews": "8.9K"
            },
            {
                "name": "POCO X3 Pro (Black, 6GB RAM, 128GB)",
                "price": "₹18,999",
                "image_url": "https://images.unsplash.com/photo-1585492841711-11584e18a59e?w=300",
                "rating": "4.5",
                "reviews": "11.2K"
            },
            {
                "name": "Motorola Moto G9 (Sapphire Green, 4GB RAM, 64GB)",
                "price": "₹9,299",
                "image_url": "https://images.unsplash.com/photo-1513149666159-fcf4e75d6a85?w=300",
                "rating": "4.2",
                "reviews": "6.5K"
            },
        ],
        "clothing": [
            {
                "name": "Men's Cotton T-Shirt (Blue)",
                "price": "₹299",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300",
                "rating": "4.3",
                "reviews": "2.1K"
            },
            {
                "name": "Women's Casual Shirt (White)",
                "price": "₹399",
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=300",
                "rating": "4.5",
                "reviews": "3.2K"
            },
        ],
        "books": [
            {
                "name": "The Midnight Library by Matt Haig",
                "price": "₹345",
                "image_url": "https://images.unsplash.com/photo-1507842217343-583f1270b3fe?w=300",
                "rating": "4.6",
                "reviews": "1.8K"
            },
            {
                "name": "Atomic Habits by James Clear",
                "price": "₹400",
                "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e01fb7d?w=300",
                "rating": "4.7",
                "reviews": "5.2K"
            },
        ]
    }
    
    products = []
    base_products = mock_data.get(search_query.lower(), mock_data['electronics'])
    
    for idx, item in enumerate(base_products):
        product = Product(
            id=str(idx + 1),
            name=item['name'],
            price=item['price'],
            image_url=item['image_url'],
            rating=item['rating'],
            reviews=item['reviews']
        )
        products.append(product)
    
    return products

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to ECommerce API", "version": "1.0"}

@app.get("/api/search")
async def search_products(q: str = "electronics", limit: int = 20) -> dict:
    """
    Search for products on Flipkart
    Query parameters:
    - q: search query (default: electronics)
    - limit: max number of products to return (default: 20)
    """
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    if limit > 100:
        limit = 100
    
    # Check cache first
    cache_key = f"{q}_{limit}".lower()
    if cache_key in products_cache:
        return {"query": q, "products": products_cache[cache_key], "cached": True}
    
    # Scrape or get mock data
    products = scrape_flipkart_search(q, limit)
    
    # Cache results
    products_cache[cache_key] = [p.dict() for p in products]
    
    return {
        "query": q,
        "products": [p.dict() for p in products],
        "cached": False,
        "count": len(products)
    }

@app.get("/api/categories")
async def get_categories():
    """Get popular categories"""
    return {
        "categories": [
            {"id": 1, "name": "Electronics", "icon": "📱"},
            {"id": 2, "name": "Clothing", "icon": "👕"},
            {"id": 3, "name": "Books", "icon": "📚"},
            {"id": 4, "name": "Home & Kitchen", "icon": "🏠"},
            {"id": 5, "name": "Sports", "icon": "⚽"},
            {"id": 6, "name": "Beauty", "icon": "💄"},
            {"id": 7, "name": "Toys", "icon": "🧸"},
            {"id": 8, "name": "Groceries", "icon": "🛒"},
        ]
    }

@app.get("/api/trending")
async def get_trending():
    """Get trending products"""
    trending = get_mock_products("electronics")
    return {
        "trending": [p.dict() for p in trending[:6]]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
