"""
测试 Grsai Nano Banana API
使用前请设置环境变量: export GRSAI_API_KEY=your_api_key
"""
import asyncio
import os

# 测试图片 (一张空房间图片)
TEST_IMAGE = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"


def test_sync():
    """同步测试"""
    from services.grsai_service import GrsaiNanoBananaServiceSync
    
    print("=" * 60)
    print("🧪 同步测试 Grsai Nano Banana API")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("❌ 请先设置 GRSAI_API_KEY 环境变量")
        print("   export GRSAI_API_KEY=your_api_key")
        return
    
    service = GrsaiNanoBananaServiceSync(api_key=api_key)
    
    print(f"📷 测试图片: {TEST_IMAGE}")
    print(f"🎨 风格: nanobanana")
    print(f"⏳ 正在生成...")
    
    result = service.generate(
        prompt="将这个毛胚房装修成精美的客厅，现代简约风格，专业室内设计效果图",
        image_url=TEST_IMAGE,
        style="nanobanana",
        model="nano-banana-pro"
    )
    
    print("\n" + "-" * 60)
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   任务ID: {result.task_id}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        print(f"   成本: ¥{result.cost}")
        print(f"   图片数: {len(result.images)}")
        for i, img in enumerate(result.images):
            print(f"   [{i+1}] {img}")
    else:
        print(f"❌ 生成失败: {result.error}")
    print("=" * 60)


async def test_async():
    """异步测试"""
    from services.grsai_service import GrsaiNanoBananaService
    
    print("=" * 60)
    print("🧪 异步测试 Grsai Nano Banana API")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("❌ 请先设置 GRSAI_API_KEY 环境变量")
        return
    
    service = GrsaiNanoBananaService(api_key=api_key)
    
    print(f"📷 测试图片: {TEST_IMAGE}")
    print(f"🎨 风格: cream_style (奶油风)")
    print(f"⏳ 正在生成...")
    
    result = await service.generate(
        prompt="将这个毛胚房装修成精美的卧室，奶油风，温馨舒适",
        image_url=TEST_IMAGE,
        style="cream_style",
        model="nano-banana-pro"
    )
    
    print("\n" + "-" * 60)
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   任务ID: {result.task_id}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        print(f"   成本: ¥{result.cost}")
        print(f"   图片: {result.images}")
    else:
        print(f"❌ 生成失败: {result.error}")
    print("=" * 60)


async def test_stream():
    """流式测试"""
    from services.grsai_service import GrsaiNanoBananaService, TaskStatus
    
    print("=" * 60)
    print("🧪 流式测试 Grsai Nano Banana API")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("❌ 请先设置 GRSAI_API_KEY 环境变量")
        return
    
    service = GrsaiNanoBananaService(api_key=api_key)
    
    print(f"📷 测试图片: {TEST_IMAGE}")
    print(f"⏳ 实时进度:")
    
    async for progress in service.generate_stream(
        prompt="现代简约客厅，北欧风格",
        image_url=TEST_IMAGE,
        model="nano-banana-pro"
    ):
        print(f"   进度: {progress.progress}% | 状态: {progress.status.value}")
        
        if progress.status == TaskStatus.SUCCEEDED:
            print(f"\n✅ 生成成功!")
            for r in progress.results:
                print(f"   图片: {r.get('url')}")
            break
        elif progress.status == TaskStatus.FAILED:
            print(f"\n❌ 生成失败: {progress.error}")
            break
    
    print("=" * 60)


def test_text_to_image():
    """纯文生图测试 (不传参考图)"""
    from services.grsai_service import GrsaiNanoBananaServiceSync
    
    print("=" * 60)
    print("🧪 文生图测试 (无参考图)")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("❌ 请先设置 GRSAI_API_KEY 环境变量")
        return
    
    service = GrsaiNanoBananaServiceSync(api_key=api_key)
    
    prompt = "一个精美的现代简约客厅，落地窗，阳光充足，米色沙发，原木茶几，绿植点缀，8K超高清"
    print(f"📝 提示词: {prompt}")
    print(f"⏳ 正在生成...")
    
    result = service.generate(
        prompt=prompt,
        model="nano-banana-pro"
    )
    
    print("\n" + "-" * 60)
    if result.success:
        print(f"✅ 生成成功!")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        print(f"   成本: ¥{result.cost}")
        for i, img in enumerate(result.images):
            print(f"   [{i+1}] {img}")
    else:
        print(f"❌ 生成失败: {result.error}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "async":
            asyncio.run(test_async())
        elif mode == "stream":
            asyncio.run(test_stream())
        elif mode == "text":
            test_text_to_image()
        else:
            test_sync()
    else:
        print("用法:")
        print("  python test_grsai.py          # 同步测试(图生图)")
        print("  python test_grsai.py async    # 异步测试")
        print("  python test_grsai.py stream   # 流式测试")
        print("  python test_grsai.py text     # 纯文生图测试")
        print()
        test_sync()
