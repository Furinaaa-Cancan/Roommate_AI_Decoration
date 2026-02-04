"""
NanoBanana AI 配置文件
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "3306"))
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "nanobanana")
    
    @property
    def url(self) -> str:
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class OSSConfig:
    endpoint: str = os.getenv("OSS_ENDPOINT", "")
    access_key: str = os.getenv("OSS_ACCESS_KEY", "")
    secret_key: str = os.getenv("OSS_SECRET_KEY", "")
    bucket: str = os.getenv("OSS_BUCKET", "nanobanana")
    
@dataclass
class AIConfig:
    """AI API 配置"""
    provider: str = os.getenv("AI_PROVIDER", "grsai")  # grsai 或 replicate
    
    # Grsai Nano Banana 配置 - ¥0.18/张，推荐
    grsai_api_key: str = os.getenv("GRSAI_API_KEY", "")
    grsai_model: str = os.getenv("GRSAI_MODEL", "nano-banana-pro")
    grsai_use_china_host: bool = os.getenv("GRSAI_USE_CHINA_HOST", "true").lower() == "true"
    
    # Replicate配置 - $0.015/次，备用
    replicate_api_token: str = os.getenv("REPLICATE_API_TOKEN", "")
    replicate_model: str = os.getenv("REPLICATE_MODEL", "youzu/stable-interiors-v2")
    
    # 备用: RunPod Serverless
    runpod_api_key: str = os.getenv("RUNPOD_API_KEY", "")
    runpod_endpoint: str = os.getenv("RUNPOD_ENDPOINT", "")

@dataclass
class Config:
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    db: DatabaseConfig = None
    oss: OSSConfig = None
    ai: AIConfig = None
    
    def __post_init__(self):
        self.db = DatabaseConfig()
        self.oss = OSSConfig()
        self.ai = AIConfig()

# 全局配置实例
config = Config()
