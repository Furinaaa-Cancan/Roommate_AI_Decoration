"""
NanoBanana AI 数据模型 (SQLAlchemy ORM)
"""
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, List
from sqlalchemy import (
    Column, BigInteger, String, Integer, Float, Text, DateTime, 
    Boolean, Enum, JSON, ForeignKey, DECIMAL, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# ============ 枚举定义 ============

class MembershipType(PyEnum):
    FREE = "free"
    PERSONAL = "personal"
    DESIGNER = "designer"
    ENTERPRISE = "enterprise"

class RoomType(PyEnum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    MASTER_BEDROOM = "master_bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    DINING_ROOM = "dining_room"
    STUDY = "study"
    BALCONY = "balcony"
    OTHER = "other"

class PhotoSource(PyEnum):
    USER_UPLOAD = "user_upload"
    DATASET_ZIND = "dataset_zind"
    DATASET_3DFRONT = "dataset_3dfront"
    DATASET_OTHER = "dataset_other"

class TaskStatus(PyEnum):
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class APIProvider(PyEnum):
    REPLICATE = "replicate"
    RUNPOD = "runpod"
    SELF_HOSTED = "self_hosted"

# ============ 数据模型 ============

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    openid = Column(String(128), unique=True)
    phone = Column(String(20), unique=True)
    nickname = Column(String(64))
    avatar_url = Column(String(512))
    membership_type = Column(Enum(MembershipType), default=MembershipType.FREE)
    membership_expire_at = Column(DateTime)
    credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    raw_photos = relationship("RawPhoto", back_populates="user")
    tasks = relationship("GenerationTask", back_populates="user")

class RawPhoto(Base):
    """毛胚房原图"""
    __tablename__ = "raw_photos"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))
    
    # 图片信息
    original_url = Column(String(512), nullable=False)
    thumbnail_url = Column(String(512))
    file_size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    
    # 空间识别
    room_type = Column(Enum(RoomType))
    room_type_confidence = Column(Float)
    
    # 来源
    source = Column(Enum(PhotoSource), default=PhotoSource.USER_UPLOAD)
    source_id = Column(String(128))
    
    # 元数据
    metadata = Column(JSON)
    status = Column(String(20), default="pending")
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="raw_photos")
    tasks = relationship("GenerationTask", back_populates="raw_photo")

class GenerationTask(Base):
    """AI生成任务"""
    __tablename__ = "generation_tasks"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_uuid = Column(String(64), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    raw_photo_id = Column(BigInteger, ForeignKey("raw_photos.id"), nullable=False)
    
    # 生成参数
    style = Column(String(64), default="nanobanana")
    style_variant = Column(String(1))
    prompt = Column(Text)
    negative_prompt = Column(Text)
    
    # API调用
    api_provider = Column(Enum(APIProvider), default=APIProvider.REPLICATE)
    api_model = Column(String(128))
    api_request_id = Column(String(128))
    api_cost = Column(DECIMAL(10, 6))
    
    # 状态
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    error_message = Column(Text)
    
    # 时间
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="tasks")
    raw_photo = relationship("RawPhoto", back_populates="tasks")
    generated_images = relationship("GeneratedImage", back_populates="task")

class GeneratedImage(Base):
    """生成结果图"""
    __tablename__ = "generated_images"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("generation_tasks.id", ondelete="CASCADE"), nullable=False)
    
    image_url = Column(String(512), nullable=False)
    thumbnail_url = Column(String(512))
    watermarked_url = Column(String(512))
    
    width = Column(Integer)
    height = Column(Integer)
    sequence_num = Column(Integer, default=1)
    
    quality_score = Column(Float)
    is_primary = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    task = relationship("GenerationTask", back_populates="generated_images")

# ============ 数据库初始化 ============

def init_db(database_url: str):
    """初始化数据库连接"""
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session
