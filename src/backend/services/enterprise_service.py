# services/enterprise_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.enterprise_crud import enterprise_crud
from backend.database.models.enterprise import Enterprise

class EnterpriseService:
    """企业服务类"""
    
    @staticmethod
    async def create_enterprise(enterprise_data: Dict[str, Any]) -> Optional[Enterprise]:
        """创建企业"""
        try:
            with get_session() as session:
                enterprise = enterprise_crud.create(session, enterprise_data)
                session.commit()
                return enterprise
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_enterprise(enterprise_id: int) -> Optional[Enterprise]:
        """获取企业信息"""
        with get_session() as session:
            return enterprise_crud.get_by_id(session, enterprise_id)
    
    @staticmethod
    async def get_enterprise_by_company_id(company_id: str) -> Optional[Enterprise]:
        """通过统一社会信用代码获取企业"""
        with get_session() as session:
            return enterprise_crud.get_by_company_id(session, company_id)
    
    @staticmethod
    async def get_enterprises(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[Enterprise]:
        """获取企业列表"""
        with get_session() as session:
            return enterprise_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_enterprise(
        enterprise_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[Enterprise]:
        """更新企业信息"""
        try:
            with get_session() as session:
                enterprise = enterprise_crud.get_by_id(session, enterprise_id)
                if not enterprise:
                    return None
                
                updated_enterprise = enterprise_crud.update(
                    session, enterprise, update_data
                )
                session.commit()
                return updated_enterprise
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_enterprise(enterprise_id: int) -> bool:
        """删除企业"""
        try:
            with get_session() as session:
                enterprise = enterprise_crud.get_by_id(session, enterprise_id)
                if not enterprise:
                    return False
                
                enterprise_crud.delete(session, enterprise)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_enterprises_by_industry(
        industry: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Enterprise]:
        """获取特定行业的企业列表"""
        with get_session() as session:
            return enterprise_crud.get_by_industry(
                session, industry, skip, limit
            )
    
    @staticmethod
    async def search_enterprises(
        name_pattern: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Enterprise]:
        """搜索企业名称"""
        with get_session() as session:
            return enterprise_crud.search_by_name(
                session, name_pattern, skip, limit
            )
    
    @staticmethod
    async def bulk_create_enterprises(
        enterprises_data: List[Dict[str, Any]]
    ) -> List[Enterprise]:
        """批量创建企业"""
        created_enterprises = []
        try:
            with get_session() as session:
                for data in enterprises_data:
                    enterprise = enterprise_crud.create(session, data)
                    created_enterprises.append(enterprise)
                session.commit()
                return created_enterprises
        except SQLAlchemyError as e:
            # 记录日志
            return []

# 创建服务实例
enterprise_service = EnterpriseService() 
