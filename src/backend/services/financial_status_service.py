# services/financial_status_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.financial_status_crud import financial_status_crud
from backend.database.models.financial_status import FinancialStatus

class FinancialStatusService:
    """财务状态服务类"""
    
    @staticmethod
    async def create_financial_status(data: Dict[str, Any]) -> Optional[FinancialStatus]:
        """创建财务状态记录"""
        try:
            with get_session() as session:
                financial_status = financial_status_crud.create(session, data)
                session.commit()
                return financial_status
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_financial_status(status_id: int) -> Optional[FinancialStatus]:
        """获取财务状态记录"""
        with get_session() as session:
            return financial_status_crud.get_by_id(session, status_id)
    
    @staticmethod
    async def get_enterprise_financial_status(
        enterprise_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialStatus]:
        """获取企业的所有财务状态记录"""
        with get_session() as session:
            return financial_status_crud.get_by_enterprise_id(
                session, enterprise_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_latest_financial_status(
        enterprise_id: int
    ) -> Optional[FinancialStatus]:
        """获取企业最新的财务状态记录"""
        with get_session() as session:
            return financial_status_crud.get_latest_by_enterprise_id(
                session, enterprise_id
            )
    
    @staticmethod
    async def get_financial_statuses(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[FinancialStatus]:
        """获取财务状态列表"""
        with get_session() as session:
            return financial_status_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_financial_status(
        status_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[FinancialStatus]:
        """更新财务状态记录"""
        try:
            with get_session() as session:
                financial_status = financial_status_crud.get_by_id(session, status_id)
                if not financial_status:
                    return None
                
                updated_status = financial_status_crud.update(
                    session, financial_status, update_data
                )
                session.commit()
                return updated_status
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_financial_status(status_id: int) -> bool:
        """删除财务状态记录"""
        try:
            with get_session() as session:
                financial_status = financial_status_crud.get_by_id(session, status_id)
                if not financial_status:
                    return False
                
                financial_status_crud.delete(session, financial_status)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_financial_status_by_date_range(
        enterprise_id: int,
        start_date: date,
        end_date: date
    ) -> List[FinancialStatus]:
        """获取指定日期范围内的财务状态记录"""
        with get_session() as session:
            return financial_status_crud.get_by_date_range(
                session, enterprise_id, start_date, end_date
            )
    
    @staticmethod
    async def get_overdue_records(
        min_overdue_rate: float = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialStatus]:
        """获取逾期记录"""
        with get_session() as session:
            return financial_status_crud.get_overdue_records(
                session,
                min_overdue_rate=min_overdue_rate,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def bulk_create_financial_status(
        status_data_list: List[Dict[str, Any]]
    ) -> List[FinancialStatus]:
        """批量创建财务状态记录"""
        created_records = []
        try:
            with get_session() as session:
                for data in status_data_list:
                    status = financial_status_crud.create(session, data)
                    created_records.append(status)
                session.commit()
                return created_records
        except SQLAlchemyError as e:
            # 记录日志
            return []

# 创建服务实例
financial_status_service = FinancialStatusService() 
