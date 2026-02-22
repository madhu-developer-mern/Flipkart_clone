from typing import List
import re

class SearchService:
    @staticmethod
    def search_products(products: list, query: str) -> list:
        """Search products by name or description"""
        if not query or len(query) < 1:
            return products
        
        query_lower = query.lower()
        results = []
        
        for product in products:
            name_match = query_lower in product.get("name", "").lower()
            desc_match = query_lower in product.get("description", "").lower() if product.get("description") else False
            
            if name_match or desc_match:
                results.append(product)
        
        return results

    @staticmethod
    def filter_by_price(products: list, min_price: float, max_price: float) -> list:
        """Filter products by price range"""
        filtered = []
        
        for product in products:
            price_str = product.get("price", "₹0").replace("₹", "").replace(",", "").strip()
            try:
                price = float(price_str)
                if min_price <= price <= max_price:
                    filtered.append(product)
            except ValueError:
                pass
        
        return filtered

    @staticmethod
    def filter_by_rating(products: list, min_rating: float) -> list:
        """Filter products by minimum rating"""
        filtered = []
        
        for product in products:
            rating_str = product.get("rating", "0")
            try:
                rating = float(rating_str)
                if rating >= min_rating:
                    filtered.append(product)
            except ValueError:
                pass
        
        return filtered

    @staticmethod
    def sort_products(products: list, sort_by: str) -> list:
        """Sort products"""
        if sort_by == "price_low":
            return sorted(products, key=lambda p: float(p.get("price", "₹0").replace("₹", "").replace(",", "") or 0))
        elif sort_by == "price_high":
            return sorted(products, key=lambda p: float(p.get("price", "₹0").replace("₹", "").replace(",", "") or 0), reverse=True)
        elif sort_by == "rating":
            return sorted(products, key=lambda p: float(p.get("rating", "0") or 0), reverse=True)
        else:
            return products
