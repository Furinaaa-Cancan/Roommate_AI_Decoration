# 空间氛围视频生成模块

## 技术定位

**SVD = 空间效果图的「动态视觉包装技术」**

- ✅ 是：静态效果图 → 有镜头感的短视频
- ❌ 不是：真实漫游、3D重建、精确结构

## 使用场景

- 室内装潢方案的第一印象展示
- 风格提案 / 氛围提案
- 销售演示 / 客户汇报
- App 内"让效果图动起来"的体验升级

## 技术要求

### 本地推理
- NVIDIA GPU（建议 12GB+ 显存）
- Python 3.10+
- CUDA 11.8+

### 依赖安装
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate
```

## 快速使用

```python
from services.video_generation import SVDService

service = SVDService()
result = await service.generate_video(
    image_path="室内效果图.jpg",
    num_frames=25,  # 约3.5秒
    motion_bucket_id=127  # 运动幅度 1-255
)

if result.success:
    print(f"视频已生成: {result.video_path}")
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| num_frames | 25 | 帧数，25帧约3.5秒 |
| fps | 7 | 帧率 |
| motion_bucket_id | 127 | 运动幅度 (1-255) |
| noise_aug_strength | 0.02 | 噪声强度，越低越稳定 |

## 推荐参数（室内场景）

```python
# 轻柔推镜（最稳定）
motion_bucket_id=80, noise_aug_strength=0.01

# 中等运动（默认）
motion_bucket_id=127, noise_aug_strength=0.02

# 明显运动（可能不稳定）
motion_bucket_id=180, noise_aug_strength=0.03
```

## 技术演进路线

```
第一阶段: SVD → "空间氛围视频" (当前)
    ↓
第二阶段: LTX-Video → "可控镜头路径"
    ↓
第三阶段: 3DGS/Marble → "真实可交互漫游"
```

## 产品命名建议

✅ 安全命名：
- 空间氛围视频
- 动态效果展示
- AI 空间动效

❌ 避免使用：
- AI 室内漫游
- 真实空间体验
- 虚拟看房
