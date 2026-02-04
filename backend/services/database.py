"""
数据库连接管理
安全的连接池和会话管理
"""
import os
from contextlib import contextmanager
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# 共享的Base，所有模型都应该继承这个
Base = declarative_base()


class DatabaseManager:
    """数据库连接管理器"""
    
    _instance = None
    _engine = None
    _SessionLocal = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def init(self, database_url: str = None):
        """初始化数据库连接"""
        if self._engine is not None:
            return
        
        if database_url is None:
            # 默认使用SQLite（无需安装）
            db_type = os.getenv("DB_TYPE", "sqlite")
            
            if db_type == "mysql":
                db_host = os.getenv("DB_HOST", "localhost")
                db_port = os.getenv("DB_PORT", "3306")
                db_user = os.getenv("DB_USER", "root")
                db_password = os.getenv("DB_PASSWORD", "")
                db_name = os.getenv("DB_NAME", "nanobanana")
                database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            else:
                # SQLite - 数据存储在本地文件
                db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "app.db")
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                database_url = f"sqlite:///{db_path}"
        
        # 创建引擎
        if "sqlite" in database_url:
            # SQLite配置
            self._engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},  # SQLite多线程支持
                echo=os.getenv("DB_ECHO", "false").lower() == "true"
            )
        else:
            # MySQL配置，使用连接池
            self._engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True,
                echo=os.getenv("DB_ECHO", "false").lower() == "true"
            )
        
        self._SessionLocal = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False
        )
    
    @contextmanager
    def get_session(self):
        """获取数据库会话（上下文管理器）"""
        if self._SessionLocal is None:
            self.init()
        
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_engine(self):
        """获取数据库引擎"""
        if self._engine is None:
            self.init()
        return self._engine
    
    def create_tables(self, base):
        """创建所有表"""
        if self._engine is None:
            self.init()
        base.metadata.create_all(self._engine)


# 全局数据库管理器实例
db_manager = DatabaseManager()


def get_db():
    """FastAPI 依赖注入用"""
    with db_manager.get_session() as session:
        yield session
