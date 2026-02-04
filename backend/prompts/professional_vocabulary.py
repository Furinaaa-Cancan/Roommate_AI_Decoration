"""
专业室内设计/建筑可视化 Prompt 词典
Professional Interior Design & Architectural Visualization Vocabulary

来源参考:
- PromptHero Interior Design Prompts
- Civitai Architecture Models
- MyArchitectAI Prompt Guide
- 建筑AI提示词词典 (yuanjineng.cn)
- Stable Diffusion 室内设计专业词汇
- Reddit r/StableDiffusion Interior Generator
"""

from typing import Dict, List
from dataclasses import dataclass


# ==================== 材质词典 Materials ====================

MATERIALS = {
    # 木材 Wood
    "wood": {
        "types": [
            ("oak", "橡木"),
            ("walnut", "胡桃木"),
            ("teak", "柚木"),
            ("mahogany", "桃花心木"),
            ("cherry", "樱桃木"),
            ("maple", "枫木"),
            ("birch", "桦木"),
            ("ash", "白蜡木"),
            ("pine", "松木"),
            ("cedar", "雪松"),
            ("bamboo", "竹子"),
            ("rosewood", "紫檀木"),
            ("ebony", "乌木"),
            ("beech", "榉木"),
            ("elm", "榆木"),
            ("cypress", "柏木"),
            ("reclaimed wood", "回收木材"),
            ("driftwood", "浮木"),
            ("plywood", "胶合板"),
            ("MDF", "中密度纤维板"),
        ],
        "finishes": [
            ("natural wood grain", "天然木纹"),
            ("polished wood", "抛光木材"),
            ("matte wood finish", "哑光木饰面"),
            ("lacquered wood", "漆面木材"),
            ("distressed wood", "做旧木材"),
            ("whitewashed wood", "白色水洗木"),
            ("stained wood", "着色木材"),
            ("oiled wood", "上油木材"),
            ("weathered wood", "风化木材"),
            ("charred wood", "碳化木"),
            ("wood veneer", "木皮贴面"),
        ]
    },
    
    # 石材 Stone
    "stone": {
        "types": [
            ("marble", "大理石"),
            ("granite", "花岗岩"),
            ("limestone", "石灰石"),
            ("travertine", "洞石"),
            ("slate", "板岩"),
            ("quartzite", "石英岩"),
            ("sandstone", "砂岩"),
            ("onyx", "玛瑙石"),
            ("basalt", "玄武岩"),
            ("terrazzo", "水磨石"),
            ("concrete", "混凝土"),
            ("microcement", "微水泥"),
            ("exposed aggregate", "露骨料"),
        ],
        "specific_marbles": [
            ("Calacatta marble", "卡拉卡塔大理石"),
            ("Carrara marble", "卡拉拉大理石"),
            ("Statuario marble", "雕像白大理石"),
            ("Nero Marquina", "黑金花大理石"),
            ("Emperador marble", "啡网大理石"),
            ("Crema Marfil", "米黄大理石"),
            ("Volakas marble", "爵士白大理石"),
        ],
        "finishes": [
            ("polished stone", "抛光石材"),
            ("honed stone", "哑光石材"),
            ("brushed stone", "拉丝石材"),
            ("flamed stone", "火烧石材"),
            ("tumbled stone", "滚磨石材"),
            ("split-face stone", "劈裂面石材"),
            ("leathered stone", "皮革面石材"),
        ]
    },
    
    # 金属 Metal
    "metal": {
        "types": [
            ("brass", "黄铜"),
            ("bronze", "青铜"),
            ("copper", "紫铜"),
            ("gold", "金色"),
            ("rose gold", "玫瑰金"),
            ("silver", "银色"),
            ("chrome", "镀铬"),
            ("stainless steel", "不锈钢"),
            ("black steel", "黑钢"),
            ("wrought iron", "锻铁"),
            ("cast iron", "铸铁"),
            ("aluminum", "铝"),
            ("titanium", "钛金属"),
            ("pewter", "白镴"),
            ("nickel", "镍"),
            ("patinated metal", "做旧金属"),
        ],
        "finishes": [
            ("polished metal", "抛光金属"),
            ("brushed metal", "拉丝金属"),
            ("matte metal", "哑光金属"),
            ("antiqued metal", "仿古金属"),
            ("hammered metal", "锤纹金属"),
            ("oxidized metal", "氧化金属"),
            ("powder-coated metal", "粉末涂层金属"),
        ]
    },
    
    # 织物 Fabric
    "fabric": {
        "types": [
            ("velvet", "丝绒"),
            ("linen", "亚麻"),
            ("cotton", "棉布"),
            ("silk", "丝绸"),
            ("wool", "羊毛"),
            ("cashmere", "羊绒"),
            ("mohair", "马海毛"),
            ("bouclé", "圈圈纱"),
            ("chenille", "雪尼尔"),
            ("tweed", "粗花呢"),
            ("suede", "绒面革"),
            ("leather", "皮革"),
            ("faux leather", "人造皮革"),
            ("microfiber", "超细纤维"),
            ("canvas", "帆布"),
            ("muslin", "细棉布"),
            ("damask", "锦缎"),
            ("brocade", "织锦"),
            ("jacquard", "提花织物"),
            ("sheer fabric", "透明纱"),
            ("blackout fabric", "遮光布"),
        ],
        "textures": [
            ("tufted", "簇绒"),
            ("pleated", "褶皱"),
            ("quilted", "绗缝"),
            ("woven", "编织"),
            ("knitted", "针织"),
            ("embroidered", "刺绣"),
            ("printed pattern", "印花图案"),
        ]
    },
    
    # 玻璃 Glass
    "glass": {
        "types": [
            ("clear glass", "透明玻璃"),
            ("frosted glass", "磨砂玻璃"),
            ("tinted glass", "有色玻璃"),
            ("smoked glass", "烟色玻璃"),
            ("mirror glass", "镜面玻璃"),
            ("antiqued mirror", "仿古镜"),
            ("stained glass", "彩色玻璃"),
            ("textured glass", "压花玻璃"),
            ("ribbed glass", "条纹玻璃"),
            ("fluted glass", "波纹玻璃"),
            ("seeded glass", "气泡玻璃"),
            ("back-painted glass", "烤漆玻璃"),
            ("low-iron glass", "超白玻璃"),
        ]
    },
    
    # 瓷砖 Tiles
    "tiles": {
        "types": [
            ("ceramic tiles", "陶瓷砖"),
            ("porcelain tiles", "瓷质砖"),
            ("terracotta tiles", "陶土砖"),
            ("mosaic tiles", "马赛克"),
            ("subway tiles", "地铁砖"),
            ("hexagonal tiles", "六角砖"),
            ("herringbone tiles", "人字形砖"),
            ("fish scale tiles", "鱼鳞砖"),
            ("encaustic tiles", "水泥花砖"),
            ("zellige tiles", "泽利格砖"),
            ("penny tiles", "圆形马赛克"),
            ("large format tiles", "大板瓷砖"),
        ]
    },
    
    # 墙面处理 Wall Treatments
    "wall_treatments": {
        "types": [
            ("plaster", "石膏"),
            ("Venetian plaster", "威尼斯灰泥"),
            ("lime wash", "石灰水洗"),
            ("textured paint", "质感涂料"),
            ("exposed brick", "裸露砖墙"),
            ("shiplap", "搭叠板"),
            ("wainscoting", "护墙板"),
            ("wallpaper", "壁纸"),
            ("fabric wall covering", "布艺墙面"),
            ("acoustic panels", "吸音板"),
            ("3D wall panels", "3D墙板"),
            ("wall molding", "墙面线条"),
            ("coffered wall", "藻井墙面"),
        ]
    },
    
    # 地板 Flooring
    "flooring": {
        "types": [
            ("hardwood flooring", "实木地板"),
            ("engineered wood", "复合木地板"),
            ("laminate flooring", "强化地板"),
            ("vinyl flooring", "乙烯基地板"),
            ("LVT flooring", "LVT地板"),
            ("parquet flooring", "拼花地板"),
            ("herringbone floor", "人字形地板"),
            ("chevron floor", "鱼骨形地板"),
            ("poured concrete floor", "自流平地面"),
            ("polished concrete", "抛光混凝土"),
            ("epoxy flooring", "环氧地坪"),
            ("natural stone floor", "天然石材地板"),
            ("cork flooring", "软木地板"),
            ("sisal flooring", "剑麻地板"),
            ("tatami", "榻榻米"),
        ]
    },
}


# ==================== 灯光词典 Lighting ====================

LIGHTING = {
    # 自然光 Natural Light
    "natural_light": [
        ("natural lighting", "自然采光"),
        ("daylight", "日光"),
        ("sunlight streaming through windows", "阳光透过窗户"),
        ("soft diffused daylight", "柔和漫射日光"),
        ("dappled light", "斑驳光影"),
        ("golden hour light", "黄金时刻光线"),
        ("morning light", "晨光"),
        ("afternoon light", "午后光线"),
        ("sunset light", "落日余晖"),
        ("north-facing light", "北向光"),
        ("skylight illumination", "天窗照明"),
        ("clerestory light", "高窗采光"),
    ],
    
    # 人工照明类型 Artificial Lighting Types
    "artificial_types": [
        ("ambient lighting", "环境照明"),
        ("task lighting", "任务照明"),
        ("accent lighting", "重点照明"),
        ("decorative lighting", "装饰照明"),
        ("cove lighting", "灯槽照明"),
        ("recessed lighting", "嵌入式照明"),
        ("track lighting", "轨道灯"),
        ("pendant lighting", "吊灯照明"),
        ("chandelier", "水晶吊灯"),
        ("wall sconces", "壁灯"),
        ("floor lamp", "落地灯"),
        ("table lamp", "台灯"),
        ("LED strip lights", "LED灯带"),
        ("under-cabinet lighting", "橱柜下照明"),
        ("picture lights", "画灯"),
        ("uplighting", "向上照明"),
        ("downlighting", "向下照明"),
        ("backlighting", "背光照明"),
        ("indirect lighting", "间接照明"),
        ("spot lighting", "射灯"),
    ],
    
    # 光线质感 Light Quality
    "light_quality": [
        ("warm light", "暖光"),
        ("cool light", "冷光"),
        ("soft light", "柔光"),
        ("harsh light", "硬光"),
        ("diffused light", "漫射光"),
        ("directional light", "定向光"),
        ("dim lighting", "暗淡照明"),
        ("bright lighting", "明亮照明"),
        ("moody lighting", "情绪照明"),
        ("dramatic lighting", "戏剧性照明"),
        ("romantic lighting", "浪漫照明"),
        ("cozy lighting", "温馨照明"),
        ("atmospheric lighting", "氛围照明"),
        ("cinematic lighting", "电影感照明"),
    ],
    
    # 色温 Color Temperature
    "color_temperature": [
        ("2700K warm white", "2700K暖白"),
        ("3000K soft white", "3000K柔白"),
        ("4000K neutral white", "4000K中性白"),
        ("5000K daylight", "5000K日光"),
        ("6500K cool daylight", "6500K冷日光"),
        ("candlelight warm", "烛光温暖色"),
        ("tungsten light", "钨丝灯色"),
        ("fluorescent light", "荧光灯色"),
    ],
}


# ==================== 相机/摄影词典 Photography ====================

PHOTOGRAPHY = {
    # 相机设备 Camera Equipment
    "cameras": [
        ("Canon EOS R5", "佳能EOS R5"),
        ("Canon EOS 5D Mark IV", "佳能5D4"),
        ("Sony A7R IV", "索尼A7R4"),
        ("Nikon D850", "尼康D850"),
        ("Hasselblad", "哈苏"),
        ("Phase One", "飞思"),
        ("Leica", "徕卡"),
        ("medium format camera", "中画幅相机"),
        ("large format camera", "大画幅相机"),
        ("tilt-shift lens", "移轴镜头"),
    ],
    
    # 镜头 Lenses
    "lenses": [
        ("14mm ultra wide", "14mm超广角"),
        ("24mm wide angle", "24mm广角"),
        ("35mm lens", "35mm镜头"),
        ("50mm lens", "50mm镜头"),
        ("85mm portrait lens", "85mm人像镜头"),
        ("24-70mm zoom", "24-70mm变焦"),
        ("f/1.4 aperture", "f/1.4大光圈"),
        ("f/2.8 aperture", "f/2.8光圈"),
        ("tilt-shift 17mm", "17mm移轴"),
        ("tilt-shift 24mm", "24mm移轴"),
    ],
    
    # 视角 Perspectives
    "perspectives": [
        ("eye-level view", "平视角"),
        ("low angle shot", "低角度"),
        ("high angle shot", "高角度"),
        ("bird's eye view", "鸟瞰视角"),
        ("worm's eye view", "仰视角"),
        ("corner view", "转角视角"),
        ("one-point perspective", "一点透视"),
        ("two-point perspective", "两点透视"),
        ("three-point perspective", "三点透视"),
        ("wide establishing shot", "全景建立镜头"),
        ("medium shot", "中景"),
        ("close-up shot", "特写"),
        ("detail shot", "细节特写"),
        ("panoramic view", "全景"),
        ("vignette composition", "暗角构图"),
        ("symmetrical composition", "对称构图"),
        ("leading lines", "引导线构图"),
        ("rule of thirds", "三分法构图"),
    ],
    
    # 景深 Depth of Field
    "depth_of_field": [
        ("shallow depth of field", "浅景深"),
        ("deep depth of field", "深景深"),
        ("bokeh effect", "虚化效果"),
        ("tack sharp", "锐利对焦"),
        ("soft focus", "柔焦"),
        ("selective focus", "选择性对焦"),
        ("focus stacking", "焦点堆叠"),
    ],
    
    # 渲染风格 Rendering Styles
    "rendering": [
        ("photorealistic", "照片级真实"),
        ("hyperrealistic", "超写实"),
        ("architectural visualization", "建筑可视化"),
        ("3D rendering", "3D渲染"),
        ("V-Ray render", "V-Ray渲染"),
        ("Corona render", "Corona渲染"),
        ("Octane render", "Octane渲染"),
        ("Unreal Engine", "虚幻引擎"),
        ("ray tracing", "光线追踪"),
        ("global illumination", "全局光照"),
        ("HDRI lighting", "HDRI照明"),
        ("architectural photography", "建筑摄影"),
        ("interior photography", "室内摄影"),
        ("editorial interior shot", "杂志室内照"),
        ("real estate photography", "房产摄影"),
    ],
}


# ==================== 色彩词典 Colors ====================

COLORS = {
    # 中性色 Neutrals
    "neutrals": [
        ("pure white", "纯白"),
        ("off-white", "米白"),
        ("ivory", "象牙白"),
        ("cream", "奶油色"),
        ("eggshell", "蛋壳白"),
        ("beige", "米色"),
        ("taupe", "灰褐色"),
        ("greige", "灰米色"),
        ("sand", "沙色"),
        ("camel", "驼色"),
        ("warm gray", "暖灰"),
        ("cool gray", "冷灰"),
        ("charcoal", "炭灰"),
        ("slate gray", "石板灰"),
        ("black", "黑色"),
        ("jet black", "亮黑"),
        ("matte black", "哑光黑"),
    ],
    
    # 暖色调 Warm Tones
    "warm_tones": [
        ("terracotta", "陶土色"),
        ("rust", "铁锈色"),
        ("burnt orange", "焦橙色"),
        ("coral", "珊瑚色"),
        ("peach", "桃色"),
        ("apricot", "杏色"),
        ("mustard", "芥末黄"),
        ("ochre", "赭色"),
        ("amber", "琥珀色"),
        ("honey", "蜂蜜色"),
        ("cognac", "干邑色"),
        ("burgundy", "勃艮第红"),
        ("wine red", "酒红色"),
        ("blush pink", "腮红粉"),
        ("dusty rose", "灰粉色"),
        ("mauve", "藕荷色"),
    ],
    
    # 冷色调 Cool Tones
    "cool_tones": [
        ("navy blue", "海军蓝"),
        ("midnight blue", "午夜蓝"),
        ("cobalt blue", "钴蓝"),
        ("sapphire", "宝石蓝"),
        ("teal", "青色"),
        ("emerald", "祖母绿"),
        ("forest green", "森林绿"),
        ("sage green", "鼠尾草绿"),
        ("olive green", "橄榄绿"),
        ("moss green", "苔藓绿"),
        ("mint green", "薄荷绿"),
        ("seafoam", "海泡绿"),
        ("lavender", "薰衣草紫"),
        ("lilac", "淡紫色"),
        ("plum", "梅紫色"),
    ],
    
    # 大地色系 Earth Tones
    "earth_tones": [
        ("earth tones", "大地色系"),
        ("warm earth palette", "暖色大地调色板"),
        ("natural color palette", "自然色调色板"),
        ("muted tones", "柔和色调"),
        ("desaturated colors", "低饱和色彩"),
        ("organic colors", "有机色彩"),
        ("clay tones", "陶土色调"),
        ("stone colors", "石材色调"),
    ],
    
    # 金属色 Metallic
    "metallic": [
        ("gold accents", "金色点缀"),
        ("rose gold", "玫瑰金"),
        ("brass tones", "黄铜色调"),
        ("bronze accents", "青铜点缀"),
        ("copper highlights", "紫铜亮点"),
        ("silver accents", "银色点缀"),
        ("chrome finish", "镀铬效果"),
        ("champagne gold", "香槟金"),
    ],
}


# ==================== 家具词典 Furniture ====================

FURNITURE = {
    # 沙发 Sofas
    "sofas": [
        ("sectional sofa", "组合沙发"),
        ("L-shaped sofa", "L型沙发"),
        ("modular sofa", "模块化沙发"),
        ("Chesterfield sofa", "切斯特菲尔德沙发"),
        ("mid-century sofa", "中古世纪沙发"),
        ("tuxedo sofa", "礼服式沙发"),
        ("curved sofa", "弧形沙发"),
        ("cloud sofa", "云朵沙发"),
        ("loveseat", "双人沙发"),
        ("daybed", "贵妃椅"),
        ("settee", "小沙发"),
        ("banquette", "卡座"),
    ],
    
    # 椅子 Chairs
    "chairs": [
        ("accent chair", "点缀椅"),
        ("armchair", "扶手椅"),
        ("wingback chair", "高背翼椅"),
        ("club chair", "俱乐部椅"),
        ("lounge chair", "躺椅"),
        ("Eames lounge chair", "伊姆斯躺椅"),
        ("Barcelona chair", "巴塞罗那椅"),
        ("Wassily chair", "瓦西里椅"),
        ("Egg chair", "蛋椅"),
        ("papasan chair", "藤编圆椅"),
        ("rocking chair", "摇椅"),
        ("swivel chair", "转椅"),
        ("dining chair", "餐椅"),
        ("side chair", "边椅"),
        ("bar stool", "吧台椅"),
        ("counter stool", "高脚椅"),
        ("ottoman", "脚凳"),
        ("pouf", "蒲团"),
        ("bench", "长凳"),
    ],
    
    # 桌子 Tables
    "tables": [
        ("coffee table", "咖啡桌"),
        ("side table", "边几"),
        ("console table", "玄关柜"),
        ("dining table", "餐桌"),
        ("round dining table", "圆形餐桌"),
        ("oval dining table", "椭圆餐桌"),
        ("extendable table", "可伸缩餐桌"),
        ("pedestal table", "单脚桌"),
        ("trestle table", "支架桌"),
        ("nesting tables", "嵌套桌"),
        ("end table", "茶几"),
        ("nightstand", "床头柜"),
        ("desk", "书桌"),
        ("writing desk", "写字台"),
        ("secretary desk", "秘书桌"),
        ("vanity table", "梳妆台"),
    ],
    
    # 床 Beds
    "beds": [
        ("platform bed", "平台床"),
        ("upholstered bed", "软包床"),
        ("canopy bed", "四柱床"),
        ("poster bed", "立柱床"),
        ("sleigh bed", "雪橇床"),
        ("panel bed", "镶板床"),
        ("storage bed", "储物床"),
        ("Murphy bed", "墨菲床"),
        ("daybed", "日床"),
        ("bunk bed", "双层床"),
        ("king size bed", "大号床"),
        ("queen size bed", "中号床"),
        ("tufted headboard", "拉扣床头"),
        ("channel tufted headboard", "条纹拉扣床头"),
        ("wingback headboard", "翼形床头"),
    ],
    
    # 储物 Storage
    "storage": [
        ("bookshelf", "书架"),
        ("built-in bookcase", "嵌入式书柜"),
        ("floating shelves", "悬浮架"),
        ("credenza", "边柜"),
        ("sideboard", "餐边柜"),
        ("buffet", "自助餐柜"),
        ("armoire", "衣柜"),
        ("wardrobe", "衣橱"),
        ("dresser", "抽屉柜"),
        ("chest of drawers", "五斗柜"),
        ("media console", "电视柜"),
        ("display cabinet", "展示柜"),
        ("curio cabinet", "珍品柜"),
        ("bar cabinet", "酒柜"),
        ("hutch", "碗柜"),
    ],
}


# ==================== 装饰元素词典 Decorative Elements ====================

DECORATIVE = {
    # 软装 Soft Furnishings
    "soft_furnishings": [
        ("throw pillows", "抱枕"),
        ("decorative cushions", "装饰靠垫"),
        ("throw blanket", "披毯"),
        ("area rug", "地毯"),
        ("Persian rug", "波斯地毯"),
        ("Moroccan rug", "摩洛哥地毯"),
        ("kilim rug", "基利姆地毯"),
        ("sheepskin rug", "羊皮地毯"),
        ("jute rug", "黄麻地毯"),
        ("sisal rug", "剑麻地毯"),
        ("curtains", "窗帘"),
        ("sheer curtains", "纱帘"),
        ("drapes", "窗帘布"),
        ("Roman shades", "罗马帘"),
        ("blinds", "百叶窗"),
    ],
    
    # 艺术品 Artwork
    "artwork": [
        ("abstract painting", "抽象画"),
        ("oil painting", "油画"),
        ("watercolor painting", "水彩画"),
        ("photography print", "摄影作品"),
        ("gallery wall", "画廊墙"),
        ("large scale art", "大尺幅艺术"),
        ("statement art piece", "焦点艺术品"),
        ("sculpture", "雕塑"),
        ("ceramic art", "陶瓷艺术"),
        ("textile art", "纺织艺术"),
        ("wall tapestry", "挂毯"),
        ("macramé wall hanging", "编织挂饰"),
    ],
    
    # 植物 Plants
    "plants": [
        ("indoor plants", "室内植物"),
        ("potted plants", "盆栽"),
        ("hanging plants", "吊兰"),
        ("fiddle leaf fig", "琴叶榕"),
        ("monstera", "龟背竹"),
        ("snake plant", "虎皮兰"),
        ("olive tree", "橄榄树"),
        ("palm tree", "棕榈"),
        ("fern", "蕨类"),
        ("succulent", "多肉植物"),
        ("orchid", "兰花"),
        ("fresh flowers", "鲜花"),
        ("dried flowers", "干花"),
        ("pampas grass", "蒲苇"),
        ("living wall", "植物墙"),
        ("vertical garden", "垂直花园"),
    ],
    
    # 配件 Accessories
    "accessories": [
        ("decorative vase", "装饰花瓶"),
        ("ceramic vase", "陶瓷花瓶"),
        ("glass vase", "玻璃花瓶"),
        ("candle holders", "烛台"),
        ("decorative bowls", "装饰碗"),
        ("coffee table books", "茶几书"),
        ("decorative objects", "装饰物件"),
        ("sculptural objects", "雕塑物件"),
        ("mirrors", "镜子"),
        ("decorative mirror", "装饰镜"),
        ("round mirror", "圆镜"),
        ("sunburst mirror", "太阳镜"),
        ("clock", "时钟"),
        ("tray", "托盘"),
        ("decorative box", "装饰盒"),
    ],
}


# ==================== 画质/质量词典 Quality ====================

QUALITY = {
    # 分辨率 Resolution
    "resolution": [
        ("8K resolution", "8K分辨率"),
        ("4K ultra HD", "4K超高清"),
        ("high resolution", "高分辨率"),
        ("ultra detailed", "超精细"),
        ("extremely detailed", "极致细节"),
        ("intricate details", "精细复杂细节"),
        ("fine details", "精细细节"),
        ("sharp focus", "清晰对焦"),
        ("tack sharp", "锐利"),
        ("crisp details", "清晰细节"),
    ],
    
    # 质量描述 Quality Descriptors
    "descriptors": [
        ("professional photography", "专业摄影"),
        ("magazine quality", "杂志品质"),
        ("editorial quality", "编辑级品质"),
        ("award-winning photography", "获奖摄影"),
        ("masterpiece", "杰作"),
        ("best quality", "最佳品质"),
        ("high quality", "高品质"),
        ("studio quality", "影棚品质"),
        ("commercial photography", "商业摄影"),
    ],
    
    # 杂志/媒体参考 Magazine References
    "magazines": [
        ("Architectural Digest style", "AD风格"),
        ("Elle Decor style", "Elle Decor风格"),
        ("Dwell magazine", "Dwell杂志"),
        ("Dezeen featured", "Dezeen特辑"),
        ("Wallpaper magazine", "Wallpaper杂志"),
        ("House Beautiful", "House Beautiful"),
        ("Vogue Living", "Vogue Living"),
        ("World of Interiors", "World of Interiors"),
    ],
}


# ==================== 负面提示词词典 Negative Prompts ====================

NEGATIVE_PROMPTS = {
    # 质量问题 Quality Issues
    "quality_issues": [
        "low quality",
        "blurry",
        "pixelated",
        "grainy",
        "noisy",
        "jpeg artifacts",
        "compression artifacts",
        "out of focus",
        "motion blur",
        "chromatic aberration",
        "lens flare",
        "overexposed",
        "underexposed",
    ],
    
    # 畸变问题 Distortion Issues
    "distortion": [
        "distorted",
        "warped",
        "stretched",
        "squished",
        "skewed",
        "crooked lines",
        "bent walls",
        "tilted perspective",
        "wrong proportions",
        "anatomically incorrect",
        "deformed",
        "disfigured",
        "mutated",
    ],
    
    # 风格问题 Style Issues
    "style_issues": [
        "cartoon",
        "anime",
        "sketch",
        "drawing",
        "painting",
        "illustration",
        "3D render",
        "CGI",
        "fake looking",
        "plastic looking",
        "unrealistic",
        "surreal",
        "fantasy",
    ],
    
    # 内容问题 Content Issues
    "content_issues": [
        "watermark",
        "text",
        "logo",
        "signature",
        "copyright",
        "banner",
        "frame",
        "border",
        "people",
        "person",
        "human",
        "face",
        "hands",
        "animals",
        "pets",
    ],
    
    # 氛围问题 Mood Issues
    "mood_issues": [
        "dark",
        "gloomy",
        "dim",
        "shadowy",
        "horror",
        "scary",
        "disturbing",
        "messy",
        "cluttered",
        "dirty",
        "old",
        "worn",
        "damaged",
    ],
}


# ==================== 建筑师/设计师参考 Designer References ====================

DESIGNERS = {
    "interior_designers": [
        ("Kelly Wearstler", "凯莉·韦斯勒"),
        ("Axel Vervoordt", "阿塞尔·维尔沃特"),
        ("Vincent Van Duysen", "文森特·范·杜伊森"),
        ("Joseph Dirand", "约瑟夫·迪朗"),
        ("John Pawson", "约翰·鲍森"),
        ("Ilse Crawford", "伊尔斯·克劳福德"),
        ("India Mahdavi", "印蒂亚·马达维"),
        ("Pierre Yovanovitch", "皮埃尔·约万诺维奇"),
        ("Neri&Hu", "如恩设计"),
        ("Studio KO", "Studio KO"),
    ],
    
    "architects": [
        ("Tadao Ando", "安藤忠雄"),
        ("Kengo Kuma", "隈研吾"),
        ("Peter Zumthor", "彼得·卒姆托"),
        ("Alvaro Siza", "阿尔瓦罗·西扎"),
        ("Herzog & de Meuron", "赫尔佐格与德梅隆"),
        ("Renzo Piano", "伦佐·皮亚诺"),
        ("Norman Foster", "诺曼·福斯特"),
        ("Zaha Hadid", "扎哈·哈迪德"),
        ("SANAA", "妹岛和世"),
        ("Bjarke Ingels", "比亚克·英格斯"),
    ],
    
    "furniture_designers": [
        ("Charles and Ray Eames", "伊姆斯夫妇"),
        ("Hans Wegner", "汉斯·韦格纳"),
        ("Arne Jacobsen", "阿恩·雅各布森"),
        ("Le Corbusier", "勒·柯布西耶"),
        ("Ludwig Mies van der Rohe", "密斯·凡·德·罗"),
        ("Isamu Noguchi", "野口勇"),
        ("Charlotte Perriand", "夏洛特·佩里昂"),
        ("Verner Panton", "维尔纳·潘顿"),
        ("Patricia Urquiola", "帕特里夏·乌奎奥拉"),
    ],
}


# ==================== 导出函数 ====================

def get_material_prompt(category: str, item_type: str = None) -> str:
    """获取材质提示词"""
    if category in MATERIALS:
        mat = MATERIALS[category]
        if item_type and item_type in mat:
            return ", ".join([en for en, zh in mat[item_type]])
        # 返回所有类型
        all_items = []
        for key, items in mat.items():
            all_items.extend([en for en, zh in items])
        return ", ".join(all_items[:10])
    return ""


def get_lighting_prompt(category: str = "natural_light") -> str:
    """获取灯光提示词"""
    if category in LIGHTING:
        return ", ".join([en for en, zh in LIGHTING[category][:8]])
    return ""


def get_color_palette(style: str = "neutrals") -> str:
    """获取色彩调色板"""
    if style in COLORS:
        return ", ".join([en for en, zh in COLORS[style][:8]])
    return ""


def get_quality_prompt(level: str = "high") -> str:
    """获取质量提示词"""
    if level == "ultra":
        return ", ".join(QUALITY["resolution"][:5] + QUALITY["descriptors"][:3] + QUALITY["magazines"][:2])
    elif level == "high":
        return ", ".join([en for en, zh in QUALITY["resolution"][:3]] + [en for en, zh in QUALITY["descriptors"][:2]])
    return "high quality, detailed"


def get_negative_prompt() -> str:
    """获取完整负面提示词"""
    all_negatives = []
    for category, items in NEGATIVE_PROMPTS.items():
        all_negatives.extend(items[:5])
    return ", ".join(all_negatives)


def build_professional_prompt(
    room_type: str,
    style: str,
    materials: List[str] = None,
    lighting: str = "natural_light",
    color_palette: str = "neutrals",
    quality: str = "high",
) -> Dict[str, str]:
    """
    构建专业的室内设计提示词
    
    Args:
        room_type: 房间类型
        style: 设计风格
        materials: 材质列表
        lighting: 灯光类型
        color_palette: 色彩调色板
        quality: 质量级别
    
    Returns:
        包含 prompt 和 negative_prompt 的字典
    """
    prompt_parts = []
    
    # 质量前缀
    prompt_parts.append(get_quality_prompt(quality))
    
    # 房间和风格
    prompt_parts.append(f"{style} {room_type}")
    
    # 材质
    if materials:
        mat_prompts = []
        for mat in materials:
            for cat, data in MATERIALS.items():
                for key, items in data.items():
                    for en, zh in items:
                        if mat.lower() in en.lower() or mat in zh:
                            mat_prompts.append(en)
                            break
        if mat_prompts:
            prompt_parts.append(", ".join(mat_prompts[:5]))
    
    # 灯光
    prompt_parts.append(get_lighting_prompt(lighting))
    
    # 色彩
    prompt_parts.append(get_color_palette(color_palette))
    
    return {
        "prompt": ", ".join(prompt_parts),
        "negative_prompt": get_negative_prompt(),
    }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("专业室内设计词典测试")
    print("=" * 60)
    
    # 统计词汇量
    total_terms = 0
    for cat, data in MATERIALS.items():
        for key, items in data.items():
            total_terms += len(items)
    print(f"材质词汇: {total_terms} 条")
    
    lighting_terms = sum(len(items) for items in LIGHTING.values())
    print(f"灯光词汇: {lighting_terms} 条")
    
    color_terms = sum(len(items) for items in COLORS.values())
    print(f"色彩词汇: {color_terms} 条")
    
    furniture_terms = sum(len(items) for items in FURNITURE.values())
    print(f"家具词汇: {furniture_terms} 条")
    
    deco_terms = sum(len(items) for items in DECORATIVE.values())
    print(f"装饰词汇: {deco_terms} 条")
    
    photo_terms = sum(len(items) for items in PHOTOGRAPHY.values())
    print(f"摄影词汇: {photo_terms} 条")
    
    print(f"\n📊 总计: {total_terms + lighting_terms + color_terms + furniture_terms + deco_terms + photo_terms}+ 专业术语")
    
    # 测试构建prompt
    print("\n" + "-" * 60)
    print("测试专业Prompt生成:")
    result = build_professional_prompt(
        room_type="living room",
        style="modern minimalist",
        materials=["oak", "marble", "velvet"],
        lighting="natural_light",
        color_palette="neutrals",
        quality="ultra"
    )
    print(f"\nPrompt:\n{result['prompt'][:200]}...")
    print(f"\nNegative:\n{result['negative_prompt'][:100]}...")
