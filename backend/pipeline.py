"""
NanoBanana AI - Baseline Pipeline
核心流程: 上传图片 → AI生成 → 返回结果

支持 Grsai Nano Banana API (推荐) 和 Replicate API
"""
import os
import uuid
import time
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class PipelineResult:
    """Pipeline执行结果"""
    success: bool
    task_id: str = None
    preview_images: list = None  # 预览图(带水印/低清)
    hd_images: list = None       # 高清图(付费后)
    processing_time: float = 0
    cost_rmb: float = 0          # 成本(人民币)
    error: str = None

class NanoBananaPipeline:
    """
    Baseline Pipeline - 最小可行流程
    
    流程:
    1. 接收毛胚房图片URL
    2. [可选] 自动识别房间类型
    3. 调用AI API生成效果图 (Grsai或Replicate)
    4. 返回结果(带水印预览)
    """
    
    def __init__(self, provider: str = None, api_key: str = None):
        # 支持的 provider: grsai, replicate, controlnet (推荐，保持结构)
        self.provider = provider or os.getenv("AI_PROVIDER", "controlnet")
        self.api_key = api_key
        
        if self.provider == "grsai":
            self.api_key = api_key or os.getenv("GRSAI_API_KEY")
        else:
            self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        
    def run(
        self,
        image_url: str,
        room_type: str = "living_room",
        style: str = "nanobanana",
        num_outputs: int = 4
    ) -> PipelineResult:
        """
        执行生成流程
        
        Args:
            image_url: 毛胚房图片URL (必须是可公开访问的URL)
            room_type: 房间类型
            style: 风格 (nanobanana, nanobanana_A, nanobanana_B, nanobanana_C)
            num_outputs: 生成数量 (1-4)
            
        Returns:
            PipelineResult
        """
        task_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        print(f"[{task_id}] Starting pipeline...")
        print(f"[{task_id}] Image: {image_url}")
        print(f"[{task_id}] Room: {room_type}, Style: {style}")
        
        try:
            # Step 1: 调用AI服务
            if self.provider == "grsai":
                result = self._call_grsai(image_url, room_type, style)
            elif self.provider == "controlnet":
                result = self._call_controlnet(image_url, style)
            else:
                result = self._call_replicate(image_url, style, num_outputs)
            
            if not result.success:
                return PipelineResult(
                    success=False,
                    task_id=task_id,
                    error=result.error,
                    processing_time=time.time() - start_time
                )
            
            # Step 2: 处理结果
            print(f"[{task_id}] Generation completed! Got {len(result.images)} images")
            
            processing_time = time.time() - start_time
            
            return PipelineResult(
                success=True,
                task_id=task_id,
                preview_images=result.images,  # baseline先不加水印
                hd_images=result.images,
                processing_time=processing_time,
                cost_rmb=result.cost
            )
            
        except Exception as e:
            return PipelineResult(
                success=False,
                task_id=task_id,
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def _call_grsai(self, image_url: str, room_type: str, style: str):
        """调用Grsai Nano Banana API"""
        from services.grsai_service import GrsaiNanoBananaServiceSync
        
        # 房间类型中文映射
        room_names = {
            "living_room": "客厅",
            "bedroom": "卧室",
            "master_bedroom": "主卧",
            "kitchen": "厨房",
            "bathroom": "卫生间",
            "dining_room": "餐厅",
            "study": "书房",
            "balcony": "阳台"
        }
        room_name = room_names.get(room_type, "房间")
        
        print(f"[Grsai] Calling Nano Banana API...")
        service = GrsaiNanoBananaServiceSync(api_key=self.api_key)
        
        prompt = f"将这个毛胚房装修成精美的{room_name}，专业室内设计效果图"
        result = service.generate(
            prompt=prompt,
            image_url=image_url,
            style=style,
            room_type=room_type,  # 传递房间类型以使用专业prompt库
            model="nano-banana-pro"
        )
        return result
    
    def _call_replicate(self, image_url: str, style: str, num_outputs: int):
        """调用Replicate API"""
        from services.ai_service import ReplicateAIServiceSync
        
        print(f"[Replicate] Calling API...")
        service = ReplicateAIServiceSync(api_token=self.api_key)
        return service.generate(
            image_url=image_url,
            style=style,
            num_outputs=num_outputs
        )

def test_pipeline():
    """测试Pipeline"""
    # 使用一张公开的毛胚房测试图片
    test_image = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"
    
    print("=" * 50)
    print("NanoBanana Pipeline Test")
    print("=" * 50)
    
    pipeline = NanoBananaPipeline()
    result = pipeline.run(
        image_url=test_image,
        room_type="living_room",
        style="nanobanana",
        num_outputs=2  # 测试只生成2张
    )
    
    print("\n" + "=" * 50)
    print("Result:")
    print(f"  Success: {result.success}")
    print(f"  Task ID: {result.task_id}")
    print(f"  Time: {result.processing_time:.1f}s")
    print(f"  Cost: ${result.cost_usd:.4f}")
    
    if result.success:
        print(f"  Images: {len(result.preview_images)}")
        for i, img in enumerate(result.preview_images):
            print(f"    [{i+1}] {img}")
    else:
        print(f"  Error: {result.error}")
    
    print("=" * 50)
    return result

if __name__ == "__main__":
    test_pipeline()
