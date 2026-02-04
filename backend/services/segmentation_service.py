"""
图像分割服务 - 基于 Grounded SAM

使用 Replicate schananas/grounded_sam 模型
- 功能: 文字标签识别 + SAM 分割
- 用途: 识别室内家具并生成 mask，支持局部替换
- 价格: ~$0.05/次
"""
import os
import time
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class SegmentedObject:
    """分割出的单个对象"""
    label: str           # 标签名称 (如 "sofa", "table")
    mask_url: str        # mask 图片 URL
    bbox: List[int] = field(default_factory=list)  # 边界框 [x1, y1, x2, y2]
    confidence: float = 0.0


@dataclass 
class SegmentationResult:
    """分割结果"""
    success: bool
    objects: List[SegmentedObject] = field(default_factory=list)
    combined_mask_url: str = None    # 合并的 mask
    annotated_image_url: str = None  # 标注后的图片
    request_id: str = None
    cost: float = 0.0
    error: str = None
    elapsed_seconds: float = 0.0


class SegmentationService:
    """
    室内家具分割服务
    
    基于 Grounded SAM:
    - Grounding DINO: 文字→检测框
    - SAM: 检测框→精确 mask
    """
    
    BASE_URL = "https://api.replicate.com/v1"
    MODEL = "schananas/grounded_sam"
    MODEL_VERSION = "ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c"
    COST_PER_RUN = 0.05  # USD
    
    # 室内常见物体标签
    INTERIOR_LABELS = [
        "sofa", "couch", "chair", "armchair", "table", "coffee table", "dining table",
        "bed", "nightstand", "dresser", "wardrobe", "cabinet", "shelf", "bookshelf",
        "lamp", "chandelier", "ceiling light", "floor lamp",
        "rug", "carpet", "curtain", "window", "door",
        "tv", "television", "monitor", "plant", "vase", "picture frame", "mirror",
        "kitchen counter", "sink", "refrigerator", "oven", "microwave",
        "bathtub", "toilet", "shower"
    ]
    
    # 中文标签映射
    LABEL_ZH = {
        "sofa": "沙发", "couch": "沙发", "chair": "椅子", "armchair": "扶手椅",
        "table": "桌子", "coffee table": "茶几", "dining table": "餐桌",
        "bed": "床", "nightstand": "床头柜", "dresser": "梳妆台",
        "wardrobe": "衣柜", "cabinet": "柜子", "shelf": "架子", "bookshelf": "书架",
        "lamp": "台灯", "chandelier": "吊灯", "ceiling light": "吸顶灯", "floor lamp": "落地灯",
        "rug": "地毯", "carpet": "地毯", "curtain": "窗帘", "window": "窗户", "door": "门",
        "tv": "电视", "television": "电视", "monitor": "显示器",
        "plant": "植物", "vase": "花瓶", "picture frame": "相框", "mirror": "镜子",
        "kitchen counter": "厨房台面", "sink": "水槽", "refrigerator": "冰箱",
        "oven": "烤箱", "microwave": "微波炉",
        "bathtub": "浴缸", "toilet": "马桶", "shower": "淋浴"
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
    
    def segment_furniture(
        self,
        image_url: str = None,
        image_base64: str = None,
        labels: List[str] = None,
        box_threshold: float = 0.25,
        text_threshold: float = 0.25,
    ) -> SegmentationResult:
        """
        分割图片中的家具
        
        Args:
            image_url: 图片URL
            image_base64: base64 编码的图片 (优先使用)
            labels: 要检测的标签列表，默认使用室内常见物体
            box_threshold: 检测框置信度阈值
            text_threshold: 文本匹配阈值
        
        Returns:
            SegmentationResult
        """
        start_time = time.time()
        
        # 确定图片输入
        if image_base64:
            # 处理 base64 输入 - 添加 data URI 前缀
            if not image_base64.startswith('data:'):
                image_base64 = f"data:image/jpeg;base64,{image_base64}"
            image_input = image_base64
        elif image_url:
            image_input = image_url
        else:
            return SegmentationResult(
                success=False,
                error="需要提供 image_url 或 image_base64",
                elapsed_seconds=time.time() - start_time
            )
        
        # 使用默认室内标签
        if labels is None:
            labels = self.INTERIOR_LABELS
        
        # 构建标签字符串 (grounded_sam 格式)
        detection_prompt = ". ".join(labels) + "."
        
        payload = {
            "version": self.MODEL_VERSION,
            "input": {
                "image": image_input,
                "detection_prompt": detection_prompt,
                "box_threshold": box_threshold,
                "text_threshold": text_threshold,
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
                return self._parse_result(result, start_time)
            elif result.get("status") == "failed":
                return SegmentationResult(
                    success=False,
                    error=result.get("error", "Segmentation failed"),
                    elapsed_seconds=time.time() - start_time
                )
            else:
                return self._poll_result(result.get("id"), start_time)
                
        except Exception as e:
            return SegmentationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _parse_result(self, result: dict, start_time: float) -> SegmentationResult:
        """解析 API 返回结果"""
        output = result.get("output", {})
        
        # grounded_sam 返回格式
        # output 通常是一个 URL 或包含多个输出的 dict
        objects = []
        
        if isinstance(output, dict):
            # 解析检测到的对象
            detections = output.get("detections", [])
            for det in detections:
                obj = SegmentedObject(
                    label=det.get("label", "unknown"),
                    mask_url=det.get("mask", ""),
                    bbox=det.get("bbox", []),
                    confidence=det.get("confidence", 0.0)
                )
                objects.append(obj)
            
            return SegmentationResult(
                success=True,
                objects=objects,
                combined_mask_url=output.get("combined_mask"),
                annotated_image_url=output.get("annotated_image"),
                request_id=result.get("id"),
                cost=self.COST_PER_RUN,
                elapsed_seconds=time.time() - start_time
            )
        elif isinstance(output, str):
            # 可能直接返回标注图片 URL
            return SegmentationResult(
                success=True,
                annotated_image_url=output,
                request_id=result.get("id"),
                cost=self.COST_PER_RUN,
                elapsed_seconds=time.time() - start_time
            )
        else:
            return SegmentationResult(
                success=True,
                request_id=result.get("id"),
                cost=self.COST_PER_RUN,
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_result(self, prediction_id: str, start_time: float, max_wait: float = 120) -> SegmentationResult:
        """轮询等待结果"""
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        
        while (time.time() - start_time) < max_wait:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            status = result.get("status")
            
            if status == "succeeded":
                return self._parse_result(result, start_time)
            elif status in ("failed", "canceled"):
                return SegmentationResult(
                    success=False,
                    error=result.get("error", f"Prediction {status}"),
                    elapsed_seconds=time.time() - start_time
                )
            
            time.sleep(2)
        
        return SegmentationResult(
            success=False,
            error=f"Timeout after {max_wait}s",
            elapsed_seconds=time.time() - start_time
        )
    
    def get_label_zh(self, label: str) -> str:
        """获取中文标签"""
        return self.LABEL_ZH.get(label.lower(), label)


class SAM2Service:
    """
    SAM 2 点击分割服务
    
    用于用户点击图片某个位置后，精确分割该区域
    """
    
    BASE_URL = "https://api.replicate.com/v1"
    MODEL = "meta/sam-2"
    MODEL_VERSION = "fe97b453a6455861e3bac769b441ca1f1086110da7466dbb65cf1eecfd60dc83"
    COST_PER_RUN = 0.02
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Prefer": "wait"
        }
    
    def segment_at_point(
        self,
        image_url: str,
        x: int,
        y: int,
        point_label: int = 1,  # 1=前景, 0=背景
    ) -> SegmentationResult:
        """
        在指定点位置进行分割
        
        Args:
            image_url: 图片URL
            x: 点击 x 坐标
            y: 点击 y 坐标
            point_label: 1=选中该区域, 0=排除该区域
        
        Returns:
            SegmentationResult
        """
        start_time = time.time()
        
        payload = {
            "version": self.MODEL_VERSION,
            "input": {
                "image": image_url,
                "point_coords": [[x, y]],
                "point_labels": [point_label],
            }
        }
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/predictions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            result = resp.json()
            
            if result.get("status") == "succeeded":
                output = result.get("output")
                mask_url = output if isinstance(output, str) else output.get("mask") if isinstance(output, dict) else None
                
                return SegmentationResult(
                    success=True,
                    objects=[SegmentedObject(label="selected", mask_url=mask_url or "")] if mask_url else [],
                    combined_mask_url=mask_url,
                    request_id=result.get("id"),
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=time.time() - start_time
                )
            elif result.get("status") == "failed":
                return SegmentationResult(
                    success=False,
                    error=result.get("error", "SAM failed"),
                    elapsed_seconds=time.time() - start_time
                )
            else:
                # 轮询
                return self._poll_result(result.get("id"), start_time)
                
        except Exception as e:
            return SegmentationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_result(self, prediction_id: str, start_time: float, max_wait: float = 60) -> SegmentationResult:
        """轮询等待结果"""
        url = f"{self.BASE_URL}/predictions/{prediction_id}"
        
        while (time.time() - start_time) < max_wait:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            status = result.get("status")
            
            if status == "succeeded":
                output = result.get("output")
                mask_url = output if isinstance(output, str) else output.get("mask") if isinstance(output, dict) else None
                
                return SegmentationResult(
                    success=True,
                    objects=[SegmentedObject(label="selected", mask_url=mask_url or "")] if mask_url else [],
                    combined_mask_url=mask_url,
                    request_id=prediction_id,
                    cost=self.COST_PER_RUN,
                    elapsed_seconds=time.time() - start_time
                )
            elif status in ("failed", "canceled"):
                return SegmentationResult(
                    success=False,
                    error=result.get("error", f"Prediction {status}"),
                    elapsed_seconds=time.time() - start_time
                )
            
            time.sleep(1)
        
        return SegmentationResult(
            success=False,
            error=f"Timeout after {max_wait}s",
            elapsed_seconds=time.time() - start_time
        )


# 测试
if __name__ == "__main__":
    # 测试家具分割
    service = SegmentationService()
    
    test_image = "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"
    
    print("=" * 50)
    print("Testing Furniture Segmentation")
    print("=" * 50)
    
    result = service.segment_furniture(
        image_url=test_image,
        labels=["sofa", "table", "lamp", "plant"]
    )
    
    if result.success:
        print(f"✅ 分割成功!")
        print(f"   检测到 {len(result.objects)} 个对象")
        for obj in result.objects:
            print(f"   - {obj.label} ({service.get_label_zh(obj.label)}): {obj.confidence:.2f}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
    else:
        print(f"❌ 分割失败: {result.error}")
