# crud/enterprise_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from backend.database.models.enterprise import Enterprise

class EnterpriseCRUD:
    """企业表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> Enterprise:
        """创建企业记录"""
        enterprise = Enterprise(**data)
        session.add(enterprise)
        session.flush()  # 获取自增ID，但不提交事务
        return enterprise
    
    @staticmethod
    def get_by_id(session: Session, enterprise_id: int) -> Optional[Enterprise]:
        """通过ID获取企业"""
        return session.get(Enterprise, enterprise_id)
    
    @staticmethod
    def get_by_company_id(session: Session, company_id: str) -> Optional[Enterprise]:
        """通过统一社会信用代码获取企业"""
        stmt = select(Enterprise).where(Enterprise.company_id == company_id)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[Enterprise]:
        """获取多个企业记录，支持过滤"""
        stmt = select(Enterprise)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(Enterprise, key) and value is not None:
                    conditions.append(getattr(Enterprise, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        enterprise: Enterprise,
        data: Dict[str, Any]
    ) -> Enterprise:
        """更新企业记录"""
        for key, value in data.items():
            if hasattr(enterprise, key) and value is not None:
                setattr(enterprise, key, value)
        session.flush()  # 刷新但不提交
        return enterprise
    
    @staticmethod
    def delete(session: Session, enterprise: Enterprise) -> None:
        """删除企业记录"""
        session.delete(enterprise)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_industry(
        session: Session,
        industry: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Enterprise]:
        """获取特定行业的企业列表"""
        stmt = select(Enterprise)\
            .where(Enterprise.industry == industry)\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def search_by_name(
        session: Session,
        name_pattern: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Enterprise]:
        """搜索企业名称"""
        stmt = select(Enterprise)\
            .where(Enterprise.company_name.ilike(f"%{name_pattern}%"))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
enterprise_crud = EnterpriseCRUD()
