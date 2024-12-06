# crud/credit_report_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from backend.database.models.credit_report import CreditReport

class CreditReportCRUD:
    """信用报告表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> CreditReport:
        """创建信用报告记录"""
        credit_report = CreditReport(**data)
        session.add(credit_report)
        session.flush()  # 获取自增ID，但不提交事务
        return credit_report
    
    @staticmethod
    def get_by_id(session: Session, report_id: int) -> Optional[CreditReport]:
        """通过ID获取信用报告"""
        return session.get(CreditReport, report_id)
    
    @staticmethod
    def get_by_enterprise_id(
        session: Session,
        enterprise_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取企业的所有信用报告"""
        stmt = select(CreditReport)\
            .where(CreditReport.enterprise_id == enterprise_id)\
            .order_by(desc(CreditReport.report_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_latest_by_enterprise_id(
        session: Session,
        enterprise_id: int
    ) -> Optional[CreditReport]:
        """获取企业最新的信用报告"""
        stmt = select(CreditReport)\
            .where(CreditReport.enterprise_id == enterprise_id)\
            .order_by(desc(CreditReport.report_date))\
            .limit(1)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[CreditReport]:
        """获取多个信用报告，支持过滤"""
        stmt = select(CreditReport)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(CreditReport, key) and value is not None:
                    conditions.append(getattr(CreditReport, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        credit_report: CreditReport,
        data: Dict[str, Any]
    ) -> CreditReport:
        """更新信用报告"""
        for key, value in data.items():
            if hasattr(credit_report, key) and value is not None:
                setattr(credit_report, key, value)
        session.flush()  # 刷新但不提交
        return credit_report
    
    @staticmethod
    def delete(session: Session, credit_report: CreditReport) -> None:
        """删除信用报告"""
        session.delete(credit_report)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_by_date_range(
        session: Session,
        enterprise_id: int,
        start_date: date,
        end_date: date
    ) -> List[CreditReport]:
        """获取指定日期范围内的信用报告"""
        stmt = select(CreditReport)\
            .where(
                and_(
                    CreditReport.enterprise_id == enterprise_id,
                    CreditReport.report_date >= start_date,
                    CreditReport.report_date <= end_date
                )
            )\
            .order_by(desc(CreditReport.report_date))
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_score_range(
        session: Session,
        min_score: float = None,
        max_score: float = None,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取指定信用分数范围内的报告"""
        conditions = []
        if min_score is not None:
            conditions.append(CreditReport.credit_score >= min_score)
        if max_score is not None:
            conditions.append(CreditReport.credit_score <= max_score)
        
        stmt = select(CreditReport)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.order_by(desc(CreditReport.credit_score))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_reports_without_file(
        session: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取没有关联文件的信用报告"""
        stmt = select(CreditReport)\
            .where(CreditReport.report_path.is_(None))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
credit_report_crud = CreditReportCRUD()
