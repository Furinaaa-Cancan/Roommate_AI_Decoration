"""
SVD (Stable Video Diffusion) 服务
用于室内效果图 → 空间氛围视频生成

技术定位：
- 输入：单张室内效果图
- 输出：2-4秒空间氛围短视频
- 用途：风格展示、氛围预览、销售演示
- 不是：真实漫游、3D重建、精确结构

依赖：
- torch + diffusers (需要 NVIDIA GPU 12GB+)
- 或调用云端 API
"""

import os
import io
import base64
from typing import Optional, Tuple
from dataclasses import dataclass
from PIL import Image


@dataclass
class VideoGenerationResult:
    """视频生成结果"""
    success: bool
    video_path: Optional[str] = None
    video_base64: Optional[str] = None
    frames_count: int = 0
    duration_seconds: float = 0
    error: Optional[str] = None


class SVDService:
    """
    Stable Video Diffusion 服务
    
    支持两种模式：
    1. 本地推理（需要 GPU）
    2. 云端 API（Replicate）
    
    内存模式（24GB Mac 适用）：
    - "normal": 标准模式，需要 32GB+
    - "low": 低内存模式，320x192 分辨率
    - "ultra_low": 极限模式，256x144 分辨率，8帧
    """
    
    # 内存配置预设
    MEMORY_PRESETS = {
        "normal": {"size": (512, 288), "frames": 25, "chunk": 8},
        "low": {"size": (320, 192), "frames": 14, "chunk": 4},
        "ultra_low": {"size": (256, 144), "frames": 8, "chunk": 2},
    }
    
    def __init__(self, mode: str = "local", device: str = "auto", memory_mode: str = "low"):
        """
        初始化 SVD 服务
        
        Args:
            mode: "local" 或 "api"
            device: "auto" / "cuda" / "mps" / "cpu"
        """
        self.mode = mode
        self.pipe = None
        self.memory_mode = memory_mode
        self.preset = self.MEMORY_PRESETS.get(memory_mode, self.MEMORY_PRESETS["low"])
        
        # 自动检测设备
        if device == "auto":
            import torch
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
        
        print(f"[SVD] 设备: {self.device}, 内存模式: {memory_mode}")
        print(f"[SVD] 预设: {self.preset['size']}, {self.preset['frames']}帧")
        
        # 输出目录
        self.output_dir = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "static", "videos"
        )
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _load_pipeline(self):
        """懒加载 SVD pipeline（节省内存）"""
        if self.pipe is not None:
            return
        
        try:
            import torch
            from diffusers import StableVideoDiffusionPipeline
            from diffusers.utils import export_to_video
            
            print("[SVD] 加载模型中...")
            
            # 加载模型，启用低内存模式
            if self.device == "mps":
                # MPS 模式：使用 float16（新版 PyTorch 支持）
                self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                    "stabilityai/stable-video-diffusion-img2vid-xt",
                    torch_dtype=torch.float16,
                    variant="fp16",
                    low_cpu_mem_usage=True,
                )
                self.pipe.to(self.device)
                
                # 启用内存优化
                self.pipe.enable_attention_slicing()  # 分块计算 attention
                
                print("[SVD] MPS 模式，启用内存优化")
            else:
                # CUDA 模式：使用 float16 + CPU offload
                self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                    "stabilityai/stable-video-diffusion-img2vid-xt",
                    torch_dtype=torch.float16,
                    variant="fp16",
                    low_cpu_mem_usage=True,
                )
                self.pipe.to(self.device)
                if self.device == "cuda":
                    self.pipe.enable_model_cpu_offload()
                self.pipe.enable_attention_slicing()
            
            print(f"[SVD] 模型加载完成 (设备: {self.device})")
            
        except ImportError as e:
            raise RuntimeError(
                f"缺少依赖: {e}\n"
                "请安装: pip install torch diffusers transformers accelerate"
            )
        except Exception as e:
            raise RuntimeError(f"加载 SVD 模型失败: {e}")
    
    def _preprocess_image(
        self, 
        image: Image.Image, 
        target_size: Tuple[int, int] = None
    ) -> Image.Image:
        """预处理图片到 SVD 尺寸"""
        # 使用预设分辨率
        if target_size is None:
            target_size = self.preset["size"]
        
        # 计算缩放比例，保持宽高比
        w, h = image.size
        target_w, target_h = target_size
        
        ratio = min(target_w / w, target_h / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        
        # 缩放
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 创建目标尺寸画布并居中粘贴
        canvas = Image.new('RGB', target_size, (0, 0, 0))
        offset_x = (target_w - new_w) // 2
        offset_y = (target_h - new_h) // 2
        canvas.paste(image, (offset_x, offset_y))
        
        return canvas
    
    async def generate_video(
        self,
        image_path: Optional[str] = None,
        image_base64: Optional[str] = None,
        num_frames: int = None,  # None = 使用预设
        fps: int = 7,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.02,
        decode_chunk_size: int = None,  # None = 使用预设
        seed: Optional[int] = None,
    ) -> VideoGenerationResult:
        """
        从图片生成空间氛围视频
        
        Args:
            image_path: 图片路径
            image_base64: 或 base64 编码的图片
            num_frames: 帧数（25帧 ≈ 3.5秒 @7fps）
            fps: 帧率
            motion_bucket_id: 运动幅度 (1-255)，127 为中等
            noise_aug_strength: 噪声强度，越低越稳定
            decode_chunk_size: 解码批次大小（降低显存）
            seed: 随机种子（可复现）
            
        Returns:
            VideoGenerationResult
        """
        try:
            # 加载图片
            if image_path:
                image = Image.open(image_path).convert('RGB')
            elif image_base64:
                if image_base64.startswith('data:'):
                    _, image_base64 = image_base64.split(',', 1)
                image_data = base64.b64decode(image_base64)
                image = Image.open(io.BytesIO(image_data)).convert('RGB')
            else:
                return VideoGenerationResult(
                    success=False, 
                    error="请提供 image_path 或 image_base64"
                )
            
            # 预处理
            image = self._preprocess_image(image)
            print(f"[SVD] 图片尺寸: {image.size}")
            
            # 使用预设值
            if num_frames is None:
                num_frames = self.preset["frames"]
            if decode_chunk_size is None:
                decode_chunk_size = self.preset["chunk"]
            
            print(f"[SVD] 参数: {num_frames}帧, chunk={decode_chunk_size}")
            
            if self.mode == "local":
                return await self._generate_local(
                    image, num_frames, fps, motion_bucket_id,
                    noise_aug_strength, decode_chunk_size, seed
                )
            else:
                return await self._generate_api(image)
                
        except Exception as e:
            return VideoGenerationResult(success=False, error=str(e))
    
    async def _generate_local(
        self,
        image: Image.Image,
        num_frames: int,
        fps: int,
        motion_bucket_id: int,
        noise_aug_strength: float,
        decode_chunk_size: int,
        seed: Optional[int],
    ) -> VideoGenerationResult:
        """本地 GPU 推理"""
        import torch
        from diffusers.utils import export_to_video
        
        self._load_pipeline()
        
        # 设置随机种子
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        
        print(f"[SVD] 开始生成 {num_frames} 帧视频...")
        
        # 生成帧
        frames = self.pipe(
            image,
            num_frames=num_frames,
            motion_bucket_id=motion_bucket_id,
            noise_aug_strength=noise_aug_strength,
            decode_chunk_size=decode_chunk_size,
            generator=generator,
        ).frames[0]
        
        # 保存视频
        import time
        output_filename = f"svd_{int(time.time())}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        export_to_video(frames, output_path, fps=fps)
        print(f"[SVD] 视频已保存: {output_path}")
        
        # 转 base64
        with open(output_path, 'rb') as f:
            video_base64 = base64.b64encode(f.read()).decode()
        
        duration = num_frames / fps
        
        return VideoGenerationResult(
            success=True,
            video_path=output_path,
            video_base64=f"data:video/mp4;base64,{video_base64}",
            frames_count=num_frames,
            duration_seconds=duration
        )
    
    async def _generate_api(self, image: Image.Image) -> VideoGenerationResult:
        """云端 API 推理（Replicate）"""
        try:
            import replicate
            import time
            
            # 图片转 base64 data URI
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            image_uri = f"data:image/png;base64,{image_base64}"
            
            print("[SVD] 调用 Replicate API...")
            start_time = time.time()
            
            # 调用 Replicate SVD 模型
            output = replicate.run(
                "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
                input={
                    "input_image": image_uri,
                    "video_length": "25_frames_with_svd_xt",
                    "sizing_strategy": "maintain_aspect_ratio",
                    "motion_bucket_id": 127,
                    "cond_aug": 0.02,
                    "fps": 7
                }
            )
            
            elapsed = time.time() - start_time
            print(f"[SVD] API 完成，耗时 {elapsed:.1f}s")
            
            # output 是视频 URL
            video_url = str(output)
            
            # 下载视频
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(video_url)
                if resp.status_code == 200:
                    output_filename = f"svd_{int(time.time())}.mp4"
                    output_path = os.path.join(self.output_dir, output_filename)
                    with open(output_path, 'wb') as f:
                        f.write(resp.content)
                    
                    video_base64 = base64.b64encode(resp.content).decode()
                    
                    return VideoGenerationResult(
                        success=True,
                        video_path=output_path,
                        video_base64=f"data:video/mp4;base64,{video_base64}",
                        frames_count=25,
                        duration_seconds=25/7
                    )
            
            return VideoGenerationResult(
                success=True,
                video_path=video_url,
                frames_count=25,
                duration_seconds=25/7
            )
            
        except ImportError:
            return VideoGenerationResult(
                success=False,
                error="请安装 replicate: pip install replicate\n并设置 REPLICATE_API_TOKEN 环境变量"
            )
        except Exception as e:
            return VideoGenerationResult(success=False, error=str(e))


# 便捷函数
async def generate_atmosphere_video(
    image_path: str,
    motion_level: str = "medium"
) -> VideoGenerationResult:
    """
    快速生成空间氛围视频
    
    Args:
        image_path: 室内效果图路径
        motion_level: "low" / "medium" / "high"
    """
    motion_map = {
        "low": 80,
        "medium": 127,
        "high": 180
    }
    
    service = SVDService()
    return await service.generate_video(
        image_path=image_path,
        motion_bucket_id=motion_map.get(motion_level, 127)
    )
