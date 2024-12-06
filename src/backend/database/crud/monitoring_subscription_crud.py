# crud/monitoring_subscription_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from backend.database.models.monitoring_subscription import MonitoringSubscription

class MonitoringSubscriptionCRUD:
    """监控订阅表CRUD操作类"""
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> MonitoringSubscription:
        """创建监控订阅记录"""
        subscription = MonitoringSubscription(**data)
        session.add(subscription)
        session.flush()  # 获取自增ID，但不提交事务
        return subscription
    
    @staticmethod
    def get_by_id(session: Session, subscription_id: int) -> Optional[MonitoringSubscription]:
        """通过ID获取监控订阅"""
        return session.get(MonitoringSubscription, subscription_id)
    
    @staticmethod
    def get_by_user_id(
        session: Session,
        user_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取用户的所有监控订阅"""
        stmt = select(MonitoringSubscription)\
            .where(MonitoringSubscription.user_id == user_id)\
            .order_by(desc(MonitoringSubscription.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_enterprise_id(
        session: Session,
        enterprise_id: int,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取企业的所有监控订阅"""
        stmt = select(MonitoringSubscription)\
            .where(MonitoringSubscription.enterprise_id == enterprise_id)\
            .order_by(desc(MonitoringSubscription.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_active_subscriptions(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取所有活跃的监控订阅"""
        stmt = select(MonitoringSubscription)\
            .where(MonitoringSubscription.is_active == True)\
            .order_by(desc(MonitoringSubscription.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[MonitoringSubscription]:
        """获取多个监控订阅，支持过滤"""
        stmt = select(MonitoringSubscription)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(MonitoringSubscription, key) and value is not None:
                    conditions.append(getattr(MonitoringSubscription, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        subscription: MonitoringSubscription,
        data: Dict[str, Any]
    ) -> MonitoringSubscription:
        """更新监控订阅"""
        for key, value in data.items():
            if hasattr(subscription, key) and value is not None:
                setattr(subscription, key, value)
        session.flush()  # 刷新但不提交
        return subscription
    
    @staticmethod
    def delete(session: Session, subscription: MonitoringSubscription) -> None:
        """删除监控订阅"""
        session.delete(subscription)
        session.flush()  # 刷新但不提交
    
    @staticmethod
    def get_expired_subscriptions(
        session: Session,
        current_date: date,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取已过期的监控订阅"""
        stmt = select(MonitoringSubscription)\
            .where(
                and_(
                    MonitoringSubscription.end_date < current_date,
                    MonitoringSubscription.is_active == True
                )
            )\
            .order_by(desc(MonitoringSubscription.end_date))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_subscriptions_by_date_range(
        session: Session,
        start_date: date,
        end_date: date,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[MonitoringSubscription]:
        """获取指定日期范围内的监控订阅"""
        stmt = select(MonitoringSubscription)\
            .where(
                and_(
                    MonitoringSubscription.start_date >= start_date,
                    MonitoringSubscription.end_date <= end_date
                )
            )\
            .order_by(desc(MonitoringSubscription.created_at))\
            .offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

# 创建单例实例
monitoring_subscription_crud = MonitoringSubscriptionCRUD() 
