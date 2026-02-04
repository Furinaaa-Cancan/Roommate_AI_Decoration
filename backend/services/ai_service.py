"""
AI生成服务 - 调用Replicate API
Replicate stable-interiors-v2: ~$0.015/次 (66次/$1)
"""
import os
import time
import uuid
import httpx
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class GenerationResult:
    success: bool
    images: List[str] = None  # 图片URL列表
    request_id: str = None
    cost: float = 0.0
    error: str = None
    elapsed_seconds: float = 0.0

class ReplicateAIService:
    """
    Replicate API 服务
    模型: youzu/stable-interiors-v2
    成本: ~$0.015/次
    """
    
    BASE_URL = "https://api.replicate.com/v1"
    MODEL = "youzu/stable-interiors-v2"
    COST_PER_RUN = 0.015  # USD
    
    # NanoBanana 风格Prompt模板
    STYLE_PROMPTS = {
        "nanobanana": {
            "prompt": "modern minimalist interior design, warm neutral tones, cream and beige palette, natural wood accents, soft lighting, cozy atmosphere, high-end furniture, professional interior photography, 8k, ultra detailed",
            "negative_prompt": "ugly, blurry, low quality, distorted, watermark, text, logo, cartoon, anime, sketch, drawing"
        },
        "nanobanana_A": {
            "prompt": "modern minimalist interior, cream white walls, light oak wood flooring, beige fabric sofa, warm ambient lighting, scandinavian style, clean lines, professional photography, 8k",
            "negative_prompt": "ugly, blurry, low quality, distorted, watermark, cluttered"
        },
        "nanobanana_B": {
            "prompt": "contemporary interior design, warm grey tones, walnut wood elements, velvet textures, golden accents, sophisticated elegance, luxury feel, professional interior photography, 8k",
            "negative_prompt": "ugly, blurry, low quality, distorted, watermark, cheap looking"
        },
        "nanobanana_C": {
            "prompt": "japandi interior style, natural materials, muted earth tones, wabi-sabi aesthetic, organic shapes, zen atmosphere, minimalist furniture, professional photography, 8k",
            "negative_prompt": "ugly, blurry, low quality, distorted, watermark, busy, cluttered"
        }
    }
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def generate(
        self,
        image_url: str,
        style: str = "nanobanana",
        num_outputs: int = 4,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50
    ) -> GenerationResult:
        """
        生成室内设计效果图
        
        Args:
            image_url: 毛胚房原图URL
            style: 风格 (nanobanana, nanobanana_A, nanobanana_B, nanobanana_C)
            num_outputs: 生成图片数量 (1-4)
            guidance_scale: 引导强度
            num_inference_steps: 推理步数
        
        Returns:
            GenerationResult
        """
        start_time = time.time()
        
        # 获取风格prompt
        style_config = self.STYLE_PROMPTS.get(style, self.STYLE_PROMPTS["nanobanana"])
        
        # 构建请求
        payload = {
            "version": "latest",
            "input": {
                "image": image_url,
                "prompt": style_config["prompt"],
                "negative_prompt": style_config["negative_prompt"],
                "num_outputs": min(num_outputs, 4),
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
                "width": 1024,
                "height": 1024
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                # 创建预测
                response = await client.post(
                    f"{self.BASE_URL}/models/{self.MODEL}/predictions",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                prediction = response.json()
                prediction_id = prediction["id"]
                
                # 轮询等待结果
                images = await self._poll_prediction(client, prediction_id)
                
                elapsed = time.time() - start_time
                return GenerationResult(
                    success=True,
                    images=images,
                    request_id=prediction_id,
                    cost=self.COST_PER_RUN * num_outputs,
                    elapsed_seconds=elapsed
                )
                
        except Exception as e:
            elapsed = time.time() - start_time
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=elapsed
            )
    
    async def _poll_prediction(
        self, 
        client: httpx.AsyncClient, 
        prediction_id: str,
        max_wait: int = 120,
        poll_interval: float = 2.0
    ) -> List[str]:
        """轮询等待预测完成"""
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        waited = 0
        
        while waited < max_wait:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            status = result.get("status")
            
            if status == "succeeded":
                return result.get("output", [])
            elif status == "failed":
                raise Exception(f"Prediction failed: {result.get('error')}")
            elif status == "canceled":
                raise Exception("Prediction was canceled")
            
            await asyncio.sleep(poll_interval)
            waited += poll_interval
        
        raise Exception(f"Prediction timed out after {max_wait}s")

# 同步版本（方便测试）
class ReplicateAIServiceSync:
    """同步版本的AI服务"""
    
    BASE_URL = "https://api.replicate.com/v1"
    MODEL = "youzu/stable-interiors-v2"
    COST_PER_RUN = 0.015
    
    STYLE_PROMPTS = ReplicateAIService.STYLE_PROMPTS
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def generate(
        self,
        image_url: str,
        style: str = "nanobanana",
        num_outputs: int = 4
    ) -> GenerationResult:
        """同步生成"""
        import requests
        
        start_time = time.time()
        style_config = self.STYLE_PROMPTS.get(style, self.STYLE_PROMPTS["nanobanana"])
        
        payload = {
            "version": "latest",
            "input": {
                "image": image_url,
                "prompt": style_config["prompt"],
                "negative_prompt": style_config["negative_prompt"],
                "num_outputs": min(num_outputs, 4),
                "width": 1024,
                "height": 1024
            }
        }
        
        try:
            # 创建预测
            resp = requests.post(
                f"{self.BASE_URL}/models/{self.MODEL}/predictions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            prediction = resp.json()
            prediction_id = prediction["id"]
            
            # 轮询
            images = self._poll_prediction(prediction_id)
            
            elapsed = time.time() - start_time
            return GenerationResult(
                success=True,
                images=images,
                request_id=prediction_id,
                cost=self.COST_PER_RUN * num_outputs,
                elapsed_seconds=elapsed
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_prediction(self, prediction_id: str, max_wait: int = 120) -> List[str]:
        import requests
        import time as t
        
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        waited = 0
        
        while waited < max_wait:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            if result["status"] == "succeeded":
                return result.get("output", [])
            elif result["status"] in ("failed", "canceled"):
                raise Exception(f"Prediction {result['status']}")
            
            t.sleep(2)
            waited += 2
        
        raise Exception("Timeout")

import asyncio  # 放在文件末尾避免循环导入
