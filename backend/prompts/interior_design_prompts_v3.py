"""
顶级室内设计 Prompt 库 v3.2（商业级稳定版）
Premium Interior Design Prompt Library v3.2 - Commercial Stable

v3.2 核心改进：
1. BlendSpec dataclass 统一 blend 规范
2. validate_mask_contract() 在 build_prompt 中自动调用
3. replace_scope 支持分部位替换
4. build_plan per-pass contract override
5. resolve_mask_class 规范化策略
6. material_replace TASK 加 ONLY 硬句
7. OBJECT_INTEGRITY_LOCK 更精准
8. window/door 从 alias 移除，强制显式选择

优先级排序：
STRUCT_LOCK → TASK → PRESERVE → TARGET → LIGHT/COLOR MATCH → STYLE → QUALITY
"""

from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import warnings
import re


# ==================== 枚举定义（用于校验）====================

class TaskMode(str, Enum):
    """任务模式"""
    FULL_RENDER = "full_render"
    MATERIAL_REPLACE = "material_replace"
    EDGE_BLEND = "edge_blend"
    FURNITURE_ADD = "furniture_add"


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


# 每个枚举的默认值（必须显式指定）
ENUM_DEFAULTS = {
    TaskMode: TaskMode.FULL_RENDER,
    Engine: Engine.NANOBANANA,
    QualityLevel: QualityLevel.HIGH,
}


def _normalize_enum(value: Union[str, Enum], enum_class: type, strict: bool = False) -> str:
    """标准化枚举值，支持字符串或枚举类型输入
    
    Args:
        value: 输入值
        enum_class: 枚举类
        strict: True=非法值抛错, False=回退默认值并警告
    """
    if isinstance(value, enum_class):
        return value.value
    try:
        return enum_class(value).value
    except ValueError:
        default = ENUM_DEFAULTS.get(enum_class, list(enum_class)[0])
        if strict:
            raise ValueError(f"Invalid {enum_class.__name__} value: '{value}'. Valid: {[e.value for e in enum_class]}")
        warnings.warn(f"Invalid {enum_class.__name__} value '{value}', falling back to '{default.value}'", UserWarning)
        return default.value


# ==================== 结构锁定（硬约束）====================

# 硬约束（命令式，SDXL/Flux/NanoBanana/Edit 用）
STRUCT_LOCK_HARD = {
    "en": "Do not change geometry. Do not move or add windows/doors. Keep all edges straight and aligned. Preserve the original perspective and camera position. Maintain exact room layout and proportions.",
    "zh": "禁止改动几何结构与透视：不新增/移动门窗，不改变墙体边界，垂直线保持笔直，镜头位置不变，保持原有房间格局和比例。",
}

# 软约束（描述式，MJ 用）
STRUCT_LOCK_MJ = {
    "en": "same room layout, same windows and doors positions, same perspective, straight vertical lines",
    "zh": "相同房间布局，相同门窗位置，相同透视角度，垂直线笔直",
}

# SDXL/Flux 结构提示符（用于 ControlNet）
STRUCT_HINT_CONTROLNET = "architectural line fidelity, straight edges, no warping, precise geometry"


# ==================== 保护指令（正向硬句）====================

# 材质替换时的保护指令
PRESERVE_MATERIAL_REPLACE = {
    "en": "Keep window frames, skirting boards, door frames, beams and columns unchanged. Only replace wall/floor/ceiling materials.",
    "zh": "保持窗框、踢脚线、门框、梁柱不变。只替换墙面/地面/天花板材质。",
}

# 家具添加时的保护指令
PRESERVE_FURNITURE_ADD = {
    "en": "Do not change existing finishes (walls, floor, ceiling). Only add furniture and soft furnishings.",
    "zh": "不改变现有饰面（墙面、地面、天花板）。只添加家具和软装。",
}

# 边缘融合时的一致性指令（从 negative 挪到正向）
CONSISTENCY_EDGE_BLEND = {
    "en": "Only adjust the narrow boundary ring region; do not repaint large areas. Match existing photo noise, grain and exposure exactly. Seamless integration with no visible boundaries. Continuous contact shadows across transitions.",
    "zh": "只调整边界环形过渡区，不要重绘大面积区域。完全匹配现有照片的噪点、颗粒和曝光。无缝融合，无可见边界。过渡区域接触阴影连续。",
}

# 对象完整性锁（更精准版本：允许修边缘但不改物体形状）
OBJECT_INTEGRITY_LOCK = {
    "en": "Do not add new objects. Keep existing objects' shapes and positions unchanged.",
    "zh": "不新增物体。保持现有物体的形状和位置不变。",
}


# ==================== 质量预设（分段 + 任务专用）====================

QUALITY_PRESETS = {
    "standard": {
        "camera": "interior photography, level camera",
        "light": "natural daylight, soft shadows",
        "color": "natural white balance",
        "real_photo": "realistic interior photo",
        "real_match": "match existing photo style",
    },
    "high": {
        "camera": "24mm wide-angle interior photography, level camera, straight vertical lines",
        "light": "soft natural daylight from windows, realistic contact shadows, layered ambient lighting",
        "color": "natural white balance, subtle contrast, professional color grading",
        "real_photo": "photorealistic interior photography, no CGI look, no render artifacts",
        "real_match": "match existing photo noise and grain and exposure, seamless integration",
    },
    "ultra": {
        "camera": "24mm wide-angle professional interior photography, perfect level camera, razor-sharp vertical lines, architectural precision",
        "light": "soft diffused natural daylight streaming from windows, physically accurate contact shadows, layered lighting system (ambient + accent + task)",
        "color": "cinematic color grading, natural white balance, rich midtones, subtle film grain",
        "real_photo": "photorealistic interior photography indistinguishable from real photo, absolutely no CGI artifacts, no render look, no synthetic feel",
        "real_match": "match existing photo noise and grain and exposure and color temperature exactly, seamless integration, no visible boundaries, continuous shadows",
    },
}

# edge_blend 专用质量预设（不带 camera、不带 golden hour、用 real_match）
QUALITY_EDGE_BLEND = {
    "light": "continuous contact shadows, match existing lighting direction and intensity",
    "color": "match white balance and exposure exactly, no color shift",
    "real_match": "match grain, noise, texture, color temperature exactly, seamless integration, no visible seams or boundaries",
}


# ==================== 材质库 ====================

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


# ==================== 负面提示词 ====================

# noise 分离：避免和正向 "match noise/grain" 冲突
NEGATIVE_QUALITY_BASE = "low quality, blurry, overexposed, oversaturated, underexposed, artifacts, jpeg compression"
NEGATIVE_NOISE = "excessive noise, blotchy noise, chroma noise, banding"
NEGATIVE_QUALITY = f"{NEGATIVE_QUALITY_BASE}, {NEGATIVE_NOISE}"
NEGATIVE_STRUCTURE = "wrong layout, changed geometry, moved windows, extra openings, warped straight lines, distorted perspective, tilted verticals, bent edges, extra doors, missing walls, wrong room shape"
NEGATIVE_CGI = "cartoon, anime, unreal engine, 3d render, cgi, game screenshot, digital art, illustration, painting, drawing, synthetic, fake, artificial"
NEGATIVE_DESIGN = "duplicate furniture, cluttered, messy, cheap materials, plastic texture, mismatched styles, wrong scale, floating objects"
NEGATIVE_WATERMARK = "text, watermark, logo, signature, copyright, banner, frame, border"
NEGATIVE_SEAMS = "visible seams, color mismatch, texture discontinuity, boundary artifacts, unnatural transition"

NEGATIVE_BY_ENGINE = {
    "sdxl": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}, {NEGATIVE_WATERMARK}",
    "flux": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}",
    "mj": f"{NEGATIVE_CGI}, blurry, low quality",
    "nanobanana": f"{NEGATIVE_QUALITY}, {NEGATIVE_STRUCTURE}, {NEGATIVE_CGI}, {NEGATIVE_DESIGN}, {NEGATIVE_WATERMARK}",
    "edit": f"{NEGATIVE_STRUCTURE}, {NEGATIVE_SEAMS}",
}

NEGATIVE_BY_TASK = {
    "full_render": "",
    "material_replace": "changed furniture, redesigned space, different layout",
    "edge_blend": "",  # 关键约束已移到正向
    "furniture_add": "changed finishes, altered walls, different flooring",
}


# ==================== Mask Class Vocabulary（统一词表）====================

MASK_VOCAB_VERSION = "1.1.0"

MASK_CLASS_VOCAB = {
    # 主类（window/door 从 alias 移除，必须显式选择 _frame 或 _glass）
    "wall": {"aliases": ["walls", "wall_surface"], "category": "surface"},
    "floor": {"aliases": ["flooring", "floor_surface"], "category": "surface"},
    "ceiling": {"aliases": ["ceiling_surface"], "category": "surface"},
    "window_frame": {"aliases": ["window_trim"], "category": "frame"},
    "window_glass": {"aliases": ["glass", "window_pane"], "category": "glass"},
    "door_frame": {"aliases": ["door_trim"], "category": "frame"},
    "skirting": {"aliases": ["baseboard", "skirting_board"], "category": "trim"},
    "beam": {"aliases": ["ceiling_beam"], "category": "structure"},
    "column": {"aliases": ["pillar"], "category": "structure"},
    "furniture": {"aliases": ["existing_furniture"], "category": "object"},
    "empty_space": {"aliases": ["floor_empty_area", "placement_zone"], "category": "zone"},
    "boundary_region": {"aliases": ["transition_zone", "edge_zone"], "category": "zone"},
    "material_center": {"aliases": ["unchanged_area", "interior_area"], "category": "zone"},
    "view_outside": {"aliases": ["exterior_view", "outside"], "category": "view"},
}

# 模糊类警告（window/door 需要显式选择）
AMBIGUOUS_CLASSES = {
    "window": ["window_frame", "window_glass"],
    "door": ["door_frame"],
    "trim": ["skirting"],
}

# Alias -> Canonical 解析器（带规范化策略）
def _normalize_class_name(name: str) -> str:
    """规范化类名：空格/连字符/驼峰 -> 下划线小写"""
    # 驼峰拆分
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    # 非字母数字替换为下划线
    name = re.sub(r'[^a-zA-Z0-9]+', '_', name)
    return name.lower().strip('_')


def resolve_mask_class(name: str, strict: bool = False) -> Optional[str]:
    """将 alias 解析为 canonical base class
    
    Args:
        name: 输入类名
        strict: True=模糊类报错, False=模糊类警告并返回None
    """
    normalized = _normalize_class_name(name)
    
    # 检查模糊类
    if normalized in AMBIGUOUS_CLASSES:
        options = AMBIGUOUS_CLASSES[normalized]
        msg = f"Ambiguous class '{name}'. Please use one of: {options}"
        if strict:
            raise ValueError(msg)
        warnings.warn(msg, UserWarning)
        return None
    
    # 直接匹配
    if normalized in MASK_CLASS_VOCAB:
        return normalized
    
    # Alias 匹配
    for canonical, info in MASK_CLASS_VOCAB.items():
        aliases_normalized = [_normalize_class_name(a) for a in info.get("aliases", [])]
        if normalized in aliases_normalized:
            return canonical
    
    return None


def validate_mask_contract(contract: 'MaskContract') -> List[str]:
    """校验 contract 中的 class 是否都在 vocab 中"""
    errors = []
    for target in contract.edit_targets:
        if resolve_mask_class(target) is None:
            errors.append(f"edit_target '{target}' not in MASK_CLASS_VOCAB")
    for target in contract.protect_targets:
        if resolve_mask_class(target) is None:
            errors.append(f"protect_target '{target}' not in MASK_CLASS_VOCAB")
    return errors


# ==================== BlendSpec（统一 blend 规范）====================

@dataclass
class BlendSpec:
    """Blend 规范（避免 schema 漂移）"""
    ratio: float = 0.005          # 相对短边的比例
    min_px: int = 3               # 最小像素
    max_px: int = 20              # 最大像素
    ring_only: bool = True        # 只修环形区域
    outward_only: bool = True     # 只向外扩展


# ==================== Mask Contract（segment 承接规范）====================

@dataclass
class MaskContract:
    """Mask 工作流规范"""
    edit_targets: List[str] = field(default_factory=list)
    protect_targets: List[str] = field(default_factory=list)
    needs_hard_mask: bool = False
    needs_blend_mask: bool = False
    blend: BlendSpec = field(default_factory=BlendSpec)
    pass_id: str = ""             # 用于日志与回放


MASK_CONTRACTS = {
    "full_render": MaskContract(
        edit_targets=["wall", "floor", "ceiling", "empty_space"],
        protect_targets=["window_glass", "view_outside"],
        needs_hard_mask=False,
        needs_blend_mask=False,
        blend=BlendSpec(ratio=0.005, min_px=3, max_px=20),
        pass_id="FR",
    ),
    "material_replace": MaskContract(
        edit_targets=["wall", "floor", "ceiling"],
        protect_targets=["window_frame", "window_glass", "skirting", "door_frame", "beam", "column", "furniture"],
        needs_hard_mask=True,
        needs_blend_mask=True,
        blend=BlendSpec(ratio=0.008, min_px=5, max_px=30),
        pass_id="MR",
    ),
    "edge_blend": MaskContract(
        edit_targets=["boundary_region"],
        protect_targets=["material_center"],
        needs_hard_mask=False,
        needs_blend_mask=True,
        blend=BlendSpec(ratio=0.015, min_px=10, max_px=50, ring_only=True),
        pass_id="BL",
    ),
    "furniture_add": MaskContract(
        edit_targets=["empty_space"],
        protect_targets=["wall", "floor", "ceiling", "furniture", "window_frame", "window_glass", "door_frame"],
        needs_hard_mask=True,
        needs_blend_mask=True,
        blend=BlendSpec(ratio=0.003, min_px=3, max_px=15),
        pass_id="FA",
    ),
}


# 允许的 replace_scope 白名单（只保留有对应 vocab/contract 的表面）
VALID_REPLACE_SCOPES = {"wall", "floor", "ceiling"}


def normalize_replace_scope(replace_scope: List[str]) -> List[str]:
    """规范化 replace_scope，返回 canonical list（用于 prompt 和 contract 一致性）"""
    if not replace_scope:
        return ["wall", "floor", "ceiling"]
    
    valid_scope = []
    for s in replace_scope:
        # 尝试 resolve
        canonical = resolve_mask_class(s)
        if canonical and canonical in VALID_REPLACE_SCOPES:
            valid_scope.append(canonical)
        elif s.lower() in VALID_REPLACE_SCOPES:
            valid_scope.append(s.lower())
        else:
            warnings.warn(f"Invalid replace_scope '{s}', skipping. Valid: {VALID_REPLACE_SCOPES}", UserWarning)
    
    if not valid_scope:
        warnings.warn(f"No valid scope in {replace_scope}, falling back to full surface", UserWarning)
        return ["wall", "floor", "ceiling"]
    
    return valid_scope


def create_scoped_contract(task_mode: str, replace_scope: List[str]) -> MaskContract:
    """创建带 replace_scope 的 contract（用于分部位替换）"""
    base = MASK_CONTRACTS.get(task_mode, MASK_CONTRACTS["material_replace"])
    
    # 使用统一的 normalize 函数
    valid_scope = normalize_replace_scope(replace_scope)
    
    # protect_targets 加入不在 scope 内的表面
    all_surfaces = {"wall", "floor", "ceiling"}
    extra_protect = [s for s in all_surfaces if s not in valid_scope]
    scoped_protect = list(set(base.protect_targets + extra_protect))
    
    return MaskContract(
        edit_targets=valid_scope,
        protect_targets=scoped_protect,
        needs_hard_mask=base.needs_hard_mask,
        needs_blend_mask=base.needs_blend_mask,
        blend=base.blend,
        pass_id=f"{base.pass_id}_{'_'.join(valid_scope)}",
    )


# edge_blend per-pass protect override
EDGE_BLEND_PROTECT_BY_SURFACE = {
    "wall": ["window_frame", "door_frame", "beam", "column", "skirting"],
    "floor": ["skirting", "door_frame", "furniture"],
    "ceiling": ["beam", "column"],
    "furniture": ["wall", "floor", "skirting"],
}


# ==================== Engine Params ====================

ENGINE_PARAMS_DEFAULT = {
    "mj": {
        "ar": "--ar 16:9",
        "stylize": "--stylize 100",
        "quality": "--quality 1",
        "version": "--v 6",
    },
    "sdxl": {
        "cfg_scale": 7,
        "steps": 30,
        "sampler": "DPM++ 2M Karras",
    },
    "flux": {
        "guidance": 3.5,
        "steps": 28,
    },
    "nanobanana": {
        "model": "nano-banana-pro",
        "aspect_ratio": "auto",
    },
    "edit": {
        "strength": 0.75,
        "mask_blur": 8,
    },
}

ENGINE_PARAMS_RANGE = {
    "edit": {
        "strength": {"min": 0.45, "max": 0.85, "edge_blend": 0.55, "material_replace": 0.70},
        "mask_blur": {"min": 4, "max": 12, "rule": "scale by resolution"},
    },
    "sdxl": {
        "cfg_scale": {"min": 5, "max": 12},
        "steps": {"min": 20, "max": 50},
    },
    "flux": {
        "guidance": {"min": 2.0, "max": 5.0},
        "steps": {"min": 20, "max": 40},
    },
}

# Legacy alias
ENGINE_PARAMS = ENGINE_PARAMS_DEFAULT


# ==================== Prompt 构建结果 ====================

@dataclass
class PromptResult:
    """Prompt构建结果（结构化输出）"""
    prompt: str
    negative_prompt: str
    sections: Dict[str, str] = field(default_factory=dict)
    
    style_name: str = ""
    style_name_en: str = ""
    room_name: str = ""
    room_name_en: str = ""
    
    task_mode: str = ""
    engine: str = ""
    quality_level: str = ""
    
    materials: Dict[str, str] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    
    # v3 新增
    mask_contract: MaskContract = None
    engine_params: Dict[str, Any] = field(default_factory=dict)
    engine_params_range: Dict[str, Any] = field(default_factory=dict)
    engine_cli: str = ""  # MJ CLI 拼接字段
    mask_vocab_version: str = MASK_VOCAB_VERSION


# ==================== Prompt 构建器 ====================

class PromptBuilder:
    """生产级 Prompt 构建器 v3"""
    
    @staticmethod
    def build_prompt(
        room_type: Union[str, None] = "living_room",
        style: Union[str, None] = "wabi_sabi",
        task_mode: Union[str, TaskMode] = "full_render",
        engine: Union[str, Engine] = "nanobanana",
        quality_level: Union[str, QualityLevel] = "high",
        materials: Dict[str, str] = None,
        custom_description: str = None,
        language: str = "en",
        marketing_mode: bool = False,
        time_of_day: str = None,  # None | "golden_hour" | "blue_hour"
        replace_scope: List[str] = None,  # v3.2: 分部位替换 ["wall"] / ["floor"] / ["ceiling"]
        validate_contract: bool = True,  # v3.2: 自动校验 contract
    ) -> PromptResult:
        """
        构建完整的Prompt结果
        
        优先级排序：
        STRUCT_LOCK → TASK → PRESERVE → TARGET → LIGHT/COLOR MATCH → STYLE → QUALITY
        """
        # ========== 枚举标准化 ==========
        task_mode = _normalize_enum(task_mode, TaskMode)
        engine = _normalize_enum(engine, Engine)
        quality_level = _normalize_enum(quality_level, QualityLevel)
        
        # ========== 获取基础数据 ==========
        style_data = STYLE_PRESETS.get(style, STYLE_PRESETS["wabi_sabi"]) if style else STYLE_PRESETS["wabi_sabi"]
        room_data = ROOM_TYPES.get(room_type, ROOM_TYPES["living_room"]) if room_type else ROOM_TYPES["living_room"]
        quality_data = QUALITY_PRESETS.get(quality_level, QUALITY_PRESETS["high"])
        
        # 材质
        style_materials_key = style_data.get("materials", "luxury_minimal")
        final_materials = MATERIAL_PRESETS.get(style_materials_key, MATERIAL_PRESETS["luxury_minimal"]).copy()
        if materials:
            final_materials.update(materials)
        
        # 语言
        lang = "en" if language != "zh" else "zh"
        room_name = room_data["name_en"] if lang == "en" else room_data["name"]
        style_name = style_data["name_en"] if lang == "en" else style_data["name"]
        
        # ========== 分段构建（按优先级）==========
        sections = {}
        
        # 1. STRUCT_LOCK（永远第一）
        if engine == "mj":
            sections["struct_lock"] = STRUCT_LOCK_MJ[lang]
        else:
            sections["struct_lock"] = STRUCT_LOCK_HARD[lang]
        
        # v3.2: 统一 canonical 化 scope（避免 prompt 文案 scope ≠ mask scope）
        scope_parts = normalize_replace_scope(replace_scope)
        scope_desc = ", ".join(scope_parts)
        
        # 2. TASK（本次要做什么）
        if task_mode == "full_render":
            sections["task"] = f"Transform this unfinished apartment into a high-end fully finished {room_name} interior design in {style_name} style"
        elif task_mode == "material_replace":
            if lang == "en":
                sections["task"] = f"Replace ONLY the specified surfaces ({scope_desc}). Do not change furniture, layout, openings, or lighting."
            else:
                sections["task"] = f"仅替换指定表面（{scope_desc}）。不改变家具、布局、门窗或照明。"
        elif task_mode == "edge_blend":
            sections["task"] = "Seamlessly blend the edges where new materials meet existing surfaces"
        elif task_mode == "furniture_add":
            sections["task"] = f"Add furniture and soft furnishings in {style_name} style"
        
        # 3. PRESERVE（明确哪些不能动）- v3.2: scope-aware
        if task_mode == "material_replace":
            if lang == "en":
                preserve_base = f"Only replace surfaces in scope: {scope_desc}. Keep window frames, skirting boards, door frames, beams and columns unchanged."
            else:
                preserve_base = f"只替换范围内表面：{scope_desc}。保持窗框、踢脚线、门框、梁柱不变。"
            sections["preserve"] = preserve_base + " " + OBJECT_INTEGRITY_LOCK[lang]
        elif task_mode == "furniture_add":
            sections["preserve"] = PRESERVE_FURNITURE_ADD[lang]
        elif task_mode == "edge_blend":
            # v3.2: BlendSpec 映射成 prompt 硬句
            blend_spec = MASK_CONTRACTS["edge_blend"].blend
            if lang == "en":
                blend_hint = f"Only modify a thin ring band around the mask boundary ({blend_spec.min_px}-{blend_spec.max_px}px). Do not edit the interior region. Feather outward only."
            else:
                blend_hint = f"只修改掩膜边界周围的细环形区域（{blend_spec.min_px}-{blend_spec.max_px}像素）。不要编辑内部区域。只向外羽化。"
            sections["preserve"] = CONSISTENCY_EDGE_BLEND[lang] + " " + blend_hint + " " + OBJECT_INTEGRITY_LOCK[lang]
        
        # 4. TARGET（材质/家具具体清单）- v3.2: 按 replace_scope 过滤
        if task_mode == "full_render":
            # full_render 保持材质清单形式（MJ 喜欢短）
            mat_parts = []
            for key in ["wall", "floor", "ceiling", "feature", "trim", "cabinet"]:
                if final_materials.get(key):
                    mat_parts.append(f"{final_materials[key]}")
            if mat_parts:
                sections["target"] = ", ".join(mat_parts)
        elif task_mode == "material_replace":
            # v3.2: 只输出 scope 内的映射
            scope_set = set(scope_parts)
            if lang == "en":
                mapping_parts = []
                if "wall" in scope_set and final_materials.get("wall"):
                    mapping_parts.append(f"Walls → {final_materials['wall']}")
                if "floor" in scope_set and final_materials.get("floor"):
                    mapping_parts.append(f"Floor → {final_materials['floor']}")
                if "ceiling" in scope_set and final_materials.get("ceiling"):
                    mapping_parts.append(f"Ceiling → {final_materials['ceiling']}")
                if "feature" in scope_set and final_materials.get("feature"):
                    mapping_parts.append(f"Feature wall → {final_materials['feature']}")
                if "trim" in scope_set and final_materials.get("trim"):
                    mapping_parts.append(f"Trim → {final_materials['trim']}")
                if mapping_parts:
                    sections["target"] = ". ".join(mapping_parts) + "."
            else:
                mapping_parts = []
                if "wall" in scope_set and final_materials.get("wall"):
                    mapping_parts.append(f"墙面→{final_materials['wall']}")
                if "floor" in scope_set and final_materials.get("floor"):
                    mapping_parts.append(f"地面→{final_materials['floor']}")
                if "ceiling" in scope_set and final_materials.get("ceiling"):
                    mapping_parts.append(f"顶面→{final_materials['ceiling']}")
                if "feature" in scope_set and final_materials.get("feature"):
                    mapping_parts.append(f"背景墙→{final_materials['feature']}")
                if "trim" in scope_set and final_materials.get("trim"):
                    mapping_parts.append(f"收口→{final_materials['trim']}")
                if mapping_parts:
                    sections["target"] = "；".join(mapping_parts) + "。"
        
        # 5. LIGHT/COLOR（edge_blend 用专用版）
        if task_mode == "edge_blend":
            sections["light"] = QUALITY_EDGE_BLEND["light"]
            sections["color"] = QUALITY_EDGE_BLEND["color"]
            sections["real"] = QUALITY_EDGE_BLEND["real_match"]
        else:
            sections["light"] = quality_data["light"]
            sections["color"] = quality_data["color"]
            # 用 real_photo 还是 real_match
            if task_mode in ["material_replace", "furniture_add"]:
                sections["real"] = quality_data["real_match"]
            else:
                sections["real"] = quality_data["real_photo"]
        
        # 6. STYLE（只在 full_render / furniture_add）
        if task_mode in ["full_render", "furniture_add"]:
            sections["style"] = style_data["prompt"]
        
        # 7. CAMERA（edge_blend 不用，避免诱导变形）
        if task_mode != "edge_blend":
            sections["camera"] = quality_data["camera"]
            # SDXL/Flux 加结构提示符
            if engine in ["sdxl", "flux"]:
                sections["struct_hint"] = STRUCT_HINT_CONTROLNET
        
        # 8. 时间（可选，edge_blend 永远不用）
        if time_of_day == "golden_hour" and task_mode != "edge_blend":
            sections["time"] = "golden hour warmth"
        
        # 9. 营销词（默认关闭）
        if marketing_mode and task_mode == "full_render":
            sections["marketing"] = "aspirational lifestyle, design magazine quality"
        
        # 10. 用户自定义（放在 PRESERVE 之后）
        if custom_description:
            # material_replace 防呆：过滤危险关键词或加限制句
            if task_mode == "material_replace":
                forbidden_keywords = ["add furniture", "new furniture", "change layout", "new windows", "add door"]
                has_forbidden = any(kw in custom_description.lower() for kw in forbidden_keywords)
                if has_forbidden:
                    sections["custom"] = custom_description + ". Only if it does not change geometry or add objects."
                else:
                    sections["custom"] = custom_description
            else:
                sections["custom"] = custom_description
        
        # ========== 拼接策略（按引擎）==========
        if engine == "mj":
            ordered_keys = ["struct_lock", "task", "style", "real"]
            separator = ", "
        elif engine == "edit":
            ordered_keys = ["struct_lock", "task", "preserve", "custom", "light", "color", "real"]
            separator = ". "
        elif task_mode == "edge_blend":
            ordered_keys = ["struct_lock", "task", "preserve", "light", "color", "real"]
            separator = ". "
        else:
            ordered_keys = ["struct_lock", "task", "preserve", "custom", "target", "style", "camera", "struct_hint", "light", "color", "real", "time"]
            separator = ", "
        
        prompt_parts = [sections[k] for k in ordered_keys if k in sections and sections[k]]
        final_prompt = separator.join(prompt_parts)
        
        # ========== 负面提示词 ==========
        base_negative = NEGATIVE_BY_ENGINE.get(engine, NEGATIVE_BY_ENGINE["nanobanana"])
        task_negative = NEGATIVE_BY_TASK.get(task_mode, "")
        final_negative = f"{base_negative}, {task_negative}" if task_negative else base_negative
        
        # ========== 约束信息 ==========
        constraints = [
            "Preserve original room geometry",
            "Keep windows and doors in exact positions",
            "Maintain vertical lines straight",
            "No perspective distortion",
        ]
        if task_mode == "material_replace":
            constraints.extend([
                "Keep window frames unchanged",
                "Keep skirting boards unchanged",
                "Keep door frames unchanged",
            ])
        elif task_mode == "edge_blend":
            constraints.extend([
                "Seamless material transitions",
                "Match color temperature exactly",
                "Match noise/grain pattern exactly",
                "No visible boundaries",
            ])
        elif task_mode == "furniture_add":
            constraints.extend([
                "Do not change wall materials",
                "Do not change floor materials",
                "Correct furniture scale and shadows",
            ])
        
        # ========== Mask Contract ==========
        if task_mode == "material_replace" and replace_scope:
            # v3.2: 使用 scoped contract
            mask_contract = create_scoped_contract(task_mode, replace_scope)
        else:
            mask_contract = MASK_CONTRACTS.get(task_mode, MASK_CONTRACTS["full_render"])
        
        # v3.2: 自动校验 contract
        if validate_contract:
            errors = validate_mask_contract(mask_contract)
            if errors:
                warnings.warn(f"MaskContract validation errors: {errors}", UserWarning)
        
        # ========== Engine Params ==========
        engine_params = ENGINE_PARAMS_DEFAULT.get(engine, {}).copy()
        engine_params_range = ENGINE_PARAMS_RANGE.get(engine, {})
        
        # MJ CLI 拼接
        engine_cli = ""
        if engine == "mj":
            mj_params = ENGINE_PARAMS_DEFAULT.get("mj", {})
            engine_cli = f"{final_prompt} {mj_params.get('ar', '')} {mj_params.get('stylize', '')} {mj_params.get('version', '')}".strip()
        
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
            mask_contract=mask_contract,
            engine_params=engine_params,
            engine_params_range=engine_params_range,
            engine_cli=engine_cli,
            mask_vocab_version=MASK_VOCAB_VERSION,
        )
    
    @staticmethod
    def get_style_list(language: str = "zh") -> List[Dict]:
        """获取风格列表"""
        key = "name" if language == "zh" else "name_en"
        return [{"id": k, "name": v[key], "description": v.get("description", "")} for k, v in STYLE_PRESETS.items()]
    
    @staticmethod
    def get_room_list(language: str = "zh") -> List[Dict]:
        """获取房间列表"""
        key = "name" if language == "zh" else "name_en"
        return [{"id": k, "name": v[key]} for k, v in ROOM_TYPES.items()]
    
    @staticmethod
    def get_material_presets() -> Dict[str, Dict[str, str]]:
        return MATERIAL_PRESETS
    
    @staticmethod
    def get_task_modes() -> List[str]:
        return [e.value for e in TaskMode]
    
    @staticmethod
    def get_quality_levels() -> List[str]:
        return [e.value for e in QualityLevel]
    
    @staticmethod
    def get_engines() -> List[str]:
        return [e.value for e in Engine]
    
    @staticmethod
    def build_plan(
        room_type: str = "living_room",
        style: str = "wabi_sabi",
        engine: str = "nanobanana",
        quality_level: str = "high",
        materials: Dict[str, str] = None,
        language: str = "en",
        include_furniture: bool = True,
        include_harmonize: bool = False,
    ) -> List['PromptResult']:
        """
        构建多 pass 执行计划（生产级工作流）
        
        标准流程：
        1. material_replace(wall) → edge_blend(wall boundary)
        2. material_replace(floor) → edge_blend(floor boundary)
        3. material_replace(ceiling) → edge_blend(ceiling boundary)
        4. furniture_add (可选)
        5. final_harmonize (可选，整体色彩噪点统一)
        
        Returns:
            List[PromptResult]: 按执行顺序的 prompt 列表
        """
        plan = []
        
        # 获取材质
        style_data = STYLE_PRESETS.get(style, STYLE_PRESETS["wabi_sabi"])
        style_materials_key = style_data.get("materials", "luxury_minimal")
        base_materials = MATERIAL_PRESETS.get(style_materials_key, MATERIAL_PRESETS["luxury_minimal"]).copy()
        if materials:
            base_materials.update(materials)
        
        # Pass 1-3: 分部位材质替换 + 边缘融合
        surface_parts = [
            ("wall", {"wall": base_materials.get("wall")}),
            ("floor", {"floor": base_materials.get("floor")}),
            ("ceiling", {"ceiling": base_materials.get("ceiling")}),
        ]
        
        for part_name, part_materials in surface_parts:
            if part_materials.get(part_name):
                # v3.2: 使用 replace_scope 分部位替换
                replace_result = PromptBuilder.build_prompt(
                    room_type=room_type,
                    style=style,
                    task_mode="material_replace",
                    engine=engine,
                    quality_level=quality_level,
                    materials=part_materials,
                    language=language,
                    replace_scope=[part_name],  # v3.2: 只替换当前部位
                )
                # 标记当前处理部位
                replace_result.constraints.append(f"Current pass: {part_name}")
                plan.append(replace_result)
                
                # 边缘融合 + v3.2: per-pass protect override
                blend_result = PromptBuilder.build_prompt(
                    room_type=room_type,
                    style=style,
                    task_mode="edge_blend",
                    engine="edit",  # edge_blend 强制用 edit 引擎
                    quality_level="ultra",
                    language=language,
                )
                blend_result.constraints.append(f"Blend {part_name} boundaries")
                # 调整 edit 参数为 edge_blend 推荐值
                blend_result.engine_params["strength"] = ENGINE_PARAMS_RANGE.get("edit", {}).get("strength", {}).get("edge_blend", 0.55)
                # v3.2: per-pass protect override（防止涂坏框线/踢脚线）
                extra_protect = EDGE_BLEND_PROTECT_BY_SURFACE.get(part_name, [])
                blend_result.mask_contract = MaskContract(
                    edit_targets=["boundary_region"],
                    protect_targets=["material_center"] + extra_protect,
                    needs_hard_mask=False,
                    needs_blend_mask=True,
                    blend=MASK_CONTRACTS["edge_blend"].blend,
                    pass_id=f"BL_{part_name}",
                )
                plan.append(blend_result)
        
        # Pass 4: 家具添加（可选）
        if include_furniture:
            furniture_result = PromptBuilder.build_prompt(
                room_type=room_type,
                style=style,
                task_mode="furniture_add",
                engine=engine,
                quality_level=quality_level,
                materials=base_materials,
                language=language,
            )
            plan.append(furniture_result)
            
            # 家具接触边缘融合
            furniture_blend = PromptBuilder.build_prompt(
                room_type=room_type,
                style=style,
                task_mode="edge_blend",
                engine="edit",
                quality_level="ultra",
                language=language,
            )
            furniture_blend.constraints.append("Blend furniture contact shadows")
            furniture_blend.engine_params["strength"] = 0.45  # 家具融合更轻
            plan.append(furniture_blend)
        
        # Pass 5: 最终统一（可选）
        if include_harmonize:
            harmonize_result = PromptBuilder.build_prompt(
                room_type=room_type,
                style=style,
                task_mode="edge_blend",
                engine="edit",
                quality_level="ultra",
                language=language,
            )
            harmonize_result.constraints = ["Final harmonization: unify color temperature, noise pattern, and overall lighting"]
            harmonize_result.engine_params["strength"] = 0.35  # 最终统一最轻
            plan.append(harmonize_result)
        
        return plan


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
    """快速生成正向和负向提示词"""
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
    """获取负面提示词"""
    base = NEGATIVE_BY_ENGINE.get(engine, NEGATIVE_BY_ENGINE["nanobanana"])
    task = NEGATIVE_BY_TASK.get(task_mode, "")
    return f"{base}, {task}" if task else base


def get_edge_blend_prompt(language: str = "en", engine: str = "edit") -> Tuple[str, str]:
    """获取边缘融合专用prompt
    
    v3.2: 默认使用 edit 引擎（更适合 inpaint 工作流）
    """
    result = PromptBuilder.build_prompt(task_mode="edge_blend", engine=engine, quality_level="ultra", language=language)
    return result.prompt, result.negative_prompt


def get_mask_contract(task_mode: str) -> MaskContract:
    """获取 Mask 工作流规范"""
    return MASK_CONTRACTS.get(task_mode, MASK_CONTRACTS["full_render"])


# ==================== Legacy exports（DEPRECATED）====================

def _deprecated_warning(name: str):
    warnings.warn(f"{name} is deprecated, use PromptBuilder.build_prompt() instead", DeprecationWarning, stacklevel=3)

STYLE_PROMPTS = {k: v["prompt"] for k, v in STYLE_PRESETS.items()}
ROOM_PROMPTS = {k: v["name"] for k, v in ROOM_TYPES.items()}
STYLE_TEMPLATES = STYLE_PRESETS
ROOM_TEMPLATES = ROOM_TYPES
MASTER_PROMPT_EN = "Transform this unfinished apartment into a high-end fully finished"  # DEPRECATED
MASTER_PROMPT_ZH = "将这个毛胚房转变为高端精装修"  # DEPRECATED
NEGATIVE_PROMPT = NEGATIVE_BY_ENGINE["nanobanana"]
QUALITY_POSITIVE = QUALITY_PRESETS["high"]["real_photo"]
QUALITY_NEGATIVE = NEGATIVE_QUALITY
QUALITY_KEYWORDS = {"positive": QUALITY_POSITIVE, "negative": QUALITY_NEGATIVE}
NEGATIVE_PROMPTS = {"default": NEGATIVE_PROMPT}
DEFAULT_NEGATIVE = NEGATIVE_PROMPT
FULL_NEGATIVE = NEGATIVE_PROMPT


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("顶级室内设计 Prompt 库 v3（生产级）测试")
    print("=" * 80)
    
    # 测试1: full_render
    print("\n【测试1: full_render】")
    r1 = PromptBuilder.build_prompt(
        room_type="living_room",
        style="wabi_sabi",
        task_mode=TaskMode.FULL_RENDER,
        engine=Engine.NANOBANANA,
        quality_level=QualityLevel.HIGH,
    )
    print(f"任务: {r1.task_mode} | 引擎: {r1.engine}")
    print(f"Prompt ({len(r1.prompt)} 字符):")
    print(r1.prompt[:500] + "...")
    print(f"\nMask Contract:")
    print(f"  edit_targets: {r1.mask_contract.edit_targets}")
    print(f"  protect_targets: {r1.mask_contract.protect_targets}")
    
    # 测试2: material_replace（新增 protect）
    print("\n" + "=" * 80)
    print("【测试2: material_replace（含 protect_targets）】")
    r2 = PromptBuilder.build_prompt(task_mode="material_replace", engine="nanobanana")
    print(f"Sections:")
    for k, v in r2.sections.items():
        print(f"  [{k}]: {v[:60]}..." if len(v) > 60 else f"  [{k}]: {v}")
    print(f"\nMask Contract:")
    print(f"  edit_targets: {r2.mask_contract.edit_targets}")
    print(f"  protect_targets: {r2.mask_contract.protect_targets}")
    print(f"  blend: {r2.mask_contract.blend}")
    
    # 测试3: edge_blend（专用质量，不带 camera）
    print("\n" + "=" * 80)
    print("【测试3: edge_blend（专用质量预设）】")
    r3 = PromptBuilder.build_prompt(task_mode="edge_blend", quality_level="ultra")
    print(f"Sections:")
    for k, v in r3.sections.items():
        print(f"  [{k}]: {v[:60]}..." if len(v) > 60 else f"  [{k}]: {v}")
    print(f"\n无 camera 段: {'camera' not in r3.sections}")
    print(f"使用 real_match: {'match' in r3.sections.get('real', '')}")
    
    # 测试4: furniture_add（正向保护指令）
    print("\n" + "=" * 80)
    print("【测试4: furniture_add（正向保护指令）】")
    r4 = PromptBuilder.build_prompt(task_mode="furniture_add", style="modern_luxury")
    print(f"preserve 段: {r4.sections.get('preserve', 'N/A')}")
    
    # 测试5: MJ 引擎（短 struct_lock）
    print("\n" + "=" * 80)
    print("【测试5: MJ 引擎（短 struct_lock）】")
    r5 = PromptBuilder.build_prompt(engine="mj", task_mode="full_render")
    print(f"struct_lock: {r5.sections.get('struct_lock', 'N/A')}")
    print(f"engine_params: {r5.engine_params}")
    
    # 测试6: Enum 校验
    print("\n" + "=" * 80)
    print("【测试6: Enum 校验】")
    r6 = PromptBuilder.build_prompt(task_mode=TaskMode.EDGE_BLEND, engine=Engine.EDIT)
    print(f"task_mode (Enum输入): {r6.task_mode}")
    r7 = PromptBuilder.build_prompt(task_mode="edge_blend", engine="edit")
    print(f"task_mode (str输入): {r7.task_mode}")
