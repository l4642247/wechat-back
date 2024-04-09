import mysql.connector

MYSQL_HOST = "121.43.130.247"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Cnm.0001+"
MYSQL_DATABASE = "coding"

def save_user_info(openid):
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    # 创建数据库游标
    cursor = conn.cursor()

    # 插入用户信息到数据库
    insert_query = "INSERT INTO users (openid) VALUES (%s)"
    cursor.execute(insert_query, (openid,))

    # 提交事务
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
