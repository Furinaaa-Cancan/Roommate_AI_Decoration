"""
NanoBanana AI - FastAPI 服务入口
支持 Grsai Nano Banana API
"""
import os
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件
import uuid
import asyncio
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from pathlib import Path
import json

app = FastAPI(
    title="NanoBanana AI",
    description="AI装修效果图生成服务 - 毛胚房秒变精装修",
    version="0.2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务 - 用于提供 mask 图片和上传的图片
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
(static_dir / "masks").mkdir(exist_ok=True)
(static_dir / "uploads").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ============ Request/Response Models ============

class GenerateRequest(BaseModel):
    image_url: HttpUrl
    room_type: str = "living_room"
    style: str = "nanobanana"
    model: str = "nano-banana-pro"  # nano-banana-fast / nano-banana-pro
    image_size: str = "4K"  # 1K / 2K / 4K
    aspect_ratio: str = "auto"
    user_id: Optional[int] = None  # 用户ID，用于积分扣除

class GenerateResponse(BaseModel):
    success: bool
    task_id: str
    message: str
    images: List[str] = []
    processing_time: float = 0
    cost_rmb: float = 0
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# ============ API Endpoints ============

@app.get("/", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="0.1.0"
    )

@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...), request: Request = None):
    """
    上传图片到服务器，返回持久化URL
    """
    import aiofiles
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="不支持的图片格式")
    
    # 生成唯一文件名
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = static_dir / "uploads" / filename
    
    # 保存文件
    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # 构建访问URL
    base_url = str(request.base_url).rstrip('/') if request else "http://localhost:8000"
    image_url = f"{base_url}/static/uploads/{filename}"
    
    return {
        "success": True,
        "url": image_url,
        "filename": filename
    }

@app.post("/api/v1/generate", response_model=GenerateResponse)
async def generate_design(request: GenerateRequest):
    """
    生成装修效果图 (同步接口，等待完成后返回)
    
    - **image_url**: 毛胚房图片URL (必须可公开访问)
    - **room_type**: 房间类型 (living_room, bedroom, kitchen, bathroom, etc.)
    - **style**: 风格 (nanobanana, nanobanana_A, nanobanana_B, nanobanana_C, cream_style, modern_chinese)
    - **model**: 模型 (nano-banana-fast, nano-banana-pro)
    - **image_size**: 分辨率 (1K, 2K, 4K)
    - **user_id**: 用户ID，用于积分扣除
    """
    from services.grsai_service import GrsaiNanoBananaService
    from services.auth_service import auth_service
    
    # 检查用户积分
    if request.user_id:
        user = auth_service.get_user(request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        if user.credits < 1:
            raise HTTPException(status_code=402, detail="积分不足，请充值")
    
    try:
        service = GrsaiNanoBananaService()
        
        # 房间类型映射
        room_names = {
            "living_room": "客厅", "bedroom": "卧室", "master_bedroom": "主卧",
            "kitchen": "厨房", "bathroom": "卫生间", "dining_room": "餐厅",
            "study": "书房", "balcony": "阳台"
        }
        room_name = room_names.get(request.room_type, "房间")
        prompt = f"将这个毛胚房装修成精美的{room_name}，专业室内设计效果图"
        
        result = await service.generate(
            prompt=prompt,
            image_url=str(request.image_url),
            style=request.style,
            room_type=request.room_type,  # 使用专业prompt库
            model=request.model,
            image_size=request.image_size,
            aspect_ratio=request.aspect_ratio
        )
        
        # 生成成功后扣除积分
        if result.success and request.user_id:
            auth_service.use_credits(request.user_id, 1)
        
        return GenerateResponse(
            success=result.success,
            task_id=result.task_id or str(uuid.uuid4())[:8],
            message="生成成功" if result.success else "生成失败",
            images=result.images or [],
            processing_time=result.elapsed_seconds,
            cost_rmb=result.cost,
            error=result.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/generate/stream")
async def generate_design_stream(request: GenerateRequest):
    """
    流式生成装修效果图 (实时返回进度)
    
    返回 Server-Sent Events 格式的进度数据
    """
    from services.grsai_service import GrsaiNanoBananaService
    
    service = GrsaiNanoBananaService()
    
    room_names = {
        "living_room": "客厅", "bedroom": "卧室", "master_bedroom": "主卧",
        "kitchen": "厨房", "bathroom": "卫生间", "dining_room": "餐厅",
        "study": "书房", "balcony": "阳台"
    }
    room_name = room_names.get(request.room_type, "房间")
    prompt = f"将这个毛胚房装修成精美的{room_name}，专业室内设计效果图"
    
    async def event_generator():
        try:
            async for progress in service.generate_stream(
                prompt=prompt,
                image_url=str(request.image_url),
                style=request.style,
                room_type=request.room_type,
                model=request.model,
                image_size=request.image_size,
                aspect_ratio=request.aspect_ratio
            ):
                data = {
                    "id": progress.id,
                    "progress": progress.progress,
                    "status": progress.status.value,
                    "images": [r.get("url") for r in progress.results] if progress.results else [],
                    "error": progress.error
                }
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/api/v1/styles")
async def list_styles():
    """获取可用风格列表"""
    return {
        "styles": [
            {"id": "nanobanana", "name": "NanoBanana 经典", "description": "温暖中性色调，奶油米色，自然木材"},
            {"id": "nanobanana_A", "name": "北欧极简", "description": "奶油白墙，浅橡木地板，简洁线条"},
            {"id": "nanobanana_B", "name": "现代轻奢", "description": "暖灰色调，胡桃木元素，金色点缀"},
            {"id": "nanobanana_C", "name": "日式侘寂", "description": "自然材质，大地色系，禅意氛围"},
            {"id": "cream_style", "name": "奶油风", "description": "浅色系，柔和温暖，法式慵懒"},
            {"id": "modern_chinese", "name": "新中式", "description": "传统与现代结合，木质元素，禅意空间"},
        ]
    }


@app.get("/api/v1/models")
async def list_models():
    """获取可用模型列表"""
    return {
        "models": [
            {"id": "nano-banana-fast", "name": "快速版", "description": "速度快，适合预览", "cost": 0.10},
            {"id": "nano-banana", "name": "标准版", "description": "平衡速度和质量", "cost": 0.15},
            {"id": "nano-banana-pro", "name": "Pro版", "description": "高质量，推荐使用", "cost": 0.18},
            {"id": "nano-banana-pro-vip", "name": "Pro VIP", "description": "最高质量，支持2K", "cost": 0.25},
            {"id": "nano-banana-pro-4k-vip", "name": "Pro 4K VIP", "description": "4K超清输出", "cost": 0.50},
        ]
    }

@app.get("/api/v1/room-types")
async def list_room_types():
    """获取房间类型列表"""
    return {
        "room_types": [
            {"id": "living_room", "name": "客厅"},
            {"id": "bedroom", "name": "卧室"},
            {"id": "master_bedroom", "name": "主卧"},
            {"id": "kitchen", "name": "厨房"},
            {"id": "bathroom", "name": "卫生间"},
            {"id": "dining_room", "name": "餐厅"},
            {"id": "study", "name": "书房"},
            {"id": "balcony", "name": "阳台"}
        ]
    }


# ============ 分割 API ============

class SegmentRequest(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None  # 支持 base64 输入
    labels: Optional[List[str]] = None  # 要检测的标签，默认使用室内家具

class SegmentPointRequest(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    x: int
    y: int
    
class SegmentedObjectResponse(BaseModel):
    label: str
    label_zh: str
    mask_url: str  # 彩色 mask（用于可视化）
    inpaint_mask_url: str = ""  # 黑白 mask URL（用于 inpaint）
    inpaint_mask_base64: str = ""  # 黑白 mask base64（直接传递给 API）
    bbox: List[int] = []
    confidence: float = 0.0

class SegmentResponse(BaseModel):
    success: bool
    objects: List[SegmentedObjectResponse] = []
    annotated_image_url: Optional[str] = None
    combined_mask_url: Optional[str] = None
    processing_time: float = 0
    error: Optional[str] = None


@app.post("/api/v1/segment", response_model=SegmentResponse)
async def segment_furniture(request: SegmentRequest):
    """
    分割图片中的家具
    
    自动识别沙发、桌子、椅子、灯具等室内物品，返回每个物品的 mask
    用于后续的局部替换功能
    支持 image_url 或 image_base64 输入
    使用本地 SAM 模型，无需 API 费用
    """
    from services.local_sam_service import LocalSAMService
    
    if not request.image_url and not request.image_base64:
        raise HTTPException(status_code=400, detail="需要提供 image_url 或 image_base64")
    
    try:
        service = LocalSAMService()
        result = service.segment_furniture(
            image_url=request.image_url,
            image_base64=request.image_base64,
            labels=request.labels
        )
        
        objects = []
        for obj in result.objects:
            objects.append(SegmentedObjectResponse(
                label=obj.label,
                label_zh=service.get_label_zh(obj.label),
                mask_url=obj.mask_url,
                inpaint_mask_url=obj.inpaint_mask_url,
                inpaint_mask_base64=obj.inpaint_mask_base64,
                bbox=obj.bbox,
                confidence=obj.confidence
            ))
        
        return SegmentResponse(
            success=result.success,
            objects=objects,
            annotated_image_url=result.annotated_image_url,
            combined_mask_url=result.combined_mask_url,
            processing_time=result.elapsed_seconds,
            error=result.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/segment/point", response_model=SegmentResponse)
async def segment_at_point(request: SegmentPointRequest):
    """
    点击分割 - 在指定坐标位置分割物体
    
    用户点击图片某个位置，返回该位置物体的 mask
    使用本地 SAM 模型
    """
    from services.local_sam_service import LocalSAMService
    
    try:
        service = LocalSAMService()
        result = service.segment_at_point(
            image_url=request.image_url,
            image_base64=request.image_base64,
            x=request.x,
            y=request.y
        )
        
        objects = []
        for obj in result.objects:
            objects.append(SegmentedObjectResponse(
                label=obj.label,
                label_zh=obj.label_zh or "选中区域",
                mask_url=obj.mask_url,
                inpaint_mask_url=obj.inpaint_mask_url or "",
                inpaint_mask_base64=obj.inpaint_mask_base64 or "",
                bbox=obj.bbox,
                confidence=obj.confidence
            ))
        
        return SegmentResponse(
            success=result.success,
            objects=objects,
            combined_mask_url=result.combined_mask_url,
            processing_time=result.elapsed_seconds,
            error=result.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ 局部重绘 API ============

class InpaintRequest(BaseModel):
    image_url: str  # 原图URL
    mask_url: str   # 主 mask URL
    mask_urls: Optional[List[str]] = None  # 多个 mask URL（逐个替换）
    furniture_type: Optional[str] = None  # 家具类型
    furniture_types: Optional[List[str]] = None  # 多个家具类型（与 mask_urls 一一对应）
    style: str = "现代简约"
    custom_prompt: Optional[str] = None

class InpaintResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    processing_time: float = 0
    cost: float = 0
    error: Optional[str] = None


@app.post("/api/v1/inpaint", response_model=InpaintResponse)
async def inpaint_region(request: InpaintRequest):
    """
    局部重绘 - 使用 NanoBanana Inpaint 对选中区域进行风格替换
    
    使用 mask 指定要替换的区域，AI 会保持其他区域不变，只对 mask 区域进行重绘
    """
    from services.grsai_service import GrsaiNanoBananaService
    import base64
    from PIL import Image
    import io
    
    try:
        # 辅助函数：压缩图片并转base64
        def compress_image_base64(data: str, max_size: int = 1024) -> str:
            """压缩图片到指定最大尺寸"""
            if not data.startswith("data:"):
                return data
            
            # 提取base64数据
            header, b64_data = data.split(",", 1)
            # 清理 base64 数据：移除空白字符，处理 URL 安全编码
            b64_data = b64_data.strip().replace(' ', '+').replace('\n', '').replace('\r', '')
            # 修复 base64 padding（长度必须是4的倍数）
            missing_padding = len(b64_data) % 4
            if missing_padding:
                b64_data += '=' * (4 - missing_padding)
            
            try:
                img_bytes = base64.b64decode(b64_data)
            except Exception as e:
                print(f"[Inpaint] base64解码失败: {e}, 数据前100字符: {b64_data[:100]}")
                raise
            
            # 打开并压缩
            try:
                img = Image.open(io.BytesIO(img_bytes))
            except Exception as e:
                print(f"[Inpaint] PIL无法识别图片: {e}, 数据长度: {len(img_bytes)}, 前16字节: {img_bytes[:16]}")
                raise
            
            # 计算缩放比例
            ratio = min(max_size / img.width, max_size / img.height, 1.0)
            if ratio < 1.0:
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 转回base64
            buffer = io.BytesIO()
            img_format = "PNG" if "png" in header else "JPEG"
            img.save(buffer, format=img_format, quality=85)
            compressed_b64 = base64.b64encode(buffer.getvalue()).decode()
            
            return f"{header},{compressed_b64}"
        
        # 辅助函数：将本地URL转为base64
        def url_to_base64(url: str, prefix: str = "data:image/png;base64,") -> str:
            # 如果已经是 base64，直接返回
            if url.startswith("data:"):
                return url
            
            local_path = None
            # 处理相对路径 /static/...
            if url.startswith("/static/"):
                local_path = url.lstrip("/")  # 去掉开头的 /
            # 处理完整 URL
            elif "localhost" in url or "127.0.0.1" in url:
                local_path = url.replace("http://localhost:8000/static/", "static/")
                local_path = local_path.replace("http://127.0.0.1:8000/static/", "static/")
                local_path = local_path.replace("http://localhost:3000/static/", "static/")
            
            if local_path:
                full_path = Path(__file__).parent / local_path
                print(f"[url_to_base64] 转换路径: {url} -> {full_path}")
                if full_path.exists():
                    with open(full_path, "rb") as f:
                        return prefix + base64.b64encode(f.read()).decode()
                else:
                    print(f"[url_to_base64] 文件不存在: {full_path}")
                    # 尝试其他可能的路径
                    alt_paths = [
                        Path(__file__).parent / "static" / "masks" / Path(local_path).name,
                        Path(__file__).parent / local_path.replace("static/", ""),
                    ]
                    for alt_path in alt_paths:
                        print(f"[url_to_base64] 尝试备用路径: {alt_path}")
                        if alt_path.exists():
                            with open(alt_path, "rb") as f:
                                return prefix + base64.b64encode(f.read()).decode()
            
            print(f"[url_to_base64] 无法找到文件: {url}")
            return ""  # 返回空字符串表示失败
        
        # 合并多个 mask 的函数
        def merge_masks(mask_data_list: List[str], max_size: int = 1024) -> str:
            """合并多个黑白 mask，白色区域叠加"""
            if len(mask_data_list) == 1:
                return mask_data_list[0]
            
            merged = None
            for mask_data in mask_data_list:
                # 解析 base64
                if mask_data.startswith("data:"):
                    _, b64 = mask_data.split(",", 1)
                    b64 = b64.strip().replace(' ', '+').replace('\n', '').replace('\r', '')
                    missing = len(b64) % 4
                    if missing:
                        b64 += '=' * (4 - missing)
                    img_bytes = base64.b64decode(b64)
                    img = Image.open(io.BytesIO(img_bytes)).convert('L')
                else:
                    continue
                
                # 压缩到统一尺寸
                ratio = min(max_size / img.width, max_size / img.height, 1.0)
                if ratio < 1.0:
                    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.Resampling.LANCZOS)
                
                import numpy as np
                arr = np.array(img)
                
                if merged is None:
                    merged = arr
                else:
                    # 如果尺寸不同，调整
                    if merged.shape != arr.shape:
                        img = img.resize((merged.shape[1], merged.shape[0]), Image.Resampling.LANCZOS)
                        arr = np.array(img)
                    # 叠加白色区域（取最大值）
                    merged = np.maximum(merged, arr)
            
            if merged is None:
                return mask_data_list[0]
            
            # 转回 base64
            result_img = Image.fromarray(merged, mode='L')
            buffer = io.BytesIO()
            result_img.save(buffer, format='PNG')
            return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        
        # 准备 mask 和 furniture_type 列表
        mask_list = request.mask_urls if request.mask_urls and len(request.mask_urls) > 0 else [request.mask_url]
        furniture_list = request.furniture_types if request.furniture_types and len(request.furniture_types) > 0 else [request.furniture_type]
        
        print(f"[Inpaint] 物品数量: {len(mask_list)}, 家具类型: {furniture_list}")
        print(f"[Inpaint] 原始 mask_list: {[m[:80] if len(str(m)) > 80 else str(m) for m in mask_list]}")
        
        # 转换所有 mask 为 base64
        processed_masks = []
        for m in mask_list:
            m = str(m)
            print(f"[Inpaint] 处理 mask: {m[:100]}...")
            if not m.startswith("data:"):
                converted = url_to_base64(m)
                print(f"[Inpaint] 转换后: {converted[:100]}...")
                m = converted
            if m.startswith("data:"):
                processed_masks.append(m)
            else:
                print(f"[Inpaint] 警告: mask 转换失败，跳过: {m[:50]}")
        
        # 合并所有 mask（一次 API 调用）
        if not processed_masks:
            raise HTTPException(status_code=400, detail="没有有效的 mask 数据")
        
        merged_mask = merge_masks(processed_masks)
        print(f"[Inpaint] 合并后 mask: {merged_mask[:100]}...")
        
        if not merged_mask.startswith("data:"):
            raise HTTPException(status_code=400, detail="mask 合并失败")
        
        merged_mask = compress_image_base64(merged_mask, max_size=1024)
        
        # 处理 image_url
        image_url = str(request.image_url)
        if not image_url.startswith("data:"):
            image_url = url_to_base64(image_url, "data:image/jpeg;base64,")
        image_url = compress_image_base64(image_url, max_size=1024)
        
        # 合并所有家具类型描述
        furniture_desc = ", ".join([f for f in furniture_list if f])
        print(f"[Inpaint] 合并后家具描述: {furniture_desc}")
        
        service = GrsaiNanoBananaService()
        result = await service.inpaint(
            image_url=image_url,
            mask_url=merged_mask,
            furniture_type=furniture_desc,  # 所有物品类型
            style=request.style,
            custom_prompt=request.custom_prompt
        )
        
        return InpaintResponse(
            success=result.success,
            image_url=result.images[0] if result.images else None,
            processing_time=result.elapsed_seconds,
            cost=result.cost,
            error=result.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/inpaint/styles")
async def list_inpaint_styles():
    """获取可用的局部重绘风格"""
    return {
        "styles": [
            {"id": "现代简约", "name": "现代简约"},
            {"id": "北欧风", "name": "北欧风"},
            {"id": "轻奢", "name": "轻奢"},
            {"id": "日式", "name": "日式"},
            {"id": "工业风", "name": "工业风"},
            {"id": "新中式", "name": "新中式"},
        ]
    }


# ============ 用户认证 API ============

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class OAuthRequest(BaseModel):
    provider: str
    provider_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    membership_type: str
    credits: int

@app.post("/api/v1/auth/login", response_model=UserResponse)
async def login(request: LoginRequest, req: Request):
    """邮箱密码登录（安全版本）"""
    from services.secure_auth_service import secure_auth_service
    
    # 获取客户端IP
    client_ip = req.client.host if req.client else None
    
    user, error, token = secure_auth_service.login(request.email, request.password, client_ip)
    if error:
        raise HTTPException(status_code=401, detail=error)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        membership_type=user.membership_type,
        credits=user.credits
    )

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(request: RegisterRequest):
    """邮箱注册（安全版本）"""
    from services.secure_auth_service import secure_auth_service
    
    user, error = secure_auth_service.register(request.email, request.password, request.name)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        membership_type=user.membership_type,
        credits=user.credits
    )

@app.post("/api/v1/auth/oauth", response_model=UserResponse)
async def oauth_login(request: OAuthRequest):
    """OAuth 登录 (Google 等)"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.oauth_login(
        provider=request.provider,
        provider_id=request.provider_id,
        email=request.email,
        name=request.name,
        avatar=request.avatar
    )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        membership_type=user.membership_type,
        credits=user.credits
    )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(user_id: str = Query(..., description="用户ID")):
    """获取当前用户信息"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        membership_type=user.membership_type,
        credits=user.credits
    )


# ============ 用户信息更新 API ============

class UpdateUserRequest(BaseModel):
    user_id: str
    name: Optional[str] = None
    avatar: Optional[str] = None

@app.post("/api/v1/auth/update", response_model=UserResponse)
async def update_user(request: UpdateUserRequest):
    """更新用户信息"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.update_user(
        user_id=request.user_id,
        name=request.name,
        avatar=request.avatar
    )
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        membership_type=user.membership_type,
        credits=user.credits
    )


# ============ 积分管理 API ============

class AddCreditsRequest(BaseModel):
    user_id: str
    amount: int
    reason: str = "充值"

class UseCreditsRequest(BaseModel):
    user_id: str
    amount: int = 1
    reason: str = "AI生成"

class CreditsResponse(BaseModel):
    success: bool
    credits: int
    message: str

@app.post("/api/v1/credits/add", response_model=CreditsResponse)
async def add_credits(request: AddCreditsRequest):
    """添加积分（充值）"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.add_credits(request.user_id, request.amount)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return CreditsResponse(
        success=True,
        credits=user.credits,
        message=f"成功添加 {request.amount} 积分"
    )

@app.post("/api/v1/credits/use", response_model=CreditsResponse)
async def use_credits(request: UseCreditsRequest):
    """使用积分"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.credits < request.amount:
        return CreditsResponse(
            success=False,
            credits=user.credits,
            message=f"积分不足，当前积分: {user.credits}"
        )
    
    success, remaining = secure_auth_service.use_credits(request.user_id, request.amount)
    
    return CreditsResponse(
        success=success,
        credits=remaining,
        message=f"成功使用 {request.amount} 积分" if success else "积分扣除失败"
    )

@app.get("/api/v1/credits/{user_id}")
async def get_credits(user_id: str):
    """获取用户积分"""
    from services.secure_auth_service import secure_auth_service
    
    user = secure_auth_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "user_id": user_id,
        "credits": user.credits,
        "membership_type": user.membership_type
    }


# ============ 订单 API ============

class CreateOrderRequest(BaseModel):
    user_id: str  # 改为str支持Google OAuth的长ID
    product_type: str  # membership / credits
    product_id: str    # designer / pack_100
    pay_method: str    # wechat / alipay

class SubmitOrderRequest(BaseModel):
    transaction_id: Optional[str] = None

class AuditOrderRequest(BaseModel):
    action: str        # approve / reject
    reason: Optional[str] = None
    admin_note: Optional[str] = None

@app.post("/api/v1/orders")
async def create_order(request: CreateOrderRequest):
    """创建订单"""
    from services.order_service import order_service
    
    order, msg = order_service.create_order(
        user_id=request.user_id,
        product_type=request.product_type,
        product_id=request.product_id,
        pay_method=request.pay_method
    )
    
    if not order:
        raise HTTPException(status_code=400, detail=msg)
    
    # 如果是已存在的订单，标记一下
    is_existing = (msg == "existing")
    
    return {
        "success": True,
        "existing": is_existing,  # 告诉前端这是已存在的订单
        "data": {
            "order_no": order.order_no,
            "product_name": order.product_name,
            "base_amount": order.base_amount,
            "pay_amount": order.pay_amount,
            "price_code": order.price_code,
            "pay_method": order.pay_method,
            "qrcode_url": f"/payment/{order.pay_method}.jpg",
            "expire_at": order.expire_at.isoformat(),
            "expire_seconds": order.expire_seconds
        }
    }

@app.get("/api/v1/orders/{order_no}")
async def get_order(order_no: str, user_id: str = Query(...)):
    """获取订单详情"""
    from services.order_service import order_service
    
    order = order_service.get_order(order_no, user_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    return {
        "success": True,
        "data": {
            "order_no": order.order_no,
            "product_type": order.product_type,
            "product_id": order.product_id,
            "product_name": order.product_name,
            "base_amount": order.base_amount,
            "pay_amount": order.pay_amount,
            "price_code": order.price_code,
            "pay_method": order.pay_method,
            "status": order.status,
            "expire_at": order.expire_at.isoformat(),
            "expire_seconds": order.expire_seconds,
            "transaction_id": order.transaction_id,
            "reject_reason": order.reject_reason
        }
    }

@app.post("/api/v1/orders/{order_no}/submit")
async def submit_order(order_no: str, request: SubmitOrderRequest, user_id: str = Query(...)):
    """提交支付凭证"""
    from services.order_service import order_service
    
    success, message = order_service.submit_order(
        order_no=order_no,
        user_id=user_id,
        transaction_id=request.transaction_id
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "success": True,
        "message": message,
        "redirect_url": "/profile"
    }

@app.post("/api/v1/orders/{order_no}/cancel")
async def cancel_order(order_no: str, user_id: str = Query(...)):
    """取消订单"""
    from services.order_service import order_service
    
    success, message = order_service.cancel_order(order_no, user_id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message}

@app.get("/api/v1/orders")
async def get_user_orders(
    user_id: str = Query(...),
    status: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """获取用户订单列表"""
    from services.order_service import order_service
    
    orders = order_service.get_user_orders(user_id, status, limit)
    
    return {
        "success": True,
        "data": [{
            "order_no": o.order_no,
            "product_name": o.product_name,
            "pay_amount": o.pay_amount,
            "status": o.status,
            "created_at": o.created_at.isoformat()
        } for o in orders]
    }


# ============ 管理员订单 API ============

@app.get("/api/v1/admin/orders")
async def get_pending_orders(req: Request, limit: int = Query(default=50, le=200)):
    """获取待审核订单列表"""
    from services.order_service import order_service
    
    # 验证管理员Token
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")
    
    token = auth_header[7:]
    if not order_service.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="无效的管理员Token")
    
    orders = order_service.get_pending_orders(limit)
    
    return {
        "success": True,
        "data": [{
            "order_no": o.order_no,
            "user_id": o.user_id,
            "product_name": o.product_name,
            "pay_amount": o.pay_amount,
            "price_code": o.price_code,
            "pay_method": o.pay_method,
            "transaction_id": o.transaction_id,
            "created_at": o.created_at.isoformat()
        } for o in orders]
    }

@app.patch("/api/v1/admin/orders/{order_no}/audit")
async def audit_order(order_no: str, request: AuditOrderRequest, req: Request):
    """审核订单（通过/驳回）"""
    from services.order_service import order_service
    
    # 验证管理员Token
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")
    
    token = auth_header[7:]
    if not order_service.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="无效的管理员Token")
    
    success, message, extra = order_service.audit_order(
        order_no=order_no,
        action=request.action,
        reason=request.reason,
        admin_note=request.admin_note
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "success": True,
        "message": message,
        "data": extra
    }

@app.post("/api/v1/admin/orders/{order_no}/force-approve")
async def force_approve_order(order_no: str, req: Request):
    """强制确认订单（用于处理付错金额的情况）"""
    from services.order_service import order_service
    
    # 验证管理员Token
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")
    
    token = auth_header[7:]
    if not order_service.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="无效的管理员Token")
    
    success, message = order_service.force_approve_order(order_no)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message}

@app.post("/api/v1/admin/orders/expire-pending")
async def expire_pending_orders(req: Request):
    """过期处理（定时任务调用）"""
    from services.order_service import order_service
    
    # 验证管理员Token
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")
    
    token = auth_header[7:]
    if not order_service.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="无效的管理员Token")
    
    count = order_service.expire_pending_orders()
    
    return {"success": True, "expired_count": count}


# ============ 会员套餐信息 ============

@app.get("/api/v1/membership/plans")
async def get_membership_plans():
    """获取会员套餐列表"""
    return {
        "plans": [
            {
                "id": "free",
                "name": "免费用户",
                "price": 0,
                "credits_per_month": 5,
                "features": ["5次免费体验", "4K分辨率", "基础风格"]
            },
            {
                "id": "personal",
                "name": "个人会员",
                "price": 39,
                "credits_per_month": 50,
                "features": ["每月50次生成", "4K超清输出", "全部风格", "历史记录保存"]
            },
            {
                "id": "designer",
                "name": "设计师会员",
                "price": 99,
                "credits_per_month": 200,
                "features": ["每月200次生成", "4K超清输出", "批量生成", "优先队列", "专属客服"]
            },
            {
                "id": "enterprise",
                "name": "企业会员",
                "price": 299,
                "credits_per_month": 800,
                "features": ["每月800次生成", "API访问", "团队协作", "定制风格", "专属客户经理"]
            }
        ],
        "credit_packs": [
            {"id": "pack_10", "credits": 10, "price": 9.9},
            {"id": "pack_40", "credits": 40, "price": 29},
            {"id": "pack_100", "credits": 100, "price": 59},
            {"id": "pack_400", "credits": 400, "price": 199}
        ]
    }


# ============ 生成历史 API ============

class SaveGenerationRequest(BaseModel):
    user_id: str
    input_image_url: str
    output_image_url: str
    generation_type: str = "full"  # full / inpaint
    style: Optional[str] = None
    room_type: Optional[str] = None
    prompt: Optional[str] = None
    mask_url: Optional[str] = None
    furniture_type: Optional[str] = None
    processing_time: float = 0
    cost: float = 0

@app.post("/api/v1/generations")
async def save_generation(request: SaveGenerationRequest):
    """保存生成记录"""
    from services.generation_service import generation_service
    
    info, error = generation_service.save_generation(
        user_id=request.user_id,
        input_image_url=request.input_image_url,
        output_image_url=request.output_image_url,
        generation_type=request.generation_type,
        style=request.style,
        room_type=request.room_type,
        prompt=request.prompt,
        mask_url=request.mask_url,
        furniture_type=request.furniture_type,
        processing_time=request.processing_time,
        cost=request.cost
    )
    
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return {
        "success": True,
        "data": {
            "generation_id": info.generation_id,
            "created_at": info.created_at.isoformat()
        }
    }

@app.get("/api/v1/generations")
async def get_generations(
    user_id: str = Query(...),
    generation_type: Optional[str] = None,
    favorites_only: bool = False,
    limit: int = Query(default=50, le=100),
    offset: int = 0
):
    """获取用户生成历史"""
    from services.generation_service import generation_service
    
    records = generation_service.get_user_generations(
        user_id=user_id,
        generation_type=generation_type,
        favorites_only=favorites_only,
        limit=limit,
        offset=offset
    )
    
    return {
        "success": True,
        "data": [{
            "generation_id": r.generation_id,
            "generation_type": r.generation_type,
            "input_image_url": r.input_image_url,
            "output_image_url": r.output_image_url,
            "style": r.style,
            "room_type": r.room_type,
            "furniture_type": r.furniture_type,
            "is_favorite": r.is_favorite,
            "processing_time": r.processing_time,
            "created_at": r.created_at.isoformat()
        } for r in records]
    }

@app.get("/api/v1/generations/{generation_id}")
async def get_generation(generation_id: str, user_id: str = Query(...)):
    """获取单个生成记录"""
    from services.generation_service import generation_service
    
    info = generation_service.get_generation(generation_id, user_id)
    if not info:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return {
        "success": True,
        "data": {
            "generation_id": info.generation_id,
            "generation_type": info.generation_type,
            "input_image_url": info.input_image_url,
            "output_image_url": info.output_image_url,
            "style": info.style,
            "room_type": info.room_type,
            "prompt": info.prompt,
            "furniture_type": info.furniture_type,
            "is_favorite": info.is_favorite,
            "processing_time": info.processing_time,
            "cost": info.cost,
            "created_at": info.created_at.isoformat(),
            "completed_at": info.completed_at.isoformat() if info.completed_at else None
        }
    }

@app.post("/api/v1/generations/{generation_id}/favorite")
async def toggle_favorite(generation_id: str, user_id: str = Query(...)):
    """切换收藏状态"""
    from services.generation_service import generation_service
    
    success, message = generation_service.toggle_favorite(generation_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message}

@app.delete("/api/v1/generations/{generation_id}")
async def delete_generation(generation_id: str, user_id: str = Query(...)):
    """删除生成记录"""
    from services.generation_service import generation_service
    
    success, message = generation_service.delete_generation(generation_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message}

@app.get("/api/v1/generations/stats")
async def get_generation_stats(user_id: str = Query(...)):
    """获取用户生成统计"""
    from services.generation_service import generation_service
    
    stats = generation_service.get_user_stats(user_id)
    return {"success": True, "data": stats}


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
