from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    token: Optional[str] = None

class Product(BaseModel):
    id: str
    name: str
    price: str
    image_url: str
    rating: str = "N/A"
    reviews: str = "0"
    description: Optional[str] = None
    specifications: Optional[dict] = None
    stock: int = 100

class CartItem(BaseModel):
    product_id: str
    product_name: str
    price: str
    quantity: int
    image_url: str

class Cart(BaseModel):
    user_id: str
    items: list[CartItem] = []
    total_price: float = 0.0

class Order(BaseModel):
    id: Optional[str] = None
    user_id: str
    user_email: str
    items: list[CartItem]
    total_price: float
    payment_status: str = "pending"
    order_status: str = "pending"
    delivery_address: str
    created_at: Optional[str] = None

class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    payment_method: str  # credit_card, debit_card, upi, net_banking
    user_id: str

class PaymentResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: float
