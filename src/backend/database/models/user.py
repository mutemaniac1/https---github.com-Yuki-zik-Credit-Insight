# database/models/user.py

"""
用户表 (users)

此表存储系统中的用户信息，包括用户名、邮箱、密码哈希、角色和创建时间。

字段描述：
- user_id: 用户的唯一标识，自增主键。
- username: 用户名，字符串类型，最大长度50，唯一且不能为空。
- email: 用户的电子邮箱，字符串类型，最大长度100，唯一且不能为空。
- password_hash: 哈希处理后的密码，字符串类型，最大长度255，不能为空。
- role: 用户的角色，字符串类型，最大长度50，不能为空，例如“管理员”或“普通用户”。
- created_at: 记录用户创建的时间，默认为当前UTC时间。
- is_active: 用户是否处于活跃状态，布尔类型，默认为True。
- last_login: 用户最后登录时间，可为空。
- updated_at: 记录最后更新时间，自动更新。

依赖关系：
- monitoring_subscriptions: 与 MonitoringSubscription 表的一对多关系，表示用户的所有监控订阅。
- decision_reports: 与 DecisionReport 表的一对多关系，表示用户创建的所有决策报告。
"""

# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, Boolean
from sqlalchemy.orm import relationship
from database.link import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    monitoring_subscriptions = relationship("MonitoringSubscription", back_populates="user")
    decision_reports = relationship("DecisionReport", back_populates="user")
