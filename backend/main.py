from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re
from datetime import datetime
import json

# Import routes
from routes.auth import router as auth_router
from routes.cart import router as cart_router
from routes.payment import router as payment_router
from services.search_service import SearchService

app = FastAPI(title="ECommerce API", version="2.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(payment_router)

class Product(BaseModel):
    id: str
    name: str
    price: str
    image_url: str
    rating: str = "N/A"
    reviews: str = "0"
    description: Optional[str] = None

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
        search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
        headers = get_flipkart_headers()
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        product_containers = soup.find_all('div', {'class': re.compile('col.*')})
        
        for container in product_containers[:max_products]:
            try:
                product_link = container.find('a', {'class': re.compile('_+1UQZyc')})
                if not product_link:
                    continue
                
                product_url = product_link.get('href', '')
                name_elem = container.find('a', {'class': re.compile('s1Q50cAgFa')})
                name = name_elem.text.strip() if name_elem else "Unknown Product"
                
                price_elem = container.find('div', {'class': re.compile('_+30jeq3')})
                price = price_elem.text.strip() if price_elem else "N/A"
                
                img_elem = container.find('img')
                image_url = img_elem.get('src', '') if img_elem else ""
                
                rating_elem = container.find('div', {'class': re.compile('_+1lRcqm')})
                rating = rating_elem.text.strip() if rating_elem else "N/A"
                
                review_elem = container.find('span', {'class': re.compile('_+1oKavI')})
                reviews = review_elem.text.strip() if review_elem else "0"
                
                if name and image_url:
                    product = Product(
                        id=hash(product_url) % ((2**31) - 1),
                        name=name[:100],
                        price=price,
                        image_url=image_url,
                        rating=rating,
                        reviews=reviews,
                        description=f"High-quality {name}. Check our amazing deals!"
                    )
                    products.append(product)
                    
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue
        
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return get_mock_products(search_query)

def get_mock_products(search_query: str = "electronics") -> List[Product]:
    """Return mock products with detailed info"""
    mock_data = {
        "electronics": [
            {
                "name": "Apple iPhone 15 (Black, 256GB)",
                "price": "₹49,999",
                "image_url": "https://images.unsplash.com/photo-1592286927505-1def25115558?w=300",
                "rating": "4.7",
                "reviews": "28.5K",
                "description": "Latest Apple iPhone 15 with advanced camera system"
            },
            {
                "name": "Samsung Galaxy S24 (Graphite, 256GB)",
                "price": "₹59,999",
                "image_url": "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=300",
                "rating": "4.6",
                "reviews": "15.2K",
                "description": "Premium Samsung smartphone with AMOLED display"
            },
            {
                "name": "OnePlus 12 (Pine Green, 256GB)",
                "price": "₹44,999",
                "image_url": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=300",
                "rating": "4.5",
                "reviews": "12.3K",
                "description": "OnePlus flagship with fast charging and 120Hz display"
            },
            {
                "name": "Redmi Note 13 (Midnight Black, 256GB)",
                "price": "₹17,999",
                "image_url": "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=300",
                "rating": "4.4",
                "reviews": "18.9K",
                "description": "Budget-friendly smartphone with great battery life"
            },
            {
                "name": "Sony WH-1000XM5 Headphones",
                "price": "₹24,999",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300",
                "rating": "4.8",
                "reviews": "8.2K",
                "description": "Premium noise-cancelling wireless headphones"
            },
            {
                "name": "iPad Air (10.9-inch, 256GB)",
                "price": "₹59,900",
                "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=300",
                "rating": "4.6",
                "reviews": "5.1K",
                "description": "Powerful tablet with M1 chip for professionals"
            },
        ],
        "clothing": [
            {
                "name": "Men's Premium Cotton T-Shirt (Blue)",
                "price": "₹599",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300",
                "rating": "4.3",
                "reviews": "2.1K",
                "description": "Comfortable and durable cotton t-shirt"
            },
            {
                "name": "Women's Casual Shirt (White)",
                "price": "₹799",
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=300",
                "rating": "4.5",
                "reviews": "3.2K",
                "description": "Stylish casual wear for everyday use"
            },
        ],
        "books": [
            {
                "name": "Atomic Habits by James Clear",
                "price": "₹400",
                "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e01fb7d?w=300",
                "rating": "4.7",
                "reviews": "5.2K",
                "description": "Transform your life with tiny habits"
            },
            {
                "name": "The Midnight Library by Matt Haig",
                "price": "₹345",
                "image_url": "https://images.unsplash.com/photo-1507842217343-583f1270b3fe?w=300",
                "rating": "4.6",
                "reviews": "1.8K",
                "description": "Explore infinite possibilities in this novel"
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
            reviews=item['reviews'],
            description=item.get('description', 'Great product!')
        )
        products.append(product)
    
    return products

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ECommerce API v2.0",
        "version": "2.0",
        "endpoints": {
            "auth": "/api/auth/*",
            "cart": "/api/cart/*",
            "payment": "/api/payment/*",
            "products": "/api/search, /api/categories, /api/trending"
        }
    }

@app.get("/api/search")
async def search_products(q: str = "electronics", limit: int = 20, sort_by: str = "relevant", min_price: float = 0, max_price: float = 100000) -> dict:
    """Search for products with advanced filtering"""
    if not q or len(q) < 1:
        raise HTTPException(status_code=400, detail="Query must be at least 1 character")
    
    if limit > 100:
        limit = 100
    
    cache_key = f"{q}_{limit}".lower()
    
    # Check cache
    if cache_key in products_cache:
        products = products_cache[cache_key]
        cached = True
    else:
        products = scrape_flipkart_search(q, limit)
        products_cache[cache_key] = [p.dict() for p in products]
        cached = False
    
    # Convert to dict for processing
    products_list = [p.dict() if hasattr(p, 'dict') else p for p in products]
    
    # Apply search filter
    products_list = SearchService.search_products(products_list, q)
    
    # Apply price filter
    products_list = SearchService.filter_by_price(products_list, min_price, max_price)
    
    # Apply sorting
    products_list = SearchService.sort_products(products_list, sort_by)
    
    # Limit results
    products_list = products_list[:limit]
    
    return {
        "query": q,
        "products": products_list,
        "cached": cached,
        "count": len(products_list),
        "filters": {
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by
        }
    }

@app.get("/api/product/{product_id}")
async def get_product_details(product_id: str) -> dict:
    """Get detailed product information"""
    # Search in cache or mock data
    all_products = get_mock_products("electronics")
    
    for product in all_products:
        if str(product.id) == product_id:
            return {
                "product": product.dict(),
                "specifications": {
                    "warranty": "1 year manufacturer warranty",
                    "return_policy": "30 days return",
                    "delivery": "Free delivery across India",
                    "seller": "Authorized Seller",
                    "cod_available": True
                },
                "offers": [
                    {"text": "₹3,315 off with Credit Card", "code": "CARD3K"},
                    {"text": "₹1,000 off with Debit Card", "code": "DB1000"}
                ]
            }
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/categories")
async def get_categories():
    """Get popular categories"""
    return {
        "categories": [
            {"id": 1, "name": "Electronics", "icon": "📱", "count": 245},
            {"id": 2, "name": "Clothing", "icon": "👕", "count": 892},
            {"id": 3, "name": "Books", "icon": "📚", "count": 156},
            {"id": 4, "name": "Home & Kitchen", "icon": "🏠", "count": 453},
            {"id": 5, "name": "Sports", "icon": "⚽", "count": 203},
            {"id": 6, "name": "Beauty", "icon": "💄", "count": 324},
            {"id": 7, "name": "Toys", "icon": "🧸", "count": 178},
            {"id": 8, "name": "Groceries", "icon": "🛒", "count": 521},
        ]
    }

@app.get("/api/trending")
async def get_trending():
    """Get trending products"""
    trending = get_mock_products("electronics")
    return {
        "trending": [p.dict() for p in trending[:6]],
        "title": "Trending Now",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "Server is running", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
