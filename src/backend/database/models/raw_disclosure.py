# -*- coding: utf-8 -*-
"""
原始票据信息披露数据模型
用于存储从Excel导入的原始数据
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric, Text, Date, func
from database.link import Base

class RawDisclosureData(Base):
    """票据信息披露原始数据表"""
    __tablename__ = 'raw_disclosure_data'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(200), nullable=False)    # 企业名称（必填）
    credit_code = Column(String(18), nullable=False)      # 统一社会信用代码（必填）
    continuous_overdue_start_date = Column(String(20), nullable=True)  # 持续逾期开始时间
    cumulative_accepted_amount = Column(Numeric(18, 2), nullable=False, default=0)  # 累计承兑发生额
    accepted_balance = Column(Numeric(18, 2), nullable=False, default=0)  # 承兑余额
    cumulative_overdue_amount = Column(Numeric(18, 2), nullable=False, default=0)  # 累计逾期发生额
    overdue_balance = Column(Numeric(18, 2), nullable=False, default=0)  # 逾期余额
    info_disclosure_date = Column(String(20), nullable=False)   # 披露信息时点日期（必填）
    disclosure_date = Column(String(20), nullable=True)         # 披露日期（可选）
    bill_medium = Column(String(50), nullable=True)       # 票据介质（可选）
    system_notes = Column(Text, nullable=True)            # 系统备注（可选）
    company_notes = Column(Text, nullable=True)           # 企业备注（可选）
    software_notes = Column(Text, nullable=True)          # 获取软件备注（可选）
    
    # 处理状态跟踪
    status = Column(String(20), nullable=False, default='pending')  # pending/processing/completed/failed
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    processed_at = Column(TIMESTAMP, nullable=True)
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return f"<RawDisclosureData(company_name='{self.company_name}', credit_code='{self.credit_code}')>" 
