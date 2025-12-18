#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
使用pandas和openpyxl生成Excel格式的分析报告
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str):
        """
        初始化报告生成器
        
        Args:
            output_dir: 输出目录路径
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def generate_excel_report(self, 
                             cost_results: List[Dict], 
                             errors: List[Dict]) -> str:
        """
        生成Excel报告
        
        Args:
            cost_results: 费用计算结果列表
            errors: 错误记录列表
            
        Returns:
            报告文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f'药品费用分析报告_{timestamp}.xlsx'
        
        with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
            # Sheet1: 费用明细表
            if cost_results:
                df_detail = pd.DataFrame(cost_results)
                df_detail.columns = ['药品名称', '单次用量', '每日次数', '年度用量', 
                                   '需购买盒数', '单价', '年度费用', '特殊说明', '规格']
                df_detail.to_excel(writer, sheet_name='费用明细', index=False)
                
                # Sheet2: 汇总统计
                summary_data = {
                    '统计项': ['药品总数', '年度总费用（元）', '平均费用（元）', '最高费用（元）', '最低费用（元）'],
                    '数值': [
                        len(cost_results),
                        df_detail['年度费用'].sum(),
                        df_detail['年度费用'].mean(),
                        df_detail['年度费用'].max(),
                        df_detail['年度费用'].min()
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='汇总统计', index=False)
            
            # Sheet3: 异常记录
            if errors:
                df_errors = pd.DataFrame(errors)
                df_errors.to_excel(writer, sheet_name='异常记录', index=False)
        
        self.logger.info(f"报告已生成: {report_path}")
        return str(report_path)
