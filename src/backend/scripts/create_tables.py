# -*- coding: utf-8 -*-
"""
数据库表创建脚本
用于创建所有数据库表
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

import logging
from database.link import Base, engine

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables():
    """创建所有数据库表"""
    try:
        # 删除所有现有表
        Base.metadata.drop_all(bind=engine)
        logger.info("已删除所有现有表")
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("已成功创建所有表")
        
    except Exception as e:
        logger.error(f"创建表时出错: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 
