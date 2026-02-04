"""
订单服务
支持个人收款码的半自动支付流程
"""
import os
import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum

from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Enum as SQLEnum, DECIMAL, Text, Index

from services.database import db_manager, Base
from services.secure_auth_service import secure_auth_service


class OrderStatus(str, Enum):
    PENDING = "pending"        # 待支付
    SUBMITTED = "submitted"    # 已提交待审核
    PAID = "paid"              # 已支付
    REJECTED = "rejected"      # 已驳回
    EXPIRED = "expired"        # 已过期
    CANCELLED = "cancelled"    # 已取消


class ProductType(str, Enum):
    MEMBERSHIP = "membership"  # 会员
    CREDITS = "credits"        # 积分包


class PayMethod(str, Enum):
    WECHAT = "wechat"
    ALIPAY = "alipay"


# 商品价格表（后端定义，不信任前端）
# 注意：ID必须与前端billing页面一致
PRODUCT_CATALOG = {
    "membership": {
        "personal": {"name": "个人版会员", "price": Decimal("39.00"), "credits": 50},
        "designer": {"name": "设计师版会员", "price": Decimal("99.00"), "credits": 200},
        "enterprise": {"name": "企业版会员", "price": Decimal("299.00"), "credits": 800},
    },
    "credits": {
        "pack_10": {"name": "10次生成", "price": Decimal("9.90"), "credits": 10},
        "pack_40": {"name": "40次生成", "price": Decimal("29.00"), "credits": 40},
        "pack_100": {"name": "100次生成", "price": Decimal("59.00"), "credits": 100},
        "pack_400": {"name": "400次生成", "price": Decimal("199.00"), "credits": 400},
    }
}


class OrderModel(Base):
    """订单数据库模型"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # SQLite需要Integer而非BigInteger
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)  # 改为String支持Google OAuth长ID
    
    # 商品信息
    product_type = Column(SQLEnum(ProductType), nullable=False)
    product_id = Column(String(32), nullable=False)
    product_name = Column(String(64), nullable=False)
    base_amount = Column(DECIMAL(10, 2), nullable=False)  # 原价
    pay_amount = Column(DECIMAL(10, 2), nullable=False)   # 实付（含微调）
    price_code = Column(String(4), nullable=False)        # 价格尾数
    credits_to_add = Column(Integer, default=0)           # 要添加的积分
    
    # 支付信息
    pay_method = Column(SQLEnum(PayMethod))
    transaction_id = Column(String(64))
    
    # 状态
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    reject_reason = Column(String(255))
    
    # 时间
    expire_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    submitted_at = Column(DateTime)
    paid_at = Column(DateTime)
    
    # 备注
    admin_note = Column(Text)
    
    # 复合索引：用于查找价格碰撞
    __table_args__ = (
        Index('idx_pending_amount', 'status', 'pay_amount', 'expire_at'),
    )


@dataclass
class OrderInfo:
    """订单信息DTO"""
    order_no: str
    user_id: str
    product_type: str
    product_id: str
    product_name: str
    base_amount: float
    pay_amount: float
    price_code: str
    pay_method: Optional[str]
    status: str
    expire_at: datetime
    expire_seconds: int
    created_at: datetime
    transaction_id: Optional[str] = None
    reject_reason: Optional[str] = None


class OrderService:
    """订单服务"""
    
    ORDER_EXPIRE_MINUTES = 15  # 订单有效期
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-this-admin-token-in-production")
    
    def __init__(self):
        db_manager.init()
        db_manager.create_tables(Base)
    
    def _generate_order_no(self) -> str:
        """生成订单号: ORD + 年月日时分秒 + 4位随机数"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = str(random.randint(1000, 9999))
        return f"ORD{timestamp}{random_suffix}"
    
    def _get_unique_pay_amount(
        self, 
        session, 
        base_amount: Decimal
    ) -> Tuple[Decimal, str]:
        """
        生成唯一的支付金额（防止碰撞）
        返回: (实付金额, 价格尾数)
        """
        for _ in range(20):  # 尝试20次
            suffix = random.randint(1, 99)
            price_code = str(suffix).zfill(2)
            pay_amount = base_amount + Decimal(f"0.{price_code}")
            
            # 检查是否有pending状态且未过期的订单使用了这个金额
            existing = session.query(OrderModel).filter(
                OrderModel.status == OrderStatus.PENDING,
                OrderModel.pay_amount == pay_amount,
                OrderModel.base_amount == base_amount,  # 同一商品价格
                OrderModel.expire_at > datetime.now()
            ).first()
            
            if not existing:
                return pay_amount, price_code
        
        # 如果20次都碰撞了，使用毫秒级时间戳
        ms = datetime.now().strftime("%f")[:2]
        return base_amount + Decimal(f"0.{ms}"), ms
    
    def _to_order_info(self, order: OrderModel) -> OrderInfo:
        """转换为OrderInfo"""
        now = datetime.now()
        expire_seconds = max(0, int((order.expire_at - now).total_seconds()))
        
        return OrderInfo(
            order_no=order.order_no,
            user_id=order.user_id,
            product_type=order.product_type.value,
            product_id=order.product_id,
            product_name=order.product_name,
            base_amount=float(order.base_amount),
            pay_amount=float(order.pay_amount),
            price_code=order.price_code,
            pay_method=order.pay_method.value if order.pay_method else None,
            status=order.status.value,
            expire_at=order.expire_at,
            expire_seconds=expire_seconds,
            created_at=order.created_at,
            transaction_id=order.transaction_id,
            reject_reason=order.reject_reason
        )
    
    def create_order(
        self,
        user_id: str,
        product_type: str,
        product_id: str,
        pay_method: str
    ) -> Tuple[Optional[OrderInfo], Optional[str]]:
        """
        创建订单
        返回: (订单信息, 错误信息)
        """
        # 验证商品
        if product_type not in PRODUCT_CATALOG:
            return None, "无效的商品类型"
        
        if product_id not in PRODUCT_CATALOG[product_type]:
            return None, "无效的商品"
        
        # 验证支付方式
        if pay_method not in [m.value for m in PayMethod]:
            return None, "无效的支付方式"
        
        product = PRODUCT_CATALOG[product_type][product_id]
        base_amount = product["price"]
        
        with db_manager.get_session() as session:
            # 检查是否有未完成的订单
            pending_order = session.query(OrderModel).filter(
                OrderModel.user_id == user_id,
                OrderModel.status == OrderStatus.PENDING,
                OrderModel.expire_at > datetime.now()
            ).first()
            
            if pending_order:
                # 如果商品相同，返回现有订单
                if pending_order.product_type.value == product_type and pending_order.product_id == product_id:
                    return self._to_order_info(pending_order), "existing"
                # 如果商品不同，自动取消旧订单
                pending_order.status = OrderStatus.CANCELLED
                session.commit()
            
            # 创建订单（价格保持原价，通过订单号+用户信息区分）
            order = OrderModel(
                order_no=self._generate_order_no(),
                user_id=user_id,
                product_type=ProductType(product_type),
                product_id=product_id,
                product_name=product["name"],
                base_amount=base_amount,
                pay_amount=base_amount,  # 实付金额=原价
                price_code="00",  # 不再使用价格微调
                credits_to_add=product["credits"],
                pay_method=PayMethod(pay_method),
                status=OrderStatus.PENDING,
                expire_at=datetime.now() + timedelta(minutes=self.ORDER_EXPIRE_MINUTES),
                created_at=datetime.now()
            )
            
            session.add(order)
            session.commit()
            session.refresh(order)
            
            return self._to_order_info(order), None
    
    def get_order(self, order_no: str, user_id: str = None) -> Optional[OrderInfo]:
        """
        获取订单详情
        如果指定user_id，则验证订单归属
        """
        with db_manager.get_session() as session:
            query = session.query(OrderModel).filter(OrderModel.order_no == order_no)
            
            if user_id is not None:
                query = query.filter(OrderModel.user_id == user_id)
            
            order = query.first()
            if not order:
                return None
            
            return self._to_order_info(order)
    
    def submit_order(
        self,
        order_no: str,
        user_id: str,
        transaction_id: str = None
    ) -> Tuple[bool, str]:
        """
        提交支付凭证
        返回: (是否成功, 消息)
        """
        with db_manager.get_session() as session:
            order = session.query(OrderModel).filter(
                OrderModel.order_no == order_no,
                OrderModel.user_id == user_id
            ).with_for_update().first()  # 加锁防止并发
            
            if not order:
                return False, "订单不存在"
            
            # 检查状态
            if order.status not in [OrderStatus.PENDING, OrderStatus.REJECTED]:
                if order.status == OrderStatus.SUBMITTED:
                    return False, "订单已提交，请等待审核"
                elif order.status == OrderStatus.PAID:
                    return False, "订单已支付"
                elif order.status == OrderStatus.EXPIRED:
                    return False, "订单已过期，请重新下单"
                elif order.status == OrderStatus.CANCELLED:
                    return False, "订单已取消"
                return False, "订单状态不允许提交"
            
            # 检查过期（submitted状态除外）
            if order.status == OrderStatus.PENDING and order.expire_at < datetime.now():
                order.status = OrderStatus.EXPIRED
                session.commit()
                return False, "订单已过期，请重新下单"
            
            # 更新订单
            order.status = OrderStatus.SUBMITTED
            order.transaction_id = transaction_id
            order.submitted_at = datetime.now()
            order.reject_reason = None  # 清除之前的驳回原因
            
            session.commit()
            return True, "订单已提交，我们将在1-24小时内确认"
    
    def cancel_order(self, order_no: str, user_id: str) -> Tuple[bool, str]:
        """取消订单"""
        with db_manager.get_session() as session:
            order = session.query(OrderModel).filter(
                OrderModel.order_no == order_no,
                OrderModel.user_id == user_id
            ).first()
            
            if not order:
                return False, "订单不存在"
            
            if order.status != OrderStatus.PENDING:
                return False, "只能取消待支付的订单"
            
            order.status = OrderStatus.CANCELLED
            session.commit()
            return True, "订单已取消"
    
    def get_user_orders(
        self, 
        user_id: str, 
        status: str = None,
        limit: int = 20
    ) -> List[OrderInfo]:
        """获取用户订单列表"""
        with db_manager.get_session() as session:
            query = session.query(OrderModel).filter(
                OrderModel.user_id == user_id
            )
            
            if status:
                query = query.filter(OrderModel.status == OrderStatus(status))
            
            orders = query.order_by(OrderModel.created_at.desc()).limit(limit).all()
            return [self._to_order_info(o) for o in orders]
    
    # ============ 管理员接口 ============
    
    def verify_admin_token(self, token: str) -> bool:
        """验证管理员Token"""
        return token == self.ADMIN_TOKEN
    
    def get_pending_orders(self, limit: int = 50) -> List[OrderInfo]:
        """获取待审核订单列表"""
        with db_manager.get_session() as session:
            orders = session.query(OrderModel).filter(
                OrderModel.status == OrderStatus.SUBMITTED
            ).order_by(OrderModel.submitted_at.asc()).limit(limit).all()
            
            return [self._to_order_info(o) for o in orders]
    
    def audit_order(
        self,
        order_no: str,
        action: str,  # "approve" or "reject"
        reason: str = None,
        admin_note: str = None
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        审核订单
        返回: (是否成功, 消息, 额外数据)
        """
        if action not in ["approve", "reject"]:
            return False, "无效的操作", None
        
        with db_manager.get_session() as session:
            order = session.query(OrderModel).filter(
                OrderModel.order_no == order_no
            ).with_for_update().first()
            
            if not order:
                return False, "订单不存在", None
            
            if order.status != OrderStatus.SUBMITTED:
                return False, f"订单状态为{order.status.value}，无法审核", None
            
            if action == "approve":
                # 确认支付
                order.status = OrderStatus.PAID
                order.paid_at = datetime.now()
                order.admin_note = admin_note
                
                # 给用户加积分
                user = secure_auth_service.add_credits(order.user_id, order.credits_to_add)
                
                # 如果是会员订单，更新用户会员类型
                membership_type = None
                if order.product_type == ProductType.MEMBERSHIP:
                    membership_type = order.product_id  # personal/designer/enterprise
                    secure_auth_service.update_membership(order.user_id, membership_type)
                
                session.commit()
                
                msg = f"已确认，用户已获得{order.credits_to_add}积分"
                if membership_type:
                    msg += f"，会员等级已升级为{membership_type}"
                
                return True, msg, {
                    "user_id": order.user_id,
                    "credits_added": order.credits_to_add,
                    "user_credits": user.credits if user else 0,
                    "membership_type": membership_type
                }
            
            else:  # reject
                if not reason:
                    return False, "驳回必须填写原因", None
                
                order.status = OrderStatus.REJECTED
                order.reject_reason = reason
                order.admin_note = admin_note
                
                session.commit()
                return True, "已驳回，用户可重新提交", None
    
    def expire_pending_orders(self) -> int:
        """
        过期处理（定时任务调用）
        只处理pending状态的订单，submitted状态不处理
        返回: 处理的订单数
        """
        with db_manager.get_session() as session:
            result = session.query(OrderModel).filter(
                OrderModel.status == OrderStatus.PENDING,
                OrderModel.expire_at < datetime.now()
            ).update({
                "status": OrderStatus.EXPIRED,
                "updated_at": datetime.now()
            })
            
            session.commit()
            return result
    
    def force_approve_order(
        self,
        order_no: str,
        admin_note: str = None
    ) -> Tuple[bool, str]:
        """
        强制确认订单（用于处理用户付错金额的情况）
        可以确认expired状态的订单
        """
        with db_manager.get_session() as session:
            order = session.query(OrderModel).filter(
                OrderModel.order_no == order_no
            ).with_for_update().first()
            
            if not order:
                return False, "订单不存在"
            
            if order.status == OrderStatus.PAID:
                return False, "订单已支付"
            
            # 确认支付
            order.status = OrderStatus.PAID
            order.paid_at = datetime.now()
            order.admin_note = admin_note or "管理员强制确认"
            
            # 给用户加积分
            secure_auth_service.add_credits(order.user_id, order.credits_to_add)
            
            session.commit()
            return True, f"已强制确认，用户已获得{order.credits_to_add}积分"


# 全局订单服务实例
order_service = OrderService()
