from sqlalchemy import text
from database.link import engine

def test_connection():
    try:
        with engine.connect() as connection:
            print("尝试连接到数据库...")
            # 使用 text() 包装查询
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"成功连接到数据库，数据库版本：{version[0]}")
    except Exception as e:
        print(f"数据库连接失败：{e}")
        raise

if __name__ == "__main__":
    test_connection()
