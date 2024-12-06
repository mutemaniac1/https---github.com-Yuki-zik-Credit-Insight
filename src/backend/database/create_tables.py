# create_tables.py
# -*- coding: utf-8 -*-
import sys
import os
import logging
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from sqlalchemy import text, inspect

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根目录到 sys.path，确保可以进行绝对导入
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.link import engine, Base, get_session
from database.models import (
    User, Enterprise, FinancialStatus, CreditReport,
    MonitoringSubscription, DecisionReport, DisclosureInfo,
    OverdueAgingAnalysis, RawDisclosureData
)

def check_database_connection():
    """检查数据库连接"""
    try:
        with get_session() as session:
            session.execute(text("SELECT 1"))
            logger.info("数据库连接正常")
            return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False

def get_existing_tables():
    """获取已存在的表"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def create_all_tables(check_first=True):
    """
    创建所有在 ORM 模型中定义的表
    
    Args:
        check_first (bool): 是否先检查表是否存在
    """
    try:
        # 首先检查数据库连接
        if not check_database_connection():
            logger.error("无法连接到数据库，退出操作")
            return False

        # 获取要创建的表列表
        tables_to_create = [table.__tablename__ for table in Base.__subclasses__()]
        logger.info(f"计划创建的表: {', '.join(tables_to_create)}")

        if check_first:
            # 检查已存在的表
            existing_tables = get_existing_tables()
            logger.info(f"已存在的表: {', '.join(existing_tables)}")

            # 检查是否有表已存在
            tables_exist = [table for table in tables_to_create if table in existing_tables]
            if tables_exist:
                logger.warning(f"以下表已存在: {', '.join(tables_exist)}")
                response = input("是否继续创建其他表？(y/n): ")
                if response.lower() != 'y':
                    logger.info("操作已取消")
                    return False

        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 验证表创建
        created_tables = get_existing_tables()
        success = all(table in created_tables for table in tables_to_create)
        
        if success:
            logger.info("所有表已成功创建！")
            # 打印表结构
            for table_name in created_tables:
                columns = [col['name'] for col in inspect(engine).get_columns(table_name)]
                logger.info(f"表 {table_name} 的列: {', '.join(columns)}")
        else:
            missing_tables = [t for t in tables_to_create if t not in created_tables]
            logger.error(f"部分表创建失败: {', '.join(missing_tables)}")
        
        return success

    except ProgrammingError as e:
        logger.error(f"SQL语法错误: {str(e)}")
        return False
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"创建表时发生未知错误: {str(e)}")
        return False

def drop_all_tables(confirm=True):
    """
    删除所有表
    
    Args:
        confirm (bool): 是否需要确认
    """
    try:
        if confirm:
            response = input("此操作将删除所有表，是否继续？(y/n): ")
            if response.lower() != 'y':
                logger.info("操作已取消")
                return False

        Base.metadata.drop_all(bind=engine)
        logger.info("所有表已成功删除")
        return True
    except Exception as e:
        logger.error(f"删除表时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库表管理工具')
    parser.add_argument('--action', choices=['create', 'drop', 'recreate'],
                      default='create', help='要执行的操作')
    parser.add_argument('--force', action='store_true',
                      help='强制执行，不进行确认')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_all_tables(check_first=not args.force)
    elif args.action == 'drop':
        drop_all_tables(confirm=not args.force)
    elif args.action == 'recreate':
        if drop_all_tables(confirm=not args.force):
            create_all_tables(check_first=False)
