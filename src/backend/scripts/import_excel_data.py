# -*- coding: utf-8 -*-
"""
Excel数据导入脚本
用于将Excel文件数据导入到数据库暂存表
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

import argparse
import logging
from database.link import get_session
from services.excel_import_service import ExcelImportService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def import_disclosure_data(excel_file_path: str):
    """导入披露数据"""
    # 验证文件路径
    file_path = Path(excel_file_path)
    if not file_path.exists():
        logger.error(f"文件不存在: {excel_file_path}")
        return
    
    if not file_path.suffix in ['.xlsx', '.xls']:
        logger.error(f"不支持的文件格式: {file_path.suffix}")
        return
    
    try:
        with get_session() as session:
            # 创建导入服务
            import_service = ExcelImportService(session)
            
            # 导入数据
            result = import_service.import_excel_data(str(file_path))
            
            if result['status'] == 'success':
                logger.info(f"成功导入 {result['total_records']} 条记录")
            else:
                logger.error(f"导入失败: {result['error']}")
                
    except Exception as e:
        logger.error(f"处理过程出错: {str(e)}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='导入Excel数据到数据库')
    parser.add_argument('excel_file', help='Excel文件路径')
    args = parser.parse_args()
    
    import_disclosure_data(args.excel_file)

if __name__ == "__main__":
    main() 
