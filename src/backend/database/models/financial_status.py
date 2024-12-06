# models/financial_status.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.link import Base

"""
财务状态表（financial_status）

此表存储企业的财务状况，包括累计承兑金额、逾期金额等。

字段描述：
- status_id: 财务状态的唯一标识，自增主键。
- enterprise_id: 企业的 ID，外键，不能为空。
- continuous_overdue_start_date: 连续逾期开始日期。
- cumulative_accepted_amount: 累计承兑金额，Decimal 类型，默认值为 0.00。
- accepted_balance: 承兑余额，Decimal 类型，默认值为 0.00。
- cumulative_overdue_amount: 累计逾期金额，Decimal 类型，默认值为 0.00。
- overdue_balance: 逾期余额，Decimal 类型，默认值为 0.00。
- information_disclosure_date: 信息披露日期，不能为空。
- disclosure_date: 实际披露日期。
- cumulative_overdue_rate: 累计逾期率，Decimal 类型（5,2）。
- current_overdue_rate: 当前逾期率，Decimal 类型（5,2）。
- overdue_duration_days: 逾期天数。
- information_disclosure_lag: 信息披露滞后天数。
- created_at: 记录创建的时间，默认为当前 UTC 时间。

依赖关系：
- enterprise: 与 Enterprise 表的多对一关系，表示所属企业。
- overdue_aging_analyses: 与 OverdueAgingAnalysis 表的一对多关系，表示逾期账龄分析数据。
"""

class FinancialStatus(Base):
    __tablename__ = 'financial_status'

    status_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    period = Column(String(50), nullable=False)
    revenue = Column(Numeric(18, 2), nullable=False)
    profit = Column(Numeric(18, 2), nullable=False)
    assets = Column(Numeric(18, 2), nullable=False)
    liabilities = Column(Numeric(18, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    enterprise = relationship("Enterprise", back_populates="financial_status")
