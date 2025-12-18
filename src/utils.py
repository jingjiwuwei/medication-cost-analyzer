#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供日志配置、缓存管理等通用功能
"""

import json
import logging
from pathlib import Path
from typing import Set


def setup_logging(log_dir: str = './output/logs'):
    """
    配置日志系统
    
    Args:
        log_dir: 日志目录路径
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    log_file = log_path / f'process_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def load_cache(cache_file: str) -> Set[str]:
    """
    加载处理缓存
    
    Args:
        cache_file: 缓存文件路径
        
    Returns:
        已处理的药品名称集合
    """
    cache_path = Path(cache_file)
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()


def save_cache(cache_file: str, processed: Set[str]):
    """
    保存处理缓存
    
    Args:
        cache_file: 缓存文件路径
        processed: 已处理的药品名称集合
    """
    cache_path = Path(cache_file)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(list(processed), f, ensure_ascii=False, indent=2)
