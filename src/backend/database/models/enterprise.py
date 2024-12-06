# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.orm import relationship
from database.link import Base

"""
企业表 (enterprises)

此表存储企业的基本信息，包括名称、信用代码、行业和创建时间。

字段描述：
- enterprise_id: 企业的唯一标识，自增主键。
- name: 企业名称，字符串类型，最大长度255，不能为空。
- credit_code: 企业的统一社会信用代码，字符串类型，最大长度50，唯一且不能为空。
- industry: 企业所属行业，字符串类型，最大长度100。
- created_at: 记录企业信息创建的时间，默认为当前UTC时间。

依赖关系：
- credit_reports: 与 CreditReport 表的一对多关系，表示企业的所有信用报告。
- monitoring_subscriptions: 与 MonitoringSubscription 表的一对多关系，表示订阅该企业的所有监控订阅。
- decision_reports: 与 DecisionReport 表的一对多关系，表示针对该企业的所有决策报告。
"""

class Enterprise(Base):
    __tablename__ = 'enterprises'

    enterprise_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    credit_code = Column(String(18), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    credit_reports = relationship("CreditReport", back_populates="enterprise")
    monitoring_subscriptions = relationship("MonitoringSubscription", back_populates="enterprise")
    decision_reports = relationship("DecisionReport", back_populates="enterprise")
    disclosure_info = relationship("DisclosureInfo", back_populates="enterprise")
    financial_status = relationship("FinancialStatus", back_populates="enterprise")
    overdue_aging_analysis = relationship("OverdueAgingAnalysis", back_populates="enterprise")
