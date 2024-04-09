import mysql.connector

MYSQL_HOST = "121.43.130.247"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Cnm.0001+"
MYSQL_DATABASE = "coding"

def save_user_info(openid):
    try:
        # 使用上下文管理器管理数据库连接和游标
        with mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        ) as conn:
            with conn.cursor() as cursor:
                # 插入用户信息到数据库
                insert_query = "INSERT INTO users (openid) VALUES (%s)"
                cursor.execute(insert_query, (openid,))
                # 提交事务
                conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # 在这里添加更多的错误处理逻辑
