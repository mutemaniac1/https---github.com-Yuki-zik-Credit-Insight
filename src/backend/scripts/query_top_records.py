# -*- coding: utf-8 -*-
"""
查询数据脚本
用于从数据库中查询前五条记录
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

import logging
from database.link import get_session
from database.models.raw_disclosure import RawDisclosureData
from sqlalchemy import select

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_date(date):
    """将日期格式化为中文格式"""
    if date is None:
        return '未有准确日期'
    return f"{date.year}年{date.month}月{date.day}日"

def query_top_records():
    """查询前五条记录"""
    try:
        with get_session() as session:
            # 构建查询
            stmt = select(RawDisclosureData).limit(5)
            
            # 执行查询
            results = session.execute(stmt).scalars().all()
            
            # 打印结果
            print("\n前5条记录：")
            print("-" * 100)
            for record in results:
                print(f"企业名称: {record.company_name}")
                print(f"统一社会信用代码: {record.credit_code}")
                print(f"持续逾期开始时间: {format_date(record.continuous_overdue_start_date)}")
                print(f"累计承兑发生额: {record.cumulative_accepted_amount:,.2f}")
                print(f"承兑余额: {record.accepted_balance:,.2f}")
                print(f"累计逾期发生额: {record.cumulative_overdue_amount:,.2f}")
                print(f"逾期余额: {record.overdue_balance:,.2f}")
                print(f"披露信息时点日期: {format_date(record.info_disclosure_date)}")
                print(f"披露日期: {format_date(record.disclosure_date)}")
                print(f"票据介质: {record.bill_medium}")
                print(f"系统备注: {record.system_notes}")
                print("-" * 100)
            
            return len(results)
            
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
        return 0

def main():
    """主函数"""
    count = query_top_records()
    if count > 0:
        logger.info(f"成功查询 {count} 条记录")
    else:
        logger.error("查询失败")

if __name__ == "__main__":
    main() 
