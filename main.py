#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
药品说明书自动化分析系统 - 主程序
批量处理PDF格式的药品说明书，提取用法用量信息，并计算年度费用
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

from config import Config
from src.utils import setup_logging, load_cache, save_cache
from src.pdf_parser import PDFParser
from src.ai_extractor import DosageExtractor
from src.cost_calculator import CostCalculator
from src.report_generator import ReportGenerator


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description='药品说明书自动化分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv
  python main.py --pdf-dir /path/to/pdfs --drug-info /path/to/info.csv --output-dir ./results
        """
    )
    parser.add_argument('--pdf-dir', required=True, help='PDF文件目录路径')
    parser.add_argument('--drug-info', required=True, help='药品信息CSV文件路径')
    parser.add_argument('--output-dir', default='./output', help='输出目录（默认：./output）')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存，重新处理所有文件')
    
    args = parser.parse_args()
    
    # 验证配置
    Config.validate()
    
    # 设置日志
    setup_logging(Config.LOG_DIR)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("药品说明书自动化分析系统 启动")
    logger.info("=" * 60)
    
    # 初始化缓存
    cache_file = Config.CACHE_DIR / 'processed.json'
    processed_cache = set() if args.no_cache else load_cache(cache_file)
    logger.info(f"已处理文件数: {len(processed_cache)}")
    
    # 步骤1: 解析PDF
    logger.info("\n[步骤 1/4] 开始解析PDF文件...")
    pdf_parser = PDFParser(args.pdf_dir)
    pdf_texts = pdf_parser.batch_process(processed_cache)
    logger.info(f"本次解析PDF数量: {len(pdf_texts)}")
    
    # 步骤2: AI提取用法用量
    logger.info("\n[步骤 2/4] 开始AI提取用法用量信息...")
    extractor = DosageExtractor(
        api_key=Config.OPENAI_API_KEY,
        model=Config.MODEL_NAME,
        max_retries=Config.MAX_RETRIES
    )
    
    dosage_results = []
    extraction_errors = []
    
    for drug_name, text in pdf_texts.items():
        if text is None:
            extraction_errors.append({
                '药品名称': drug_name,
                '错误类型': 'PDF解析失败',
                '错误信息': '无法提取PDF文本'
            })
            continue
        
        result = extractor.extract_dosage_info(drug_name, text)
        if result:
            dosage_results.append(result)
            processed_cache.add(drug_name)
        else:
            extraction_errors.append({
                '药品名称': drug_name,
                '错误类型': 'AI提取失败',
                '错误信息': '无法提取用法用量信息'
            })
    
    logger.info(f"成功提取: {len(dosage_results)}, 失败: {len(extraction_errors)}")
    
    # 保存缓存
    if Config.ENABLE_CACHE:
        save_cache(cache_file, processed_cache)
    
    # 步骤3: 计算费用
    logger.info("\n[步骤 3/4] 开始计算年度费用...")
    calculator = CostCalculator(args.drug_info)
    
    cost_results = []
    calculation_errors = []
    
    for dosage_data in dosage_results:
        result = calculator.calculate_annual_cost(dosage_data)
        if result:
            cost_results.append(result)
        else:
            calculation_errors.append({
                '药品名称': dosage_data.get('drug_name'),
                '错误类型': '费用计算失败',
                '错误信息': '药品信息不匹配或计算异常'
            })
    
    logger.info(f"成功计算: {len(cost_results)}, 失败: {len(calculation_errors)}")
    
    # 步骤4: 生成报告
    logger.info("\n[步骤 4/4] 生成分析报告...")
    all_errors = extraction_errors + calculation_errors
    
    reporter = ReportGenerator(args.output_dir)
    report_path = reporter.generate_excel_report(cost_results, all_errors)
    
    # 输出总结
    logger.info("\n" + "=" * 60)
    logger.info("处理完成！")
    logger.info(f"总处理数: {len(pdf_texts)}")
    logger.info(f"成功数: {len(cost_results)}")
    logger.info(f"失败数: {len(all_errors)}")
    if cost_results:
        total_cost = sum(r['annual_cost'] for r in cost_results)
        logger.info(f"年度总费用: ¥{total_cost:,.2f}")
    logger.info(f"报告路径: {report_path}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
