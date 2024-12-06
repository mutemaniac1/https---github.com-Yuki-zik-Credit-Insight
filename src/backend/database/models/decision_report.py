# models/decision_report.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from database.link import Base

"""
决策报告表（decision_reports）

此表存储用户对企业生成的决策报告，包括参数和报告路径。

字段描述：
- decision_report_id: 决策报告的唯一标识，自增主键。
- user_id: 用户的 ID，外键，不能为空。
- enterprise_id: 企业的 ID，外键，不能为空。
- parameters: 报告生成的参数，文本类型。
- report_path: 报告文件路径，字符串类型。
- status: 报告状态，字符串类型，默认值为 "已生成"。
- created_at: 记录创建的时间，默认为当前 UTC 时间。

依赖关系：
- user: 与 User 表的多对一关系，表示报告创建者。
- enterprise: 与 Enterprise 表的多对一关系，表示相关企业。
"""

class DecisionReport(Base):
    __tablename__ = 'decision_reports'

    report_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    decision = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    enterprise = relationship("Enterprise", back_populates="decision_reports")
    user = relationship("User", back_populates="decision_reports")
