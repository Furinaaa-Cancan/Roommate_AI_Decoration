"""
用户生成历史服务
保存和查询用户的AI生成记录
"""
import uuid
from datetime import datetime
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime, Float, Text, Index, Enum as SQLEnum

from services.database import db_manager, Base


class GenerationType(str, Enum):
    FULL = "full"           # 整体生成
    INPAINT = "inpaint"     # 局部替换


class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationModel(Base):
    """用户生成历史表"""
    __tablename__ = "generations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    
    # 生成类型
    generation_type = Column(SQLEnum(GenerationType), default=GenerationType.FULL)
    
    # 输入图片
    input_image_url = Column(String(512), nullable=False)
    input_thumbnail_url = Column(String(512))
    
    # 输出图片
    output_image_url = Column(String(512))
    output_thumbnail_url = Column(String(512))
    
    # 生成参数
    style = Column(String(64))
    room_type = Column(String(64))
    prompt = Column(Text)
    
    # 局部替换相关
    mask_url = Column(String(512))
    furniture_type = Column(String(128))
    
    # 状态和成本
    status = Column(SQLEnum(GenerationStatus), default=GenerationStatus.PENDING)
    processing_time = Column(Float, default=0)
    cost = Column(Float, default=0)
    error_message = Column(Text)
    
    # 用户交互
    is_favorite = Column(Integer, default=0)  # 是否收藏
    is_deleted = Column(Integer, default=0)   # 软删除
    
    # 时间
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_user_favorite', 'user_id', 'is_favorite'),
    )


@dataclass
class GenerationInfo:
    """生成记录DTO"""
    generation_id: str
    user_id: str
    generation_type: str
    input_image_url: str
    output_image_url: Optional[str]
    style: Optional[str]
    room_type: Optional[str]
    prompt: Optional[str]
    furniture_type: Optional[str]
    status: str
    processing_time: float
    cost: float
    is_favorite: bool
    created_at: datetime
    completed_at: Optional[datetime]


class GenerationService:
    """生成历史服务"""
    
    _table_created = False
    
    def _ensure_table(self):
        """延迟创建表"""
        if not GenerationService._table_created:
            try:
                GenerationModel.__table__.create(db_manager._engine, checkfirst=True)
                GenerationService._table_created = True
            except Exception:
                pass  # 表可能已存在
    
    def _to_info(self, record: GenerationModel) -> GenerationInfo:
        return GenerationInfo(
            generation_id=record.generation_id,
            user_id=record.user_id,
            generation_type=record.generation_type.value if record.generation_type else "full",
            input_image_url=record.input_image_url,
            output_image_url=record.output_image_url,
            style=record.style,
            room_type=record.room_type,
            prompt=record.prompt,
            furniture_type=record.furniture_type,
            status=record.status.value if record.status else "pending",
            processing_time=record.processing_time or 0,
            cost=record.cost or 0,
            is_favorite=bool(record.is_favorite),
            created_at=record.created_at,
            completed_at=record.completed_at
        )
    
    def save_generation(
        self,
        user_id: str,
        input_image_url: str,
        output_image_url: str,
        generation_type: str = "full",
        style: str = None,
        room_type: str = None,
        prompt: str = None,
        mask_url: str = None,
        furniture_type: str = None,
        processing_time: float = 0,
        cost: float = 0
    ) -> Tuple[Optional[GenerationInfo], Optional[str]]:
        """
        保存生成记录
        返回: (生成信息, 错误信息)
        """
        self._ensure_table()
        try:
            with db_manager.get_session() as session:
                record = GenerationModel(
                    generation_id=f"GEN{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}",
                    user_id=user_id,
                    generation_type=GenerationType(generation_type) if generation_type in ["full", "inpaint"] else GenerationType.FULL,
                    input_image_url=input_image_url,
                    output_image_url=output_image_url,
                    style=style,
                    room_type=room_type,
                    prompt=prompt,
                    mask_url=mask_url,
                    furniture_type=furniture_type,
                    status=GenerationStatus.COMPLETED,
                    processing_time=processing_time,
                    cost=cost,
                    created_at=datetime.now(),
                    completed_at=datetime.now()
                )
                
                session.add(record)
                session.commit()
                session.refresh(record)
                
                return self._to_info(record), None
        except Exception as e:
            return None, str(e)
    
    def get_user_generations(
        self,
        user_id: str,
        generation_type: str = None,
        favorites_only: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> List[GenerationInfo]:
        """获取用户生成历史"""
        self._ensure_table()
        with db_manager.get_session() as session:
            query = session.query(GenerationModel).filter(
                GenerationModel.user_id == user_id,
                GenerationModel.is_deleted == 0
            )
            
            if generation_type:
                query = query.filter(GenerationModel.generation_type == generation_type)
            
            if favorites_only:
                query = query.filter(GenerationModel.is_favorite == 1)
            
            records = query.order_by(GenerationModel.created_at.desc()).offset(offset).limit(limit).all()
            
            return [self._to_info(r) for r in records]
    
    def get_generation(self, generation_id: str, user_id: str = None) -> Optional[GenerationInfo]:
        """获取单个生成记录"""
        self._ensure_table()
        with db_manager.get_session() as session:
            query = session.query(GenerationModel).filter(
                GenerationModel.generation_id == generation_id
            )
            
            if user_id:
                query = query.filter(GenerationModel.user_id == user_id)
            
            record = query.first()
            if not record:
                return None
            
            return self._to_info(record)
    
    def toggle_favorite(self, generation_id: str, user_id: str) -> Tuple[bool, str]:
        """切换收藏状态"""
        self._ensure_table()
        with db_manager.get_session() as session:
            record = session.query(GenerationModel).filter(
                GenerationModel.generation_id == generation_id,
                GenerationModel.user_id == user_id
            ).first()
            
            if not record:
                return False, "记录不存在"
            
            record.is_favorite = 0 if record.is_favorite else 1
            session.commit()
            
            return True, "已收藏" if record.is_favorite else "已取消收藏"
    
    def delete_generation(self, generation_id: str, user_id: str) -> Tuple[bool, str]:
        """软删除生成记录"""
        self._ensure_table()
        with db_manager.get_session() as session:
            record = session.query(GenerationModel).filter(
                GenerationModel.generation_id == generation_id,
                GenerationModel.user_id == user_id
            ).first()
            
            if not record:
                return False, "记录不存在"
            
            record.is_deleted = 1
            session.commit()
            
            return True, "已删除"
    
    def get_user_stats(self, user_id: str) -> dict:
        """获取用户生成统计"""
        self._ensure_table()
        with db_manager.get_session() as session:
            from sqlalchemy import func
            
            total = session.query(func.count(GenerationModel.id)).filter(
                GenerationModel.user_id == user_id,
                GenerationModel.is_deleted == 0
            ).scalar() or 0
            
            favorites = session.query(func.count(GenerationModel.id)).filter(
                GenerationModel.user_id == user_id,
                GenerationModel.is_favorite == 1,
                GenerationModel.is_deleted == 0
            ).scalar() or 0
            
            total_cost = session.query(func.sum(GenerationModel.cost)).filter(
                GenerationModel.user_id == user_id,
                GenerationModel.is_deleted == 0
            ).scalar() or 0
            
            return {
                "total_generations": total,
                "favorites_count": favorites,
                "total_cost": round(total_cost, 2)
            }


# 全局服务实例
generation_service = GenerationService()
