"""
顶级室内设计 Prompt 库 v2（产品级）
Premium Interior Design Prompt Library v2 - Production Grade

核心特性：
1. task_mode: full_render / material_replace / edge_blend / furniture_add
2. engine_profile: sdxl / flux / mj / nanobanana / edit
3. quality_level: standard / high / ultra
4. prompt_sections: 分段输出，调用方可控拼接
5. materials: 参数化材质库
6. STRUCT_LOCK: 硬约束前置，防结构漂移
7. negative 按引擎+任务拆分
"""

from typing import Dict, List, Tuple, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum


# ==================== 枚举定义 ====================

class TaskMode(str, Enum):
    """任务模式"""
    FULL_RENDER = "full_render"           # 整图生成效果图
    MATERIAL_REPLACE = "material_replace" # 材质替换（墙/地/顶）
    EDGE_BLEND = "edge_blend"             # 边缘融合修复
    FURNITURE_ADD = "furniture_add"       # 软装添加


class Engine(str, Enum):
    """引擎类型"""
    SDXL = "sdxl"
    FLUX = "flux"
    MJ = "mj"
    NANOBANANA = "nanobanana"
    EDIT = "edit"


class QualityLevel(str, Enum):
    """质量级别"""
    STANDARD = "standard"
    HIGH = "high"
    ULTRA = "ultra"


# ==================== 结构锁定（硬约束，永远前置）====================

STRUCT_LOCK = {
    "en": "Do not change geometry. Do not move or add windows/doors. Keep all edges straight and aligned. Preserve the original perspective and camera position. Maintain exact room layout and proportions.",
    "zh": "禁止改动几何结构与透视：不新增/移动门窗，不改变墙体边界，垂直线保持笔直，镜头位置不变，保持原有房间格局和比例。",
}

STRUCT_LOCK_SOFT = {
    "en": "Keep the original unfinished apartment structure unchanged (same walls, windows, door openings, beams and columns).",
    "zh": "保持原始毛胚房空间结构不变（墙体、窗户、门洞、梁柱位置完全一致）。",
}


# ==================== 质量预设（分段）====================

QUALITY_PRESETS = {
    "standard": {
        "camera": "interior photography, level camera",
        "light": "natural daylight, soft shadows",
        "color": "natural white balance",
        "real": "realistic interior photo",
    },
    "high": {
        "camera": "24mm wide-angle interior photography, level camera, straight vertical lines",
        "light": "soft natural daylight from windows, realistic contact shadows, layered ambient lighting",
        "color": "natural white balance, subtle contrast, professional color grading",
        "real": "photorealistic interior photography, no CGI look, no render artifacts",
    },
    "ultra": {
        "camera": "24mm wide-angle professional interior photography, perfect level camera, razor-sharp vertical lines, architectural precision",
        "light": "soft diffused natural daylight streaming from windows, physically accurate contact shadows, layered lighting system (ambient + accent + task), golden hour warmth",
        "color": "cinematic color grading, natural white balance, rich midtones, subtle film grain, professional post-processing",
        "real": "photorealistic interior photography indistinguishable from real photo, absolutely no CGI artifacts, no render look, no synthetic feel, magazine-quality editorial shot",
    },
}


# ==================== 材质库（参数化）====================

MATERIAL_PRESETS = {
    "luxury_minimal": {
        "wall": "light microcement",
        "floor": "wide-plank light oak hardwood",
        "feature": "stone slab",
        "trim": "3mm brushed black metal",
        "ceiling": "matte white plaster",
        "cabinet": "handleless floor-to-ceiling integrated cabinetry",
    },
    "wabi_sabi": {
        "wall": "textured plaster with natural imperfections",
        "floor": "wide-plank white oak",
        "feature": "lime wash texture wall",
        "trim": "concealed skirting",
        "ceiling": "raw plaster with subtle texture",
        "cabinet": "solid wood with rounded edges",
    },
    "modern_luxury": {
        "wall": "large format porcelain slab",
        "floor": "herringbone oak parquet",
        "feature": "bookmatched marble slab",
        "trim": "ultra-narrow 3mm gold metal",
        "ceiling": "recessed cove with hidden LED",
        "cabinet": "high-gloss lacquer floor-to-ceiling",
    },
    "japandi": {
        "wall": "creamy white matte paint",
        "floor": "light honey oak wide-plank",
        "feature": "wood slat partition",
        "trim": "natural wood edge",
        "ceiling": "white with exposed wood beams",
        "cabinet": "light wood with rattan inserts",
    },
    "industrial": {
        "wall": "exposed brick",
        "floor": "polished concrete",
        "feature": "raw steel beam",
        "trim": "black iron pipe",
        "ceiling": "exposed ductwork and beams",
        "cabinet": "reclaimed wood and metal",
    },
}

DEFAULT_MATERIALS = MATERIAL_PRESETS["luxury_minimal"]


# ==================== 风格预设 ====================

STYLE_PRESETS = {
    "wabi_sabi": {
        "name": "侘寂极简",
        "name_en": "Wabi-Sabi Minimal",
        "description": "高级、克制、耐看",
        "prompt": "wabi-sabi minimalism, understated luxury, muted earth tones, gray-white-beige palette, low saturation, natural imperfections embraced, handmade ceramics, linen textiles, generous white space, warm natural light, zen tranquility",
        "materials": "wabi_sabi",
    },
    "modern_luxury": {
        "name": "现代极简豪宅",
        "name_en": "Modern Minimal Mansion",
        "description": "豪宅感、干净利落",
        "prompt": "modern minimal luxury, large format stone slab, ultra-narrow metal trims, floor-to-ceiling integrated storage, floating consoles, hidden LED strips, low modular seating, glass and metal accents, black-white-gray with warm wood, extreme precision and cleanliness",
        "materials": "modern_luxury",
    },
    "japandi_cream": {
        "name": "日式原木奶油风",
        "name_en": "Japandi Cream",
        "description": "温馨高级、好住",
        "prompt": "Japandi style, creamy white walls, light honey oak, rounded furniture shapes, oatmeal linen upholstery, curved forms, rattan and cane accents, soft diffused lighting, indoor plants in ceramic planters, warm inviting atmosphere",
        "materials": "japandi",
    },
    "modern": {
        "name": "现代简约",
        "name_en": "Modern Minimalist",
        "description": "干净整洁、功能主义",
        "prompt": "modern minimalist, clean geometric lines, neutral palette, white and light gray, light oak flooring, functional furniture, hidden storage, recessed lighting, uncluttered space",
        "materials": "luxury_minimal",
    },
    "scandinavian": {
        "name": "北欧风格",
        "name_en": "Scandinavian",
        "description": "温馨舒适、自然明亮",
        "prompt": "Scandinavian Nordic, white painted walls, light birch wood, natural wood furniture, soft gray-white tones, wool textiles, ceramic vases, indoor plants, pendant lights with warm glow, cozy and bright",
        "materials": "japandi",
    },
    "new_chinese": {
        "name": "新中式",
        "name_en": "Modern Chinese",
        "description": "东方意境、现代演绎",
        "prompt": "modern new Chinese, ink wash palette (black white gray), dark walnut furniture, Ming dynasty silhouettes, Chinese landscape elements, porcelain vases, bamboo accents, bronze hardware, symmetrical balance, oriental elegance",
        "materials": "luxury_minimal",
    },
    "luxury": {
        "name": "轻奢风格",
        "name_en": "Light Luxury",
        "description": "精致高端、低调奢华",
        "prompt": "light luxury, understated opulence, Italian marble, brushed brass details, velvet upholstery, herringbone oak, Venetian plaster, designer furniture, modern chandelier, champagne and charcoal palette",
        "materials": "modern_luxury",
    },
    "industrial": {
        "name": "工业风格",
        "name_en": "Industrial Loft",
        "description": "粗犷原始、都市感",
        "prompt": "industrial loft, exposed brick, raw concrete, steel beams, factory windows, Edison bulb pendants, distressed leather, reclaimed wood, metal pipe details, urban warehouse aesthetic",
        "materials": "industrial",
    },
}


# ==================== 房间类型 ====================

ROOM_TYPES = {
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


# ==================== 负面提示词（按引擎+任务拆分）====================

# 通用质量问题
NEGATIVE_QUALITY = "low quality, blurry, overexposed, oversaturated, underexposed, noise, artifacts, jpeg compression"

# 结构漂移（关键！）
NEGATIVE_STRUCTURE = "wrong layout, changed geometry, moved windows, extra openings, warped straight lines, distorted perspective, tilted verticals, bent edges, extra doors, missing walls, wrong room shape"

# CGI渲染感
NEGATIVE_CGI = "cartoon, anime, unreal engine, 3d render, cgi, game screenshot, digital art, illustration, painting, drawing, synthetic, fake, artificial"

# 设计问题
NEGATIVE_DESIGN = "duplicate furniture, cluttered, messy, cheap materials, plastic texture, mismatched styles, wrong scale, floating objects"

# 水印
NEGATIVE_WATERMARK = "text, watermark, logo, signature, copyright, banner, frame, border"

# 按引擎组合
NEGATIVE_BY_ENGINE = {
    "sdxl": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}, {NEGATIVE_WATERMARK}",
    "flux": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}",
    "mj": f"{NEGATIVE_CGI}, {NEGATIVE_DESIGN}, blurry, low quality",  # MJ负面词要简洁
    "nanobanana": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}, {NEGATIVE_WATERMARK}",
    "edit": f"{NEGATIVE_STRUCTURE}, visible seams, color mismatch, texture discontinuity, boundary artifacts",
}

# 按任务模式的额外负面词
NEGATIVE_BY_TASK = {
    "full_render": "",
    "material_replace": "different room layout, changed perspective, new furniture, redesigned space",
    "edge_blend": "visible boundaries, seam lines, color shift at edges, mismatched grain, texture discontinuity, unnatural transition",
    "furniture_add": "changed room structure, different flooring, altered walls, redesigned layout",
}


# ==================== 任务模式专用Prompt ====================

TASK_MODE_PROMPTS = {
    "full_render": {
        "prefix": "Transform this unfinished apartment into a high-end fully finished",
        "suffix": "interior design",
        "focus": "complete interior transformation with all design elements",
    },
    "material_replace": {
        "prefix": "Replace the surface materials in this space with",
        "suffix": "materials while keeping everything else unchanged",
        "focus": "material replacement only, preserve all other elements exactly",
    },
    "edge_blend": {
        "prefix": "Seamlessly blend the edges where new materials meet existing surfaces",
        "suffix": "",
        "focus": "seamless edge blending, continuous contact shadows, match grain and noise and color temperature, no visible boundaries, perfect transition",
    },
    "furniture_add": {
        "prefix": "Add furniture and soft furnishings to this interior space",
        "suffix": "while preserving the existing room structure and finishes",
        "focus": "furniture placement only, correct scale and proportion, proper shadows and reflections",
    },
}


# ==================== Prompt 构建结果 ====================

@dataclass
class PromptResult:
    """Prompt构建结果（结构化输出）"""
    # 完整prompt（拼接后）
    prompt: str
    negative_prompt: str
    
    # 分段输出（调用方可控拼接）
    sections: Dict[str, str] = field(default_factory=dict)
    
    # 元数据
    style_name: str = ""
    style_name_en: str = ""
    room_name: str = ""
    room_name_en: str = ""
    
    # 配置信息
    task_mode: str = ""
    engine: str = ""
    quality_level: str = ""
    
    # 材质信息
    materials: Dict[str, str] = field(default_factory=dict)
    
    # 约束信息
    constraints: List[str] = field(default_factory=list)
    
    # 推荐mask类别（用于segment）
    recommended_mask_classes: List[str] = field(default_factory=list)


# ==================== Prompt 构建器 ====================

class PromptBuilder:
    """产品级 Prompt 构建器"""
    
    @staticmethod
    def build_prompt(
        room_type: str = "living_room",
        style: str = "wabi_sabi",
        task_mode: str = "full_render",
        engine: str = "nanobanana",
        quality_level: str = "high",
        materials: Dict[str, str] = None,
        custom_description: str = None,
        language: str = "en",
        marketing_mode: bool = False,
    ) -> PromptResult:
        """
        构建完整的Prompt结果
        
        Args:
            room_type: 房间类型
            style: 设计风格
            task_mode: 任务模式 (full_render/material_replace/edge_blend/furniture_add)
            engine: 引擎类型 (sdxl/flux/mj/nanobanana/edit)
            quality_level: 质量级别 (standard/high/ultra)
            materials: 自定义材质dict，覆盖风格默认材质
            custom_description: 用户自定义描述
            language: 语言 (en/zh)
            marketing_mode: 是否启用网红审美词
        
        Returns:
            PromptResult with sections, constraints, materials, etc.
        """
        # 获取基础数据
        style_data = STYLE_PRESETS.get(style, STYLE_PRESETS["wabi_sabi"])
        room_data = ROOM_TYPES.get(room_type, ROOM_TYPES["living_room"])
        quality_data = QUALITY_PRESETS.get(quality_level, QUALITY_PRESETS["high"])
        task_data = TASK_MODE_PROMPTS.get(task_mode, TASK_MODE_PROMPTS["full_render"])
        
        # 材质：自定义 > 风格默认 > 通用默认
        style_materials_key = style_data.get("materials", "luxury_minimal")
        final_materials = MATERIAL_PRESETS.get(style_materials_key, DEFAULT_MATERIALS).copy()
        if materials:
            final_materials.update(materials)
        
        # 语言选择
        lang = "en" if language != "zh" else "zh"
        room_name = room_data["name_en"] if lang == "en" else room_data["name"]
        style_name = style_data["name_en"] if lang == "en" else style_data["name"]
        
        # ========== 分段构建 ==========
        sections = {}
        
        # 1. 结构锁定（永远第一段）
        if task_mode in ["full_render", "material_replace"]:
            sections["struct_lock"] = STRUCT_LOCK[lang]
        elif task_mode == "edge_blend":
            sections["struct_lock"] = STRUCT_LOCK[lang]  # 边缘融合也需要锁结构
        else:
            sections["struct_lock"] = STRUCT_LOCK_SOFT[lang]
        
        # 2. 任务指令
        if task_mode == "full_render":
            sections["task"] = f"{task_data['prefix']} {room_name} {task_data['suffix']} in {style_name} style"
        elif task_mode == "material_replace":
            material_desc = f"{final_materials.get('wall', 'microcement')} walls, {final_materials.get('floor', 'oak')} flooring"
            sections["task"] = f"{task_data['prefix']} {material_desc} {task_data['suffix']}"
        elif task_mode == "edge_blend":
            sections["task"] = task_data["focus"]
        elif task_mode == "furniture_add":
            sections["task"] = f"{task_data['prefix']} in {style_name} style {task_data['suffix']}"
        
        # 3. 用户自定义描述（在结构锁定后、风格前）
        if custom_description:
            sections["custom"] = custom_description
        
        # 4. 材质系统（仅full_render和material_replace）
        if task_mode in ["full_render", "material_replace"]:
            mat_parts = []
            if final_materials.get("wall"):
                mat_parts.append(f"{final_materials['wall']} walls")
            if final_materials.get("floor"):
                mat_parts.append(f"{final_materials['floor']} flooring")
            if final_materials.get("feature"):
                mat_parts.append(f"{final_materials['feature']} feature wall")
            if final_materials.get("trim"):
                mat_parts.append(f"{final_materials['trim']} trim details")
            if final_materials.get("cabinet"):
                mat_parts.append(final_materials['cabinet'])
            sections["materials"] = ", ".join(mat_parts)
        
        # 5. 风格（仅full_render和furniture_add）
        if task_mode in ["full_render", "furniture_add"]:
            sections["style"] = style_data["prompt"]
        
        # 6. 质量（分四段）
        sections["camera"] = quality_data["camera"]
        sections["light"] = quality_data["light"]
        sections["color"] = quality_data["color"]
        sections["real"] = quality_data["real"]
        
        # 边缘融合模式：只用light/color/real，不用style
        if task_mode == "edge_blend":
            sections.pop("style", None)
            sections.pop("materials", None)
        
        # 网红模式词汇（默认不启用）
        if marketing_mode and task_mode == "full_render":
            sections["marketing"] = "Instagram-worthy, Pinterest-perfect, aspirational lifestyle"
        
        # ========== 拼接策略（按引擎）==========
        if engine == "mj":
            # MJ更吃简洁语义
            ordered_keys = ["struct_lock", "task", "style", "real"]
            separator = ", "
        elif engine == "edit":
            # 编辑模型更吃分段指令
            ordered_keys = ["struct_lock", "task", "custom", "light", "color", "real"]
            separator = ". "
        else:
            # SDXL/Flux/NanoBanana
            ordered_keys = ["struct_lock", "task", "custom", "materials", "style", "camera", "light", "color", "real"]
            separator = ", "
        
        prompt_parts = [sections[k] for k in ordered_keys if k in sections and sections[k]]
        final_prompt = separator.join(prompt_parts)
        
        # ========== 负面提示词 ==========
        base_negative = NEGATIVE_BY_ENGINE.get(engine, NEGATIVE_BY_ENGINE["nanobanana"])
        task_negative = NEGATIVE_BY_TASK.get(task_mode, "")
        if task_negative:
            final_negative = f"{base_negative}, {task_negative}"
        else:
            final_negative = base_negative
        
        # ========== 约束信息 ==========
        constraints = [
            "Preserve original room geometry",
            "Keep windows and doors in exact positions",
            "Maintain vertical lines straight",
            "No perspective distortion",
        ]
        if task_mode == "edge_blend":
            constraints.extend([
                "Seamless material transitions",
                "Match color temperature across boundaries",
                "Consistent noise/grain pattern",
            ])
        
        # ========== 推荐mask类别（用于segment）==========
        mask_classes = []
        if task_mode == "material_replace":
            mask_classes = ["wall", "floor", "ceiling"]
        elif task_mode == "furniture_add":
            mask_classes = ["floor", "empty_space"]
        elif task_mode == "edge_blend":
            mask_classes = ["boundary_region", "transition_zone"]
        else:
            mask_classes = ["wall", "floor", "ceiling", "window", "door"]
        
        return PromptResult(
            prompt=final_prompt,
            negative_prompt=final_negative,
            sections=sections,
            style_name=style_data["name"],
            style_name_en=style_data["name_en"],
            room_name=room_data["name"],
            room_name_en=room_data["name_en"],
            task_mode=task_mode,
            engine=engine,
            quality_level=quality_level,
            materials=final_materials,
            constraints=constraints,
            recommended_mask_classes=mask_classes,
        )
    
    @staticmethod
    def get_style_list(language: str = "zh") -> List[Dict]:
        """获取风格列表（按语言过滤）"""
        if language == "zh":
            return [
                {"id": k, "name": v["name"], "description": v.get("description", "")}
                for k, v in STYLE_PRESETS.items()
            ]
        else:
            return [
                {"id": k, "name": v["name_en"], "description": v.get("description", "")}
                for k, v in STYLE_PRESETS.items()
            ]
    
    @staticmethod
    def get_room_list(language: str = "zh") -> List[Dict]:
        """获取房间列表（按语言过滤）"""
        if language == "zh":
            return [{"id": k, "name": v["name"]} for k, v in ROOM_TYPES.items()]
        else:
            return [{"id": k, "name": v["name_en"]} for k, v in ROOM_TYPES.items()]
    
    @staticmethod
    def get_material_presets() -> Dict[str, Dict[str, str]]:
        """获取所有材质预设"""
        return MATERIAL_PRESETS
    
    @staticmethod
    def get_task_modes() -> List[str]:
        """获取所有任务模式"""
        return list(TASK_MODE_PROMPTS.keys())
    
    @staticmethod
    def get_quality_levels() -> List[str]:
        """获取所有质量级别"""
        return list(QUALITY_PRESETS.keys())


# ==================== 便捷函数 ====================

def generate_prompt(
    room_type: str = "living_room",
    style: str = "wabi_sabi",
    task_mode: str = "full_render",
    engine: str = "nanobanana",
    quality_level: str = "high",
    materials: Dict[str, str] = None,
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
        task_mode=task_mode,
        engine=engine,
        quality_level=quality_level,
        materials=materials,
        custom_description=description,
        language=language,
    )
    return result.prompt, result.negative_prompt


def get_negative_prompt(engine: str = "nanobanana", task_mode: str = "full_render") -> str:
    """获取负面提示词（按引擎和任务）"""
    base = NEGATIVE_BY_ENGINE.get(engine, NEGATIVE_BY_ENGINE["nanobanana"])
    task = NEGATIVE_BY_TASK.get(task_mode, "")
    return f"{base}, {task}" if task else base


def get_edge_blend_prompt(language: str = "en") -> Tuple[str, str]:
    """获取边缘融合专用prompt"""
    result = PromptBuilder.build_prompt(
        task_mode="edge_blend",
        engine="nanobanana",
        quality_level="ultra",
        language=language,
    )
    return result.prompt, result.negative_prompt


# ==================== Legacy exports（兼容旧代码）====================

STYLE_PROMPTS = {k: v["prompt"] for k, v in STYLE_PRESETS.items()}
ROOM_PROMPTS = {k: v["name"] for k, v in ROOM_TYPES.items()}
STYLE_TEMPLATES = STYLE_PRESETS
ROOM_TEMPLATES = ROOM_TYPES
MASTER_PROMPT_EN = TASK_MODE_PROMPTS["full_render"]["prefix"]
MASTER_PROMPT_ZH = "将这个毛胚房转变为高端精装修"
NEGATIVE_PROMPT = NEGATIVE_BY_ENGINE["nanobanana"]
QUALITY_POSITIVE = QUALITY_PRESETS["high"]["real"]
QUALITY_NEGATIVE = NEGATIVE_QUALITY
QUALITY_KEYWORDS = {"positive": QUALITY_POSITIVE, "negative": QUALITY_NEGATIVE}
NEGATIVE_PROMPTS = {"default": NEGATIVE_PROMPT}
DEFAULT_NEGATIVE = NEGATIVE_PROMPT
FULL_NEGATIVE = NEGATIVE_PROMPT


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("顶级室内设计 Prompt 库 v2（产品级）测试")
    print("=" * 80)
    
    # 测试1: 整图生成
    print("\n【测试1: full_render 整图生成】")
    result = PromptBuilder.build_prompt(
        room_type="living_room",
        style="wabi_sabi",
        task_mode="full_render",
        engine="nanobanana",
        quality_level="high",
    )
    print(f"风格: {result.style_name} ({result.style_name_en})")
    print(f"任务: {result.task_mode} | 引擎: {result.engine} | 质量: {result.quality_level}")
    print(f"\n正向Prompt ({len(result.prompt)} 字符):")
    print("-" * 80)
    print(result.prompt)
    print(f"\n负向Prompt ({len(result.negative_prompt)} 字符):")
    print("-" * 80)
    print(result.negative_prompt)
    print(f"\n材质: {result.materials}")
    print(f"约束: {result.constraints}")
    print(f"推荐Mask类别: {result.recommended_mask_classes}")
    
    # 测试2: 边缘融合
    print("\n" + "=" * 80)
    print("【测试2: edge_blend 边缘融合】")
    result2 = PromptBuilder.build_prompt(
        task_mode="edge_blend",
        engine="nanobanana",
        quality_level="ultra",
    )
    print(f"Prompt ({len(result2.prompt)} 字符):")
    print(result2.prompt)
    print(f"\n负向Prompt:")
    print(result2.negative_prompt)
    
    # 测试3: 分段输出
    print("\n" + "=" * 80)
    print("【测试3: 分段输出 sections】")
    for key, value in result.sections.items():
        print(f"  [{key}]: {value[:60]}..." if len(value) > 60 else f"  [{key}]: {value}")
    
    # 测试4: 自定义材质
    print("\n" + "=" * 80)
    print("【测试4: 自定义材质】")
    result4 = PromptBuilder.build_prompt(
        room_type="living_room",
        style="modern_luxury",
        materials={"wall": "Venetian plaster", "floor": "grey travertine"},
    )
    print(f"材质段: {result4.sections.get('materials', 'N/A')}")
