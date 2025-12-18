#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
费用计算模块
根据用法用量和药品价格信息计算年度费用
"""

import pandas as pd
import re
from typing import Dict, Optional
import logging
import math


class CostCalculator:
    """费用计算器"""
    
    def __init__(self, drug_info_path: str):
        """
        初始化费用计算器
        
        Args:
            drug_info_path: 药品信息CSV文件路径
        """
        self.drug_info = pd.read_csv(drug_info_path)
        self.logger = logging.getLogger(__name__)
        
        # 创建药品名称索引（方便查找）
        self.drug_dict = self.drug_info.set_index('药品名称').to_dict('index')
    
    def calculate_annual_cost(self, dosage_data: Dict) -> Optional[Dict]:
        """
        计算年度费用
        
        Args:
            dosage_data: AI提取的用法用量数据
            
        Returns:
            包含费用计算结果的字典，失败返回None
        """
        drug_name = dosage_data.get('drug_name')
        
        if drug_name not in self.drug_dict:
            self.logger.warning(f"药品信息表中未找到: {drug_name}")
            return None
        
        drug_info = self.drug_dict[drug_name]
        
        try:
            # 提取数据
            dosage_number = float(dosage_data.get('dosage_number', 0))
            frequency = int(dosage_data.get('frequency_per_day', 0))
            duration = dosage_data.get('duration_days')
            
            # 计算年度用量
            if duration:
                # 如果有明确疗程，按疗程计算
                cycles_per_year = 365 / duration
                annual_dosage = dosage_number * frequency * duration * cycles_per_year
            else:
                # 否则按全年每日服用计算
                annual_dosage = dosage_number * frequency * 365
            
            # 从药品信息中获取价格和包装
            price = float(drug_info['单价'])
            package_size = float(drug_info['包装规格'])
            
            # 计算需要购买的盒数（向上取整）
            boxes_needed = math.ceil(annual_dosage / package_size)
            
            # 计算年度费用
            annual_cost = boxes_needed * price
            
            result = {
                'drug_name': drug_name,
                'dosage_per_time': dosage_data.get('dosage_per_time'),
                'frequency_per_day': frequency,
                'annual_dosage': annual_dosage,
                'boxes_needed': boxes_needed,
                'unit_price': price,
                'annual_cost': annual_cost,
                'special_notes': dosage_data.get('special_notes', ''),
                'spec': drug_info['规格']
            }
            
            self.logger.info(f"{drug_name} 年度费用: ¥{annual_cost:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"计算 {drug_name} 费用失败: {str(e)}")
            return None
