import hashlib
from typing import List, Optional, Dict
from models.schemas import CartItem, Cart
from datetime import datetime

class CartService:
    carts_db: Dict[str, dict] = {}

    @staticmethod
    def get_cart(user_id: str) -> dict:
        """Get user's cart"""
        if user_id not in CartService.carts_db:
            CartService.carts_db[user_id] = {
                "user_id": user_id,
                "items": [],
                "total_price": 0.0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        return CartService.carts_db[user_id]

    @staticmethod
    def add_to_cart(user_id: str, product_id: str, product_name: str, price: str, quantity: int, image_url: str) -> dict:
        """Add item to cart"""
        cart = CartService.get_cart(user_id)
        
        # Check if item already exists
        for item in cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                CartService._update_total(cart)
                cart["updated_at"] = datetime.now().isoformat()
                return cart
        
        # Add new item
        new_item = {
            "product_id": product_id,
            "product_name": product_name,
            "price": price,
            "quantity": quantity,
            "image_url": image_url
        }
        
        cart["items"].append(new_item)
        CartService._update_total(cart)
        cart["updated_at"] = datetime.now().isoformat()
        
        return cart

    @staticmethod
    def remove_from_cart(user_id: str, product_id: str) -> dict:
        """Remove item from cart"""
        cart = CartService.get_cart(user_id)
        cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
        CartService._update_total(cart)
        cart["updated_at"] = datetime.now().isoformat()
        return cart

    @staticmethod
    def update_quantity(user_id: str, product_id: str, quantity: int) -> dict:
        """Update item quantity"""
        cart = CartService.get_cart(user_id)
        
        for item in cart["items"]:
            if item["product_id"] == product_id:
                if quantity <= 0:
                    CartService.remove_from_cart(user_id, product_id)
                else:
                    item["quantity"] = quantity
                break
        
        CartService._update_total(cart)
        cart["updated_at"] = datetime.now().isoformat()
        return cart

    @staticmethod
    def clear_cart(user_id: str) -> dict:
        """Clear user's cart"""
        CartService.carts_db[user_id] = {
            "user_id": user_id,
            "items": [],
            "total_price": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        return CartService.carts_db[user_id]

    @staticmethod
    def _update_total(cart: dict):
        """Calculate total price"""
        total = 0.0
        for item in cart["items"]:
            # Extract numeric price
            price_str = item["price"].replace("₹", "").replace(",", "").strip()
            try:
                price = float(price_str)
                total += price * item["quantity"]
            except ValueError:
                pass
        
        cart["total_price"] = round(total, 2)
