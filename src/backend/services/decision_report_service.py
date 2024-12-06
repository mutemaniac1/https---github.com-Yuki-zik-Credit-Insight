# services/decision_report_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.decision_report_crud import decision_report_crud
from backend.database.models.decision_report import DecisionReport

class DecisionReportService:
    """决策报告服务类"""
    
    @staticmethod
    async def create_decision_report(data: Dict[str, Any]) -> Optional[DecisionReport]:
        """创建决策报告"""
        try:
            with get_session() as session:
                decision_report = decision_report_crud.create(session, data)
                session.commit()
                return decision_report
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_decision_report(report_id: int) -> Optional[DecisionReport]:
        """获取决策报告"""
        with get_session() as session:
            return decision_report_crud.get_by_id(session, report_id)
    
    @staticmethod
    async def get_user_decision_reports(
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取用户的所有决策报告"""
        with get_session() as session:
            return decision_report_crud.get_by_user_id(
                session, user_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_enterprise_decision_reports(
        enterprise_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取企业的所有决策报告"""
        with get_session() as session:
            return decision_report_crud.get_by_enterprise_id(
                session, enterprise_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_latest_enterprise_report(
        enterprise_id: int
    ) -> Optional[DecisionReport]:
        """获取企业最新的决策报告"""
        with get_session() as session:
            return decision_report_crud.get_latest_by_enterprise_id(
                session, enterprise_id
            )
    
    @staticmethod
    async def get_decision_reports(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[DecisionReport]:
        """获取决策报告列表"""
        with get_session() as session:
            return decision_report_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_decision_report(
        report_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[DecisionReport]:
        """更新决策报告"""
        try:
            with get_session() as session:
                decision_report = decision_report_crud.get_by_id(session, report_id)
                if not decision_report:
                    return None
                
                updated_report = decision_report_crud.update(
                    session, decision_report, update_data
                )
                session.commit()
                return updated_report
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_decision_report(report_id: int) -> bool:
        """删除决策报告"""
        try:
            with get_session() as session:
                decision_report = decision_report_crud.get_by_id(session, report_id)
                if not decision_report:
                    return False
                
                decision_report_crud.delete(session, decision_report)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_reports_by_date_range(
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取指定日期范围内的决策报告"""
        with get_session() as session:
            return decision_report_crud.get_by_date_range(
                session,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_reports_by_decision_type(
        decision_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取特定决策类型的报告"""
        with get_session() as session:
            return decision_report_crud.get_by_decision_type(
                session,
                decision_type=decision_type,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_reports_by_risk_level(
        risk_level: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[DecisionReport]:
        """获取特定风险等级的报告"""
        with get_session() as session:
            return decision_report_crud.get_by_risk_level(
                session,
                risk_level=risk_level,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def bulk_create_decision_reports(
        reports_data: List[Dict[str, Any]]
    ) -> List[DecisionReport]:
        """批量创建决策报告"""
        created_reports = []
        try:
            with get_session() as session:
                for data in reports_data:
                    report = decision_report_crud.create(session, data)
                    created_reports.append(report)
                session.commit()
                return created_reports
        except SQLAlchemyError as e:
            # 记录日志
            return []

# 创建服务实例
decision_report_service = DecisionReportService() 
