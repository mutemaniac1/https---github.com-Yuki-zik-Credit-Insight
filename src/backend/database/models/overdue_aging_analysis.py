# models/overdue_aging_analysis.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.link import Base


"""
逾期账龄分析表（overdue_aging_analysis）

此表存储企业的逾期账龄分布情况，包括逾期区间和对应的逾期金额。

字段描述：
- analysis_id: 逾期账龄记录的唯一标识，自增主键。
- enterprise_id: 关联的企业ID，外键，不能为空。
- period: 逾期区间，字符串类型，不能为空。
- aging_range: 逾期区间，字符串类型，不能为空。
- amount: 该逾期区间的逾期金额，Decimal 类型，默认值为 0.00。
- percentage: 该逾期区间的逾期金额占比，Decimal 类型，默认值为 0.00。
- created_at: 记录创建的时间，默认为当前 UTC 时间。
- updated_at: 记录更新的时间，默认为当前 UTC 时间。

依赖关系：
- enterprise: 与 Enterprise 表的多对一关系，表示所属的企业。
"""

class OverdueAgingAnalysis(Base):
    __tablename__ = 'overdue_aging_analysis'

    analysis_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    period = Column(String(50), nullable=False)
    aging_range = Column(String(50), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    percentage = Column(Numeric(5, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    enterprise = relationship("Enterprise", back_populates="overdue_aging_analysis")
