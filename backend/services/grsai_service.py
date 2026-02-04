"""
Grsai Nano Banana API 服务
官方文档: https://grsai.dakka.com.cn
成本: ~¥0.18/张 (nano-banana-pro)
"""
import os
import time
import asyncio
import httpx
from typing import Optional, List, Callable, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum


class NanoBananaModel(str, Enum):
    """支持的模型"""
    FAST = "nano-banana-fast"           # 快速版
    STANDARD = "nano-banana"            # 标准版
    PRO = "nano-banana-pro"             # Pro版，支持1K/2K/4K
    PRO_VT = "nano-banana-pro-vt"       # Pro VT版
    PRO_CL = "nano-banana-pro-cl"       # Pro CL版
    PRO_VIP = "nano-banana-pro-vip"     # Pro VIP (只支持1K/2K)
    PRO_4K_VIP = "nano-banana-pro-4k-vip"  # Pro 4K VIP (只支持4K)


class ImageSize(str, Enum):
    """输出图像大小"""
    SIZE_1K = "1K"
    SIZE_2K = "2K"
    SIZE_4K = "4K"


class AspectRatio(str, Enum):
    """宽高比"""
    AUTO = "auto"
    RATIO_1_1 = "1:1"
    RATIO_16_9 = "16:9"
    RATIO_9_16 = "9:16"
    RATIO_4_3 = "4:3"
    RATIO_3_4 = "3:4"
    RATIO_3_2 = "3:2"
    RATIO_2_3 = "2:3"
    RATIO_5_4 = "5:4"
    RATIO_4_5 = "4:5"
    RATIO_21_9 = "21:9"


class TaskStatus(str, Enum):
    """任务状态"""
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class GenerationProgress:
    """生成进度"""
    id: str
    progress: int  # 0-100
    status: TaskStatus
    results: List[dict] = field(default_factory=list)
    failure_reason: str = ""
    error: str = ""


@dataclass
class GenerationResult:
    """生成结果"""
    success: bool
    task_id: str = None
    images: List[str] = None  # 图片URL列表
    content: str = None       # 回复内容
    cost: float = 0.0         # 成本(RMB)
    error: str = None
    elapsed_seconds: float = 0.0


class GrsaiNanoBananaService:
    """
    Grsai Nano Banana API 异步服务
    
    使用示例:
        service = GrsaiNanoBananaService(api_key="your_api_key")
        
        # 方式1: 流式响应
        async for progress in service.generate_stream(prompt="现代简约客厅", image_url="https://..."):
            print(f"进度: {progress.progress}%")
            if progress.status == TaskStatus.SUCCEEDED:
                print(f"结果: {progress.results}")
        
        # 方式2: 直接获取结果
        result = await service.generate(prompt="现代简约客厅", image_url="https://...")
        print(result.images)
    """
    
    # API地址
    HOST_OVERSEAS = "https://grsaiapi.com"
    HOST_CHINA = "https://grsai.dakka.com.cn"
    
    # 接口路径
    ENDPOINT_DRAW = "/v1/draw/nano-banana"
    ENDPOINT_RESULT = "/v1/draw/result"
    
    # 成本估算 (RMB)
    COST_MAP = {
        NanoBananaModel.FAST: 0.10,
        NanoBananaModel.STANDARD: 0.15,
        NanoBananaModel.PRO: 0.18,
        NanoBananaModel.PRO_VT: 0.20,
        NanoBananaModel.PRO_CL: 0.20,
        NanoBananaModel.PRO_VIP: 0.25,
        NanoBananaModel.PRO_4K_VIP: 0.50,
    }
    
    # NanoBanana 装修风格Prompt模板 - 从prompts库加载
    @staticmethod
    def _load_style_prompts():
        """从prompts库加载风格模板"""
        try:
            from prompts import STYLE_PROMPTS, PromptBuilder
            return STYLE_PROMPTS, PromptBuilder
        except ImportError:
            # 降级到内置模板
            return {
                "nanobanana": {"prompt_zh": "现代简约装修风格，温暖中性色调，奶油色和米色调色板，天然木质元素，柔和照明，温馨氛围，高端家具，专业室内摄影，8K超高清"},
                "nanobanana_A": {"prompt_zh": "现代简约室内设计，奶油白墙面，浅橡木地板，米色布艺沙发，暖色氛围灯光，北欧风格，线条简洁，专业摄影，8K"},
                "nanobanana_B": {"prompt_zh": "当代室内设计，暖灰色调，胡桃木元素，丝绒质感，金色点缀，精致优雅，轻奢感，专业室内摄影，8K"},
                "nanobanana_C": {"prompt_zh": "日式侘寂风格，天然材质，柔和大地色系，禅意美学，有机造型，极简家具，专业摄影，8K"},
                "modern_chinese": {"prompt_zh": "新中式装修风格，传统与现代结合，木质元素，中式屏风，水墨画装饰，禅意空间，高端质感，8K"},
                "cream_style": {"prompt_zh": "奶油风装修，浅色系，柔和温暖，法式慵懒，圆润家具，自然光线，温馨舒适，8K"},
                "cream": {"prompt_zh": "奶油风室内设计，柔和暖色调，奶油白墙面，米色象牙白，圆润家具，舒适质感，柔和灯光，法式慵懒"},
                "scandinavian": {"prompt_zh": "北欧室内设计，白色墙面，浅色木地板，舒适纺织品，功能性家具，温馨氛围，绿植"},
                "japanese": {"prompt_zh": "日式室内设计，榻榻米，障子门，低矮家具，天然材质，禅意庭院，极简装饰"},
                "industrial": {"prompt_zh": "工业风室内设计，裸露砖墙，金属横梁，水泥地面，复古工厂元素，爱迪生灯泡，做旧皮革"},
                "modern": {"prompt_zh": "现代室内设计，简洁线条，中性色调，开放空间，极简家具，光滑表面，大窗户，自然采光"},
            }, None
    
    STYLE_PROMPTS = {
        "nanobanana": "现代简约装修风格，温暖中性色调，奶油色和米色调色板，天然木质元素，柔和照明，温馨氛围，高端家具，专业室内摄影，8K超高清",
        "nanobanana_A": "现代简约室内设计，奶油白墙面，浅橡木地板，米色布艺沙发，暖色氛围灯光，北欧风格，线条简洁，专业摄影，8K",
        "nanobanana_B": "当代室内设计，暖灰色调，胡桃木元素，丝绒质感，金色点缀，精致优雅，轻奢感，专业室内摄影，8K",
        "nanobanana_C": "日式侘寂风格，天然材质，柔和大地色系，禅意美学，有机造型，极简家具，专业摄影，8K",
        "modern_chinese": "新中式装修风格，传统与现代结合，木质元素，中式屏风，水墨画装饰，禅意空间，高端质感，8K",
        "cream_style": "奶油风装修，浅色系，柔和温暖，法式慵懒，圆润家具，自然光线，温馨舒适，8K",
    }
    
    def __init__(
        self, 
        api_key: str = None,
        use_china_host: bool = True,
        timeout: float = 180.0
    ):
        """
        初始化服务
        
        Args:
            api_key: API密钥，不传则从环境变量 GRSAI_API_KEY 获取
            use_china_host: 是否使用国内直连地址
            timeout: 请求超时时间(秒)
        """
        self.api_key = api_key or os.getenv("GRSAI_API_KEY")
        if not self.api_key:
            raise ValueError("GRSAI_API_KEY is required")
        
        self.base_url = self.HOST_CHINA if use_china_host else self.HOST_OVERSEAS
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _build_prompt(self, prompt: str, style: str = None, room_type: str = None) -> str:
        """构建完整的prompt，优先使用prompts库，强制加入结构锁定"""
        try:
            from prompts import PromptBuilder, STYLE_PROMPTS, STRUCT_LOCK_HARD
            
            # 结构锁定指令（始终前置）
            struct_lock = STRUCT_LOCK_HARD.get("zh", "")
            
            # 使用PromptBuilder构建专业prompt
            if room_type and style:
                result = PromptBuilder.build_prompt(
                    room_type=room_type,
                    style=style,
                    custom_description=prompt,
                    language="zh",
                    quality_level="high"
                )
                # PromptBuilder 已内置 struct_lock，直接返回
                return result["prompt"]
            
            # 只有风格时，从风格库获取，手动加入结构锁定
            if style and style in STYLE_PROMPTS:
                style_data = STYLE_PROMPTS[style]
                style_prompt = style_data.get("prompt_zh", style_data.get("prompt", ""))
                return f"{struct_lock}，{style_prompt}，{prompt}"
            
            # 无风格时，只加结构锁定
            return f"{struct_lock}，{prompt}"
            
        except ImportError:
            # 降级到内置模板，手动加入结构锁定
            struct_lock = "禁止改动几何结构与透视：不新增/移动门窗，不改变墙体边界，垂直线保持笔直，镜头位置不变，保持原有房间格局和比例"
            if style and style in self.STYLE_PROMPTS:
                return f"{struct_lock}，{self.STYLE_PROMPTS[style]}，{prompt}"
            return f"{struct_lock}，{prompt}"
    
    async def generate(
        self,
        prompt: str,
        image_url: str = None,
        model: NanoBananaModel = NanoBananaModel.PRO,
        style: str = None,
        room_type: str = None,
        aspect_ratio: AspectRatio = AspectRatio.AUTO,
        image_size: ImageSize = ImageSize.SIZE_1K,
    ) -> GenerationResult:
        """
        生成图片（等待完成后返回结果）
        
        Args:
            prompt: 提示词
            image_url: 参考图URL（用于图生图）
            model: 使用的模型
            style: 风格模板名称 (nanobanana, scandinavian, japanese, etc.)
            room_type: 房间类型 (living_room, bedroom, kitchen, etc.)
            aspect_ratio: 输出宽高比
            image_size: 输出分辨率
        
        Returns:
            GenerationResult
        """
        start_time = time.time()
        
        # 构建请求 - 使用prompts库生成专业prompt
        full_prompt = self._build_prompt(prompt, style, room_type)
        payload = {
            "model": model.value if isinstance(model, NanoBananaModel) else model,
            "prompt": full_prompt,
            "aspectRatio": aspect_ratio.value if isinstance(aspect_ratio, AspectRatio) else aspect_ratio,
            "imageSize": image_size.value if isinstance(image_size, ImageSize) else image_size,
            "shutProgress": True,  # 不需要进度，直接返回结果
        }
        
        if image_url:
            payload["urls"] = [image_url] if isinstance(image_url, str) else image_url
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 发送请求，使用流式响应
                url = f"{self.base_url}{self.ENDPOINT_DRAW}"
                
                async with client.stream("POST", url, headers=self.headers, json=payload) as response:
                    response.raise_for_status()
                    
                    final_result = None
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                import json
                                data = json.loads(line)
                                if data.get("status") == "succeeded":
                                    final_result = data
                                    break
                                elif data.get("status") == "failed":
                                    raise Exception(data.get("error") or data.get("failure_reason") or "Generation failed")
                            except json.JSONDecodeError:
                                continue
                    
                    if not final_result:
                        raise Exception("No result received")
                    
                    elapsed = time.time() - start_time
                    images = [r["url"] for r in final_result.get("results", [])]
                    content = final_result.get("results", [{}])[0].get("content", "")
                    
                    # 估算成本
                    model_key = NanoBananaModel(payload["model"]) if payload["model"] in [m.value for m in NanoBananaModel] else NanoBananaModel.PRO
                    cost = self.COST_MAP.get(model_key, 0.18)
                    
                    return GenerationResult(
                        success=True,
                        task_id=final_result.get("id"),
                        images=images,
                        content=content,
                        cost=cost,
                        elapsed_seconds=elapsed
                    )
                    
        except Exception as e:
            elapsed = time.time() - start_time
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=elapsed
            )
    
    async def generate_stream(
        self,
        prompt: str,
        image_url: str = None,
        model: NanoBananaModel = NanoBananaModel.PRO,
        style: str = None,
        room_type: str = None,
        aspect_ratio: AspectRatio = AspectRatio.AUTO,
        image_size: ImageSize = ImageSize.SIZE_1K,
    ) -> AsyncGenerator[GenerationProgress, None]:
        """
        流式生成图片（实时返回进度）
        
        Args:
            prompt: 提示词
            image_url: 参考图URL
            model: 使用的模型
            style: 风格模板
            room_type: 房间类型
            aspect_ratio: 输出宽高比
            image_size: 输出分辨率
        
        Yields:
            GenerationProgress 进度对象
        """
        full_prompt = self._build_prompt(prompt, style, room_type)
        payload = {
            "model": model.value if isinstance(model, NanoBananaModel) else model,
            "prompt": full_prompt,
            "aspectRatio": aspect_ratio.value if isinstance(aspect_ratio, AspectRatio) else aspect_ratio,
            "imageSize": image_size.value if isinstance(image_size, ImageSize) else image_size,
            "shutProgress": False,  # 需要进度
        }
        
        if image_url:
            payload["urls"] = [image_url] if isinstance(image_url, str) else image_url
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{self.ENDPOINT_DRAW}"
            
            async with client.stream("POST", url, headers=self.headers, json=payload) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            import json
                            data = json.loads(line)
                            yield GenerationProgress(
                                id=data.get("id", ""),
                                progress=data.get("progress", 0),
                                status=TaskStatus(data.get("status", "running")),
                                results=data.get("results", []),
                                failure_reason=data.get("failure_reason", ""),
                                error=data.get("error", "")
                            )
                        except json.JSONDecodeError:
                            continue
    
    async def generate_with_webhook(
        self,
        prompt: str,
        webhook_url: str,
        image_url: str = None,
        model: NanoBananaModel = NanoBananaModel.PRO,
        style: str = None,
        room_type: str = None,
        aspect_ratio: AspectRatio = AspectRatio.AUTO,
        image_size: ImageSize = ImageSize.SIZE_1K,
    ) -> str:
        """
        使用WebHook回调生成图片
        
        Args:
            prompt: 提示词
            webhook_url: 回调地址
            image_url: 参考图URL
            model: 使用的模型
            style: 风格模板
            room_type: 房间类型
            aspect_ratio: 输出宽高比
            image_size: 输出分辨率
        
        Returns:
            任务ID
        """
        full_prompt = self._build_prompt(prompt, style, room_type)
        payload = {
            "model": model.value if isinstance(model, NanoBananaModel) else model,
            "prompt": full_prompt,
            "aspectRatio": aspect_ratio.value if isinstance(aspect_ratio, AspectRatio) else aspect_ratio,
            "imageSize": image_size.value if isinstance(image_size, ImageSize) else image_size,
            "webHook": webhook_url,
            "shutProgress": False,
        }
        
        if image_url:
            payload["urls"] = [image_url] if isinstance(image_url, str) else image_url
        
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{self.base_url}{self.ENDPOINT_DRAW}"
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("id", "")
    
    async def generate_with_polling(
        self,
        prompt: str,
        image_url: str = None,
        model: NanoBananaModel = NanoBananaModel.PRO,
        style: str = None,
        room_type: str = None,
        aspect_ratio: AspectRatio = AspectRatio.AUTO,
        image_size: ImageSize = ImageSize.SIZE_1K,
        poll_interval: float = 2.0,
        max_wait: float = 180.0,
    ) -> GenerationResult:
        """
        使用轮询方式获取结果
        
        Args:
            prompt: 提示词
            image_url: 参考图URL
            model: 使用的模型
            style: 风格模板
            room_type: 房间类型
            aspect_ratio: 输出宽高比
            image_size: 输出分辨率
            poll_interval: 轮询间隔(秒)
            max_wait: 最大等待时间(秒)
        
        Returns:
            GenerationResult
        """
        start_time = time.time()
        
        full_prompt = self._build_prompt(prompt, style, room_type)
        payload = {
            "model": model.value if isinstance(model, NanoBananaModel) else model,
            "prompt": full_prompt,
            "aspectRatio": aspect_ratio.value if isinstance(aspect_ratio, AspectRatio) else aspect_ratio,
            "imageSize": image_size.value if isinstance(image_size, ImageSize) else image_size,
            "webHook": "-1",  # 立即返回ID，用于轮询
        }
        
        if image_url:
            payload["urls"] = [image_url] if isinstance(image_url, str) else image_url
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # 提交任务
                url = f"{self.base_url}{self.ENDPOINT_DRAW}"
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                task_id = data.get("data", {}).get("id", "")
                
                if not task_id:
                    raise Exception("Failed to get task ID")
                
                # 轮询结果
                result = await self._poll_result(client, task_id, poll_interval, max_wait)
                
                elapsed = time.time() - start_time
                images = [r["url"] for r in result.get("results", [])]
                content = result.get("results", [{}])[0].get("content", "")
                
                model_key = NanoBananaModel(payload["model"]) if payload["model"] in [m.value for m in NanoBananaModel] else NanoBananaModel.PRO
                cost = self.COST_MAP.get(model_key, 0.18)
                
                return GenerationResult(
                    success=True,
                    task_id=task_id,
                    images=images,
                    content=content,
                    cost=cost,
                    elapsed_seconds=elapsed
                )
                
        except Exception as e:
            elapsed = time.time() - start_time
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=elapsed
            )
    
    async def _poll_result(
        self, 
        client: httpx.AsyncClient, 
        task_id: str,
        poll_interval: float = 2.0,
        max_wait: float = 180.0
    ) -> dict:
        """轮询获取结果"""
        url = f"{self.base_url}{self.ENDPOINT_RESULT}"
        waited = 0.0
        
        while waited < max_wait:
            response = await client.post(url, headers=self.headers, json={"id": task_id})
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == -22:
                raise Exception("Task not found")
            
            result = data.get("data", {})
            status = result.get("status")
            
            if status == "succeeded":
                return result
            elif status == "failed":
                raise Exception(result.get("error") or result.get("failure_reason") or "Generation failed")
            
            await asyncio.sleep(poll_interval)
            waited += poll_interval
        
        raise Exception(f"Timeout after {max_wait}s")
    
    async def get_result(self, task_id: str) -> GenerationProgress:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
        
        Returns:
            GenerationProgress
        """
        async with httpx.AsyncClient(timeout=30) as client:
            url = f"{self.base_url}{self.ENDPOINT_RESULT}"
            response = await client.post(url, headers=self.headers, json={"id": task_id})
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == -22:
                raise Exception("Task not found")
            
            result = data.get("data", {})
            return GenerationProgress(
                id=result.get("id", task_id),
                progress=result.get("progress", 0),
                status=TaskStatus(result.get("status", "running")),
                results=result.get("results", []),
                failure_reason=result.get("failure_reason", ""),
                error=result.get("error", "")
            )

    # ============ Inpaint 局部重绘 ============
    
    async def inpaint(
        self,
        image_url: str,
        mask_url: str,
        furniture_type: str = None,
        style: str = "现代简约",
        custom_prompt: str = None,
    ) -> GenerationResult:
        """局部重绘 - 使用 nano-banana-pro 替换选中的家具
        
        Nano Banana Pro 通过 prompt + 原图 + mask 实现 inpaint 功能
        """
        start_time = time.time()
        
        # 抹除模式 - 特殊处理
        if style == "抹除":
            # 抹除物品，用背景填充
            erase_prompt = f"REMOVE and ERASE the objects in the white masked area completely. Fill the masked region with natural background - clean empty floor, wall texture, or surrounding environment. Make it look like the objects were never there. Seamless blend with surroundings. Photorealistic empty space. Keep ALL areas outside the white mask EXACTLY unchanged."
            if custom_prompt:
                erase_prompt += f" {custom_prompt}"
            
            print(f"[Inpaint-Erase] Prompt: {erase_prompt}")
            print(f"[Inpaint-Erase] 抹除物品: {furniture_type}")
            
            payload = {
                "model": "nano-banana-pro",
                "prompt": erase_prompt,
                "urls": [image_url, mask_url],
                "shutProgress": True,
                "imageSize": "4K",
            }
            
            try:
                async with httpx.AsyncClient(timeout=300) as client:
                    url = f"{self.base_url}{self.ENDPOINT_DRAW}"
                    async with client.stream("POST", url, headers=self.headers, json=payload) as response:
                        response.raise_for_status()
                        final_result = None
                        async for line in response.aiter_lines():
                            if line.strip():
                                json_str = line
                                if line.startswith("data: "):
                                    json_str = line[6:]
                                try:
                                    import json
                                    data = json.loads(json_str)
                                    if data.get("status") == "succeeded":
                                        final_result = data
                                        break
                                    elif data.get("status") == "failed":
                                        raise Exception(data.get("error") or "Erase failed")
                                except json.JSONDecodeError:
                                    continue
                        
                        if not final_result:
                            raise Exception("No result received")
                        
                        elapsed = time.time() - start_time
                        images = [r["url"] for r in final_result.get("results", [])]
                        
                        return GenerationResult(
                            success=True,
                            task_id=final_result.get("id"),
                            images=images,
                            cost=0.18,
                            elapsed_seconds=elapsed
                        )
            except Exception as e:
                return GenerationResult(
                    success=False,
                    error=str(e),
                    elapsed_seconds=time.time() - start_time
                )
        
        # 风格Prompt模板（用于替换，非抹除）
        style_prompts = {
            "现代简约": "modern minimalist style, clean lines, neutral colors, high quality",
            "北欧风": "scandinavian style, light wood, white and pastel colors, cozy",
            "轻奢": "luxury style, velvet fabric, gold accents, elegant, premium",
            "日式": "japanese style, natural wood, zen minimalist, peaceful",
            "工业风": "industrial style, metal and leather, urban loft, raw",
            "新中式": "modern chinese style, dark wood, traditional patterns, elegant",
            "侘寂风": "wabi-sabi style, natural imperfection, earthy tones, organic",
            "奶油风": "cream style, soft warm tones, rounded shapes, comfortable",
        }
        
        # 家具Prompt模板（英文，更好的效果）
        furniture_prompts = {
            "sofa": "elegant designer sofa, comfortable seating, high-quality fabric",
            "chair": "stylish modern chair, ergonomic design, premium materials",
            "table": "beautiful coffee table, solid construction, refined finish",
            "bed": "luxurious bed, comfortable mattress, elegant headboard",
            "cabinet": "modern storage cabinet, ample storage, sleek design",
            "lamp": "designer floor lamp, ambient lighting, artistic form",
            "curtain": "elegant curtains, flowing fabric, natural drape",
            "rug": "premium area rug, soft texture, beautiful pattern",
            "tv": "large flat screen TV, modern entertainment center",
            "plant": "lush green plant, natural foliage, decorative pot",
            "pillow": "decorative throw pillows, soft cushions",
            "vase": "elegant vase, artistic design, fresh flowers",
            "painting": "beautiful artwork, framed painting on wall",
            "mirror": "decorative wall mirror, ornate frame",
        }
        
        # 获取风格描述
        style_prompt = style_prompts.get(style, style_prompts["现代简约"])
        
        # 获取家具描述
        if furniture_type and furniture_type.lower() in furniture_prompts:
            furniture_desc = furniture_prompts[furniture_type.lower()]
        else:
            furniture_desc = "new stylish furniture piece"
        
        # 优化 prompt，描述多个物品替换
        # furniture_type 可能是 "rug, painting, vase" 这样的多个物品
        items = furniture_type.split(",") if furniture_type else ["furniture"]
        items_desc = " and ".join([f.strip() for f in items])
        
        # 强调只修改白色mask区域，其他区域完全保持原样
        prompt = f"INPAINT ONLY the white masked region. Replace ONLY the {items_desc} in the white mask area with new {style_prompt} {items_desc}. CRITICAL: Keep ALL other areas EXACTLY as they are - do not modify anything outside the white mask. The black mask areas must remain COMPLETELY UNCHANGED - same colors, textures, objects, lighting. Only regenerate content inside the white masked region."
        if custom_prompt:
            prompt += f" {custom_prompt}"
        
        print(f"[Inpaint] Prompt: {prompt}")
        print(f"[Inpaint] 家具: {furniture_type}, 风格: {style}")
        
        # 使用 nano-banana-pro 模型 + 4K
        payload = {
            "model": "nano-banana-pro",
            "prompt": prompt,
            "urls": [image_url, mask_url],
            "shutProgress": True,
            "imageSize": "4K",
        }
        
        try:
            # inpaint需要更长超时时间
            async with httpx.AsyncClient(timeout=300) as client:
                url = f"{self.base_url}{self.ENDPOINT_DRAW}"
                print(f"[Inpaint] 调用API: {url}")
                print(f"[Inpaint] Payload: {payload}")
                
                async with client.stream("POST", url, headers=self.headers, json=payload) as response:
                    response.raise_for_status()
                    final_result = None
                    all_lines = []
                    async for line in response.aiter_lines():
                        if line.strip():
                            all_lines.append(line)
                            # SSE格式：去掉 "data: " 前缀
                            json_str = line
                            if line.startswith("data: "):
                                json_str = line[6:]
                            print(f"[Inpaint] 响应行: {json_str[:200]}...")
                            try:
                                import json
                                data = json.loads(json_str)
                                if data.get("status") == "succeeded":
                                    final_result = data
                                    break
                                elif data.get("status") == "failed":
                                    raise Exception(data.get("error") or data.get("failure_reason") or "Inpaint failed")
                            except json.JSONDecodeError:
                                continue
                    
                    if not final_result:
                        print(f"[Inpaint] 未收到结果，所有响应: {all_lines}")
                        raise Exception(f"No result received. Lines: {len(all_lines)}")
                    
                    images = [r["url"] for r in final_result.get("results", [])]
                    return GenerationResult(
                        success=True,
                        task_id=final_result.get("id"),
                        images=images,
                        cost=0.20,
                        elapsed_seconds=time.time() - start_time
                    )
        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )


class GrsaiNanoBananaServiceSync:
    """
    同步版本 - 方便测试和简单场景使用
    """
    
    HOST_CHINA = "https://grsai.dakka.com.cn"
    ENDPOINT_DRAW = "/v1/draw/nano-banana"
    ENDPOINT_RESULT = "/v1/draw/result"
    COST_MAP = GrsaiNanoBananaService.COST_MAP
    STYLE_PROMPTS = GrsaiNanoBananaService.STYLE_PROMPTS
    
    def __init__(self, api_key: str = None, use_china_host: bool = True):
        self.api_key = api_key or os.getenv("GRSAI_API_KEY")
        if not self.api_key:
            raise ValueError("GRSAI_API_KEY is required")
        
        self.base_url = self.HOST_CHINA if use_china_host else GrsaiNanoBananaService.HOST_OVERSEAS
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _build_prompt(self, prompt: str, style: str = None, room_type: str = None) -> str:
        """构建完整的prompt，优先使用prompts库，强制加入结构锁定"""
        try:
            from prompts import PromptBuilder, STYLE_PROMPTS, STRUCT_LOCK_HARD
            
            struct_lock = STRUCT_LOCK_HARD.get("zh", "")
            
            if room_type and style:
                result = PromptBuilder.build_prompt(
                    room_type=room_type,
                    style=style,
                    custom_description=prompt,
                    language="zh",
                    quality_level="high"
                )
                return result["prompt"]
            
            if style and style in STYLE_PROMPTS:
                style_data = STYLE_PROMPTS[style]
                style_prompt = style_data.get("prompt_zh", style_data.get("prompt", ""))
                return f"{struct_lock}，{style_prompt}，{prompt}"
            
            return f"{struct_lock}，{prompt}"
                
        except ImportError:
            struct_lock = "禁止改动几何结构与透视：不新增/移动门窗，不改变墙体边界，垂直线保持笔直，镜头位置不变，保持原有房间格局和比例"
            if style and style in self.STYLE_PROMPTS:
                return f"{struct_lock}，{self.STYLE_PROMPTS[style]}，{prompt}"
            return f"{struct_lock}，{prompt}"
    
    def generate(
        self,
        prompt: str,
        image_url: str = None,
        model: str = "nano-banana-pro",
        style: str = None,
        room_type: str = None,
        aspect_ratio: str = "auto",
        image_size: str = "1K",
        max_wait: float = 180.0,
    ) -> GenerationResult:
        """同步生成图片"""
        import requests
        
        start_time = time.time()
        full_prompt = self._build_prompt(prompt, style, room_type)
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
            "webHook": "-1",
        }
        
        if image_url:
            payload["urls"] = [image_url] if isinstance(image_url, str) else image_url
        
        try:
            # 提交任务
            url = f"{self.base_url}{self.ENDPOINT_DRAW}"
            resp = requests.post(url, headers=self.headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            task_id = data.get("data", {}).get("id", "")
            
            if not task_id:
                raise Exception("Failed to get task ID")
            
            # 轮询
            result = self._poll_result(task_id, max_wait)
            
            elapsed = time.time() - start_time
            images = [r["url"] for r in result.get("results", [])]
            content = result.get("results", [{}])[0].get("content", "")
            
            cost = self.COST_MAP.get(NanoBananaModel(model), 0.18) if model in [m.value for m in NanoBananaModel] else 0.18
            
            return GenerationResult(
                success=True,
                task_id=task_id,
                images=images,
                content=content,
                cost=cost,
                elapsed_seconds=elapsed
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e),
                elapsed_seconds=time.time() - start_time
            )
    
    def _poll_result(self, task_id: str, max_wait: float = 180.0) -> dict:
        import requests
        
        url = f"{self.base_url}{self.ENDPOINT_RESULT}"
        waited = 0.0
        
        while waited < max_wait:
            resp = requests.post(url, headers=self.headers, json={"id": task_id}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get("code") == -22:
                raise Exception("Task not found")
            
            result = data.get("data", {})
            status = result.get("status")
            
            if status == "succeeded":
                return result
            elif status == "failed":
                raise Exception(result.get("error") or "Generation failed")
            
            time.sleep(2)
            waited += 2
        
        raise Exception(f"Timeout after {max_wait}s")


# 便捷函数
async def generate_interior_design(
    image_url: str,
    room_type: str = "客厅",
    style: str = "nanobanana",
    api_key: str = None,
) -> GenerationResult:
    """
    便捷函数：生成室内装修效果图
    
    Args:
        image_url: 毛胚房图片URL
        room_type: 房间类型 (客厅/卧室/厨房/卫生间等)
        style: 风格 (nanobanana/nanobanana_A/nanobanana_B/nanobanana_C/cream_style/modern_chinese)
        api_key: API密钥
    
    Returns:
        GenerationResult
    
    使用示例:
        result = await generate_interior_design(
            image_url="https://example.com/raw_room.jpg",
            room_type="客厅",
            style="nanobanana"
        )
        if result.success:
            print(f"生成成功: {result.images}")
    """
    service = GrsaiNanoBananaService(api_key=api_key)
    prompt = f"将这个毛胚房装修成精美的{room_type}，专业室内设计效果图"
    
    return await service.generate(
        prompt=prompt,
        image_url=image_url,
        style=style,
        model=NanoBananaModel.PRO,
        image_size=ImageSize.SIZE_1K
    )


# 测试代码
if __name__ == "__main__":
    async def test():
        # 需要设置环境变量 GRSAI_API_KEY
        service = GrsaiNanoBananaService()
        
        # 测试文生图
        result = await service.generate(
            prompt="现代简约风格客厅，奶油色调，温馨舒适",
            style="nanobanana",
            model=NanoBananaModel.PRO
        )
        
        if result.success:
            print(f"✅ 生成成功!")
            print(f"   任务ID: {result.task_id}")
            print(f"   图片: {result.images}")
            print(f"   耗时: {result.elapsed_seconds:.1f}s")
            print(f"   成本: ¥{result.cost}")
        else:
            print(f"❌ 生成失败: {result.error}")
    
    asyncio.run(test())
