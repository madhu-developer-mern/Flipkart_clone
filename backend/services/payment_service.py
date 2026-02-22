import uuid
from datetime import datetime
from typing import Dict
import random

class PaymentService:
    orders_db: Dict[str, dict] = {}
    transactions_db: Dict[str, dict] = {}

    @staticmethod
    def create_order(user_id: str, user_email: str, items: list, total_price: float, delivery_address: str) -> dict:
        """Create new order"""
        order_id = str(uuid.uuid4())[:12]
        
        order = {
            "id": order_id,
            "user_id": user_id,
            "user_email": user_email,
            "items": items,
            "total_price": total_price,
            "payment_status": "pending",
            "order_status": "pending",
            "delivery_address": delivery_address,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        PaymentService.orders_db[order_id] = order
        return order

    @staticmethod
    def process_payment(order_id: str, amount: float, payment_method: str, user_id: str) -> dict:
        """Process payment (simulated)"""
        if order_id not in PaymentService.orders_db:
            raise ValueError("Order not found")
        
        # Simulate payment processing
        success = random.choice([True, True, True, False])  # 75% success rate for demo
        transaction_id = str(uuid.uuid4())[:16]
        
        transaction = {
            "id": transaction_id,
            "order_id": order_id,
            "amount": amount,
            "payment_method": payment_method,
            "user_id": user_id,
            "status": "success" if success else "failed",
            "timestamp": datetime.now().isoformat()
        }
        
        PaymentService.transactions_db[transaction_id] = transaction
        
        if success:
            order = PaymentService.orders_db[order_id]
            order["payment_status"] = "completed"
            order["order_status"] = "confirmed"
            order["updated_at"] = datetime.now().isoformat()
        
        return {
            "success": success,
            "transaction_id": transaction_id,
            "order_id": order_id,
            "amount": amount,
            "message": "Payment processed successfully!" if success else "Payment failed. Please try again."
        }

    @staticmethod
    def get_order(order_id: str) -> dict:
        """Get order details"""
        if order_id not in PaymentService.orders_db:
            raise ValueError("Order not found")
        return PaymentService.orders_db[order_id]

    @staticmethod
    def get_user_orders(user_id: str) -> list:
        """Get all user orders"""
        return [order for order in PaymentService.orders_db.values() if order["user_id"] == user_id]

    @staticmethod
    def get_transaction(transaction_id: str) -> dict:
        """Get transaction details"""
        if transaction_id not in PaymentService.transactions_db:
            raise ValueError("Transaction not found")
        return PaymentService.transactions_db[transaction_id]
