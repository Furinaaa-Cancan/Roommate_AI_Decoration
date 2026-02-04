"""
SVD 云端 API 测试脚本（Replicate）

使用方法：
1. 安装: pip install replicate
2. 设置环境变量: export REPLICATE_API_TOKEN=your_token
3. 运行: python -m services.video_generation.test_svd_api
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.video_generation.svd_service import SVDService


async def test_svd_api():
    """测试 SVD API 模式"""
    
    # 检查 API Token
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("❌ 请设置 REPLICATE_API_TOKEN 环境变量")
        print("   获取 Token: https://replicate.com/account/api-tokens")
        print("   设置方法: export REPLICATE_API_TOKEN=r8_xxxxxx")
        return
    
    # 测试图片
    test_image = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "test_images", "output", "wabi_sabi_living_room_4k.png"
    )
    
    if not os.path.exists(test_image):
        print(f"测试图片不存在: {test_image}")
        return
    
    print(f"使用测试图片: {test_image}")
    print("-" * 50)
    
    # 使用 API 模式
    service = SVDService(mode="api")
    
    print("开始生成空间氛围视频（云端 API）...")
    result = await service.generate_video(image_path=test_image)
    
    print("-" * 50)
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   视频路径: {result.video_path}")
        print(f"   帧数: {result.frames_count}")
        print(f"   时长: {result.duration_seconds:.1f} 秒")
    else:
        print(f"❌ 生成失败: {result.error}")


if __name__ == "__main__":
    asyncio.run(test_svd_api())
