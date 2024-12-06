# services/user_service.py
# -*- coding: utf-8 -*-
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.database.link import get_session
from backend.database.crud.user_crud import user_crud
from backend.database.models.user import User

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类
    职责：处理用户相关的业务逻辑
    """
    
    @staticmethod
    def _to_dict(user: User) -> Dict[str, Any]:
        """将User对象转换为字典"""
        if not user:
            return None
        return {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'role': user.role,
            'created_at': user.created_at,
            'is_active': user.is_active,
            'last_login': user.last_login,
            'updated_at': user.updated_at
        }
    
    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Optional[int]:
        """创建用户"""
        try:
            with get_session() as session:
                # 添加默认值
                user_data['is_active'] = user_data.get('is_active', True)
                user = user_crud.create(session, user_data)
                return user.user_id if user else None
        except IntegrityError as e:
            logger.error(f"创建用户失败，可能存在重复数据: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"创建用户时发生未知错误: {str(e)}")
            return None
    
    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        try:
            with get_session() as session:
                user = user_crud.get_by_id(session, user_id)
                return UserService._to_dict(user)
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """通过邮箱获取用户"""
        try:
            with get_session() as session:
                user = user_crud.get_by_email(session, email)
                return UserService._to_dict(user)
        except Exception as e:
            logger.error(f"通过邮箱获取用户失败: {str(e)}")
            return None
    
    @staticmethod
    async def update_user(
        user_id: int,
        update_data: Dict[str, Any]
    ) -> bool:
        """更新用户信息"""
        try:
            with get_session() as session:
                user = user_crud.update(session, user_id, update_data)
                return user is not None
        except IntegrityError as e:
            logger.error(f"更新用户失败，可能违反唯一性约束: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"更新用户时发生未知错误: {str(e)}")
            return False
    
    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """删除用户"""
        try:
            with get_session() as session:
                return user_crud.delete(session, user_id)
        except Exception as e:
            logger.error(f"删除用户失败: {str(e)}")
            return False
    
    @staticmethod
    async def get_users(
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[Dict[str, Any]]:
        """获取用户列表"""
        try:
            with get_session() as session:
                users = user_crud.get_multi(
                    session,
                    skip=skip,
                    limit=limit,
                    **filters
                )
                return [UserService._to_dict(user) for user in users]
        except Exception as e:
            logger.error(f"获取用户列表失败: {str(e)}")
            return []
    
    @staticmethod
    async def soft_delete_user(user_id: int) -> bool:
        """软删除用户"""
        return await UserService.update_user(user_id, {"is_active": False})
    
    @staticmethod
    async def restore_user(user_id: int) -> bool:
        """恢复已软删除的用户"""
        return await UserService.update_user(user_id, {"is_active": True})
    
    @staticmethod
    async def update_last_login(user_id: int) -> bool:
        """更新用户最后登录时间"""
        return await UserService.update_user(
            user_id,
            {"last_login": datetime.utcnow()}
        )

# 创建服务实例
user_service = UserService()
