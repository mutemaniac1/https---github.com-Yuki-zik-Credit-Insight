# Database Module Documentation

## 模块概述

数据库模块是 Credit Insight 后端的核心组件，负责管理与 OpenGauss 数据库的所有交互。该模块采用 SQLAlchemy ORM 框架，实现了连接池管理、会话处理、错误处理等功能。

## 架构设计

```mermaid
classDiagram
    class DatabaseConfig {
        +DATABASE_URL: str
        +POOL_SIZE: int
        +MAX_OVERFLOW: int
        +POOL_TIMEOUT: int
        +POOL_RECYCLE: int
        +ECHO_SQL: bool
        +__init__()
    }
    
    class DatabaseManager {
        -_engine: Engine
        -_SessionLocal: sessionmaker
        +Base: declarative_base
        +__init__()
        +_initialize_engine()
        +_setup_engine_events()
        +get_session()
        +check_connection()
        +get_engine_stats()
    }
    
    DatabaseManager --> DatabaseConfig : uses
    DatabaseManager --> Base : creates
```

## 连接池工作流程

```mermaid
sequenceDiagram
    participant App as 应用程序
    participant Manager as DatabaseManager
    participant Pool as 连接池
    participant DB as OpenGauss

    App->>Manager: 请求数据库会话
    Manager->>Pool: 检查可用连接
    alt 有可用连接
        Pool->>Manager: 返回现有连接
    else 无可用连接
        Pool->>DB: 创建新连接
        DB-->>Pool: 返回新连接
        Pool->>Manager: 返回新连接
    end
    Manager->>App: 返回数据库会话
    App->>App: 执行数据库操作
    App->>Manager: 释放会话
    Manager->>Pool: 归还连接
```

## 主要组件说明

### 1. 数据库配置 (DatabaseConfig)

负责管理数据库连接和连接池的配置参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| POOL_SIZE | 连接池大小 | 20 |
| MAX_OVERFLOW | 最大溢出连接数 | 10 |
| POOL_TIMEOUT | 连接超时时间(秒) | 30 |
| POOL_RECYCLE | 连接回收时间(秒) | 1800 |
| ECHO_SQL | 是否打印SQL语句 | False |

### 2. 数据库管理器 (DatabaseManager)

核心功能类，提供以下功能：
- 数据库引擎初始化
- 连接池管理
- 会话管理
- 性能监控
- 错误处理

### 3. 会话管理

```mermaid
stateDiagram-v2
    [*] --> 获取会话
    获取会话 --> 执行操作
    执行操作 --> 提交事务: 成功
    执行操作 --> 回滚事务: 失败
    提交事务 --> 关闭会话
    回滚事务 --> 关闭会话
    关闭会话 --> [*]
```

## 使用示例

### 1. 基本查询操作

```python
from database.link import get_session

with get_session() as session:
    # 执行查询
    result = session.execute(text("SELECT * FROM users"))
    users = result.fetchall()
```

### 2. 使用 ORM 模型

```python
from database.models import User

with get_session() as session:
    # 创建新用户
    new_user = User(username="test", email="test@example.com")
    session.add(new_user)
    # 会话结束时自动提交
```

### 3. 检查数据库连接

```python
from database.link import check_connection

if check_connection():
    print("数据库连接正常")
else:
    print("数据库连接失败")
```

## 性能监控

### 连接池统计信息

```python
from database.link import db_manager

stats = db_manager.get_engine_stats()
print(f"连接池统计: {stats}")
```

统计信息包含：
- pool_size: 当前连接池大小
- checkedin: 可用连接数
- checkedout: 使用中的连接数
- overflow: 溢出连接数

## 错误处理

模块实现了完整的错误处理机制：

```mermaid
flowchart TD
    A[数据库操作] --> B{是否成功?}
    B -->|是| C[提交事务]
    B -->|否| D[回滚事务]
    D --> E[记录错误日志]
    E --> F[抛出异常]
    C --> G[关闭会话]
    F --> G
```

### 日志记录

所有数据库操作都会记录详细日志：
- 信息级别：成功的连接和操作
- 错误级别：失败的操作和异常
- 调试级别：SQL 语句和执行时间（当 ECHO_SQL=True）

## 配置说明

在 `.env` 文件中配置数据库参数：

```env
# 必需配置
DATABASE_URL=opengauss+psycopg2://username:password@host:port/dbname

# 可选配置
POOL_SIZE=20
MAX_OVERFLOW=10
POOL_TIMEOUT=30
POOL_RECYCLE=1800
ECHO_SQL=False
```

## 高级配置说明

### 数据库引擎配置

```python
engine = create_engine(
    DATABASE_URL,
    # 基础配置
    echo=config.ECHO_SQL,                    # SQL语句输出
    
    # 连接池配置
    pool_size=max(cpu_count() * 2, 20),     # 基础连接池大小（CPU核心数*2）
    max_overflow=POOL_SIZE // 2,            # 允许的额外连接数
    pool_timeout=30,                        # 等待连接的超时时间（秒）
    pool_recycle=1800,                      # 连接回收时间（30分钟）
    pool_pre_ping=True,                     # 连接健康检查
    
    # 事务配置
    isolation_level='READ_COMMITTED',        # 事务隔离级别
    
    # 应用标识
    connect_args={
        "application_name": "Credit-Insight"  # 应用名称标识
    }
).execution_options(
    timeout=30000  # 语句执行超时时间（毫秒）
)
```

### 配置参数说明

#### 1. 连接池配置

| 参数 | 说明 | 推荐值 | 环境变量 |
|------|------|--------|----------|
| pool_size | 基础连接池大小 | CPU核心数 * 2 | POOL_SIZE |
| max_overflow | 允许的额外连接数 | pool_size // 2 | MAX_OVERFLOW |
| pool_timeout | 等待连接超时时间 | 30秒 | POOL_TIMEOUT |
| pool_recycle | 连接回收时间 | 1800秒 | POOL_RECYCLE |
| pool_pre_ping | 连接健康检查 | True | - |

#### 2. 事务配置

| 参数 | 说明 | 推荐值 | 环境变量 |
|------|------|--------|----------|
| isolation_level | 事务隔离级别 | READ_COMMITTED | ISOLATION_LEVEL |
| statement_timeout | 语句执行超时 | 30000ms | STATEMENT_TIMEOUT |

#### 3. 重试配置

| 参数 | 说明 | 推荐值 | 环境变量 |
|------|------|--------|----------|
| max_retries | 最大重试次数 | 3 | MAX_RETRIES |
| retry_delay | 重试延迟时间 | 0.1秒 | RETRY_DELAY |

### 环境变量配置示例

```env
# 数据库连接
DATABASE_URL=opengauss+psycopg2://username:password@host:port/dbname

# 连接池配置
POOL_SIZE=20                # 或者使用 CPU核心数 * 2
MAX_OVERFLOW=10            # 或者使用 POOL_SIZE // 2
POOL_TIMEOUT=30
POOL_RECYCLE=1800

# 事务配置
ISOLATION_LEVEL=READ_COMMITTED
STATEMENT_TIMEOUT=30000    

# 重试配置
MAX_RETRIES=3
RETRY_DELAY=0.1

# 调试配置
ECHO_SQL=False            # 是否打印SQL语句
```

### 性能监控指标

```python
class DatabaseMetrics:
    """数据库性能指标收集器"""
    def __init__(self):
        self.active_connections = 0      # 活动连接数
        self.waiting_connections = 0     # 等待连接数
        self.total_queries = 0          # 总查询数
        self.slow_queries = 0           # 慢查询数
        self.deadlocks = 0              # 死锁次数
        self.query_times = []           # 查询时间记录
```

#### 监控指标说明

| 指标 | 说明 | 警告阈值 | 处理建议 |
|------|------|----------|----------|
| active_connections | 当前活动连接数 | >80% pool_size | 考虑增加连接池大小 |
| slow_queries | 慢查询数量 | >1% total_queries | 优化相关查询 |
| deadlocks | 死锁次数 | >0 | 检查事务逻辑 |
| avg_query_time | 平均查询时间 | >1秒 | 优化查询性能 |

### 使用建议

1. **连接池配置**
   ```python
   # 根据服务器CPU核心数动态配置
   POOL_SIZE = max(cpu_count() * 2, 20)
   MAX_OVERFLOW = POOL_SIZE // 2
   ```

2. **会话管理**
   ```python
   # 使用超时会话
   with timeout_session(timeout_seconds=30) as session:
       result = session.query(User).all()
   ```

3. **重试机制**
   ```python
   # 使用重试装饰器
   @execute_with_retry
   def get_user(session, user_id):
       return session.query(User).get(user_id)
   ```

4. **性能监控**
   ```python
   # 获取性能统计
   stats = db_manager.get_engine_stats()
   if stats["slow_queries"] > 0:
       logger.warning(f"检测到 {stats['slow_queries']} 个慢查询")
   ```


## 依赖要求

- Python >= 3.12
- SQLAlchemy >= 2.0
- opengauss-sqlalchemy >= 2.2.0
- python-dotenv >= 1.0.0 

## 并发处理

### 并发场景分析

```mermaid
sequenceDiagram
    participant C1 as 客户端1
    participant C2 as 客户端2
    participant Pool as 连接池
    participant DB as 数据库

    C1->>Pool: 请求连接
    C2->>Pool: 请求连接
    
    alt 连接池未满
        Pool->>C1: 分配连接1
        Pool->>C2: 分配连接2
    else 连接池已满
        Pool->>C2: 等待可用连接
        Note over C2: 等待超时时抛出异常
    end
    
    C1->>DB: 执行事务1
    C2->>DB: 执行事务2
    
    Note over DB: 可能的死锁情况
    
    C1-->>Pool: 归还连接
    C2-->>Pool: 归还连接
```

### 潜在的并发问题

1. **资源竞争**
   - 连接池耗尽
   - 连接获取超时
   - 死锁
   
2. **事务隔离**
   - 脏读
   - 不可重复读
   - 幻读

3. **连接泄漏**
   - 连接未正确释放
   - 长事务占用

### 解决方案

1. **连接池配置优化**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,               # 基础连接池大小
    max_overflow=10,            # 允许的额外连接数
    pool_timeout=30,            # 等待连接的超时时间
    pool_recycle=1800,          # 连接回收时间
    pool_pre_ping=True,         # 连接健康检查
    isolation_level='READ COMMITTED'  # 事务隔离级别
)
```

2. **事务隔离级别**

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 性能影响 |
|---------|------|------------|------|---------|
| READ UNCOMMITTED | 可能 | 可能 | 可能 | 最小 |
| READ COMMITTED | 不可能 | 可能 | 可能 | 较小 |
| REPEATABLE READ | 不可能 | 不可能 | 可能 | 中等 |
| SERIALIZABLE | 不可能 | 不可能 | 不可能 | 最大 |

3. **死锁处理**
```python
from sqlalchemy.exc import OperationalError

def execute_with_retry(session, operation, max_retries=3):
    """带有重试机制的数据库操作执行器"""
    for attempt in range(max_retries):
        try:
            result = operation(session)
            session.commit()
            return result
        except OperationalError as e:
            if "deadlock" in str(e) and attempt < max_retries - 1:
                session.rollback()
                continue
            raise
```

4. **连接泄漏防护**
```python
from contextlib import contextmanager
import time

@contextmanager
def timeout_session(timeout_seconds=30):
    """带有超时机制的数据库会话"""
    start_time = time.time()
    session = get_session()
    try:
        yield session
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("数据库操作超时")
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

### 并发性能监控

```python
class DatabaseMetrics:
    """数据库性能指标收集器"""
    def __init__(self):
        self.active_connections = 0
        self.waiting_connections = 0
        self.total_queries = 0
        self.slow_queries = 0
        self.deadlocks = 0
        
    def record_query_time(self, duration):
        self.total_queries += 1
        if duration > 1.0:  # 慢查询阈值：1秒
            self.slow_queries += 1
            
    def record_deadlock(self):
        self.deadlocks += 1
```

1. **连接池配置**
   ```python
   # 生产环境推荐配置
   POOL_SIZE = max(cpu_count() * 2, 20)  # 基于CPU核心数
   MAX_OVERFLOW = POOL_SIZE // 2          # 额外连接数
   POOL_TIMEOUT = 30                      # 等待超时
   POOL_RECYCLE = 3600                    # 定期回收
   ```

## 数据库交互指南

### 1. 基础数据库操作

```python
from database.link import get_session, timeout_session, execute_with_retry
from database.models import User  # 导入需要的模型
from sqlalchemy import text

# 1. 基本查询操作
def get_user_by_id(user_id: int):
    with get_session() as session:
        return session.query(User).filter(User.id == user_id).first()

# 2. 带超时的查询操作
def get_user_with_timeout(user_id: int):
    with timeout_session(timeout_seconds=5) as session:
        return session.query(User).filter(User.id == user_id).first()

# 3. 带重试的数据库操作
def create_user_with_retry(username: str, email: str):
    def _operation(session):
        user = User(username=username, email=email)
        session.add(user)
        return user
    
    with get_session() as session:
        return execute_with_retry(session, _operation)
```

### 2. 使用 CRUD 操作

```python
from database.crud.user_crud import UserCRUD
from database.crud.enterprise_crud import EnterpriseCRUD

# 1. 初始化 CRUD 操作类
user_crud = UserCRUD()
enterprise_crud = EnterpriseCRUD()

# 2. 执行 CRUD 操作
async def handle_user_operations():
    # 创建用户
    new_user = await user_crud.create(
        username="test_user",
        email="test@example.com"
    )
    
    # 查询用户
    user = await user_crud.get(id=1)
    
    # 更新用户
    updated_user = await user_crud.update(
        id=1,
        data={"email": "new@example.com"}
    )
    
    # 删除用户
    await user_crud.delete(id=1)
```

### 3. 事务操作

```python
from database.link import get_session
from sqlalchemy.exc import SQLAlchemyError

def transfer_credits(from_user_id: int, to_user_id: int, amount: float):
    with get_session() as session:
        try:
            # 在同一事务中执行多个操作
            from_user = session.query(User).filter(User.id == from_user_id).first()
            to_user = session.query(User).filter(User.id == to_user_id).first()
            
            from_user.credits -= amount
            to_user.credits += amount
            
            # 事务会在 with 块结束时自动提交
            # 如果发生异常，会自动回滚
        except SQLAlchemyError as e:
            # 记录错误并重新抛出
            logger.error(f"转账操作失败: {str(e)}")
            raise
```

### 4. 性能监控使用

```python
from database.link import db_manager

def monitor_database_performance():
    # 获取数据库性能统计
    stats = db_manager.get_engine_stats()
    
    # 检查连接池状态
    if stats["checkedout"] / stats["pool_size"] > 0.8:
        logger.warning("连接池使用率超过80%")
    
    # 检查慢查询
    if stats["slow_queries"] > 0:
        logger.warning(f"检测到 {stats['slow_queries']} 个慢查询")
    
    # 检查死锁情况
    if stats["deadlocks"] > 0:
        logger.error(f"检测到 {stats['deadlocks']} 次死锁")
```

### 5. 错误处理最佳实践


### 6. 常见使用场景

1. **API 路由中使用**：
```python
from fastapi import APIRouter, Depends
from database.crud.user_crud import UserCRUD

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user_crud = UserCRUD()
    return await user_crud.get(id=user_id)
```

2. **服务层中使用**：
```python
from database.link import get_session
from database.models import User, Enterprise

class UserService:
    def get_user_with_enterprises(self, user_id: int):
        with get_session() as session:
            user = session.query(User)\
                .join(Enterprise)\
                .filter(User.id == user_id)\
                .first()
            return user
```

3. **后台任务中使用**：
```python
from database.link import get_session, timeout_session

async def background_task():
    with timeout_session(timeout_seconds=300) as session:
        # 执行可能耗时的操作
        results = session.execute(
            text("SELECT * FROM heavy_calculation")
        )
        return results.fetchall()
```

### 7. 注意事项

1. **会话管理**：
   - 始终使用 `with` 语句管理会话
   - 对于长时间操作使用 `timeout_session`
   - 不要在不同的请求之间共享会话

2. **错误处理**：
   - 使用适当的异常捕获
   - 记录详细的错误日志
   - 在合适的层级处理异常

3. **性能考虑**：
   - 及时关闭不需要的会话
   - 避免在循环中创建新会话
   - 使用批量操作代替循环单条操作

4. **并发处理**：
   - 使用 `execute_with_retry` 处理死锁
   - 合理设置事务隔离级别
   - 注意连接池的使用情况

---


当然！以下是编写 CRUD 层的最佳实践总结：

## CRUD 层编写指南

### 1. 只负责基本的数据库操作

- **增**：创建新记录并添加到会话
- **查**：查询记录并返回模型实例
- **改**：更新记录的属性
- **删**：标记记录为删除

### 2. 不处理事务（commit/rollback）

- CRUD 方法不应该调用 `commit()` 或 `rollback()`
- 事务管理应在服务层或调用层处理

### 3. 接收会话作为参数

- CRUD 方法应接收 `Session` 对象作为参数
- 由调用者提供会话，确保灵活性

### 4. 返回模型实例

- 返回 ORM 模型实例而不是原始数据
- 允许调用者直接操作返回的对象
