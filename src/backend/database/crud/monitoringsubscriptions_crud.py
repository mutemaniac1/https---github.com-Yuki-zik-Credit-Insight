# crud/monitoring_subscription.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from database.models.monitoring_subscription import MonitoringSubscription

class MonitoringSubscriptionCRUD:
    def create_subscription(self, db: Session, subscription_data: dict):
        """
        创建新的监控订阅
        """
        new_subscription = MonitoringSubscription(**subscription_data)
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return new_subscription

    def get_subscription_by_id(self, db: Session, subscription_id: int):
        """
        根据订阅ID获取监控订阅
        """
        return db.query(MonitoringSubscription).filter(MonitoringSubscription.subscription_id == subscription_id).first()

    def get_subscriptions_by_user(self, db: Session, user_id: int):
        """
        获取某个用户的所有监控订阅
        """
        return db.query(MonitoringSubscription).filter(MonitoringSubscription.user_id == user_id).all()

    def get_subscriptions_by_enterprise(self, db: Session, enterprise_id: int):
        """
        获取某个企业的所有监控订阅
        """
        return db.query(MonitoringSubscription).filter(MonitoringSubscription.enterprise_id == enterprise_id).all()

    def update_subscription(self, db: Session, subscription_id: int, update_data: dict):
        """
        更新监控订阅信息
        """
        subscription = db.query(MonitoringSubscription).filter(MonitoringSubscription.subscription_id == subscription_id).first()
        if subscription:
            for key, value in update_data.items():
                setattr(subscription, key, value)
            db.commit()
            db.refresh(subscription)
        return subscription

    def delete_subscription(self, db: Session, subscription_id: int):
        """
        删除监控订阅
        """
        subscription = db.query(MonitoringSubscription).filter(MonitoringSubscription.subscription_id == subscription_id).first()
        if subscription:
            db.delete(subscription)
            db.commit()
        return subscription

# 实例化 MonitoringSubscriptionCRUD
monitoring_subscription_crud = MonitoringSubscriptionCRUD()
