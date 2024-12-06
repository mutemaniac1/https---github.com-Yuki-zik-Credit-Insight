# -*- coding: utf-8 -*-
"""
Excel数据导入服务
处理Excel文件的读取和数据导入到暂存表
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from pathlib import Path
from database.models.raw_disclosure import RawDisclosureData

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelImportService:
    def __init__(self, session: Session):
        self.session = session
    
    def import_excel_data(self, file_path: str) -> Dict[str, Any]:
        """导入Excel数据到暂存表"""
        try:
            logger.info(f"开始导入Excel文件: {file_path}")
            
            # 确保文件路径是绝对路径
            file_path = str(Path(file_path).resolve())
            logger.info(f"使用绝对路径: {file_path}")
            
            try:
                # 读取Excel文件
                df = pd.read_excel(file_path)
                logger.info(f"成功读取Excel文件，共 {len(df)} 行数据")
                logger.info(f"Excel列名: {list(df.columns)}")
            except Exception as e:
                logger.error(f"读取Excel文件失败: {str(e)}")
                return {
                    "status": "failed",
                    "error": f"读取Excel文件失败: {str(e)}",
                    "timestamp": datetime.now()
                }
            
            # 数据清洗和标准化
            try:
                df = self._preprocess_dataframe(df)
            except Exception as e:
                logger.error(f"数据预处理失败: {str(e)}")
                return {
                    "status": "failed",
                    "error": f"数据预处理失败: {str(e)}",
                    "timestamp": datetime.now()
                }
            
            # 验证必填字段
            if not self._validate_required_fields(df):
                return {
                    "status": "failed",
                    "error": "存在必填字段为空的数据",
                    "timestamp": datetime.now()
                }
            
            # 转换为数据库记录
            try:
                records = self._convert_to_db_records(df)
                logger.info(f"成功转换 {len(records)} 条记录")
            except Exception as e:
                logger.error(f"数据转换失败: {str(e)}")
                return {
                    "status": "failed",
                    "error": f"数据转换失败: {str(e)}",
                    "timestamp": datetime.now()
                }
            
            # 批量插入数据库
            try:
                self._bulk_insert_records(records)
            except Exception as e:
                logger.error(f"数据插入失败: {str(e)}")
                return {
                    "status": "failed",
                    "error": f"数据插入失败: {str(e)}",
                    "timestamp": datetime.now()
                }
            
            result = {
                "status": "success",
                "total_records": len(records),
                "timestamp": datetime.now()
            }
            logger.info(f"数据导入成功: {result}")
            return result
            
        except Exception as e:
            error_msg = f"数据导入失败: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "failed",
                "error": error_msg,
                "timestamp": datetime.now()
            }
    
    def _validate_required_fields(self, df: pd.DataFrame) -> bool:
        """验证必填字段"""
        required_fields = {
            'company_name': '企业名称',
            'credit_code': '统一社会信用代码',
            'info_disclosure_date': '披露信息时点日期'
        }
        
        # 检查是否所有必填字段都存在
        for eng_name, cn_name in required_fields.items():
            if eng_name not in df.columns:
                logger.error(f"缺少必填字段: {cn_name} ({eng_name})")
                return False
        
        # 创建有效记录的掩码
        valid_mask = pd.Series(True, index=df.index)
        skipped_records = []
        
        # 检查每个必填字段
        for eng_name, cn_name in required_fields.items():
            null_mask = df[eng_name].isnull()
            if null_mask.any():
                null_rows = df[null_mask].index.tolist()
                logger.warning(f"字段 {cn_name} 在以下行中存在空值: {null_rows}")
                valid_mask &= ~null_mask
                skipped_records.extend([(index + 1, cn_name) for index in null_rows])
        
        # 如果有无效记录，记录它们
        if skipped_records:
            logger.warning(f"以下记录将被跳过（行号，缺失字段）: {skipped_records}")
            # 只保留有效记录
            df.drop(df[~valid_mask].index, inplace=True)
            logger.info(f"保留 {len(df)} 条有效记录")
            
        return len(df) > 0  # 如果还有有效记录则返回True
    
    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """预处理DataFrame数据"""
        logger.info("开始数据预处理")
        logger.info(f"原始列名: {list(df.columns)}")
        
        # 统一列名
        column_mapping = {
            '企业名称': 'company_name',
            '统一社会信用代码': 'credit_code',
            '持续逾期开始时间': 'continuous_overdue_start_date',
            '累计承兑发生额（元）': 'cumulative_accepted_amount',
            '承兑余额（元': 'accepted_balance',
            '累计逾期发生额（元）': 'cumulative_overdue_amount',
            '逾期余额（元）': 'overdue_balance',
            '披露信息时点日期': 'info_disclosure_date',
            '披露日期': 'disclosure_date',
            '票据介质': 'bill_medium',
            '系统备注': 'system_notes',
            '企业注': 'company_notes',
            '获取软件备注': 'software_notes'
        }
        
        # 检查列名是否存在
        for cn_name, eng_name in column_mapping.items():
            if cn_name not in df.columns:
                logger.warning(f"Excel中缺少列: {cn_name}")
        
        df = df.rename(columns=column_mapping)
        logger.info(f"转换后的列名: {list(df.columns)}")
        
        def parse_chinese_date(date_str):
            """解析中文日期格式"""
            if pd.isna(date_str):
                return None
            try:
                # 如果已经是datetime格式，转换为字符串
                if isinstance(date_str, (datetime, pd.Timestamp)):
                    return date_str.strftime('%Y年%m月%d日')
                # 如果是字符串格式，确保是正确的中文格式
                elif isinstance(date_str, str):
                    # 移除可能的空格
                    date_str = date_str.strip()
                    # 检查是否已经是中文格式
                    if '年' in date_str and '月' in date_str and '日' in date_str:
                        return date_str
                    # 如果不是中文格式，尝试转换
                    try:
                        dt = pd.to_datetime(date_str)
                        return dt.strftime('%Y年%m月%d日')
                    except:
                        return None
                return None
            except Exception:
                return None
        
        # 处理日期字段
        date_columns = ['continuous_overdue_start_date', 'info_disclosure_date', 'disclosure_date']
        for col in date_columns:
            if col in df.columns:
                try:
                    # 使用自定义函数解析日期
                    df[col] = df[col].apply(parse_chinese_date)
                    logger.info(f"日期字段 {col} 转换完成")
                except Exception as e:
                    logger.error(f"日期字段 {col} 转换失败: {str(e)}")
        
        # 处理金额字段
        numeric_columns = [
            'cumulative_accepted_amount', 
            'accepted_balance',
            'cumulative_overdue_amount', 
            'overdue_balance'
        ]
        for col in numeric_columns:
            if col in df.columns:
                try:
                    # 将空值替换为0
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace(',', ''),
                        errors='coerce'
                    ).fillna(0)
                    logger.info(f"金额字段 {col} 转换完成")
                except Exception as e:
                    logger.error(f"金额字段 {col} 转换失败: {str(e)}")
        
        # 处理可能为空的字符串字段
        optional_text_fields = ['bill_medium', 'system_notes', 'company_notes', 'software_notes']
        for field in optional_text_fields:
            if field in df.columns:
                df[field] = df[field].where(pd.notna(df[field]), None)
                logger.info(f"文本字段 {field} 空值处理完成")
        
        logger.info("数据预处理完成")
        return df
    
    def _convert_to_db_records(self, df: pd.DataFrame) -> List[Dict]:
        """转换DataFrame为数据库记录格式"""
        logger.info("开始转换数据格式")
        records = []
        
        for index, row in df.iterrows():
            try:
                # 处理日期字段，将NaT转换为None
                continuous_overdue_start_date = None if pd.isna(row.get('continuous_overdue_start_date')) else row['continuous_overdue_start_date']
                disclosure_date = None if pd.isna(row.get('disclosure_date')) else row['disclosure_date']
                info_disclosure_date = row['info_disclosure_date']  # 这是必填字段，不会为空
                
                record = {
                    # 必填字段
                    'company_name': row['company_name'],
                    'credit_code': row['credit_code'],
                    'info_disclosure_date': info_disclosure_date,
                    
                    # 数值字段（默认0）
                    'cumulative_accepted_amount': row.get('cumulative_accepted_amount', 0),
                    'accepted_balance': row.get('accepted_balance', 0),
                    'cumulative_overdue_amount': row.get('cumulative_overdue_amount', 0),
                    'overdue_balance': row.get('overdue_balance', 0),
                    
                    # 可选日期字段
                    'continuous_overdue_start_date': continuous_overdue_start_date,
                    'disclosure_date': disclosure_date,
                    
                    # 可选文本字段
                    'bill_medium': row.get('bill_medium'),
                    'system_notes': row.get('system_notes'),
                    'company_notes': row.get('company_notes'),
                    'software_notes': row.get('software_notes'),
                    
                    'status': 'pending'
                }
                records.append(record)
            except Exception as e:
                logger.error(f"第 {index + 1} 行数据转换失败: {str(e)}")
                raise
        
        logger.info(f"数据格式转换完成，共 {len(records)} 条记录")
        return records
    
    def _bulk_insert_records(self, records: List[Dict]):
        """批量插入记录到数据库"""
        try:
            logger.info(f"开始批量插入数据，共 {len(records)} 条记录")
            self.session.bulk_insert_mappings(RawDisclosureData, records)
            self.session.commit()
            logger.info("数据批量插入完成")
        except Exception as e:
            self.session.rollback()
            logger.error(f"数据插入失败: {str(e)}")
            raise e
