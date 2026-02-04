# 🏛️ NanoBanana AI - 顶级室内设计AI平台

> **Transform Empty Spaces into Dream Interiors with AI**
> 
> 将毛胚房一键转化为精装效果图的商业级AI设计平台

---

## ✨ 项目定位

**商业级 · 极致精致 · 高端建筑美学**

面向房地产开发商、室内设计师、装修公司的专业AI渲染平台，提供：
- 🏠 毛胚房 → 精装效果图（4K超清）
- 🎨 10+ 顶级设计风格（侘寂、奶油风、新中式...）
- ⚡ 78秒出图，¥0.18/张超低成本
- 🔄 多Pass工作流（材质替换 → 边缘融合 → 家具添加）

---

## 🎯 设计理念

### 视觉风格
- **建筑网格布局** - 精确、有序、专业感
- **大气摄影展示** - 氛围感胜过临床感
- **极简交互** - 聚焦核心功能，减少干扰
- **深色/浅色双模式** - 适应不同场景

### 参考标杆
- Architectural Digest 官网
- Kelly Wearstler Studio
- Norm Architects
- Studio McGee

---

## 🛠️ 技术栈

### 核心框架
| 技术 | 版本 | 用途 |
|------|------|------|
| **Next.js** | 15.x | React全栈框架，App Router |
| **React** | 19.x | UI组件库 |
| **TypeScript** | 5.x | 类型安全 |

### UI/样式
| 技术 | 版本 | 用途 |
|------|------|------|
| **Tailwind CSS** | 4.x | 原子化CSS |
| **shadcn/ui** | latest | 高质量组件库 |
| **Radix UI** | latest | 无障碍原语组件 |
| **Lucide Icons** | latest | 精致图标库 |
| **Framer Motion** | 11.x | 流畅动画 |

### 状态/数据
| 技术 | 用途 |
|------|------|
| **Zustand** | 轻量状态管理 |
| **TanStack Query** | 服务端状态/缓存 |
| **React Hook Form** | 表单处理 |
| **Zod** | Schema验证 |

### 工具链
| 技术 | 用途 |
|------|------|
| **pnpm** | 包管理器 |
| **ESLint** | 代码检查 |
| **Prettier** | 代码格式化 |
| **Husky** | Git Hooks |

---

## 📁 项目结构

```
frontend/
├── app/                      # Next.js App Router
│   ├── (marketing)/          # 营销页面组
│   │   ├── page.tsx          # 首页
│   │   ├── pricing/          # 定价页
│   │   └── about/            # 关于我们
│   ├── (app)/                # 应用页面组
│   │   ├── studio/           # AI设计工作台
│   │   ├── gallery/          # 作品展示
│   │   ├── projects/         # 项目管理
│   │   └── settings/         # 设置
│   ├── api/                  # API Routes
│   ├── layout.tsx            # 根布局
│   └── globals.css           # 全局样式
│
├── components/               # 组件库
│   ├── ui/                   # shadcn/ui 基础组件
│   ├── layout/               # 布局组件
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── Navigation.tsx
│   ├── marketing/            # 营销组件
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   ├── Showcase.tsx
│   │   ├── Testimonials.tsx
│   │   └── CTA.tsx
│   ├── studio/               # 工作台组件
│   │   ├── ImageUploader.tsx
│   │   ├── StyleSelector.tsx
│   │   ├── RoomTypeSelector.tsx
│   │   ├── MaterialPicker.tsx
│   │   ├── PreviewPanel.tsx
│   │   ├── GenerationProgress.tsx
│   │   └── ResultGallery.tsx
│   └── shared/               # 共享组件
│       ├── ImageCompare.tsx
│       ├── BeforeAfter.tsx
│       └── LoadingSpinner.tsx
│
├── lib/                      # 工具库
│   ├── api/                  # API客户端
│   │   ├── client.ts
│   │   ├── endpoints.ts
│   │   └── types.ts
│   ├── hooks/                # 自定义Hooks
│   │   ├── useGenerate.ts
│   │   ├── useUpload.ts
│   │   └── useProject.ts
│   ├── stores/               # Zustand stores
│   │   ├── studio.ts
│   │   └── user.ts
│   ├── utils/                # 工具函数
│   │   ├── cn.ts
│   │   ├── format.ts
│   │   └── validation.ts
│   └── constants/            # 常量
│       ├── styles.ts
│       ├── rooms.ts
│       └── materials.ts
│
├── public/                   # 静态资源
│   ├── images/
│   │   ├── hero/
│   │   ├── showcase/
│   │   └── styles/
│   ├── fonts/
│   └── icons/
│
├── styles/                   # 样式文件
│   └── themes/
│       ├── light.css
│       └── dark.css
│
├── types/                    # TypeScript类型
│   ├── api.ts
│   ├── studio.ts
│   └── project.ts
│
├── .env.local                # 环境变量
├── .env.example              # 环境变量示例
├── next.config.ts            # Next.js配置
├── tailwind.config.ts        # Tailwind配置
├── tsconfig.json             # TypeScript配置
├── package.json              # 依赖配置
└── README.md                 # 项目文档
```

---

## 🎨 页面规划

### 1. 营销首页 `/`
- **Hero区域** - 震撼的Before/After对比展示
- **功能亮点** - 4K超清、多风格、快速出图
- **风格展廊** - 10+设计风格预览
- **客户案例** - 真实项目展示
- **定价方案** - 透明定价
- **CTA** - 立即体验

### 2. AI工作台 `/studio`
- **左侧** - 图片上传区
- **中间** - 风格/房型/材质选择
- **右侧** - 实时预览 + 生成进度
- **底部** - 历史记录

### 3. 作品展廊 `/gallery`
- **瀑布流布局** - 精美作品展示
- **筛选器** - 按风格/房型筛选
- **详情弹窗** - 大图 + 参数信息

### 4. 项目管理 `/projects`
- **项目列表** - 卡片式展示
- **项目详情** - 多版本对比
- **导出功能** - 4K下载/分享

---

## 🚀 快速开始

### 环境要求
- Node.js >= 18.0
- pnpm >= 8.0

### 安装依赖
```bash
cd frontend
pnpm install
```

### 环境变量
```bash
cp .env.example .env.local
# 编辑 .env.local 填入 API 配置
```

### 启动开发服务器
```bash
pnpm dev
```

### 构建生产版本
```bash
pnpm build
pnpm start
```

---

## 📦 依赖安装命令

```bash
# 创建 Next.js 项目
pnpm create next-app@latest . --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"

# 安装 shadcn/ui
pnpm dlx shadcn@latest init

# 安装核心组件
pnpm dlx shadcn@latest add button card dialog dropdown-menu input label select tabs toast tooltip avatar badge separator skeleton slider switch textarea scroll-area sheet popover command

# 安装其他依赖
pnpm add zustand @tanstack/react-query framer-motion lucide-react react-dropzone react-compare-image

# 安装开发依赖
pnpm add -D @types/node prettier eslint-config-prettier
```

---

## 🎯 开发规范

### 组件规范
- 使用函数组件 + Hooks
- Props 使用 TypeScript interface
- 组件文件使用 PascalCase
- 工具函数使用 camelCase

### 样式规范
- 优先使用 Tailwind 类
- 复杂样式抽取到 CSS 变量
- 响应式设计：mobile-first
- 深色模式：使用 `dark:` 前缀

### Git规范
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 样式
- refactor: 重构
- perf: 性能优化

---

## 📄 License

MIT © 2024 NanoBanana AI
