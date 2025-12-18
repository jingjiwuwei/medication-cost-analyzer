#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试示例
测试模块导入是否正常
"""

import sys
from pathlib import Path

# 添加项目路径到sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_import():
    """测试模块导入"""
    try:
        from src.pdf_parser import PDFParser
        from src.ai_extractor import DosageExtractor
        from src.cost_calculator import CostCalculator
        from src.report_generator import ReportGenerator
        print("✓ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False


if __name__ == '__main__':
    success = test_import()
    sys.exit(0 if success else 1)
