# services/disclosure_info_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.disclosure_info_crud import disclosure_info_crud
from backend.database.models.disclosure_info import DisclosureInfo

class DisclosureInfoService:
    """信息披露服务类"""
    
    @staticmethod
    async def create_disclosure_info(data: Dict[str, Any]) -> Optional[DisclosureInfo]:
        """创建信息披露"""
        try:
            with get_session() as session:
                disclosure_info = disclosure_info_crud.create(session, data)
                session.commit()
                return disclosure_info
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_disclosure_info(disclosure_id: int) -> Optional[DisclosureInfo]:
        """获取信息披露"""
        with get_session() as session:
            return disclosure_info_crud.get_by_id(session, disclosure_id)
    
    @staticmethod
    async def get_enterprise_disclosures(
        enterprise_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取企业的所有信息披露"""
        with get_session() as session:
            return disclosure_info_crud.get_by_enterprise_id(
                session, enterprise_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_latest_enterprise_disclosure(
        enterprise_id: int
    ) -> Optional[DisclosureInfo]:
        """获取企业最新的信息披露"""
        with get_session() as session:
            return disclosure_info_crud.get_latest_by_enterprise_id(
                session, enterprise_id
            )
    
    @staticmethod
    async def get_disclosure_infos(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[DisclosureInfo]:
        """获取信息披露列表"""
        with get_session() as session:
            return disclosure_info_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_disclosure_info(
        disclosure_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[DisclosureInfo]:
        """更新信息披露"""
        try:
            with get_session() as session:
                disclosure_info = disclosure_info_crud.get_by_id(session, disclosure_id)
                if not disclosure_info:
                    return None
                
                updated_info = disclosure_info_crud.update(
                    session, disclosure_info, update_data
                )
                session.commit()
                return updated_info
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_disclosure_info(disclosure_id: int) -> bool:
        """删除信息披露"""
        try:
            with get_session() as session:
                disclosure_info = disclosure_info_crud.get_by_id(session, disclosure_id)
                if not disclosure_info:
                    return False
                
                disclosure_info_crud.delete(session, disclosure_info)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_disclosures_by_date_range(
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取指定日期范围内的信息披露"""
        with get_session() as session:
            return disclosure_info_crud.get_by_date_range(
                session,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_disclosures_by_type(
        disclosure_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取特定类型的信息披露"""
        with get_session() as session:
            return disclosure_info_crud.get_by_disclosure_type(
                session,
                disclosure_type=disclosure_type,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_delayed_disclosures(
        skip: int = 0,
        limit: int = 100
    ) -> List[DisclosureInfo]:
        """获取延迟披露的信息"""
        with get_session() as session:
            return disclosure_info_crud.get_delayed_disclosures(
                session,
                current_date=date.today(),
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def bulk_create_disclosure_infos(
        infos_data: List[Dict[str, Any]]
    ) -> List[DisclosureInfo]:
        """批量创建信息披露"""
        created_infos = []
        try:
            with get_session() as session:
                for data in infos_data:
                    info = disclosure_info_crud.create(session, data)
                    created_infos.append(info)
                session.commit()
                return created_infos
        except SQLAlchemyError as e:
            # 记录日志
            return []
    
    @staticmethod
    async def mark_as_disclosed(
        disclosure_id: int,
        disclosure_date: date = None
    ) -> Optional[DisclosureInfo]:
        """标记信息已披露"""
        try:
            with get_session() as session:
                disclosure_info = disclosure_info_crud.get_by_id(session, disclosure_id)
                if not disclosure_info:
                    return None
                
                update_data = {
                    "disclosure_date": disclosure_date or date.today(),
                    "status": "已披露"
                }
                
                updated_info = disclosure_info_crud.update(
                    session, disclosure_info, update_data
                )
                session.commit()
                return updated_info
        except SQLAlchemyError as e:
            # 记录日志
            return None

# 创建服务实例
disclosure_info_service = DisclosureInfoService() 
