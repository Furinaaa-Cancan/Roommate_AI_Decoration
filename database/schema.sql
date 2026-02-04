-- NanoBanana AI 数据库Schema
-- 用于存储毛胚房照片和AI生成结果

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) COMMENT '密码哈希',
    password_salt VARCHAR(64) COMMENT '密码盐值',
    openid VARCHAR(128) UNIQUE COMMENT '微信openid',
    google_id VARCHAR(128) UNIQUE COMMENT 'Google账号ID',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    nickname VARCHAR(64) COMMENT '昵称',
    avatar_url VARCHAR(512) COMMENT '头像URL',
    membership_type ENUM('free', 'personal', 'designer', 'enterprise') DEFAULT 'free' COMMENT '会员类型',
    membership_expire_at DATETIME COMMENT '会员过期时间',
    credits INT DEFAULT 10 COMMENT '剩余积分/次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_openid (openid),
    INDEX idx_google_id (google_id),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. OAuth 账号关联表
CREATE TABLE IF NOT EXISTS oauth_accounts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    provider VARCHAR(32) NOT NULL COMMENT 'OAuth提供商 (google/wechat/github)',
    provider_account_id VARCHAR(255) NOT NULL COMMENT '提供商账号ID',
    access_token TEXT COMMENT '访问令牌',
    refresh_token TEXT COMMENT '刷新令牌',
    expires_at DATETIME COMMENT '令牌过期时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_provider_account (provider, provider_account_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='OAuth账号关联表';

-- 2. 毛胚房原图表
CREATE TABLE IF NOT EXISTS raw_photos (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT COMMENT '上传用户ID，NULL表示系统数据集',
    
    -- 图片信息
    original_url VARCHAR(512) NOT NULL COMMENT '原图OSS地址',
    thumbnail_url VARCHAR(512) COMMENT '缩略图地址',
    file_size INT COMMENT '文件大小(bytes)',
    width INT COMMENT '图片宽度',
    height INT COMMENT '图片高度',
    
    -- 空间识别
    room_type ENUM('living_room', 'bedroom', 'master_bedroom', 'kitchen', 'bathroom', 'dining_room', 'study', 'balcony', 'other') COMMENT '房间类型',
    room_type_confidence FLOAT COMMENT 'AI识别置信度',
    
    -- 来源标记
    source ENUM('user_upload', 'dataset_zind', 'dataset_3dfront', 'dataset_other') DEFAULT 'user_upload' COMMENT '图片来源',
    source_id VARCHAR(128) COMMENT '数据集中的原始ID',
    
    -- 元数据
    metadata JSON COMMENT '其他元数据(EXIF等)',
    
    status ENUM('pending', 'ready', 'processing', 'error') DEFAULT 'pending' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_room_type (room_type),
    INDEX idx_source (source),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='毛胚房原图表';

-- 3. AI生成任务表
CREATE TABLE IF NOT EXISTS generation_tasks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_uuid VARCHAR(64) UNIQUE NOT NULL COMMENT '任务唯一标识',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    raw_photo_id BIGINT NOT NULL COMMENT '原图ID',
    
    -- 生成参数
    style VARCHAR(64) DEFAULT 'nanobanana' COMMENT '风格',
    style_variant CHAR(1) COMMENT '风格变体 A/B/C',
    prompt TEXT COMMENT '生成prompt',
    negative_prompt TEXT COMMENT '负向prompt',
    
    -- API调用
    api_provider ENUM('replicate', 'runpod', 'self_hosted') DEFAULT 'replicate' COMMENT 'API提供商',
    api_model VARCHAR(128) COMMENT '使用的模型',
    api_request_id VARCHAR(128) COMMENT 'API请求ID',
    api_cost DECIMAL(10, 6) COMMENT 'API调用成本(USD)',
    
    -- 状态
    status ENUM('pending', 'queued', 'processing', 'completed', 'failed') DEFAULT 'pending',
    error_message TEXT COMMENT '错误信息',
    
    -- 时间
    started_at DATETIME COMMENT '开始处理时间',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_task_uuid (task_uuid),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (raw_photo_id) REFERENCES raw_photos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI生成任务表';

-- 4. 生成结果图表
CREATE TABLE IF NOT EXISTS generated_images (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL COMMENT '任务ID',
    
    -- 图片信息
    image_url VARCHAR(512) NOT NULL COMMENT '生成图OSS地址',
    thumbnail_url VARCHAR(512) COMMENT '缩略图地址',
    watermarked_url VARCHAR(512) COMMENT '带水印版本',
    
    -- 图片属性
    width INT COMMENT '宽度',
    height INT COMMENT '高度',
    sequence_num INT DEFAULT 1 COMMENT '序号(同一任务多张)',
    
    -- 质量标记
    quality_score FLOAT COMMENT 'AI质量评分',
    is_primary BOOLEAN DEFAULT FALSE COMMENT '是否主图',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_task_id (task_id),
    FOREIGN KEY (task_id) REFERENCES generation_tasks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生成结果图表';

-- 5. 订单表（付费解锁）
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(64) UNIQUE NOT NULL COMMENT '订单号',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    
    -- 订单类型
    order_type ENUM('unlock_hd', 'multi_plan', 'full_house', 'material_list', 'edit_pack', 'membership') NOT NULL COMMENT '订单类型',
    
    -- 关联
    task_id BIGINT COMMENT '关联的生成任务',
    
    -- 金额
    amount DECIMAL(10, 2) NOT NULL COMMENT '订单金额(CNY)',
    paid_amount DECIMAL(10, 2) COMMENT '实付金额',
    
    -- 支付
    pay_channel ENUM('wechat', 'alipay') COMMENT '支付渠道',
    pay_trade_no VARCHAR(128) COMMENT '第三方支付单号',
    
    -- 状态
    status ENUM('pending', 'paid', 'refunded', 'cancelled') DEFAULT 'pending',
    paid_at DATETIME COMMENT '支付时间',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES generation_tasks(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 6. 数据集导入记录表（用于追踪开源数据集）
CREATE TABLE IF NOT EXISTS dataset_imports (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    dataset_name VARCHAR(64) NOT NULL COMMENT '数据集名称',
    dataset_version VARCHAR(32) COMMENT '版本',
    source_url VARCHAR(512) COMMENT '来源URL',
    
    total_count INT DEFAULT 0 COMMENT '总数量',
    imported_count INT DEFAULT 0 COMMENT '已导入数量',
    failed_count INT DEFAULT 0 COMMENT '失败数量',
    
    status ENUM('pending', 'importing', 'completed', 'failed') DEFAULT 'pending',
    started_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_dataset_name (dataset_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据集导入记录表';
