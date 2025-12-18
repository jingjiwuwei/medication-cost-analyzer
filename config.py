#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责加载和验证环境变量配置
"""

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    """配置类"""
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
    
    # 处理配置
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    
    # 路径配置
    CACHE_DIR = Path(os.getenv('CACHE_DIR', './data/cache'))
    OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', './output'))
    LOG_DIR = Path(os.getenv('LOG_DIR', './output/logs'))
    
    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("请在.env文件中配置OPENAI_API_KEY")
