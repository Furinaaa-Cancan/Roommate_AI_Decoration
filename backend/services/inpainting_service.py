"""
局部重绘服务 - Inpainting

使用 mask 对图片指定区域进行 AI 重绘，保持其他区域不变
"""
import os
import time
import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class InpaintingResult:
    """重绘结果"""
    success: bool
    image_url: str = None
    request_id: str = None
    cost: float = 0.0
    error: str = None
    elapsed_seconds: float = 0.0


class InpaintingService:
    """
    局部重绘服务
    
    使用 Replicate stability-ai/stable-diffusion-inpainting 或类似模型
    对指定 mask 区域进行重绘
    """
    
    BASE_URL = "https://api.replicate.com/v1"
    # 使用 stability-ai 的 inpainting 模型
    MODEL = "stability-ai/stable-diffusion-inpainting"
    MODEL_VERSION = "c11bac58203367db93f3c552c2c405b8e3de03879793c0c7626ce9d0ca62c8bc"
    COST_PER_RUN = 0.008
    
    # 室内设计重绘风格
    INPAINT_STYLES = {
        "现代简约": {
            "prompt": "modern minimalist furniture, clean lines, neutral colors, simple elegant design, professional interior photography",
            "negative": "cluttered, ornate, low quality, blurry"
        },
        "北欧风": {
            "prompt": "scandinavian furniture, light wood, white and pastel colors, cozy minimal design, natural materials",
            "negative": "dark colors, heavy ornate furniture, cluttered"
        },
        "轻奢": {
            "prompt": "luxury furniture, velvet fabric, gold accents, elegant sophisticated design, high-end materials",
            "negative": "cheap looking, plastic, cluttered"
        },
        "日式": {
            "prompt": "japanese style furniture, natural wood, zen minimalist design, tatami elements, peaceful atmosphere",
            "negative": "western style, colorful, cluttered"
        },
        "工业风": {
            "prompt": "industrial style furniture, metal and leather, exposed materials, urban loft design, vintage elements",
            "negative": "traditional, ornate, pastel colors"
        },
        "新中式": {
            "prompt": "modern chinese furniture, dark wood, traditional patterns with contemporary design, zen atmosphere",
            "negative": "western style, cheap looking, cluttered"
        },
    }
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Prefer": "wait"
        }
    
    def inpaint(
        self,
        image_url: str,
        mask_url: str,
        style: str = "现代简约",
        custom_prompt: str = None,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
    ) -> InpaintingResult:
        """
        对图片指定区域进行重绘
        
        Args:
            image_url: 原图 URL
            mask_url: mask 图片 URL（白色区域将被重绘）
            style: 重绘风格
            custom_prompt: 自定义提示词
            guidance_scale: 引导强度
            num_inference_steps: 推理步数
        
        Returns:
            InpaintingResult
        """
        start_time = time.time()
        
        # 获取风格配置
        style_config = self.INPAINT_STYLES.get(style, self.INPAINT_STYLES["现代简约"])
        
        # 构建 prompt
        prompt = style_config["prompt"]
        if custom_prompt:
            prompt = f"{prompt}, {custom_prompt}"
        
        payload = {
            "version": self.MODEL_VERSION,
            "input": {
                "image": image_url,
                "mask": mask_url,
                "prompt": prompt,
                "negative_prompt": style_config["negative"],
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
            }
        }
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/predictions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            result = resp.json()
            
            if result.get("status") == "succeeded":
                output = result.get("output")
                image_url = output[0] if isinstance(output, list) else output
                
                return InpaintingResult(
                    success=True,
                    image_url=image_url,
                    request_id=result.get("id"),
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=time.time() - start_time
                )
            elif result.get("status") == "failed":
                return InpaintingResult(
                    success=False,
                    error=result.get("error", "Inpainting failed"),
                    elapsed_seconds=time.time() - start_time
                )
            else:
                return self._poll_result(result.get("id"), start_time)
                
        except Exception as e:
            return InpaintingResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_result(self, prediction_id: str, start_time: float, max_wait: float = 120) -> InpaintingResult:
        """轮询等待结果"""
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        
        while (time.time() - start_time) < max_wait:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            status = result.get("status")
            
            if status == "succeeded":
                output = result.get("output")
                image_url = output[0] if isinstance(output, list) else output
                
                return InpaintingResult(
                    success=True,
                    image_url=image_url,
                    request_id=prediction_id,
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=time.time() - start_time
                )
            elif status in ("failed", "canceled"):
                return InpaintingResult(
                    success=False,
                    error=result.get("error", f"Prediction {status}"),
                    elapsed_seconds=time.time() - start_time
                )
            
            time.sleep(2)
        
        return InpaintingResult(
            success=False,
            error=f"Timeout after {max_wait}s",
            elapsed_seconds=time.time() - start_time
        )


# 测试
if __name__ == "__main__":
    service = InpaintingService()
    
    # 测试需要真实的图片和 mask URL
    print("InpaintingService initialized successfully")
    print("Available styles:", list(service.INPAINT_STYLES.keys()))
