# crud/decision_report_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from backend.database.models.decision_report import DecisionReport

class DecisionReportCRUD:
    """决策报告表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> DecisionReport:
        """创建决策报告记录"""
        decision_report = DecisionReport(**data)
        session.add(decision_report)
        session.flush()  # 获取自增ID，但不提交事务
        return decision_report
    
    @staticmethod
    def get_by_id(session: Session, report_id: int) -> Optional[DecisionReport]:
        """通过ID获取决策报告"""
        return session.get(DecisionReport, report_id)
    
    @staticmethod
    def get_by_user_id(
        session: Session,
        user_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取用户的所有决策报告"""
        stmt = select(DecisionReport)\
            .where(DecisionReport.user_id == user_id)\
            .order_by(desc(DecisionReport.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_enterprise_id(
        session: Session,
        enterprise_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取企业的所有决策报告"""
        stmt = select(DecisionReport)\
            .where(DecisionReport.enterprise_id == enterprise_id)\
            .order_by(desc(DecisionReport.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_latest_by_enterprise_id(
        session: Session,
        enterprise_id: int
    ) -> Optional[DecisionReport]:
        """获取企业最新的决策报告"""
        stmt = select(DecisionReport)\
            .where(DecisionReport.enterprise_id == enterprise_id)\
            .order_by(desc(DecisionReport.created_at))\
            .limit(1)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[DecisionReport]:
        """获取多个决策报告，支持过滤"""
        stmt = select(DecisionReport)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(DecisionReport, key) and value is not None:
                    conditions.append(getattr(DecisionReport, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        decision_report: DecisionReport,
        data: Dict[str, Any]
    ) -> DecisionReport:
        """更新决策报告"""
        for key, value in data.items():
            if hasattr(decision_report, key) and value is not None:
                setattr(decision_report, key, value)
        session.flush()  # 刷新但不提交
        return decision_report
    
    @staticmethod
    def delete(session: Session, decision_report: DecisionReport) -> None:
        """删除决策报告"""
        session.delete(decision_report)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_date_range(
        session: Session,
        start_date: date,
        end_date: date,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取指定日期范围内的决策报告"""
        stmt = select(DecisionReport)\
            .where(
                and_(
                    DecisionReport.created_at >= start_date,
                    DecisionReport.created_at <= end_date
                )
            )\
            .order_by(desc(DecisionReport.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_decision_type(
        session: Session,
        decision_type: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取特定决策类型的报告"""
        stmt = select(DecisionReport)\
            .where(DecisionReport.decision_type == decision_type)\
            .order_by(desc(DecisionReport.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_risk_level(
        session: Session,
        risk_level: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取特定风险等级的报告"""
        stmt = select(DecisionReport)\
            .where(DecisionReport.risk_level == risk_level)\
            .order_by(desc(DecisionReport.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
decision_report_crud = DecisionReportCRUD() 
