from fastapi import APIRouter, HTTPException
from services.cart_service import CartService

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/{user_id}")
async def get_cart(user_id: str):
    """Get user's cart"""
    try:
        cart = CartService.get_cart(user_id)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{user_id}/add")
async def add_to_cart(user_id: str, product_id: str, product_name: str, price: str, quantity: int, image_url: str):
    """Add item to cart"""
    try:
        cart = CartService.add_to_cart(user_id, product_id, product_name, price, quantity, image_url)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}/remove/{product_id}")
async def remove_from_cart(user_id: str, product_id: str):
    """Remove item from cart"""
    try:
        cart = CartService.remove_from_cart(user_id, product_id)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/update/{product_id}")
async def update_quantity(user_id: str, product_id: str, quantity: int):
    """Update item quantity"""
    try:
        cart = CartService.update_quantity(user_id, product_id, quantity)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}/clear")
async def clear_cart(user_id: str):
    """Clear cart"""
    try:
        cart = CartService.clear_cart(user_id)
        return cart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
