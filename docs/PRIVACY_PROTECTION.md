# 隐私保护说明

## 已保护的敏感文件

本项目已对以下包含隐私信息的文件进行保护,确保它们不会被提交到版本控制系统:

### 1. 根目录图片文件
- `56acda7da2749042222a103c8276ef80.jpg` - 可能包含二维码等隐私信息
- `d971ba76018d4b1f6aba32bde295b617.jpg` - 可能包含二维码等隐私信息

### 2. 支付二维码目录
- `frontend/public/payment/*.jpg` - 微信/支付宝收款码
- `frontend/public/payment/*.png` - 其他格式的收款码
- `frontend/public/payment/*.jpeg` - 其他格式的收款码

### 3. 环境变量文件
- `.env.local` - 包含 API 密钥、OAuth 凭证等敏感信息
- `.env` - 本地环境配置

## 使用说明

### 添加支付二维码

如需添加支付二维码,请将图片放置在 `frontend/public/payment/` 目录下:

```
frontend/public/payment/
├── wechat.jpg   # 微信收款码
└── alipay.jpg   # 支付宝收款码
```

这些文件已被 `.gitignore` 保护,不会被提交到 Git 仓库。

### 环境变量配置

1. 复制 `.env.example` 为 `.env.local`
2. 填入真实的 API 密钥和凭证
3. 确保 `.env.local` 不被提交(已在 `.gitignore` 中配置)

## 安全检查清单

在提交代码前,请确认:

- [ ] 没有硬编码 API 密钥或密码
- [ ] 支付二维码未被添加到 Git
- [ ] `.env.local` 文件未被提交
- [ ] 个人隐私图片已添加到 `.gitignore`

## 相关文件

- `.gitignore` - Git 忽略规则配置
- `frontend/.env.example` - 环境变量模板
- `frontend/app/(app)/checkout/page.tsx` - 支付页面(引用二维码)

---

**最后更新**: 2026-02-16
