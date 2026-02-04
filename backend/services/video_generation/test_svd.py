"""
SVD 视频生成测试脚本

使用方法：
1. 确保已安装依赖：pip install torch diffusers transformers accelerate
2. 准备一张室内效果图
3. 运行：python -m services.video_generation.test_svd
"""

import asyncio
import os
import sys

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.video_generation.svd_service import SVDService, VideoGenerationResult


async def test_svd_generation():
    """测试 SVD 视频生成"""
    
    # 测试图片路径（使用现有的测试图片）
    test_image = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "test_images", "output", "wabi_sabi_living_room_4k.png"
    )
    
    if not os.path.exists(test_image):
        print(f"测试图片不存在: {test_image}")
        print("请准备一张室内效果图")
        return
    
    print(f"使用测试图片: {test_image}")
    print("-" * 50)
    
    # 初始化服务（自动检测设备：MPS/CUDA/CPU）
    service = SVDService(mode="local", device="auto")
    
    # 生成视频（减少帧数以节省内存）
    print("开始生成空间氛围视频...")
    result = await service.generate_video(
        image_path=test_image,
        num_frames=14,  # 减少帧数节省内存
        fps=7,
        motion_bucket_id=80,  # 较低运动幅度
        noise_aug_strength=0.02,
        decode_chunk_size=4,  # 分块解码
        seed=42
    )
    
    print("-" * 50)
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   视频路径: {result.video_path}")
        print(f"   帧数: {result.frames_count}")
        print(f"   时长: {result.duration_seconds:.1f} 秒")
    else:
        print(f"❌ 生成失败: {result.error}")


def check_environment():
    """检查运行环境"""
    print("=" * 50)
    print("环境检查")
    print("=" * 50)
    
    gpu_available = False
    
    try:
        import torch
        print(f"PyTorch 版本: {torch.__version__}")
        
        # 检查 CUDA
        cuda_available = torch.cuda.is_available()
        print(f"CUDA 可用: {cuda_available}")
        if cuda_available:
            print(f"  CUDA 版本: {torch.version.cuda}")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            gpu_available = True
        
        # 检查 MPS (Apple Silicon)
        mps_available = torch.backends.mps.is_available()
        print(f"MPS 可用: {mps_available}")
        if mps_available:
            print("  Apple Silicon GPU 加速已启用")
            gpu_available = True
            
    except ImportError:
        print("❌ PyTorch 未安装")
        print("   Mac 请运行: pip install torch torchvision")
        return False
    
    # 检查 diffusers
    try:
        import diffusers
        print(f"Diffusers 版本: {diffusers.__version__}")
    except ImportError:
        print("❌ Diffusers 未安装")
        print("   请运行: pip install diffusers transformers accelerate")
        return False
    
    print("=" * 50)
    
    if not gpu_available:
        print("⚠️ 警告: 没有检测到 GPU，将使用 CPU（非常慢）")
    
    return True  # 允许在没有 GPU 的情况下运行（虽然很慢）


if __name__ == "__main__":
    if check_environment():
        asyncio.run(test_svd_generation())
    else:
        print("\n请先安装依赖后再运行测试")
