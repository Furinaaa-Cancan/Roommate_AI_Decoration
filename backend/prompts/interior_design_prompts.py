"""
顶级室内设计 Prompt 库（毛胚房 → 精装效果图）
Premium Interior Design Prompt Library

核心逻辑：
1. 保持空间结构不变（墙体、窗户、门洞、梁柱位置完全一致）
2. 材质真实可落地（微水泥、木饰面、岩板、艺术漆、金属收口）
3. 光影真实（自然光方向、曝光、阴影）
4. 设计完整（灯光系统、收纳系统、软装系统）
5. 出图像真实摄影（不要CGI渲染感）

参考来源：ChatGPT 顶级提示词工程方案
"""

from typing import Dict, List, Tuple


# ==================== 顶级通用模板（毛胚房专用）====================

# 英文主提示词模板（更容易出国际顶级效果）
MASTER_PROMPT_EN = """Keep the original unfinished apartment structure unchanged (same walls, windows, door openings, beams and columns). Transform it into a high-end fully finished {room_type} interior design in {style} style. Clean, minimal, luxury and buildable materials: light microcement / textured plaster walls, wide-plank light oak flooring, partial stone slab or wood veneer feature wall, concealed skirting, precise metal trims, full-height custom cabinetry with handleless design, layered lighting system (linear lights + downlights + wall washer), soft natural daylight from windows with realistic shadows and reflections, correct furniture scale, premium minimal soft furnishings (linen, leather, brushed metal), airy and spacious composition, photorealistic interior photography, 24mm wide-angle, ultra-detailed, 8K, natural color grading, no CGI look"""

# 中文主提示词模板
MASTER_PROMPT_ZH = """保持原始毛胚房空间结构不变（墙体、窗户、门洞、梁柱位置完全一致），在此基础上完成{room_type}的高端精装修设计，风格为{style}，整体干净克制高级，材质真实可落地：大面积浅色微水泥/艺术漆墙面，通铺浅橡木地板，局部岩板或木饰面背景墙，隐藏踢脚线与金属收口细节，定制通顶收纳柜（无拉手），线性灯+筒灯+洗墙灯的分层照明，柔和自然日光从窗户射入，真实阴影与反射，家具比例准确，软装极简但有质感（亚麻、皮革、磨砂金属），空间通透，摄影级真实室内照片风格，24mm广角室内摄影，超清细节，8K，真实色彩，真实质感，非夸张渲染"""


# ==================== 顶级负面提示词 ====================

NEGATIVE_PROMPT = """low quality, blurry, cartoon, anime, unreal engine, 3d render, cgi, overexposed, oversaturated, distorted perspective, warped walls, broken windows, wrong layout, extra doors, duplicate furniture, messy design, cheap materials, plastic texture, unrealistic lighting, bad shadows, text, watermark, logo"""


# ==================== 3套顶级风格方案 ====================

STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    
    # ⭐ 方案A：侘寂极简（最稳高级，不翻车）
    "wabi_sabi": {
        "name": "侘寂极简",
        "name_en": "Wabi-Sabi Minimal Luxury",
        "description": "高级、克制、耐看、不翻车",
        "style_prompt": "wabi-sabi minimalism, understated luxury, muted earth tones, gray-white-beige color system, low saturation, microcement walls, natural solid wood with rounded edges, handmade ceramics, linen textiles, generous white space, warm natural light, zen tranquility, meditative calm",
        "style_prompt_zh": "侘寂极简，高级灰白米色体系，微水泥墙面，原木家具，圆角造型，低饱和度，留白，温润自然光，极简灯光系统，干净无主灯设计",
    },
    
    # ⭐ 方案B：现代极简豪宅（最像样板间）
    "modern_luxury": {
        "name": "现代极简豪宅",
        "name_en": "Modern Minimal Mansion",
        "description": "豪宅感、干净利落、很贵",
        "style_prompt": "modern minimal luxury mansion, large format stone slab feature wall, ultra-narrow metal trims (3mm), floor-to-ceiling integrated cabinetry, floating TV console, hidden LED strips, low modular sofa, glass and metal details, black-white-gray with warm wood accents, extreme cleanliness and precision",
        "style_prompt_zh": "大面积岩板背景墙，极窄金属收口，通顶柜体，悬浮电视柜，隐藏灯带，低矮模块沙发，玻璃与金属细节，黑白灰+木色，极致整洁",
    },
    
    # ⭐ 方案C：日式原木奶油风（最容易出温柔高级）
    "japandi_cream": {
        "name": "日式原木奶油风",
        "name_en": "Japandi Creamy Wood",
        "description": "温馨但高级、好住、耐看",
        "style_prompt": "Japandi style, creamy white walls, light honey oak flooring, rounded furniture shapes, oatmeal linen sofa, curved armchairs, rattan and cane details, soft diffused lighting, paper lantern accents, indoor plants in ceramic planters, warm inviting atmosphere, Instagram-worthy yet livable",
        "style_prompt_zh": "奶油白墙面，浅橡木地板，圆润家具，布艺沙发，亚麻窗帘，藤编细节，柔光氛围灯，温暖自然光，舒适生活感",
    },
    
    # 现代简约
    "modern": {
        "name": "现代简约",
        "name_en": "Modern Minimalist",
        "description": "干净整洁、功能主义",
        "style_prompt": "modern minimalist, clean geometric lines, neutral color palette, white and light gray walls, light oak flooring, functional furniture, hidden storage, recessed lighting, uncluttered space",
        "style_prompt_zh": "现代简约，干净线条，中性色调，白色墙面，橡木地板，功能性家具，隐藏收纳，嵌入式灯光",
    },
    
    # 北欧风格
    "scandinavian": {
        "name": "北欧风格",
        "name_en": "Scandinavian Nordic",
        "description": "温馨舒适、自然明亮",
        "style_prompt": "Scandinavian Nordic hygge, white painted walls, light birch wood flooring, natural wood furniture, soft gray and white tones, wool throws, sheepskin rugs, ceramic vases, indoor plants, pendant lights with warm glow, candle ambiance, cozy and bright",
        "style_prompt_zh": "北欧风格，白色墙面，浅色木地板，自然木质家具，柔和灰白色调，羊毛毯，陶瓷花瓶，绿植，温暖吊灯，蜡烛氛围",
    },
    
    # 新中式
    "new_chinese": {
        "name": "新中式",
        "name_en": "Modern Chinese",
        "description": "东方意境、现代演绎",
        "style_prompt": "modern new Chinese style, ink wash color palette (black white gray), dark walnut wood furniture, Ming dynasty inspired silhouettes, Chinese landscape painting, porcelain vases, bamboo elements, bronze hardware, symmetrical balance, refined oriental elegance",
        "style_prompt_zh": "新中式，水墨色调，深色胡桃木家具，明式轮廓，山水画，青瓷花瓶，竹元素，铜质五金，对称平衡，东方雅韵",
    },
    
    # 轻奢风格
    "luxury": {
        "name": "轻奢风格",
        "name_en": "Light Luxury",
        "description": "精致高端、低调奢华",
        "style_prompt": "light luxury, understated opulence, Italian marble accents, brushed brass and gold details, velvet upholstery, herringbone oak flooring, Venetian plaster walls, designer furniture, crystal or modern chandelier, champagne and charcoal palette",
        "style_prompt_zh": "轻奢风格，低调奢华，意大利大理石，拉丝黄铜细节，丝绒面料，人字拼地板，艺术漆墙面，设计师家具，现代吊灯",
    },
    
    # 奶油风
    "cream": {
        "name": "奶油风",
        "name_en": "Cream Style",
        "description": "柔和温暖、治愈系",
        "style_prompt": "cream style, soft warm aesthetic, creamy white walls, ivory and beige palette, light caramel wood, curved rounded furniture, bouclé fabric sofa, arched mirrors, dried pampas grass, soft diffused lighting, gentle feminine atmosphere",
        "style_prompt_zh": "奶油风，柔和温暖，奶白色墙面，米色调，浅焦糖木色，圆润家具，泰迪绒沙发，拱形镜，干花装饰，柔光",
    },
    
    # 工业风格
    "industrial": {
        "name": "工业风格",
        "name_en": "Industrial Loft",
        "description": "粗犷原始、都市感",
        "style_prompt": "industrial loft, exposed brick walls, raw concrete floors, steel beams, large factory windows, Edison bulb pendant lights, distressed leather sofa, reclaimed wood, metal pipe details, urban warehouse aesthetic",
        "style_prompt_zh": "工业风格，裸露砖墙，水泥地面，钢梁，大窗户，爱迪生灯泡，皮质沙发，做旧木材，金属管道细节",
    },
}


# ==================== 房间类型 ====================

ROOM_TYPES: Dict[str, Dict[str, str]] = {
    "living_room": {"name": "客厅", "name_en": "living room"},
    "bedroom": {"name": "卧室", "name_en": "bedroom"},
    "master_bedroom": {"name": "主卧", "name_en": "master bedroom"},
    "kitchen": {"name": "厨房", "name_en": "kitchen"},
    "bathroom": {"name": "卫生间", "name_en": "bathroom"},
    "dining_room": {"name": "餐厅", "name_en": "dining room"},
    "study": {"name": "书房", "name_en": "study room"},
    "balcony": {"name": "阳台", "name_en": "balcony"},
    "entrance": {"name": "玄关", "name_en": "entrance hall"},
    "children_room": {"name": "儿童房", "name_en": "children's room"},
}


# ==================== Prompt 构建器 ====================

class PromptBuilder:
    """顶级 Prompt 构建器"""
    
    @staticmethod
    def build_prompt(
        room_type: str,
        style: str,
        custom_description: str = None,
        language: str = "en",
        quality_level: str = "high",
    ) -> Dict[str, str]:
        """
        构建完整的正向和负向提示词
        
        Args:
            room_type: 房间类型 (living_room, bedroom, etc.)
            style: 设计风格 (wabi_sabi, modern_luxury, japandi_cream, etc.)
            custom_description: 用户自定义描述
            language: 语言 (zh/en)
            quality_level: 质量级别
        
        Returns:
            Dict with 'prompt', 'negative_prompt', 'style_name', 'room_name'
        """
        # 获取风格和房间数据
        style_data = STYLE_PRESETS.get(style, STYLE_PRESETS["wabi_sabi"])
        room_data = ROOM_TYPES.get(room_type, ROOM_TYPES["living_room"])
        
        # 选择语言
        if language == "zh":
            room_name = room_data["name"]
            style_name = style_data["name"]
            style_prompt = style_data.get("style_prompt_zh", style_data["style_prompt"])
            base_prompt = MASTER_PROMPT_ZH.format(room_type=room_name, style=style_name)
        else:
            room_name = room_data["name_en"]
            style_name = style_data["name_en"]
            style_prompt = style_data["style_prompt"]
            base_prompt = MASTER_PROMPT_EN.format(room_type=room_name, style=style_name)
        
        # 组合最终prompt
        prompt_parts = []
        
        # 用户自定义描述放最前面
        if custom_description:
            prompt_parts.append(custom_description)
        
        # 主模板
        prompt_parts.append(base_prompt)
        
        # 风格特定增强词
        prompt_parts.append(style_prompt)
        
        final_prompt = ", ".join(prompt_parts)
        
        return {
            "prompt": final_prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "style_name": style_data["name"],
            "style_name_en": style_data["name_en"],
            "room_name": room_data["name"],
            "room_name_en": room_data["name_en"],
            "description": style_data.get("description", ""),
        }
    
    @staticmethod
    def get_style_list(language: str = "zh") -> List[Dict]:
        """获取所有可用风格列表"""
        return [
            {
                "id": k,
                "name": v["name"],
                "name_en": v["name_en"],
                "description": v.get("description", ""),
            }
            for k, v in STYLE_PRESETS.items()
        ]
    
    @staticmethod
    def get_room_list(language: str = "zh") -> List[Dict]:
        """获取所有房间类型列表"""
        return [
            {"id": k, "name": v["name"], "name_en": v["name_en"]}
            for k, v in ROOM_TYPES.items()
        ]


# ==================== 便捷函数 ====================

def generate_prompt(
    room_type: str = "living_room",
    style: str = "wabi_sabi",
    description: str = None,
    language: str = "en",
) -> Tuple[str, str]:
    """
    快速生成正向和负向提示词
    
    Returns:
        Tuple of (positive_prompt, negative_prompt)
    """
    result = PromptBuilder.build_prompt(
        room_type=room_type,
        style=style,
        custom_description=description,
        language=language,
    )
    return result["prompt"], result["negative_prompt"]


def get_negative_prompt() -> str:
    """获取通用负向提示词"""
    return NEGATIVE_PROMPT


# ==================== Legacy exports (兼容旧代码) ====================

STYLE_PROMPTS = {k: v["style_prompt"] for k, v in STYLE_PRESETS.items()}
ROOM_PROMPTS = {k: v["name"] for k, v in ROOM_TYPES.items()}
STYLE_TEMPLATES = STYLE_PRESETS
ROOM_TEMPLATES = ROOM_TYPES
QUALITY_POSITIVE = "photorealistic interior photography, 8K, ultra-detailed, natural color grading"
QUALITY_NEGATIVE = NEGATIVE_PROMPT
QUALITY_KEYWORDS = {"positive": QUALITY_POSITIVE, "negative": QUALITY_NEGATIVE}
NEGATIVE_PROMPTS = {"default": NEGATIVE_PROMPT}
DEFAULT_NEGATIVE = NEGATIVE_PROMPT
FULL_NEGATIVE = NEGATIVE_PROMPT


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 70)
    print("顶级室内设计 Prompt 库测试")
    print("=" * 70)
    
    # 测试侘寂极简
    result = PromptBuilder.build_prompt("living_room", "wabi_sabi", language="en")
    
    print(f"\n【{result['style_name']} - {result['room_name']}】")
    print(f"描述: {result['description']}")
    print(f"\n正向提示词 ({len(result['prompt'])} 字符):")
    print("-" * 70)
    print(result['prompt'])
    print(f"\n负向提示词 ({len(result['negative_prompt'])} 字符):")
    print("-" * 70)
    print(result['negative_prompt'])
    
    print("\n" + "=" * 70)
    print("可用风格:")
    for s in PromptBuilder.get_style_list():
        print(f"  ⭐ {s['id']}: {s['name']} ({s['name_en']}) - {s['description']}")
    
    print("\n可用房间:")
    for r in PromptBuilder.get_room_list():
        print(f"  - {r['id']}: {r['name']} ({r['name_en']})")
