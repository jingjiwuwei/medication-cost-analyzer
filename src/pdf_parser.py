#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF解析模块
使用pdfplumber提取PDF文本内容，支持批量处理
"""

import pdfplumber
from pathlib import Path
from typing import Dict, List
import logging
from tqdm import tqdm


class PDFParser:
    """PDF解析器"""
    
    def __init__(self, pdf_directory: str):
        """
        初始化PDF解析器
        
        Args:
            pdf_directory: PDF文件目录路径
        """
        self.pdf_directory = Path(pdf_directory)
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, pdf_path: Path) -> str:
        """
        提取单个PDF的文本内容
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            提取的文本内容
            
        Raises:
            Exception: PDF解析失败时抛出异常
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
            return text
        except Exception as e:
            self.logger.error(f"解析PDF失败 {pdf_path}: {str(e)}")
            raise
    
    def batch_process(self, processed_cache: set = None) -> Dict[str, str]:
        """
        批量处理所有PDF文件
        
        Args:
            processed_cache: 已处理的文件集合（用于断点续传）
            
        Returns:
            {药品名称: 文本内容} 字典
        """
        if processed_cache is None:
            processed_cache = set()
        
        pdf_files = list(self.pdf_directory.glob('*.pdf'))
        results = {}
        
        for pdf_file in tqdm(pdf_files, desc="解析PDF文件"):
            drug_name = pdf_file.stem  # 文件名作为药品名称
            
            if drug_name in processed_cache:
                self.logger.info(f"跳过已处理文件: {drug_name}")
                continue
            
            try:
                text = self.extract_text(pdf_file)
                results[drug_name] = text
            except Exception as e:
                self.logger.error(f"处理 {drug_name} 失败: {str(e)}")
                results[drug_name] = None
        
        return results
