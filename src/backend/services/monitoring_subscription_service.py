# services/monitoring_subscription_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError
from backend.database.link import get_session
from backend.database.crud.monitoring_subscription_crud import monitoring_subscription_crud
from backend.database.models.monitoring_subscription import MonitoringSubscription

class MonitoringSubscriptionService:
    """监控订阅服务类"""
    
    @staticmethod
    async def create_subscription(data: Dict[str, Any]) -> Optional[MonitoringSubscription]:
        """创建监控订阅"""
        try:
            with get_session() as session:
                subscription = monitoring_subscription_crud.create(session, data)
                session.commit()
                return subscription
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def get_subscription(subscription_id: int) -> Optional[MonitoringSubscription]:
        """获取监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_by_id(session, subscription_id)
    
    @staticmethod
    async def get_user_subscriptions(
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取用户的所有监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_by_user_id(
                session, user_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_enterprise_subscriptions(
        enterprise_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取企业的所有监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_by_enterprise_id(
                session, enterprise_id, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_active_subscriptions(
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取所有活跃的监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_active_subscriptions(
                session, skip=skip, limit=limit
            )
    
    @staticmethod
    async def get_subscriptions(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[MonitoringSubscription]:
        """获取监控订阅列表"""
        with get_session() as session:
            return monitoring_subscription_crud.get_multi(
                session,
                skip=skip,
                limit=limit,
                **filters
            )
    
    @staticmethod
    async def update_subscription(
        subscription_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[MonitoringSubscription]:
        """更新监控订阅"""
        try:
            with get_session() as session:
                subscription = monitoring_subscription_crud.get_by_id(
                    session, subscription_id
                )
                if not subscription:
                    return None
                
                updated_subscription = monitoring_subscription_crud.update(
                    session, subscription, update_data
                )
                session.commit()
                return updated_subscription
        except SQLAlchemyError as e:
            # 记录日志
            return None
    
    @staticmethod
    async def delete_subscription(subscription_id: int) -> bool:
        """删除监控订阅"""
        try:
            with get_session() as session:
                subscription = monitoring_subscription_crud.get_by_id(
                    session, subscription_id
                )
                if not subscription:
                    return False
                
                monitoring_subscription_crud.delete(session, subscription)
                session.commit()
                return True
        except SQLAlchemyError as e:
            # 记录日志
            return False
    
    @staticmethod
    async def get_expired_subscriptions(
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取已过期的监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_expired_subscriptions(
                session,
                current_date=date.today(),
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def get_subscriptions_by_date_range(
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取指定日期范围内的监控订阅"""
        with get_session() as session:
            return monitoring_subscription_crud.get_subscriptions_by_date_range(
                session,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit
            )
    
    @staticmethod
    async def deactivate_expired_subscriptions() -> int:
        """停用所有过期的订阅"""
        try:
            with get_session() as session:
                expired_subscriptions = monitoring_subscription_crud.get_expired_subscriptions(
                    session,
                    current_date=date.today()
                )
                
                count = 0
                for subscription in expired_subscriptions:
                    monitoring_subscription_crud.update(
                        session,
                        subscription,
                        {"is_active": False}
                    )
                    count += 1
                
                session.commit()
                return count
        except SQLAlchemyError as e:
            # 记录日志
            return 0
    
    @staticmethod
    async def bulk_create_subscriptions(
        subscriptions_data: List[Dict[str, Any]]
    ) -> List[MonitoringSubscription]:
        """批量创建监控订阅"""
        created_subscriptions = []
        try:
            with get_session() as session:
                for data in subscriptions_data:
                    subscription = monitoring_subscription_crud.create(
                        session, data
                    )
                    created_subscriptions.append(subscription)
                session.commit()
                return created_subscriptions
        except SQLAlchemyError as e:
            # 记录日志
            return []

# 创建服务实例
monitoring_subscription_service = MonitoringSubscriptionService() 
