"""
UserService 直接测试模块
直接测试数据库 CRUD 操作

运行测试命令:
    所有测试: pytest test_user_direct.py -v
    单个测试: pytest test_user_direct.py::test_user_crud -v
    覆盖率报告: pytest test_user_direct.py --cov=backend.services.user_service -v
"""

import pytest
import uuid
from backend.services.user_service import UserService
from datetime import datetime

pytestmark = pytest.mark.asyncio

@pytest.fixture(autouse=True)
async def cleanup_test_data():
    """清理测试数据的fixture"""
    yield  # 等待测试完成
    # 清理所有测试用户数据
    users = await UserService.get_users(skip=0, limit=1000)
    for user in users:
        try:
            username = await UserService.get_user_field(user['user_id'], "username")
            if username and username.startswith(("testuser_", "updated_user_", "another_user_")):
                await UserService.delete_user(user['user_id'])
        except Exception as e:
            print(f"清理用户时出错: {e}")

@pytest.mark.asyncio
async def test_user_crud():
    """测试用户 CRUD 操作"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password_hash": "hashed_password123",
        "role": "user"
    }
    
    # 1. 创建用户
    user_id = await UserService.create_user(user_data)
    assert user_id is not None
    
    # 2. 获取用户信息
    user = await UserService.get_user(user_id)
    assert user is not None
    assert user['username'] == user_data["username"]
    
    # 3. 更新用户
    update_data = {
        "username": f"updated_user_{unique_id}",
        "role": "admin"
    }
    success = await UserService.update_user(user_id, update_data)
    assert success is True
    
    # 获取更新后的用户信息
    updated_user = await UserService.get_user(user_id)
    assert updated_user is not None
    assert updated_user['username'] == update_data["username"]
    assert updated_user['role'] == "admin"
    
    # 4. 删除用户
    delete_result = await UserService.delete_user(user_id)
    assert delete_result is True
    
    # 验证删除
    deleted_user = await UserService.get_user(user_id)
    assert deleted_user is None

@pytest.mark.asyncio
async def test_user_list():
    """测试用户列表操作"""
    # First, ensure we start with a clean slate
    existing_users = await UserService.get_users(skip=0, limit=1000)
    for user in existing_users:
        # Access the user_id as an attribute instead of dictionary key
        user_id = user['user_id']
        await UserService.delete_user(user_id)
    
    test_user_ids = []
    
    # Create exactly 5 test users
    for i in range(5):
        unique_id = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"testuser_{unique_id}_{i}",
            "email": f"test_{unique_id}_{i}@example.com",
            "password_hash": f"hash{i}",
            "role": "user"
        }
        user_id = await UserService.create_user(user_data)
        assert user_id is not None
        test_user_ids.append(user_id)
    
    try:
        # Now we know exactly how many users exist
        users_page1 = await UserService.get_users(skip=0, limit=3)
        assert len(users_page1) == 3
        
        users_page2 = await UserService.get_users(skip=3, limit=3)
        assert len(users_page2) == 2  # Should now pass as we have exactly 5 users
    finally:
        # Clean up
        for user_id in test_user_ids:
            await UserService.delete_user(user_id)

@pytest.mark.asyncio
async def test_duplicate_email():
    """测试重复邮箱处理"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password_hash": "hashed_password123",
        "role": "user"
    }
    
    # 创建第一个用户
    first_user_id = await UserService.create_user(user_data)
    assert first_user_id is not None
    
    try:
        # 尝试创建具有相同邮箱的第二个用户
        duplicate_data = user_data.copy()
        duplicate_data["username"] = f"another_user_{unique_id}"
        second_user_id = await UserService.create_user(duplicate_data)
        assert second_user_id is None  # 应该返回 None 表示创建失败
    finally:
        # 清理测试数据
        await UserService.delete_user(first_user_id)

@pytest.mark.asyncio
async def test_soft_delete_and_restore():
    """测试用户软删除和恢复功能"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password_hash": "hashed_password123",
        "role": "user"
    }
    
    # 创建用户
    user_id = await UserService.create_user(user_data)
    assert user_id is not None
    
    # 软删除用户
    success = await UserService.update_user(user_id, {"is_active": False})
    assert success is True
    
    # 验证用户被软删除
    user = await UserService.get_user(user_id)
    assert user is not None
    assert user['is_active'] is False
    
    # 恢复用户
    success = await UserService.update_user(user_id, {"is_active": True})
    assert success is True
    
    # 验证用户被恢复
    user = await UserService.get_user(user_id)
    assert user is not None
    assert user['is_active'] is True
    
    # 清理测试数据
    await UserService.delete_user(user_id)

@pytest.mark.asyncio
async def test_last_login_update():
    """测试更新最后登录时间"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password_hash": "hashed_password123",
        "role": "user"
    }
    
    # 创建用户
    user_id = await UserService.create_user(user_data)
    assert user_id is not None
    
    # 更新最后登录时间
    update_data = {"last_login": datetime.utcnow()}
    success = await UserService.update_user(user_id, update_data)
    assert success is True
    
    # 验证最后登录时间已更新
    user = await UserService.get_user(user_id)
    assert user is not None
    assert user['last_login'] is not None
    
    # 清理测试数据
    await UserService.delete_user(user_id)
