"""
用户认证服务
支持邮箱密码登录和 OAuth (Google) 登录
"""
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class MembershipType(str, Enum):
    FREE = "free"
    PERSONAL = "personal"
    DESIGNER = "designer"
    ENTERPRISE = "enterprise"


@dataclass
class User:
    id: int
    email: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    membership_type: str
    credits: int
    created_at: datetime


class AuthService:
    """
    用户认证服务
    
    目前使用内存存储（演示用）
    生产环境应替换为数据库存储
    """
    
    def __init__(self):
        self._users: dict[int, dict] = {}
        self._users_by_email: dict[str, int] = {}
        self._users_by_provider: dict[str, int] = {}
        self._next_id = 1
    
    def _hash_password(self, password: str, salt: str = None) -> tuple[str, str]:
        """哈希密码"""
        if salt is None:
            salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        ).hex()
        return hashed, salt
    
    def _verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """验证密码"""
        new_hash, _ = self._hash_password(password, salt)
        return new_hash == hashed
    
    def register(
        self,
        email: str,
        password: str,
        name: str = None
    ) -> Optional[User]:
        """邮箱注册"""
        if email in self._users_by_email:
            return None
        
        hashed, salt = self._hash_password(password)
        
        user_id = self._next_id
        self._next_id += 1
        
        user_data = {
            "id": user_id,
            "email": email,
            "name": name or email.split("@")[0],
            "avatar": None,
            "password_hash": hashed,
            "password_salt": salt,
            "membership_type": MembershipType.FREE.value,
            "credits": 5,
            "created_at": datetime.now(),
        }
        
        self._users[user_id] = user_data
        self._users_by_email[email] = user_id
        
        return self._to_user(user_data)
    
    def login(self, email: str, password: str) -> Optional[User]:
        """邮箱登录"""
        user_id = self._users_by_email.get(email)
        if not user_id:
            return None
        
        user_data = self._users.get(user_id)
        if not user_data:
            return None
        
        if not self._verify_password(
            password,
            user_data["password_hash"],
            user_data["password_salt"]
        ):
            return None
        
        return self._to_user(user_data)
    
    def oauth_login(
        self,
        provider: str,
        provider_id: str,
        email: str = None,
        name: str = None,
        avatar: str = None
    ) -> User:
        """OAuth 登录（Google 等）"""
        provider_key = f"{provider}:{provider_id}"
        
        user_id = self._users_by_provider.get(provider_key)
        
        if user_id:
            user_data = self._users[user_id]
            if name:
                user_data["name"] = name
            if avatar:
                user_data["avatar"] = avatar
            return self._to_user(user_data)
        
        if email and email in self._users_by_email:
            user_id = self._users_by_email[email]
            user_data = self._users[user_id]
            self._users_by_provider[provider_key] = user_id
            if name:
                user_data["name"] = name
            if avatar:
                user_data["avatar"] = avatar
            return self._to_user(user_data)
        
        user_id = self._next_id
        self._next_id += 1
        
        user_data = {
            "id": user_id,
            "email": email,
            "name": name or "用户",
            "avatar": avatar,
            "password_hash": None,
            "password_salt": None,
            "membership_type": MembershipType.FREE.value,
            "credits": 5,
            "created_at": datetime.now(),
        }
        
        self._users[user_id] = user_data
        self._users_by_provider[provider_key] = user_id
        if email:
            self._users_by_email[email] = user_id
        
        return self._to_user(user_data)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """获取用户信息"""
        user_data = self._users.get(user_id)
        if not user_data:
            return None
        return self._to_user(user_data)
    
    def update_user(
        self,
        user_id: int,
        name: str = None,
        avatar: str = None
    ) -> Optional[User]:
        """更新用户信息"""
        user_data = self._users.get(user_id)
        if not user_data:
            return None
        
        if name:
            user_data["name"] = name
        if avatar:
            user_data["avatar"] = avatar
        
        return self._to_user(user_data)
    
    def add_credits(self, user_id: int, amount: int) -> Optional[User]:
        """添加积分"""
        user_data = self._users.get(user_id)
        if not user_data:
            return None
        
        user_data["credits"] += amount
        return self._to_user(user_data)
    
    def use_credits(self, user_id: int, amount: int) -> bool:
        """使用积分"""
        user_data = self._users.get(user_id)
        if not user_data:
            return False
        
        if user_data["credits"] < amount:
            return False
        
        user_data["credits"] -= amount
        return True
    
    def _to_user(self, data: dict) -> User:
        """转换为 User 对象"""
        return User(
            id=data["id"],
            email=data.get("email"),
            name=data.get("name"),
            avatar=data.get("avatar"),
            membership_type=data.get("membership_type", MembershipType.FREE.value),
            credits=data.get("credits", 0),
            created_at=data.get("created_at", datetime.now()),
        )


auth_service = AuthService()
