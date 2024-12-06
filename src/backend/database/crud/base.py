from typing import Generic, TypeVar, Type, Any, Optional, Dict, List
from sqlalchemy.orm import Session
from database.link import get_session, execute_with_retry, timeout_session

ModelType = TypeVar("ModelType")

class CRUDBase(Generic[ModelType]):
    """
    基础 CRUD 类，支持连接池和事务管理
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _get_session(self, timeout: Optional[int] = None):
        """获取数据库会话，支持超时设置"""
        if timeout:
            return timeout_session(timeout_seconds=timeout)
        return get_session()

    async def create(self, data: Dict[str, Any]) -> ModelType:
        """创建记录"""
        def _operation(session: Session):
            db_obj = self.model(**data)
            session.add(db_obj)
            session.flush()  # 立即获取数据库生成的ID
            return db_obj

        with self._get_session() as session:
            return execute_with_retry(session, _operation)

    async def get(self, id: Any) -> Optional[ModelType]:
        """获取单条记录"""
        with self._get_session() as session:
            return session.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        timeout: Optional[int] = None
    ) -> List[ModelType]:
        """获取多条记录，支持超时设置"""
        with self._get_session(timeout=timeout) as session:
            return session.query(self.model)\
                .offset(skip)\
                .limit(limit)\
                .all()

    async def update(
        self, 
        id: Any, 
        data: Dict[str, Any]
    ) -> Optional[ModelType]:
        """更新记录"""
        def _operation(session: Session):
            obj = session.query(self.model).filter(self.model.id == id).first()
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
            return obj

        with self._get_session() as session:
            return execute_with_retry(session, _operation)

    async def delete(self, id: Any) -> bool:
        """删除记录"""
        with self._get_session() as session:
            obj = session.query(self.model).filter(self.model.id == id).first()
            if obj:
                session.delete(obj)
                return True
            return False

    async def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """批量创建记录"""
        def _operation(session: Session):
            objects = [self.model(**data) for data in data_list]
            session.bulk_save_objects(objects)
            session.flush()
            return objects

        with self._get_session() as session:
            return execute_with_retry(session, _operation)

    async def execute_with_session(self, operation: Any, timeout: Optional[int] = None):
        """执行自定义会话操作"""
        with self._get_session(timeout=timeout) as session:
            return execute_with_retry(session, operation) 
