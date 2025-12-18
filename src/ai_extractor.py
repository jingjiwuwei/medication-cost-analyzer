#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI提取模块
使用OpenAI API从药品说明书中提取用法用量信息
"""

from openai import OpenAI
import json
import logging
from typing import Dict, Optional
import time


class DosageExtractor:
    """使用OpenAI API提取用法用量信息"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_retries: int = 3):
        """
        初始化用法用量提取器
        
        Args:
            api_key: OpenAI API密钥
            model: 使用的模型名称
            max_retries: 最大重试次数
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
    
    def extract_dosage_info(self, drug_name: str, text: str) -> Optional[Dict]:
        """
        使用LLM提取用法用量信息
        
        Args:
            drug_name: 药品名称
            text: 说明书文本内容
            
        Returns:
            提取的结构化信息字典，失败返回None
        """
        prompt = f"""你是专业的药品说明书分析专家。请从以下说明书中提取用法用量信息。

药品名称：{drug_name}

说明书内容：
{text[:4000]}

请仔细阅读"用法用量"部分，以JSON格式返回：
{{
    "drug_name": "药品名称",
    "dosage_per_time": "单次用量（如：2片、10mg、5ml等）",
    "dosage_number": 单次用量的数值部分（浮点数，如2.0、10.0）,
    "dosage_unit": "用量单位（如：片、粒、mg、ml等）",
    "frequency_per_day": 每日用药次数（整数）,
    "duration_days": 推荐疗程天数（整数，如不明确则为null）,
    "special_notes": "特殊说明（如饭前饭后、长期服用等）"
}}

要求：
1. 只返回JSON格式，不要任何其他文字
2. 如果某项信息无法确定，对应字段设为null
3. dosage_number必须是纯数字（浮点数）
4. frequency_per_day必须是整数

只返回JSON，不要其他内容。"""

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是专业的药品说明书分析助手，擅长提取结构化信息。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                
                result = json.loads(response.choices[0].message.content)
                self.logger.info(f"成功提取 {drug_name} 的用法用量信息")
                return result
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON解析失败 {drug_name} (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
            except Exception as e:
                self.logger.error(f"API调用失败 {drug_name} (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
            
            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
        
        return None
