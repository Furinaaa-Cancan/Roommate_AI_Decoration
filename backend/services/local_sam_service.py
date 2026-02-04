"""
本地 SAM 3 分割服务 - 使用 HuggingFace transformers

基于 Meta SAM 3 模型 (facebook/sam3)，支持：
- 文本提示分割 (如 "sofa", "chair")
- 边界框分割
- 自动识别室内家具
- 不需要 API 费用，本地运行
"""
import os
import io
import base64
import time
import uuid
import numpy as np
from PIL import Image
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# 延迟导入，避免启动时加载模型
_sam3_model = None
_sam3_processor = None


@dataclass
class SegmentedObject:
    """分割出的单个对象"""
    label: str
    label_zh: str
    mask: np.ndarray = None  # numpy mask
    mask_url: str = ""       # 保存后的彩色 mask URL（用于可视化）
    inpaint_mask_url: str = ""  # 黑白 mask URL（用于 inpaint API）
    inpaint_mask_base64: str = ""  # 黑白 mask base64（直接传递给 API）
    bbox: List[int] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class LocalSegmentationResult:
    """分割结果"""
    success: bool
    objects: List[SegmentedObject] = field(default_factory=list)
    combined_mask_url: str = None
    annotated_image_url: str = None
    error: str = None
    elapsed_seconds: float = 0.0


class LocalSAMService:
    """
    本地 SAM 分割服务
    
    使用 HuggingFace 的 SAM2 模型进行图像分割
    """
    
    # 中文标签映射
    LABEL_ZH = {
        # 主要家具
        "sofa": "沙发", "couch": "沙发", "chair": "椅子", "armchair": "扶手椅",
        "table": "桌子", "coffee table": "茶几", "dining table": "餐桌",
        "tv stand": "电视柜", "side table": "边桌", "end table": "边桌",
        "wooden stool": "木凳", "stool": "凳子",
        "bed": "床", "nightstand": "床头柜", "dresser": "梳妆台",
        "wardrobe": "衣柜", "cabinet": "柜子", "shelf": "架子", "bookshelf": "书架",
        # 灯具
        "lamp": "台灯", "chandelier": "吊灯", "ceiling light": "吸顶灯", "floor lamp": "落地灯",
        "table lamp": "台灯", "light strip": "灯带",
        # 纺织品
        "rug": "地毯", "carpet": "地毯", "curtain": "窗帘", "drape": "窗帘",
        "pillow": "枕头", "cushion": "靠垫", "throw blanket": "毛毯", "blanket": "毯子",
        # 建筑元素
        "window": "窗户", "door": "门", "balcony door": "阳台门", "glass door": "玻璃门",
        "floor": "地板", "wooden floor": "木地板", "wall": "墙面",
        # 电器
        "tv": "电视", "television": "电视", "monitor": "显示器",
        "refrigerator": "冰箱", "oven": "烤箱", "microwave": "微波炉",
        # 装饰品
        "plant": "植物", "vase": "花瓶", "ceramic pot": "陶罐", "pottery": "陶器",
        "bowl": "碗", "decorative bowl": "装饰碗",
        "picture frame": "相框", "painting": "画作", "artwork": "艺术品", "mirror": "镜子",
        "book": "书", "books": "书籍",
        # 卫浴
        "bathtub": "浴缸", "toilet": "马桶", "shower": "淋浴",
        # 通用
        "object": "物体", "furniture": "家具"
    }
    
    def __init__(self, output_dir: str = None):
        """
        初始化服务
        
        Args:
            output_dir: mask 图片保存目录
        """
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(__file__), "..", "static", "masks"
        )
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._sam_loaded = False
        self._grounding_loaded = False
    
    def _load_sam3_model(self):
        """延迟加载 SAM 3 模型"""
        global _sam3_model, _sam3_processor
        
        if _sam3_model is not None:
            return
        
        print("正在加载 SAM 3 模型 (facebook/sam3)...")
        from transformers import Sam3Model, Sam3Processor
        import torch
        
        model_id = "facebook/sam3"
        _sam3_processor = Sam3Processor.from_pretrained(model_id)
        _sam3_model = Sam3Model.from_pretrained(model_id)
        
        # 选择设备
        if torch.cuda.is_available():
            _sam3_model = _sam3_model.to("cuda")
            print("SAM 3 模型已加载到 CUDA")
        elif torch.backends.mps.is_available():
            _sam3_model = _sam3_model.to("mps")
            print("SAM 3 模型已加载到 MPS (Apple Silicon)")
        else:
            print("SAM 3 模型已加载到 CPU")
        
        self._sam_loaded = True
        print("SAM 3 模型加载完成")
    
    def _load_image(self, image_url: str = None, image_base64: str = None) -> Image.Image:
        """加载图片"""
        if image_base64:
            # 处理 base64
            if image_base64.startswith('data:'):
                image_base64 = image_base64.split(',')[1]
            image_data = base64.b64decode(image_base64)
            return Image.open(io.BytesIO(image_data)).convert("RGB")
        elif image_url:
            if image_url.startswith('http'):
                import requests
                response = requests.get(image_url, timeout=30)
                return Image.open(io.BytesIO(response.content)).convert("RGB")
            else:
                return Image.open(image_url).convert("RGB")
        else:
            raise ValueError("需要提供 image_url 或 image_base64")
    
    def _save_mask(self, mask: np.ndarray, prefix: str = "mask", color: tuple = None) -> str:
        """保存 mask 为彩色半透明 PNG 并返回 URL（用于可视化）"""
        filename = f"{prefix}_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # 使用随机颜色或指定颜色
        if color is None:
            import random
            color = (
                random.randint(100, 255),
                random.randint(100, 255), 
                random.randint(100, 255)
            )
        
        # 创建 RGBA 彩色半透明 mask
        h, w = mask.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        rgba[mask, 0] = color[0]  # R
        rgba[mask, 1] = color[1]  # G
        rgba[mask, 2] = color[2]  # B
        rgba[mask, 3] = 180  # Alpha (半透明)
        
        mask_img = Image.fromarray(rgba, mode='RGBA')
        mask_img.save(filepath)
        
        # 返回相对 URL
        return f"/static/masks/{filename}"
    
    def _save_inpaint_mask(self, mask: np.ndarray, prefix: str = "inpaint_mask") -> str:
        """保存用于 inpaint 的黑白 mask
        
        格式：白色 (255) = 要编辑的区域，黑色 (0) = 保持不变
        这是 AI inpaint API 需要的标准格式
        """
        filename = f"{prefix}_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # 创建黑白 mask：白色=编辑区域，黑色=保持不变
        h, w = mask.shape
        bw_mask = np.zeros((h, w), dtype=np.uint8)
        bw_mask[mask] = 255  # 白色区域为要编辑的部分
        
        mask_img = Image.fromarray(bw_mask, mode='L')
        mask_img.save(filepath)
        
        return f"/static/masks/{filename}"
    
    def _mask_to_base64(self, mask: np.ndarray) -> str:
        """将 mask 转换为 base64 格式（用于直接传递给 API）
        
        格式：白色 (255) = 要编辑的区域，黑色 (0) = 保持不变
        """
        # 创建黑白 mask
        h, w = mask.shape
        bw_mask = np.zeros((h, w), dtype=np.uint8)
        bw_mask[mask] = 255
        
        mask_img = Image.fromarray(bw_mask, mode='L')
        
        # 转为 base64
        buffer = io.BytesIO()
        mask_img.save(buffer, format='PNG')
        b64_data = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{b64_data}"
    
    def get_label_zh(self, label: str) -> str:
        """获取中文标签"""
        return self.LABEL_ZH.get(label.lower(), label)
    
    def segment_furniture(
        self,
        image_url: str = None,
        image_base64: str = None,
        labels: List[str] = None,
        box_threshold: float = 0.15,  # 降低阈值提高识别率
    ) -> LocalSegmentationResult:
        """
        分割图片中的家具
        
        使用 Grounding DINO 检测 + SAM 分割
        """
        start_time = time.time()
        
        try:
            # 加载 SAM 3 模型
            self._load_sam3_model()
            
            # 加载图片
            image = self._load_image(image_url, image_base64)
            
            # 默认检测标签 - 精简核心家具列表（提高速度）
            if labels is None:
                labels = [
                    # 核心家具（8个）
                    "sofa", "chair", "table", "bed", "cabinet", "lamp",
                    "curtain", "rug",
                    # 常见物品（6个）
                    "tv", "plant", "pillow", "vase", "painting", "mirror"
                ]
            
            import torch
            
            objects = []
            
            # SAM 3 支持文本提示分割 - 逐个标签检测
            for label in labels:
                inputs = _sam3_processor(
                    images=image, 
                    text=label,
                    return_tensors="pt"
                )
                
                device = next(_sam3_model.parameters()).device
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = _sam3_model(**inputs)
                
                # SAM 3 后处理
                results = _sam3_processor.post_process_instance_segmentation(
                    outputs,
                    threshold=box_threshold,
                    mask_threshold=0.5,
                    target_sizes=inputs.get("original_sizes").tolist()
                )[0]
                
                # 处理检测到的物体
                for i, (mask, box, score) in enumerate(zip(
                    results.get("masks", []),
                    results.get("boxes", []),
                    results.get("scores", [])
                )):
                    mask_np = mask.cpu().numpy().astype(bool)
                    box_list = box.cpu().numpy().tolist()
                    
                    # 保存彩色 mask（用于可视化）
                    mask_url = self._save_mask(mask_np, f"mask_{label}_{i}")
                    # 保存黑白 mask（用于 inpaint）
                    inpaint_mask_url = self._save_inpaint_mask(mask_np, f"inpaint_{label}_{i}")
                    # 生成 base64 格式（用于直接传递给 API）
                    inpaint_mask_base64 = self._mask_to_base64(mask_np)
                    
                    objects.append(SegmentedObject(
                        label=label,
                        label_zh=self.get_label_zh(label),
                        mask=mask_np,
                        mask_url=mask_url,
                        inpaint_mask_url=inpaint_mask_url,
                        inpaint_mask_base64=inpaint_mask_base64,
                        bbox=[int(x) for x in box_list],
                        confidence=float(score)
                    ))
            
            return LocalSegmentationResult(
                success=True,
                objects=objects,
                elapsed_seconds=time.time() - start_time
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return LocalSegmentationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def segment_at_point(
        self,
        image_url: str = None,
        image_base64: str = None,
        x: int = 0,
        y: int = 0,
    ) -> LocalSegmentationResult:
        """
        点击分割 - 在指定坐标位置分割物体
        使用 SAM 3 模型，通过边界框近似点击位置
        """
        start_time = time.time()
        
        try:
            self._load_sam3_model()
            
            image = self._load_image(image_url, image_base64)
            
            import torch
            
            # SAM 3 使用边界框，创建一个以点击位置为中心的小框
            box_size = 50
            box_xyxy = [
                max(0, x - box_size),
                max(0, y - box_size),
                min(image.width, x + box_size),
                min(image.height, y + box_size)
            ]
            
            input_boxes = [[box_xyxy]]
            input_boxes_labels = [[1]]  # 1 = positive
            
            inputs = _sam3_processor(
                images=image,
                input_boxes=input_boxes,
                input_boxes_labels=input_boxes_labels,
                return_tensors="pt"
            )
            
            device = next(_sam3_model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = _sam3_model(**inputs)
            
            # SAM 3 后处理
            results = _sam3_processor.post_process_instance_segmentation(
                outputs,
                threshold=0.3,
                mask_threshold=0.5,
                target_sizes=inputs.get("original_sizes").tolist()
            )[0]
            
            if len(results.get("masks", [])) > 0:
                mask = results["masks"][0]
                box = results["boxes"][0]
                score = results["scores"][0]
                
                mask_np = mask.cpu().numpy().astype(bool)
                box_list = box.cpu().numpy().tolist()
                
                # 保存彩色 mask（用于可视化）
                mask_url = self._save_mask(mask_np, "point_mask")
                # 保存黑白 mask（用于 inpaint）
                inpaint_mask_url = self._save_inpaint_mask(mask_np, "point_inpaint")
                # 生成 base64 格式
                inpaint_mask_base64 = self._mask_to_base64(mask_np)
                
                obj = SegmentedObject(
                    label="object",
                    label_zh="选中区域",
                    mask=mask_np,
                    mask_url=mask_url,
                    inpaint_mask_url=inpaint_mask_url,
                    inpaint_mask_base64=inpaint_mask_base64,
                    bbox=[int(x) for x in box_list],
                    confidence=float(score)
                )
            else:
                # 没有检测到物体，返回空
                obj = SegmentedObject(
                    label="object",
                    label_zh="未检测到物体",
                    mask_url="",
                    bbox=[x-25, y-25, x+25, y+25],
                    confidence=0.0
                )
            
            return LocalSegmentationResult(
                success=True,
                objects=[obj],
                elapsed_seconds=time.time() - start_time
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return LocalSegmentationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def auto_segment_all(
        self,
        image_url: str = None,
        image_base64: str = None,
    ) -> LocalSegmentationResult:
        """
        自动分割图片中的所有物体
        
        使用 SAM 3 文本提示分割常见家具（使用默认扩展标签列表）
        """
        # 使用 segment_furniture 方法，labels=None 使用默认扩展标签
        return self.segment_furniture(
            image_url=image_url,
            image_base64=image_base64,
            labels=None
        )


# 测试
if __name__ == "__main__":
    service = LocalSAMService()
    print("LocalSAMService (SAM 3) 初始化成功")
    print("标签映射:", list(service.LABEL_ZH.keys())[:5])
