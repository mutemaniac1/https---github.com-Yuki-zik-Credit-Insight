# crud/financial_status_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from backend.database.models.financial_status import FinancialStatus

class FinancialStatusCRUD:
    """财务状态表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> FinancialStatus:
        """创建财务状态记录"""
        financial_status = FinancialStatus(**data)
        session.add(financial_status)
        session.flush()  # 获取自增ID，但不提交事务
        return financial_status
    
    @staticmethod
    def get_by_id(session: Session, status_id: int) -> Optional[FinancialStatus]:
        """通过ID获取财务状态"""
        return session.get(FinancialStatus, status_id)
    
    @staticmethod
    def get_by_enterprise_id(
        session: Session,
        enterprise_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialStatus]:
        """获取企业的所有财务状态记录"""
        stmt = select(FinancialStatus)\
            .where(FinancialStatus.enterprise_id == enterprise_id)\
            .order_by(desc(FinancialStatus.information_disclosure_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_latest_by_enterprise_id(
        session: Session,
        enterprise_id: int
    ) -> Optional[FinancialStatus]:
        """获取企业最新的财务状态记录"""
        stmt = select(FinancialStatus)\
            .where(FinancialStatus.enterprise_id == enterprise_id)\
            .order_by(desc(FinancialStatus.information_disclosure_date))\
            .limit(1)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[FinancialStatus]:
        """获取多个财务状态记录，支持过滤"""
        stmt = select(FinancialStatus)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(FinancialStatus, key) and value is not None:
                    conditions.append(getattr(FinancialStatus, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        financial_status: FinancialStatus,
        data: Dict[str, Any]
    ) -> FinancialStatus:
        """更新财务状态记录"""
        for key, value in data.items():
            if hasattr(financial_status, key) and value is not None:
                setattr(financial_status, key, value)
        session.flush()  # 刷新但不提交
        return financial_status
    
    @staticmethod
    def delete(session: Session, financial_status: FinancialStatus) -> None:
        """删除财务状态记录"""
        session.delete(financial_status)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_date_range(
        session: Session,
        enterprise_id: int,
        start_date: date,
        end_date: date
    ) -> List[FinancialStatus]:
        """获取指定日期范围内的财务状态记录"""
        stmt = select(FinancialStatus)\
            .where(
                and_(
                    FinancialStatus.enterprise_id == enterprise_id,
                    FinancialStatus.information_disclosure_date >= start_date,
                    FinancialStatus.information_disclosure_date <= end_date
                )
            )\
            .order_by(desc(FinancialStatus.information_disclosure_date))
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_overdue_records(
        session: Session,
        *,
        min_overdue_rate: float = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialStatus]:
        """获取逾期记录"""
        conditions = []
        if min_overdue_rate is not None:
            conditions.append(FinancialStatus.current_overdue_rate >= min_overdue_rate)
        
        stmt = select(FinancialStatus)\
            .where(and_(*conditions))\
            .order_by(desc(FinancialStatus.current_overdue_rate))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
financial_status_crud = FinancialStatusCRUD() 
