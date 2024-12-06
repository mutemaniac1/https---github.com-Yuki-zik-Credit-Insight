# crud/disclosure_info_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from backend.database.models.disclosure_info import DisclosureInfo

class DisclosureInfoCRUD:
    """信息披露表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> DisclosureInfo:
        """创建信息披露记录"""
        disclosure_info = DisclosureInfo(**data)
        session.add(disclosure_info)
        session.flush()  # 获取自增ID，但不提交事务
        return disclosure_info
    
    @staticmethod
    def get_by_id(session: Session, disclosure_id: int) -> Optional[DisclosureInfo]:
        """通过ID获取信息披露"""
        return session.get(DisclosureInfo, disclosure_id)
    
    @staticmethod
    def get_by_enterprise_id(
        session: Session,
        enterprise_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取企业的所有信息披露"""
        stmt = select(DisclosureInfo)\
            .where(DisclosureInfo.enterprise_id == enterprise_id)\
            .order_by(desc(DisclosureInfo.disclosure_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_latest_by_enterprise_id(
        session: Session,
        enterprise_id: int
    ) -> Optional[DisclosureInfo]:
        """获取企业最新的信息披露"""
        stmt = select(DisclosureInfo)\
            .where(DisclosureInfo.enterprise_id == enterprise_id)\
            .order_by(desc(DisclosureInfo.disclosure_date))\
            .limit(1)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[DisclosureInfo]:
        """获取多个信息披露，支持过滤"""
        stmt = select(DisclosureInfo)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(DisclosureInfo, key) and value is not None:
                    conditions.append(getattr(DisclosureInfo, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        disclosure_info: DisclosureInfo,
        data: Dict[str, Any]
    ) -> DisclosureInfo:
        """更新信息披露"""
        for key, value in data.items():
            if hasattr(disclosure_info, key) and value is not None:
                setattr(disclosure_info, key, value)
        session.flush()  # 刷新但不提交
        return disclosure_info
    
    @staticmethod
    def delete(session: Session, disclosure_info: DisclosureInfo) -> None:
        """删除信息披露"""
        session.delete(disclosure_info)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_date_range(
        session: Session,
        start_date: date,
        end_date: date,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取指定日期范围内的信息披露"""
        stmt = select(DisclosureInfo)\
            .where(
                and_(
                    DisclosureInfo.disclosure_date >= start_date,
                    DisclosureInfo.disclosure_date <= end_date
                )
            )\
            .order_by(desc(DisclosureInfo.disclosure_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_disclosure_type(
        session: Session,
        disclosure_type: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取特定类型的信息披露"""
        stmt = select(DisclosureInfo)\
            .where(DisclosureInfo.disclosure_type == disclosure_type)\
            .order_by(desc(DisclosureInfo.disclosure_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_delayed_disclosures(
        session: Session,
        current_date: date,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取延迟披露的信息"""
        stmt = select(DisclosureInfo)\
            .where(
                and_(
                    DisclosureInfo.expected_disclosure_date < current_date,
                    DisclosureInfo.disclosure_date.is_(None)
                )
            )\
            .order_by(desc(DisclosureInfo.expected_disclosure_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
disclosure_info_crud = DisclosureInfoCRUD() 
