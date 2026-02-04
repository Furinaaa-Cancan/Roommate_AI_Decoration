"""
安全用户认证服务
- 使用MySQL数据库持久化存储
- 密码加密使用bcrypt
- 登录失败限制防暴力破解
- JWT token 认证
"""
import os
import re
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import bcrypt
import jwt
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Enum as SQLEnum, text
from sqlalchemy.exc import IntegrityError

from services.database import db_manager, Base


class MembershipType(str, Enum):
    FREE = "free"
    PERSONAL = "personal"
    DESIGNER = "designer"
    ENTERPRISE = "enterprise"


class UserModel(Base):
    """用户数据库模型"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    password_salt = Column(String(64))
    google_id = Column(String(128), unique=True, index=True)
    openid = Column(String(128), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    nickname = Column(String(64))
    avatar_url = Column(String(512))
    membership_type = Column(SQLEnum(MembershipType), default=MembershipType.FREE)
    membership_expire_at = Column(DateTime)
    credits = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 安全字段
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    last_login_at = Column(DateTime)
    last_login_ip = Column(String(45))


@dataclass
class User:
    """用户数据传输对象"""
    id: int
    email: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    membership_type: str
    credits: int
    created_at: datetime


class PasswordValidator:
    """密码强度验证器"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    @classmethod
    def validate(cls, password: str) -> Tuple[bool, str]:
        """
        验证密码强度
        返回: (是否有效, 错误信息)
        """
        if len(password) < cls.MIN_LENGTH:
            return False, f"密码长度至少{cls.MIN_LENGTH}位"
        
        if len(password) > cls.MAX_LENGTH:
            return False, f"密码长度不能超过{cls.MAX_LENGTH}位"
        
        if not re.search(r'[a-zA-Z]', password):
            return False, "密码必须包含字母"
        
        if not re.search(r'\d', password):
            return False, "密码必须包含数字"
        
        # 检查常见弱密码
        weak_passwords = ['12345678', 'password', 'qwerty123', '11111111']
        if password.lower() in weak_passwords:
            return False, "密码太简单，请使用更复杂的密码"
        
        return True, ""


class LoginRateLimiter:
    """登录频率限制器"""
    
    MAX_ATTEMPTS = 5          # 最大尝试次数
    LOCK_DURATION = 15        # 锁定时间（分钟）
    
    @classmethod
    def check_locked(cls, user: UserModel) -> Tuple[bool, Optional[int]]:
        """
        检查账户是否被锁定
        返回: (是否锁定, 剩余锁定秒数)
        """
        if user.locked_until and user.locked_until > datetime.now():
            remaining = (user.locked_until - datetime.now()).seconds
            return True, remaining
        return False, None
    
    @classmethod
    def record_failure(cls, user: UserModel, session) -> bool:
        """
        记录登录失败
        返回: 是否触发锁定
        """
        user.login_attempts = (user.login_attempts or 0) + 1
        
        if user.login_attempts >= cls.MAX_ATTEMPTS:
            user.locked_until = datetime.now() + timedelta(minutes=cls.LOCK_DURATION)
            user.login_attempts = 0
            session.commit()
            return True
        
        session.commit()
        return False
    
    @classmethod
    def reset(cls, user: UserModel, session):
        """重置登录尝试计数"""
        user.login_attempts = 0
        user.locked_until = None
        session.commit()


class SecureAuthService:
    """安全认证服务"""
    
    JWT_SECRET = os.getenv("JWT_SECRET", os.getenv("NEXTAUTH_SECRET", "change-this-in-production"))
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_HOURS = 24 * 7  # 7天
    
    def __init__(self):
        # 确保数据库已初始化并创建表
        db_manager.init()
        db_manager.create_tables(Base)
    
    def _hash_password(self, password: str) -> str:
        """使用bcrypt哈希密码"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """验证密码"""
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False
    
    def _generate_token(self, user_id: str, email: str) -> str:
        """生成JWT token"""
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=self.JWT_EXPIRE_HOURS),
            "iat": datetime.utcnow(),
            "jti": secrets.token_hex(16)  # 唯一token ID
        }
        return jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """验证JWT token"""
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def _to_user(self, model: UserModel) -> User:
        """转换为User对象"""
        return User(
            id=model.id,
            email=model.email,
            name=model.nickname,
            avatar=model.avatar_url,
            membership_type=model.membership_type.value if model.membership_type else "free",
            credits=model.credits or 0,
            created_at=model.created_at or datetime.now()
        )
    
    def register(
        self,
        email: str,
        password: str,
        name: str = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        用户注册
        返回: (用户对象, 错误信息)
        """
        # 验证邮箱格式
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return None, "邮箱格式不正确"
        
        # 验证密码强度
        valid, error = PasswordValidator.validate(password)
        if not valid:
            return None, error
        
        # 哈希密码
        password_hash = self._hash_password(password)
        
        with db_manager.get_session() as session:
            # 检查邮箱是否已存在
            existing = session.query(UserModel).filter(UserModel.email == email).first()
            if existing:
                return None, "该邮箱已被注册"
            
            # 创建用户
            user = UserModel(
                email=email,
                password_hash=password_hash,
                nickname=name or email.split("@")[0],
                membership_type=MembershipType.FREE,
                credits=10,  # 新用户赠送10次
                created_at=datetime.now()
            )
            
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return self._to_user(user), None
            except IntegrityError:
                session.rollback()
                return None, "注册失败，请稍后重试"
    
    def login(
        self,
        email: str,
        password: str,
        ip_address: str = None
    ) -> Tuple[Optional[User], Optional[str], Optional[str]]:
        """
        用户登录
        返回: (用户对象, 错误信息, JWT token)
        """
        with db_manager.get_session() as session:
            user = session.query(UserModel).filter(UserModel.email == email).first()
            
            if not user:
                return None, "邮箱或密码错误", None
            
            # 检查账户是否被锁定
            is_locked, remaining = LoginRateLimiter.check_locked(user)
            if is_locked:
                return None, f"账户已锁定，请{remaining // 60 + 1}分钟后重试", None
            
            # 验证密码
            if not self._verify_password(password, user.password_hash):
                # 记录失败
                locked = LoginRateLimiter.record_failure(user, session)
                if locked:
                    return None, f"登录失败次数过多，账户已锁定{LoginRateLimiter.LOCK_DURATION}分钟", None
                remaining_attempts = LoginRateLimiter.MAX_ATTEMPTS - user.login_attempts
                return None, f"邮箱或密码错误，还可尝试{remaining_attempts}次", None
            
            # 登录成功，重置计数
            LoginRateLimiter.reset(user, session)
            
            # 更新登录信息
            user.last_login_at = datetime.now()
            if ip_address:
                user.last_login_ip = ip_address
            session.commit()
            
            # 生成token
            token = self._generate_token(user.id, user.email)
            
            return self._to_user(user), None, token
    
    def oauth_login(
        self,
        provider: str,
        provider_id: str,
        email: str = None,
        name: str = None,
        avatar: str = None
    ) -> User:
        """OAuth登录（Google等）"""
        with db_manager.get_session() as session:
            user = None
            
            # 根据provider查找用户
            if provider == "google":
                user = session.query(UserModel).filter(UserModel.google_id == provider_id).first()
            
            # 如果没找到，尝试用邮箱查找
            if not user and email:
                user = session.query(UserModel).filter(UserModel.email == email).first()
                if user:
                    # 关联OAuth账号
                    if provider == "google":
                        user.google_id = provider_id
            
            # 如果还是没找到，创建新用户
            if not user:
                user = UserModel(
                    email=email,
                    google_id=provider_id if provider == "google" else None,
                    nickname=name or "用户",
                    avatar_url=avatar,
                    membership_type=MembershipType.FREE,
                    credits=10,
                    created_at=datetime.now()
                )
                session.add(user)
            else:
                # 更新用户信息
                if name:
                    user.nickname = name
                if avatar:
                    user.avatar_url = avatar
            
            session.commit()
            session.refresh(user)
            return self._to_user(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户信息"""
        with db_manager.get_session() as session:
            # 支持通过id或provider_id查找用户
            user = session.query(UserModel).filter(
                (UserModel.id == user_id) | (UserModel.provider_id == user_id)
            ).first()
            if not user:
                return None
            return self._to_user(user)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        with db_manager.get_session() as session:
            user = session.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                return None
            return self._to_user(user)
    
    def update_user(
        self,
        user_id: str,
        name: str = None,
        avatar: str = None
    ) -> Optional[User]:
        """更新用户信息"""
        with db_manager.get_session() as session:
            # 支持通过id或provider_id查找用户
            user = session.query(UserModel).filter(
                (UserModel.id == user_id) | (UserModel.provider_id == user_id)
            ).first()
            if not user:
                return None
            
            if name:
                user.nickname = name
            if avatar:
                user.avatar_url = avatar
            
            session.commit()
            session.refresh(user)
            return self._to_user(user)
    
    def add_credits(self, user_id: str, amount: int) -> Optional[User]:
        """添加积分"""
        with db_manager.get_session() as session:
            # 支持通过id或provider_id查找用户
            user = session.query(UserModel).filter(
                (UserModel.id == user_id) | (UserModel.provider_id == user_id)
            ).first()
            if not user:
                return None
            
            user.credits = (user.credits or 0) + amount
            session.commit()
            session.refresh(user)
            return self._to_user(user)
    
    def use_credits(self, user_id: str, amount: int) -> Tuple[bool, int]:
        """
        使用积分
        返回: (是否成功, 剩余积分)
        """
        with db_manager.get_session() as session:
            # 支持通过id或provider_id查找用户
            user = session.query(UserModel).filter(
                (UserModel.id == user_id) | (UserModel.provider_id == user_id)
            ).first()
            if not user:
                return False, 0
            
            if (user.credits or 0) < amount:
                return False, user.credits or 0
            
            user.credits = user.credits - amount
            session.commit()
            return True, user.credits
    
    def update_membership(
        self,
        user_id: str,
        membership_type: str,
        expire_at: datetime = None
    ) -> Optional[User]:
        """更新会员状态"""
        with db_manager.get_session() as session:
            # 支持通过id或provider_id查找用户
            user = session.query(UserModel).filter(
                (UserModel.id == user_id) | (UserModel.provider_id == user_id)
            ).first()
            if not user:
                return None
            
            user.membership_type = MembershipType(membership_type)
            user.membership_expire_at = expire_at
            # 积分通过add_credits单独添加，这里只更新会员类型
            
            session.commit()
            session.refresh(user)
            return self._to_user(user)


# 全局安全认证服务实例
secure_auth_service = SecureAuthService()
