from fastapi import APIRouter, HTTPException
from models.schemas import User, UserResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(email: str, password: str, full_name: str):
    """Register new user"""
    try:
        user = AuthService.register_user(email, password, full_name)
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            phone=user.get("phone"),
            address=user.get("address"),
            city=user.get("city"),
            country=user.get("country"),
            token=user.get("token")
        )
        return user_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
async def login(email: str, password: str):
    """Login user"""
    try:
        user = AuthService.login_user(email, password)
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            phone=user.get("phone"),
            address=user.get("address"),
            city=user.get("city"),
            country=user.get("country"),
            token=user.get("token")
        )
        return user_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{email}", response_model=UserResponse)
async def get_user(email: str):
    """Get user details"""
    user = AuthService.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        phone=user.get("phone"),
        address=user.get("address"),
        city=user.get("city"),
        country=user.get("country")
    )
    return user_response

@router.put("/user/{email}")
async def update_user(email: str, full_name: str = None, phone: str = None, address: str = None, city: str = None, country: str = None):
    """Update user details"""
    try:
        kwargs = {}
        if full_name:
            kwargs["full_name"] = full_name
        if phone:
            kwargs["phone"] = phone
        if address:
            kwargs["address"] = address
        if city:
            kwargs["city"] = city
        if country:
            kwargs["country"] = country
        
        user = AuthService.update_user(email, **kwargs)
        
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            phone=user.get("phone"),
            address=user.get("address"),
            city=user.get("city"),
            country=user.get("country")
        )
        return user_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
