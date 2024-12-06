# crud/user_crud.py
# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from backend.database.models.user import User

class UserCRUD:
    """用户表CRUD操作类
    职责：提供对用户表的基础数据库操作
    原则：简单、可靠、专注于数据访问
    """
    
    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> Optional[User]:
        """创建用户记录"""
        try:
            user = User(**data)
            session.add(user)
            session.flush()
            return user
        except Exception:
            session.rollback()
            return None
    
    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[User]:
        """通过ID获取用户"""
        return session.get(User, user_id)
    
    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_multi(
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[User]:
        """获取多个用户记录"""
        stmt = select(User)
        
        # 添加过滤条件
        if filters:
            conditions = []
            for key, value in filters.items():
                if hasattr(User, key):
                    conditions.append(getattr(User, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(
        session: Session,
        user_id: int,
        data: Dict[str, Any]
    ) -> Optional[User]:
        """更新用户记录"""
        try:
            user = session.get(User, user_id)
            if not user:
                return None
            
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            session.flush()
            return user
        except Exception:
            session.rollback()
            return None
    
    @staticmethod
    def delete(session: Session, user_id: int) -> bool:
        """删除用户记录"""
        try:
            user = session.get(User, user_id)
            if not user:
                return False
            session.delete(user)
            session.flush()
            return True
        except Exception:
            session.rollback()
            return False

# 创建单例实例
user_crud = UserCRUD()
