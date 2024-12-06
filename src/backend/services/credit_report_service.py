# services/credit_report_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.credit_report_crud import credit_report_crud
from backend.database.models.credit_report import CreditReport

class CreditReportService:
    """信用报告服务类"""
    
    @staticmethod
    async def create_credit_report(data: Dict[str, Any]) -> Optional[CreditReport]:
        """创建信用报告"""
        try:
            with get_session() as session:
                credit_report = credit_report_crud.create(session, data)
                session.commit()
                return credit_report
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_credit_report(report_id: int) -> Optional[CreditReport]:
        """获取信用报告"""
        with get_session() as session:
            return credit_report_crud.get_by_id(session, report_id)
    
    @staticmethod
    async def get_enterprise_credit_reports(
        enterprise_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取企业的所有信用报告"""
        with get_session() as session:
            return credit_report_crud.get_by_enterprise_id(
                session, enterprise_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_latest_credit_report(
        enterprise_id: int
    ) -> Optional[CreditReport]:
        """获取企业最新的信用报告"""
        with get_session() as session:
            return credit_report_crud.get_latest_by_enterprise_id(
                session, enterprise_id
            )
    
    @staticmethod
    async def get_credit_reports(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[CreditReport]:
        """获取信用报告列表"""
        with get_session() as session:
            return credit_report_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_credit_report(
        report_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[CreditReport]:
        """更新信用报告"""
        try:
            with get_session() as session:
                credit_report = credit_report_crud.get_by_id(session, report_id)
                if not credit_report:
                    return None
                
                updated_report = credit_report_crud.update(
                    session, credit_report, update_data
                )
                session.commit()
                return updated_report
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_credit_report(report_id: int) -> bool:
        """删除信用报告"""
        try:
            with get_session() as session:
                credit_report = credit_report_crud.get_by_id(session, report_id)
                if not credit_report:
                    return False
                
                credit_report_crud.delete(session, credit_report)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_credit_reports_by_date_range(
        enterprise_id: int,
        start_date: date,
        end_date: date
    ) -> List[CreditReport]:
        """获取指定日期范围内的信用报告"""
        with get_session() as session:
            return credit_report_crud.get_by_date_range(
                session, enterprise_id, start_date, end_date
            )
    
    @staticmethod
    async def get_credit_reports_by_score_range(
        min_score: float = None,
        max_score: float = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取指定信用分数范围内的报告"""
        with get_session() as session:
            return credit_report_crud.get_by_score_range(
                session,
                min_score=min_score,
                max_score=max_score,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_reports_without_file(
        skip: int = 0,
        limit: int = 100
    ) -> List[CreditReport]:
        """获取没有关联文件的信用报告"""
        with get_session() as session:
            return credit_report_crud.get_reports_without_file(
                session, skip=skip, limit=limit
            )
    
    @staticmethod
    async def bulk_create_credit_reports(
        reports_data: List[Dict[str, Any]]
    ) -> List[CreditReport]:
        """批量创建信用报告"""
        created_reports = []
        try:
            with get_session() as session:
                for data in reports_data:
                    report = credit_report_crud.create(session, data)
                    created_reports.append(report)
                session.commit()
                return created_reports
        except SQLAlchemyError as e:
            # 记录日志
            return []

# 创建服务实例
credit_report_service = CreditReportService() 
