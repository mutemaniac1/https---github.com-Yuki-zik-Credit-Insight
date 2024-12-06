# models/disclosure_info.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from database.link import Base

"""
信息披露表（disclosure_info）

此表存储企业的信息披露内容，包括披露日期和具体信息。

字段描述：
- disclosure_id: 信息披露的唯一标识，自增主键。
- enterprise_id: 企业的 ID，外键，不能为空。
- disclosure_date: 信息披露日期，不能为空。
- disclosure_info: 披露的详细信息，文本类型。
- created_at: 记录创建的时间，默认为当前 UTC 时间。

依赖关系：
- enterprise: 与 Enterprise 表的多对一关系，表示所属企业。
"""

class DisclosureInfo(Base):
    __tablename__ = 'disclosure_info'

    info_id = Column(Integer, primary_key=True)
    enterprise_id = Column(Integer, ForeignKey('enterprises.enterprise_id'), nullable=False)
    info_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP')
    )

    # Relationships
    enterprise = relationship("Enterprise", back_populates="disclosure_info")
