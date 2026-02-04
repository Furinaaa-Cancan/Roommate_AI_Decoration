"""
端到端测试 - 验证整个流程能跑通
测试流程: Prompt库 → Grsai API → 生成结果

使用前:
    export GRSAI_API_KEY=your_api_key
    cd backend
    python test_e2e.py
"""
import os
import sys
import asyncio

# 测试图片
TEST_IMAGES = {
    "empty_room": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800",
    "raw_room": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
}


def test_prompt_library():
    """测试1: Prompt库"""
    print("\n" + "=" * 60)
    print("🧪 测试1: Prompt库")
    print("=" * 60)
    
    from prompts import PromptBuilder, STYLE_PROMPTS, ROOM_PROMPTS
    
    # 测试风格数量
    print(f"✅ 已加载 {len(STYLE_PROMPTS)} 种设计风格")
    print(f"✅ 已加载 {len(ROOM_PROMPTS)} 种房间类型")
    
    # 测试Prompt生成
    test_cases = [
        ("living_room", "nanobanana"),
        ("bedroom", "scandinavian"),
        ("kitchen", "modern"),
        ("bathroom", "japandi"),
        ("study", "new_chinese"),
    ]
    
    print("\n📝 Prompt生成测试:")
    for room, style in test_cases:
        result = PromptBuilder.build_prompt(room, style, language="zh")
        prompt = result["prompt"]
        print(f"  [{result['room_name']} + {result['style_name']}]")
        print(f"     {prompt[:80]}...")
    
    # 显示所有可用风格
    print("\n🎨 可用风格列表:")
    styles = PromptBuilder.get_style_list()
    for s in styles[:8]:
        print(f"  - {s['id']}: {s['name']}")
    print(f"  ... 共 {len(styles)} 种风格")
    
    print("\n✅ Prompt库测试通过!")
    return True


def test_grsai_service_init():
    """测试2: Grsai服务初始化"""
    print("\n" + "=" * 60)
    print("🧪 测试2: Grsai服务初始化")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("⚠️  未设置 GRSAI_API_KEY，跳过API测试")
        print("   请运行: export GRSAI_API_KEY=your_api_key")
        return False
    
    from services.grsai_service import GrsaiNanoBananaService, NanoBananaModel
    
    service = GrsaiNanoBananaService(api_key=api_key)
    print(f"✅ 服务初始化成功")
    print(f"   Base URL: {service.base_url}")
    print(f"   可用模型: {[m.value for m in NanoBananaModel]}")
    
    return True


async def test_grsai_generate():
    """测试3: Grsai API调用"""
    print("\n" + "=" * 60)
    print("🧪 测试3: Grsai API调用 (图生图)")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("⚠️  未设置 GRSAI_API_KEY，跳过")
        return False
    
    from services.grsai_service import GrsaiNanoBananaService
    
    service = GrsaiNanoBananaService(api_key=api_key)
    
    print(f"📷 测试图片: {TEST_IMAGES['empty_room']}")
    print(f"🏠 房间类型: 客厅")
    print(f"🎨 设计风格: NanoBanana经典")
    print(f"⏳ 正在调用API生成...")
    
    result = await service.generate(
        prompt="装修效果图",
        image_url=TEST_IMAGES["empty_room"],
        room_type="living_room",
        style="nanobanana",
        model="nano-banana-pro"
    )
    
    if result.success:
        print(f"\n✅ 生成成功!")
        print(f"   任务ID: {result.task_id}")
        print(f"   耗时: {result.elapsed_seconds:.1f}s")
        print(f"   成本: ¥{result.cost}")
        print(f"   图片数量: {len(result.images)}")
        for i, img in enumerate(result.images):
            print(f"   [{i+1}] {img[:80]}...")
        return True
    else:
        print(f"\n❌ 生成失败: {result.error}")
        return False


async def test_multiple_styles():
    """测试4: 多风格生成"""
    print("\n" + "=" * 60)
    print("🧪 测试4: 多风格生成测试")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("⚠️  未设置 GRSAI_API_KEY，跳过")
        return False
    
    from services.grsai_service import GrsaiNanoBananaService
    
    service = GrsaiNanoBananaService(api_key=api_key)
    
    # 只测试2种风格，节省API调用
    test_styles = [
        ("bedroom", "scandinavian", "北欧风卧室"),
        ("kitchen", "modern", "现代简约厨房"),
    ]
    
    results = []
    for room, style, desc in test_styles:
        print(f"\n🎨 测试: {desc}")
        result = await service.generate(
            prompt="装修效果图",
            image_url=TEST_IMAGES["empty_room"],
            room_type=room,
            style=style,
            model="nano-banana-fast"  # 用快速模型节省时间
        )
        
        if result.success:
            print(f"   ✅ 成功 | 耗时: {result.elapsed_seconds:.1f}s | 图片: {len(result.images)}")
            results.append(True)
        else:
            print(f"   ❌ 失败: {result.error}")
            results.append(False)
    
    success_count = sum(results)
    print(f"\n📊 结果: {success_count}/{len(test_styles)} 成功")
    return all(results)


def test_pipeline():
    """测试5: Pipeline流程"""
    print("\n" + "=" * 60)
    print("🧪 测试5: Pipeline完整流程")
    print("=" * 60)
    
    api_key = os.getenv("GRSAI_API_KEY")
    if not api_key:
        print("⚠️  未设置 GRSAI_API_KEY，跳过")
        return False
    
    from pipeline import NanoBananaPipeline
    
    pipeline = NanoBananaPipeline(provider="grsai", api_key=api_key)
    
    print(f"📷 测试图片: {TEST_IMAGES['empty_room']}")
    print(f"⏳ 运行Pipeline...")
    
    result = pipeline.run(
        image_url=TEST_IMAGES["empty_room"],
        room_type="living_room",
        style="nanobanana"
    )
    
    if result.success:
        print(f"\n✅ Pipeline成功!")
        print(f"   任务ID: {result.task_id}")
        print(f"   耗时: {result.processing_time:.1f}s")
        print(f"   成本: ¥{result.cost_rmb}")
        print(f"   预览图: {len(result.preview_images or [])}")
        return True
    else:
        print(f"\n❌ Pipeline失败: {result.error}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 NanoBanana AI 端到端测试")
    print("=" * 60)
    
    results = {}
    
    # 测试1: Prompt库 (不需要API)
    results["Prompt库"] = test_prompt_library()
    
    # 测试2: 服务初始化
    results["服务初始化"] = test_grsai_service_init()
    
    # 如果有API Key，继续测试API调用
    if os.getenv("GRSAI_API_KEY"):
        # 测试3: API调用
        results["API调用"] = await test_grsai_generate()
        
        # 测试4: 多风格 (可选，消耗API)
        # results["多风格生成"] = await test_multiple_styles()
        
        # 测试5: Pipeline
        results["Pipeline"] = test_pipeline()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过! 流程已跑通!")
    else:
        print("\n⚠️  部分测试未通过，请检查配置")
    
    return passed == total


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "prompt":
            test_prompt_library()
        elif test_name == "init":
            test_grsai_service_init()
        elif test_name == "api":
            asyncio.run(test_grsai_generate())
        elif test_name == "pipeline":
            test_pipeline()
        elif test_name == "styles":
            asyncio.run(test_multiple_styles())
        else:
            print(f"未知测试: {test_name}")
            print("可用测试: prompt, init, api, pipeline, styles")
    else:
        # 运行所有测试
        asyncio.run(run_all_tests())
