# AI API 与数据集资源汇总

## 🎯 推荐API (便宜且好用)

### 1. Replicate - stable-interiors-v2 ⭐⭐⭐⭐⭐ 首选

| 项目 | 详情 |
|-----|------|
| **模型** | youzu/stable-interiors-v2 |
| **价格** | **$0.015/次** (约 ¥0.11/次) |
| **换算** | 66次生成/$1，约 600次/¥50 |
| **输出** | 1024×1024 高清图 |
| **速度** | ~16秒/张 |
| **URL** | https://replicate.com/youzu/stable-interiors-v2 |

```python
# 快速调用示例
import replicate

output = replicate.run(
    "youzu/stable-interiors-v2",
    input={
        "image": "https://your-image-url.jpg",
        "prompt": "modern minimalist interior, warm tones",
        "num_outputs": 4
    }
)
```

**优势**:
- 价格极低，适合起步验证
- 开箱即用，无需部署
- 支持高清1024x1024输出
- 室内设计专用模型

---

### 2. 其他备选API

| API | 价格 | 特点 |
|-----|------|------|
| **Decor8 AI** | ~$0.05/张 | 虚拟staging专用 |
| **Spacely AI** | 订阅制 | 商业化产品 |
| **RunPod Serverless** | ~$0.01/张 | 需自己部署模型 |
| **自建GPU** | ~$0.005/张 | 需购买/租用GPU服务器 |

---

### 3. 成本估算

按每天1000次生成计算:

| 方案 | 日成本 | 月成本 |
|-----|--------|--------|
| Replicate | $15 (¥110) | $450 (¥3300) |
| RunPod | $10 (¥73) | $300 (¥2200) |
| 自建(A100) | $5 (¥37) | $150 (¥1100) |

**建议**: 先用Replicate验证流程，日均>5000次后考虑自建

---

## 📦 开源数据集

### 1. Zillow Indoor Dataset (ZInD) ⭐⭐⭐⭐⭐ 最佳

| 项目 | 详情 |
|-----|------|
| **数量** | 67,448张全景图 |
| **来源** | 1,575个未装修住宅 |
| **格式** | 360° RGB全景 |
| **标注** | 3D布局、门窗标注、户型图 |
| **大小** | ~40GB |
| **授权** | 非商用免费，商用需联系 |
| **URL** | https://github.com/zillow/zind |

**下载步骤**:
1. 注册 https://bridgedataoutput.com/register/zgindoor
2. 等待审批 (1-2周)
3. 获取Server Token
4. 运行下载脚本

---

### 2. 3D-FRONT (阿里巴巴)

| 项目 | 详情 |
|-----|------|
| **数量** | 18,797个房间 |
| **家具** | 7,302个3D家具模型 |
| **格式** | 3D场景 + 渲染图 |
| **URL** | https://tianchi.aliyun.com/specials/promotion/alibaba-3d-scene-dataset |

---

### 3. Kaggle 数据集 (快速获取)

| 数据集 | 数量 | 大小 | 链接 |
|-------|------|------|------|
| Interior Design | 4,147张 | ~500MB | kaggle.com/aishahsofea/interior-design |
| Furniture Detector | 4,447张 | ~300MB | kaggle.com/akkithetechie/furniture-detector |

```bash
# 快速下载
pip install kaggle
kaggle datasets download -d aishahsofea/interior-design
```

---

### 4. 其他资源

| 数据集 | 说明 |
|-------|------|
| **InteriorNet** | 20M张室内图，需申请 |
| **SUN RGB-D** | 10K张RGBD室内图 |
| **SceneNet** | 500万合成室内场景 |

---

## 🚀 Baseline 快速启动

### Step 1: 配置环境

```bash
cd 建筑AI
cp .env.example .env
# 编辑 .env，填入 REPLICATE_API_TOKEN
```

### Step 2: 获取 Replicate Token

1. 访问 https://replicate.com
2. 注册/登录
3. 进入 Account Settings → API Tokens
4. 创建新Token，复制到 `.env`

### Step 3: 安装依赖

```bash
pip install -r requirements.txt
```

### Step 4: 测试生成

```bash
cd backend
python pipeline.py
```

### Step 5: 启动API服务

```bash
cd backend
uvicorn main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看API文档

---

## 💰 商业化建议

1. **起步期 (0-1000次/天)**: 
   - 使用 Replicate，成本可控 (~¥100/天)

2. **增长期 (1000-5000次/天)**:
   - 考虑 RunPod Serverless
   - 或租用GPU服务器

3. **规模期 (5000+次/天)**:
   - 自建GPU集群
   - 多模型负载均衡
