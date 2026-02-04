"""
下载开源数据集脚本

支持的数据集:
1. Zillow Indoor Dataset (ZInD) - 67,448张毛胚房全景图
2. 3D-FRONT - 18,797个带家具房间
3. Interior Design Dataset (Kaggle) - 4,147张室内设计图

注意: 部分数据集需要申请访问权限
"""
import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

@dataclass
class DatasetInfo:
    name: str
    url: str
    description: str
    size: str
    requires_auth: bool
    instructions: str

# 数据集信息
DATASETS = {
    "zind": DatasetInfo(
        name="Zillow Indoor Dataset (ZInD)",
        url="https://github.com/zillow/zind",
        description="67,448张360°全景图，来自1,575个未装修住宅",
        size="~40GB",
        requires_auth=True,
        instructions="""
下载步骤:
1. 访问 https://bridgedataoutput.com/register/zgindoor 注册账号
2. 同意 Zillow Data Terms of Use
3. 等待审批 (约1-2周)
4. 获取 Server Token
5. 运行: python download_data.py -s <server_token> -o ./data/zind
"""
    ),
    "3dfront": DatasetInfo(
        name="3D-FRONT Dataset",
        url="https://tianchi.aliyun.com/specials/promotion/alibaba-3d-scene-dataset",
        description="18,797个带家具的3D房间，7,302个家具模型",
        size="~20GB",
        requires_auth=True,
        instructions="""
下载步骤:
1. 访问阿里云天池数据集页面
2. 使用阿里云账号登录
3. 申请数据集访问权限
4. 下载数据集文件
"""
    ),
    "interior_design_kaggle": DatasetInfo(
        name="Interior Design Dataset (Kaggle)",
        url="https://www.kaggle.com/aishahsofea/interior-design",
        description="4,147张室内设计图 (256x256)",
        size="~500MB",
        requires_auth=False,
        instructions="""
下载步骤:
1. 安装 kaggle CLI: pip install kaggle
2. 配置 API key: ~/.kaggle/kaggle.json
3. 运行: kaggle datasets download -d aishahsofea/interior-design
"""
    ),
    "furniture_detector": DatasetInfo(
        name="Furniture Detector Dataset",
        url="https://www.kaggle.com/akkithetechie/furniture-detector",
        description="4,447张家具图片 (床/椅子/沙发/转椅/桌子)",
        size="~300MB",
        requires_auth=False,
        instructions="""
下载步骤:
1. 安装 kaggle CLI: pip install kaggle
2. 运行: kaggle datasets download -d akkithetechie/furniture-detector
"""
    )
}

def print_dataset_info():
    """打印所有数据集信息"""
    print("=" * 60)
    print("可用的开源数据集")
    print("=" * 60)
    
    for key, ds in DATASETS.items():
        print(f"\n📁 {ds.name}")
        print(f"   ID: {key}")
        print(f"   URL: {ds.url}")
        print(f"   描述: {ds.description}")
        print(f"   大小: {ds.size}")
        print(f"   需要认证: {'是' if ds.requires_auth else '否'}")
        print(f"   {ds.instructions}")

def download_kaggle_dataset(dataset_name: str, output_dir: Path):
    """下载Kaggle数据集"""
    try:
        import kaggle
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {dataset_name} to {output_dir}...")
        kaggle.api.dataset_download_files(dataset_name, path=str(output_dir), unzip=True)
        print("Download completed!")
    except ImportError:
        print("请先安装kaggle: pip install kaggle")
    except Exception as e:
        print(f"下载失败: {e}")

def setup_data_directories():
    """创建数据目录结构"""
    dirs = [
        DATA_DIR / "raw" / "zind",
        DATA_DIR / "raw" / "3dfront",
        DATA_DIR / "raw" / "kaggle",
        DATA_DIR / "processed",
        DATA_DIR / "uploads",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created: {d}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="下载室内设计数据集")
    parser.add_argument("--list", action="store_true", help="列出所有可用数据集")
    parser.add_argument("--download", type=str, help="下载指定数据集 (如: interior_design_kaggle)")
    parser.add_argument("--setup", action="store_true", help="创建数据目录结构")
    
    args = parser.parse_args()
    
    if args.list:
        print_dataset_info()
    elif args.setup:
        setup_data_directories()
    elif args.download:
        if args.download == "interior_design_kaggle":
            download_kaggle_dataset("aishahsofea/interior-design", DATA_DIR / "raw" / "kaggle")
        elif args.download == "furniture_detector":
            download_kaggle_dataset("akkithetechie/furniture-detector", DATA_DIR / "raw" / "kaggle")
        else:
            ds = DATASETS.get(args.download)
            if ds:
                print(f"\n{ds.name} 需要手动下载:")
                print(ds.instructions)
            else:
                print(f"未知数据集: {args.download}")
                print("使用 --list 查看所有可用数据集")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
