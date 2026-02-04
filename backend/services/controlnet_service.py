"""
ControlNet 室内设计服务 - 保持房间结构布局

使用 Replicate adirik/interior-design 模型
- 技术: MLSD ControlNet + Inpainting
- 价格: ~$0.006/次 (约 ¥0.04/次)
- 速度: ~7秒
- 特点: 保持房间直线结构（墙壁、窗户、门框等）
"""
import os
import time
import httpx
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ControlNetResult:
    """生成结果"""
    success: bool
    images: List[str] = None
    request_id: str = None
    cost: float = 0.0
    error: str = None
    elapsed_seconds: float = 0.0


class ControlNetInteriorService:
    """
    使用 ControlNet MLSD 保持房间结构的室内设计服务
    
    模型: adirik/interior-design
    - 结合 Realistic Vision V3.0 inpainting + MLSD ControlNet
    - 专门为空房间→装修设计优化
    - 保持墙壁、窗户、门等直线结构
    """
    
    BASE_URL = "https://api.replicate.com/v1"
    MODEL = "adirik/interior-design"
    MODEL_VERSION = "76604baddc85b1b4616e1c6475eca080da339c8875bd4996705440484a6eac38"
    COST_PER_RUN = 0.006  # USD
    
    # 风格 Prompt 模板
    STYLE_PROMPTS = {
        "nanobanana": {
            "prompt": "modern minimalist interior design, warm neutral tones, cream and beige palette, natural wood accents, soft ambient lighting, cozy atmosphere, high-end designer furniture, professional interior photography, 8k ultra detailed, magazine quality",
            "negative_prompt": "ugly, blurry, low quality, distorted, watermark, text, cartoon, anime, sketch, people, person"
        },
        "现代简约": {
            "prompt": "modern minimalist interior, clean lines, neutral colors, simple elegant furniture, open space, natural light, white walls, wooden floor, professional photography",
            "negative_prompt": "cluttered, ornate, traditional, busy patterns, low quality"
        },
        "北欧风": {
            "prompt": "scandinavian interior design, bright airy space, white walls, light wood flooring, cozy textiles, indoor plants, hygge atmosphere, natural materials, soft lighting",
            "negative_prompt": "dark colors, heavy furniture, ornate details, cluttered"
        },
        "侘寂风": {
            "prompt": "wabi-sabi interior design, japanese aesthetics, natural imperfect materials, earth tones, minimal decoration, zen atmosphere, organic textures, soft diffused light",
            "negative_prompt": "bright colors, modern tech, plastic materials, cluttered"
        },
        "新中式": {
            "prompt": "modern chinese interior design, traditional elements with contemporary style, dark wood furniture, subtle patterns, elegant screens, ink painting decoration, zen atmosphere",
            "negative_prompt": "western style, industrial, colorful, cheap looking"
        },
        "轻奢": {
            "prompt": "light luxury interior design, elegant marble surfaces, gold accents, velvet textures, crystal chandelier, sophisticated atmosphere, high-end materials",
            "negative_prompt": "cheap materials, industrial, rustic, cluttered"
        },
        "工业风": {
            "prompt": "industrial interior design, exposed brick walls, metal pipes, concrete floor, Edison bulbs, urban loft style, raw materials, vintage furniture",
            "negative_prompt": "traditional, ornate, soft textures, pastel colors"
        },
        "日式": {
            "prompt": "japanese interior design, tatami flooring, shoji screens, natural wood, zen garden view, minimalist furniture, peaceful atmosphere, soft natural light",
            "negative_prompt": "western furniture, bright colors, cluttered, heavy furniture"
        },
        "法式": {
            "prompt": "french interior design, elegant crown moldings, crystal chandelier, parquet floors, romantic atmosphere, luxurious fabrics, antique furniture, soft pastel colors",
            "negative_prompt": "modern, industrial, minimal, cheap looking"
        },
    }
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Prefer": "wait"  # 同步等待结果
        }
    
    def generate(
        self,
        image_url: str,
        style: str = "nanobanana",
        custom_prompt: str = None,
        prompt_strength: float = 0.8,
        guidance_scale: float = 15.0,
        num_inference_steps: int = 50,
        seed: int = None,
    ) -> ControlNetResult:
        """
        生成室内设计效果图（保持房间结构）
        
        Args:
            image_url: 毛胚房原图URL（必须是公开可访问的URL）
            style: 风格名称
            custom_prompt: 自定义提示词（会追加到风格prompt后）
            prompt_strength: 提示词强度 (0-1)，越高变化越大，但可能影响结构保持
            guidance_scale: 引导强度，推荐 12-20
            num_inference_steps: 推理步数，推荐 40-60
            seed: 随机种子，用于复现结果
        
        Returns:
            ControlNetResult
        """
        import requests
        
        start_time = time.time()
        
        # 获取风格配置
        style_config = self.STYLE_PROMPTS.get(style, self.STYLE_PROMPTS["nanobanana"])
        
        # 构建完整 prompt
        prompt = style_config["prompt"]
        if custom_prompt:
            prompt = f"{prompt}, {custom_prompt}"
        
        # 构建请求
        payload = {
            "version": self.MODEL_VERSION,
            "input": {
                "image": image_url,
                "prompt": prompt,
                "negative_prompt": style_config["negative_prompt"],
                "prompt_strength": prompt_strength,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
            }
        }
        
        if seed is not None:
            payload["input"]["seed"] = seed
        
        try:
            # 发送请求
            resp = requests.post(
                f"{self.BASE_URL}/predictions",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            result = resp.json()
            
            # 检查状态
            if result.get("status") == "succeeded":
                output = result.get("output")
                images = [output] if isinstance(output, str) else output
                
                elapsed = time.time() - start_time
                return ControlNetResult(
                    success=True,
                    images=images,
                    request_id=result.get("id"),
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=elapsed
                )
            elif result.get("status") == "failed":
                return ControlNetResult(
                    success=False,
                    error=result.get("error", "Generation failed"),
                    elapsed_seconds=time.time() - start_time
                )
            else:
                # 需要轮询
                return self._poll_result(result.get("id"))
                
        except Exception as e:
            return ControlNetResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_result(self, prediction_id: str, max_wait: float = 120) -> ControlNetResult:
        """轮询等待结果"""
        import requests
        
        start_time = time.time()
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        
        while (time.time() - start_time) < max_wait:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            status = result.get("status")
            
            if status == "succeeded":
                output = result.get("output")
                images = [output] if isinstance(output, str) else output
                return ControlNetResult(
                    success=True,
                    images=images,
                    request_id=prediction_id,
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=time.time() - start_time
                )
            elif status in ("failed", "canceled"):
                return ControlNetResult(
                    success=False,
                    error=result.get("error", f"Prediction {status}"),
                    elapsed_seconds=time.time() - start_time
                )
            
            time.sleep(2)
        
        return ControlNetResult(
            success=False,
            error=f"Timeout after {max_wait}s",
            elapsed_seconds=time.time() - start_time
        )
    
    def generate_with_structure_control(
        self,
        image_url: str,
        style: str = "nanobanana",
        structure_strength: str = "high",
    ) -> ControlNetResult:
        """
        便捷方法：根据结构保持强度自动调整参数
        
        Args:
            image_url: 毛胚房图片URL
            style: 风格名称
            structure_strength: 结构保持强度
                - "high": 严格保持原始布局（prompt_strength=0.6）
                - "medium": 平衡模式（prompt_strength=0.75）
                - "low": 允许更多变化（prompt_strength=0.9）
        """
        strength_config = {
            "high": {"prompt_strength": 0.6, "guidance_scale": 12},
            "medium": {"prompt_strength": 0.75, "guidance_scale": 15},
            "low": {"prompt_strength": 0.9, "guidance_scale": 18},
        }
        
        config = strength_config.get(structure_strength, strength_config["high"])
        
        return self.generate(
            image_url=image_url,
            style=style,
            prompt_strength=config["prompt_strength"],
            guidance_scale=config["guidance_scale"],
        )


# 测试代码
if __name__ == "__main__":
    # 需要设置环境变量 REPLICATE_API_TOKEN
    service = ControlNetInteriorService()
    
    # 测试图片
    test_image = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"
    
    print("=" * 50)
    print("ControlNet Interior Design Test")
    print("=" * 50)
    
    result = service.generate_with_structure_control(
        image_url=test_image,
        style="nanobanana",
        structure_strength="high"  # 严格保持结构
    )
    
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   图片: {result.images}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        print(f"   成本: ${result.cost}")
    else:
        print(f"❌ 生成失败: {result.error}")
