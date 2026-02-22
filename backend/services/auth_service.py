import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, List

# In-memory storage (for demo purposes)
users_db: Dict[str, dict] = {}
carts_db: Dict[str, dict] = {}
orders_db: Dict[str, dict] = {}

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password

    @staticmethod
    def register_user(email: str, password: str, full_name: str) -> dict:
        """Register new user"""
        if email in users_db:
            raise ValueError("User already exists")
        
        user_id = hashlib.md5(email.encode()).hexdigest()[:12]
        hashed_pw = AuthService.hash_password(password)
        
        user_data = {
            "id": user_id,
            "email": email,
            "password": hashed_pw,
            "full_name": full_name,
            "phone": None,
            "address": None,
            "city": None,
            "country": None,
            "created_at": datetime.now().isoformat()
        }
        
        users_db[email] = user_data
        return user_data

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """Login user"""
        if email not in users_db:
            raise ValueError("User not found")
        
        user = users_db[email]
        if not AuthService.verify_password(password, user["password"]):
            raise ValueError("Invalid credentials")
        
        # Generate token (simple JWT-like dummy token)
        token = hashlib.sha256(f"{email}{datetime.now().isoformat()}".encode()).hexdigest()
        user["token"] = token
        
        return user

    @staticmethod
    def get_user(email: str) -> Optional[dict]:
        """Get user by email"""
        return users_db.get(email)

    @staticmethod
    def update_user(email: str, **kwargs) -> dict:
        """Update user details"""
        if email not in users_db:
            raise ValueError("User not found")
        
        user = users_db[email]
        for key, value in kwargs.items():
            if key in user and key != "password":
                user[key] = value
        
        return user
