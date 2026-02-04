"""
测试 Inpaint 功能
使用测试图片和手动创建的 mask 测试 GrsAI inpaint API
"""
import asyncio
import base64
import numpy as np
from PIL import Image
import io
import os

# 确保在 backend 目录下运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from services.grsai_service import GrsaiNanoBananaService


def image_to_base64(image_path: str, max_size: int = 1024) -> str:
    """将图片压缩并转换为 base64"""
    img = Image.open(image_path)
    
    # 压缩到 max_size
    ratio = min(max_size / img.width, max_size / img.height, 1.0)
    if ratio < 1.0:
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"   图片已压缩: {img.width}x{img.height}")
    
    # 转换为 JPEG（更小的文件大小）
    buffer = io.BytesIO()
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(buffer, format='JPEG', quality=85)
    data = buffer.getvalue()
    
    return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"


def create_sofa_mask(image_path: str, output_path: str, max_size: int = 1024) -> str:
    """
    创建一个简单的沙发区域 mask（压缩到与图片相同尺寸）
    基于图片分析，沙发大约在左侧 1/3 区域
    """
    img = Image.open(image_path)
    orig_width, orig_height = img.size
    
    # 压缩到 max_size（与图片压缩保持一致）
    ratio = min(max_size / orig_width, max_size / orig_height, 1.0)
    width = int(orig_width * ratio)
    height = int(orig_height * ratio)
    
    # 创建黑白 mask（白色=要编辑的区域）
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 沙发区域大约在：
    # x: 10% ~ 45% 的宽度
    # y: 40% ~ 75% 的高度
    x1, x2 = int(width * 0.08), int(width * 0.42)
    y1, y2 = int(height * 0.35), int(height * 0.75)
    
    # 白色区域 = 要替换的部分
    mask[y1:y2, x1:x2] = 255
    
    # 保存 mask
    mask_img = Image.fromarray(mask, mode='L')
    mask_img.save(output_path)
    print(f"✅ Mask 已创建: {width}x{height}")
    print(f"   沙发区域: ({x1}, {y1}) -> ({x2}, {y2})")
    
    return output_path


def mask_to_base64(mask_path: str) -> str:
    """将 mask 转换为 base64"""
    with open(mask_path, "rb") as f:
        data = f.read()
    return f"data:image/png;base64,{base64.b64encode(data).decode()}"


async def test_inpaint():
    """测试 inpaint 功能"""
    # 测试图片路径
    test_image = "test_images/output/wabi_sabi_living_room_4k.png"
    mask_output = "test_images/masks/sofa_mask.png"
    
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return
    
    print("=" * 50)
    print("🧪 测试 Inpaint 功能")
    print("=" * 50)
    
    # 1. 创建 mask
    print("\n📝 步骤 1: 创建沙发区域 mask...")
    create_sofa_mask(test_image, mask_output)
    
    # 2. 转换为 base64
    print("\n📝 步骤 2: 转换图片为 base64...")
    image_base64 = image_to_base64(test_image)
    mask_base64 = mask_to_base64(mask_output)
    print(f"   图片 base64 长度: {len(image_base64)}")
    print(f"   Mask base64 长度: {len(mask_base64)}")
    
    # 3. 调用 inpaint API
    print("\n📝 步骤 3: 调用 GrsAI Inpaint API...")
    print("   风格: 北欧风")
    print("   家具类型: sofa")
    
    try:
        service = GrsaiNanoBananaService()
        result = await service.inpaint(
            image_url=image_base64,
            mask_url=mask_base64,
            furniture_type="sofa",
            style="北欧风",
            custom_prompt="light colored scandinavian sofa, cozy and comfortable"
        )
        
        print("\n" + "=" * 50)
        if result.success:
            print("✅ Inpaint 成功!")
            print(f"   任务ID: {result.task_id}")
            print(f"   耗时: {result.elapsed_seconds:.1f}s")
            print(f"   成本: ¥{result.cost}")
            if result.images:
                print(f"   生成图片: {result.images[0][:100]}...")
                
                # 下载并保存结果
                import httpx
                output_path = "test_images/output/inpaint_result.png"
                async with httpx.AsyncClient() as client:
                    resp = await client.get(result.images[0])
                    with open(output_path, "wb") as f:
                        f.write(resp.content)
                print(f"   结果已保存到: {output_path}")
        else:
            print("❌ Inpaint 失败!")
            print(f"   错误: {result.error}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 发生异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_inpaint())
