# -*- coding: utf-8 -*-
from contextlib import contextmanager
from typing import Generator, Any, Callable
import logging
import time
from multiprocessing import cpu_count
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from dotenv import load_dotenv
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(override=True)  # 强制重新加载环境变量
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseMetrics:
    """数据库性能指标收集器"""
    def __init__(self):
        self.active_connections = 0
        self.waiting_connections = 0
        self.total_queries = 0
        self.slow_queries = 0
        self.deadlocks = 0
        self.query_times = []  # 存储最近的查询时间
        
    def record_query_time(self, duration: float) -> None:
        """记录查询时间"""
        self.total_queries += 1
        self.query_times.append(duration)
        if len(self.query_times) > 1000:  # 保留最近1000次查询的时间
            self.query_times.pop(0)
        if duration > 1.0:  # 慢查询阈值：1秒
            self.slow_queries += 1
            logger.warning(f"检测到慢查询，耗时: {duration:.2f}秒")
            
    def record_deadlock(self) -> None:
        """记录死锁事件"""
        self.deadlocks += 1
        logger.error(f"检测到死锁，当前死锁总数: {self.deadlocks}")
        
    def get_average_query_time(self) -> float:
        """获取平均查询时间"""
        if not self.query_times:
            return 0.0
        return sum(self.query_times) / len(self.query_times)

class DatabaseConfig:
    """数据库配置类"""
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 从环境变量获取数据库URL
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL 环境变量未设置")
            
        # 连接池配置
        self.POOL_SIZE = int(os.getenv('POOL_SIZE', str(max(cpu_count() * 2, 20))))
        self.MAX_OVERFLOW = int(os.getenv('MAX_OVERFLOW', str(self.POOL_SIZE // 2)))
        self.POOL_TIMEOUT = int(os.getenv('POOL_TIMEOUT', '30'))
        self.POOL_RECYCLE = int(os.getenv('POOL_RECYCLE', '1800'))
        self.ECHO_SQL = os.getenv('ECHO_SQL', 'False').lower() == 'true'
        
        # 重试配置
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
        self.RETRY_DELAY = float(os.getenv('RETRY_DELAY', '0.1'))
        
        # 事务配置
        self.DEFAULT_ISOLATION_LEVEL = os.getenv('ISOLATION_LEVEL', 'READ_COMMITTED')
        self.STATEMENT_TIMEOUT = int(os.getenv('STATEMENT_TIMEOUT', '30000'))  

class DatabaseManager:
    """数据库管理类"""
    def __init__(self):
        self.config = DatabaseConfig()
        self._engine = None
        self._SessionLocal = None
        self.Base = declarative_base()
        self.metrics = DatabaseMetrics()
        
        # 确保 OpenGauss 支持
        try:
            import opengauss_sqlalchemy as opengauss
        except ImportError:
            raise ImportError(
                "请确保已安装 opengauss-sqlalchemy 库。使用 pip install opengauss-sqlalchemy 进行安装。"
            )
        
        self._initialize_engine()
        self._setup_engine_events()

    def _initialize_engine(self) -> None:
        """初始化数据库引擎"""
        try:
            self._engine = create_engine(
                self.config.DATABASE_URL,
                echo=self.config.ECHO_SQL,
                pool_size=self.config.POOL_SIZE,
                max_overflow=self.config.MAX_OVERFLOW,
                pool_timeout=self.config.POOL_TIMEOUT,
                pool_recycle=self.config.POOL_RECYCLE,
                pool_pre_ping=True,  # 连接健康检查
                isolation_level=self.config.DEFAULT_ISOLATION_LEVEL
            ).execution_options(
                timeout=self.config.STATEMENT_TIMEOUT
            )
            
            self._SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
            logger.info("数据库引擎初始化成功")
        except Exception as e:
            logger.error(f"数据库引擎初始化失败: {str(e)}")
            raise

    def _setup_engine_events(self) -> None:
        """设置引擎事件监听器"""
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(datetime.now())
            if self.config.ECHO_SQL:
                logger.debug(f"执行SQL: {statement}")
                logger.debug(f"参数: {parameters}")

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            duration = (datetime.now() - conn.info['query_start_time'].pop()).total_seconds()
            self.metrics.record_query_time(duration)
            if self.config.ECHO_SQL:
                logger.debug(f"SQL执行时间: {duration:.2f}秒")

    def execute_with_retry(self, session: Session, operation: Callable[[Session], Any]) -> Any:
        """带有重试机制的数据库操作执行器"""
        for attempt in range(self.config.MAX_RETRIES):
            try:
                result = operation(session)
                return result
            except OperationalError as e:
                if "deadlock" in str(e).lower():
                    self.metrics.record_deadlock()
                if attempt < self.config.MAX_RETRIES - 1:
                    session.rollback()
                    time.sleep(self.config.RETRY_DELAY * (attempt + 1))  # 指数退避
                    continue
                raise
            except Exception as e:
                logger.error(f"数据库操作失败: {str(e)}")
                raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """获取数据库会话的上下文管理器"""
        session: Session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"数据库操作错误: {str(e)}")
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"未知错误: {str(e)}")
            raise
        finally:
            session.close()

    @contextmanager
    def timeout_session(self, timeout_seconds: int = 30) -> Generator[Session, None, None]:
        """带有超时机制的数据库会话"""
        start_time = time.time()
        session = self._SessionLocal()
        try:
            yield session
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError("数据库操作超时")
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"会话执行错误: {str(e)}")
            raise
        finally:
            session.close()

    def check_connection(self) -> bool:
        """检查数据库连接"""
        try:
            with self.timeout_session(timeout_seconds=5) as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"数据库连接检查失败: {str(e)}")
            return False

    def get_engine_stats(self) -> dict:
        """获取数据库引擎统计信息"""
        if not self._engine:
            return {}
        
        stats = {
            "pool_size": self._engine.pool.size(),
            "checkedin": self._engine.pool.checkedin(),
            "checkedout": self._engine.pool.checkedout(),
            "overflow": self._engine.pool.overflow(),
            "total_queries": self.metrics.total_queries,
            "slow_queries": self.metrics.slow_queries,
            "deadlocks": self.metrics.deadlocks,
            "avg_query_time": self.metrics.get_average_query_time()
        }
        
        # 添加警告信息
        if stats["checkedout"] / stats["pool_size"] > 0.8:
            logger.warning("连接池使用率超过80%")
            
        return stats

# 创建全局数据库管理器实例
db_manager = DatabaseManager()

# 导出数据库对象
engine = db_manager._engine
Base = db_manager.Base
SessionLocal = db_manager._SessionLocal

# 导出常用函数
get_session = db_manager.get_session
timeout_session = db_manager.timeout_session
check_connection = db_manager.check_connection
execute_with_retry = db_manager.execute_with_retry

if __name__ == "__main__":
    # 测试数据库连接
    if check_connection():
        print("数据库连接成功")
        print("连接池统计:", db_manager.get_engine_stats())
    else:
        print("数据库连接失败")
