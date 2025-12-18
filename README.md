# 药品说明书自动化分析系统

🏥 一个全自动化的药品费用分析工具，能够批量处理PDF格式的药品说明书，使用AI智能提取用法用量信息，并计算年度药品费用。

## ✨ 功能特点

- 📄 **批量PDF处理** - 一次性处理几千份药品说明书
- 🤖 **AI智能提取** - 使用OpenAI API自动提取用法用量信息
- 💰 **自动费用计算** - 结合药品规格和价格自动计算年度花费
- 💾 **断点续传** - 支持中断后继续处理，不重复工作
- 📊 **详细报告** - 生成Excel格式的详细分析报告
- 📝 **完整日志** - 记录处理过程，便于追溯

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- OpenAI API密钥

### 2. 安装依赖

```bash
# 克隆仓库（如果从远程获取）
git clone https://github.com/jingjiwuwei/medication-cost-analyzer.git
cd medication-cost-analyzer

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置

```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件，填入您的OpenAI API密钥
# OPENAI_API_KEY=sk-your-api-key-here
```

### 4. 准备数据

#### a) 准备PDF文件
将药品说明书PDF文件放入 `data/pdfs/` 目录：
- **文件命名规则**：文件名即为药品名称（如 `阿司匹林肠溶片.pdf`）
- 支持中文文件名

#### b) 准备药品信息表
复制并编辑 `data/drug_info_template.csv`：

```csv
药品名称,规格,单价,包装规格,备注
阿司匹林肠溶片,100mg*30片,15.50,30,饭后服用
二甲双胍缓释片,500mg*48片,8.90,48,餐中或餐后服用
```

**字段说明**：
- `药品名称`：必须与PDF文件名一致
- `规格`：药品规格描述
- `单价`：每盒价格（元）
- `包装规格`：每盒包含的片/粒数
- `备注`：可选

### 5. 运行分析

```bash
python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv
```

### 6. 查看结果

分析完成后，在 `output/reports/` 目录查看生成的Excel报告：
- **费用明细**：每个药品的详细用量和费用
- **汇总统计**：总费用、平均费用等
- **异常记录**：处理失败的药品列表

## 📖 使用说明

### 命令行参数

```bash
python main.py [选项]

必需参数:
  --pdf-dir PATH      PDF文件目录路径
  --drug-info PATH    药品信息CSV文件路径

可选参数:
  --output-dir PATH   输出目录（默认：./output）
  --no-cache          禁用缓存，重新处理所有文件
  -h, --help          显示帮助信息
```

### 使用示例

```bash
# 基本用法
python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv

# 指定输出目录
python main.py --pdf-dir /path/to/pdfs --drug-info /path/to/info.csv --output-dir ./results

# 重新处理所有文件（忽略缓存）
python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv --no-cache
```

## 📊 输出报告格式

### Sheet1: 费用明细表

| 药品名称 | 单次用量 | 每日次数 | 年度用量 | 需购买盒数 | 单价 | 年度费用 | 特殊说明 | 规格 |
|---------|---------|---------|---------|-----------|------|---------|---------|------|
| 阿司匹林 | 2片 | 1 | 730 | 25 | 15.5 | 387.5 | 饭后服用 | 100mg*30片 |

### Sheet2: 汇总统计表

| 统计项 | 数值 |
|-------|------|
| 药品总数 | 10 |
| 年度总费用（元） | 5280.50 |
| 平均费用（元） | 528.05 |

### Sheet3: 异常记录表

| 药品名称 | 错误类型 | 错误信息 |
|---------|---------|---------|
| XXX药品 | AI提取失败 | 无法提取用法用量信息 |

## ⚙️ 配置说明

### 环境变量（.env文件）

```env
# OpenAI API配置
OPENAI_API_KEY=sk-xxxxx        # 必填：您的OpenAI API密钥
MODEL_NAME=gpt-4o-mini          # 可选：使用的模型（默认：gpt-4o-mini）

# 处理配置
BATCH_SIZE=10                   # 批处理大小（暂未使用）
MAX_RETRIES=3                   # API调用失败重试次数
ENABLE_CACHE=true               # 是否启用缓存

# 路径配置
CACHE_DIR=./data/cache          # 缓存目录
OUTPUT_DIR=./output             # 输出目录
LOG_DIR=./output/logs           # 日志目录
```

## 🔧 高级功能

### 断点续传

系统会自动记录已处理的文件，中断后再次运行会跳过已处理的文件：

```bash
# 第一次运行（处理了500份）
python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv

# 中断后继续运行（从第501份开始）
python main.py --pdf-dir ./data/pdfs --drug-info ./data/drug_info.csv
```

如需重新处理所有文件，使用 `--no-cache` 参数。

### 日志查看

所有处理日志保存在 `output/logs/` 目录，文件名包含时间戳：

```
output/logs/process_20231215_143052.log
```

## 📁 项目结构

```
medication-cost-analyzer/
├── README.md                      # 详细使用说明（中文）
├── requirements.txt               # 依赖包列表
├── .env.example                   # 配置文件模板
├── .gitignore                     # Git忽略文件
├── config.py                      # 配置管理
├── main.py                        # 主程序入口
├── src/
│   ├── __init__.py
│   ├── pdf_parser.py              # PDF解析模块
│   ├── ai_extractor.py            # AI提取模块（OpenAI）
│   ├── cost_calculator.py         # 费用计算模块
│   ├── report_generator.py        # 报告生成模块
│   └── utils.py                   # 工具函数（日志、缓存等）
├── data/
│   ├── pdfs/                      # PDF存放目录（示例）
│   │   └── .gitkeep
│   ├── drug_info_template.csv     # 药品信息模板
│   └── cache/                     # 缓存目录
│       └── .gitkeep
├── output/                        # 输出目录
│   ├── reports/                   # Excel报告
│   │   └── .gitkeep
│   └── logs/                      # 日志文件
│       └── .gitkeep
└── tests/
    └── test_sample.py             # 测试文件
```

## ❓ 常见问题

### 1. API密钥错误

**问题**：`ValueError: 请在.env文件中配置OPENAI_API_KEY`

**解决**：
1. 确保已创建 `.env` 文件
2. 检查API密钥是否正确填写
3. 确认 `.env` 文件在项目根目录

### 2. PDF解析失败

**问题**：某些PDF无法提取文本

**可能原因**：
- PDF是扫描版（图片格式）
- PDF加密或损坏

**解决**：
- 使用OCR工具转换扫描版PDF
- 检查PDF文件完整性

### 3. 药品名称不匹配

**问题**：报告中显示"药品信息表中未找到"

**解决**：
- 确保CSV中的药品名称与PDF文件名完全一致
- 注意中英文标点符号

### 4. API调用过快

**问题**：OpenAI API报错 `Rate limit exceeded`

**解决**：
- 减少并发数量
- 在代码中增加延迟（修改 `src/ai_extractor.py`）

## 📝 开发计划

- [ ] 支持更多PDF格式（扫描版OCR）
- [ ] 添加更多LLM后端支持（Azure、本地模型）
- [ ] 支持多线程/异步处理
- [ ] 添加Web界面
- [ ] 支持更多报告格式（PDF、HTML）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请通过GitHub Issues联系。
