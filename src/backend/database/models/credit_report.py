# models/credit_report.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from database.link import Base

"""
信用报告表（credit_reports）

此表存储企业的信用报告信息，包括信用评分和报告路径。

字段描述：
- report_id: 信用报告的唯一标识，自增主键。
- enterprise_id: 企业的 ID，外键，不能为空。
- report_date: 报告日期，不能为空。
- credit_score: 信用评分，Decimal 类型，（5,2），不能为空。
- report_path: 报告文件路径，字符串类型。
- created_at: 记录创建的时间，默认为当前 UTC 时间。

依赖关系：
- enterprise: 与 Enterprise 表的多对一关系，表示所属企业。
"""

class CreditReport(Base):
    __tablename__ = 'credit_reports'

    report_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    report_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    enterprise = relationship("Enterprise", back_populates="credit_reports")
