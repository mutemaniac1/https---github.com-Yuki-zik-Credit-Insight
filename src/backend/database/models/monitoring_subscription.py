# models/monitoring_subscription.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.link import Base

"""
监控订阅表（monitoring_subscriptions）

此表存储用户对企业的监控订阅信息，包括订阅条件和创建时间。

字段描述：
- subscription_id: 订阅的唯一标识，自增主键。
- user_id: 订阅用户的 ID，外键，不能为空。
- enterprise_id: 被订阅企业的 ID，外键，不能为空。
- condition: 监控条件，字符串类型。
- created_at: 记录订阅创建的时间，默认为当前 UTC 时间。

依赖关系：
- user: 与 User 表的多对一关系，表示订阅的用户。
- enterprise: 与 Enterprise 表的多对一关系，表示被订阅的企业。
"""

class MonitoringSubscription(Base):
    __tablename__ = 'monitoring_subscriptions'

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    alert_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    user = relationship("User", back_populates="monitoring_subscriptions")
    enterprise = relationship("Enterprise", back_populates="monitoring_subscriptions")
