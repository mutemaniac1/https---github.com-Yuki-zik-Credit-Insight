# crud/overdue_aging_analysis_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc, func
from backend.database.models.overdue_aging_analysis import OverdueAgingAnalysis

class OverdueAgingAnalysisCRUD:
    """逾期账龄分析表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> OverdueAgingAnalysis:
        """创建逾期账龄分析记录"""
        analysis = OverdueAgingAnalysis(**data)
        session.add(analysis)
        session.flush()  # 获取自增ID，但不提交事务
        return analysis
    
    @staticmethod
    def get_by_id(session: Session, analysis_id: int) -> Optional[OverdueAgingAnalysis]:
        """通过ID获取逾期账龄分析"""
        return session.get(OverdueAgingAnalysis, analysis_id)
    
    @staticmethod
    def get_by_financial_status_id(
        session: Session,
        financial_status_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[OverdueAgingAnalysis]:
        """获取财务状态的所有逾期账龄分析"""
        stmt = select(OverdueAgingAnalysis)\
            .where(OverdueAgingAnalysis.financial_status_id == financial_status_id)\
            .order_by(desc(OverdueAgingAnalysis.aging_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_latest_by_financial_status_id(
        session: Session,
        financial_status_id: int
    ) -> Optional[OverdueAgingAnalysis]:
        """获取财务状态最新的逾期账龄分析"""
        stmt = select(OverdueAgingAnalysis)\
            .where(OverdueAgingAnalysis.financial_status_id == financial_status_id)\
            .order_by(desc(OverdueAgingAnalysis.aging_date))\
            .limit(1)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[OverdueAgingAnalysis]:
        """获取多个逾期账龄分析，支持过滤"""
        stmt = select(OverdueAgingAnalysis)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(OverdueAgingAnalysis, key) and value is not None:
                    conditions.append(getattr(OverdueAgingAnalysis, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        analysis: OverdueAgingAnalysis,
        data: Dict[str, Any]
    ) -> OverdueAgingAnalysis:
        """更新逾期账龄分析"""
        for key, value in data.items():
            if hasattr(analysis, key) and value is not None:
                setattr(analysis, key, value)
        session.flush()  # 刷新但不提交
        return analysis
    
    @staticmethod
    def delete(session: Session, analysis: OverdueAgingAnalysis) -> None:
        """删除逾期账龄分析"""
        session.delete(analysis)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_date_range(
        session: Session,
        financial_status_id: int,
        start_date: date,
        end_date: date
    ) -> List[OverdueAgingAnalysis]:
        """获取指定日期范围内的逾期账龄分析"""
        stmt = select(OverdueAgingAnalysis)\
            .where(
                and_(
                    OverdueAgingAnalysis.financial_status_id == financial_status_id,
                    OverdueAgingAnalysis.aging_date >= start_date,
                    OverdueAgingAnalysis.aging_date <= end_date
                )
            )\
            .order_by(desc(OverdueAgingAnalysis.aging_date))
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_aging_period(
        session: Session,
        min_days: int = None,
        max_days: int = None,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[OverdueAgingAnalysis]:
        """获取特定账龄期间的分析记录"""
        conditions = []
        if min_days is not None:
            conditions.append(OverdueAgingAnalysis.aging_days >= min_days)
        if max_days is not None:
            conditions.append(OverdueAgingAnalysis.aging_days <= max_days)
        
        stmt = select(OverdueAgingAnalysis)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.order_by(desc(OverdueAgingAnalysis.aging_days))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_aging_statistics(
        session: Session,
        financial_status_id: int
    ) -> Dict[str, Any]:
        """获取账龄统计信息"""
        result = session.execute(
            select(
                func.count().label('total_count'),
                func.avg(OverdueAgingAnalysis.aging_days).label('avg_aging_days'),
                func.max(OverdueAgingAnalysis.aging_days).label('max_aging_days'),
                func.sum(OverdueAgingAnalysis.overdue_amount).label('total_overdue_amount')
            ).where(OverdueAgingAnalysis.financial_status_id == financial_status_id)
        ).first()
        
        return {
            'total_count': result.total_count,
            'avg_aging_days': float(result.avg_aging_days) if result.avg_aging_days else 0,
            'max_aging_days': result.max_aging_days or 0,
            'total_overdue_amount': float(result.total_overdue_amount) if result.total_overdue_amount else 0
        }

# 创建单例实例
overdue_aging_analysis_crud = OverdueAgingAnalysisCRUD() 
