from fastapi import APIRouter, HTTPException
from services.payment_service import PaymentService

router = APIRouter(prefix="/api/payment", tags=["payment"])

@router.post("/create-order")
async def create_order(user_id: str, user_email: str, items: list, total_price: float, delivery_address: str):
    """Create new order"""
    try:
        order = PaymentService.create_order(user_id, user_email, items, total_price, delivery_address)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process")
async def process_payment(order_id: str, amount: float, payment_method: str, user_id: str):
    """Process payment"""
    try:
        result = PaymentService.process_payment(order_id, amount, payment_method, user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order/{order_id}")
async def get_order(order_id: str):
    """Get order details"""
    try:
        order = PaymentService.get_order(order_id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/orders/{user_id}")
async def get_user_orders(user_id: str):
    """Get all user orders"""
    try:
        orders = PaymentService.get_user_orders(user_id)
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transaction/{transaction_id}")
async def get_transaction(transaction_id: str):
    """Get transaction details"""
    try:
        transaction = PaymentService.get_transaction(transaction_id)
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
