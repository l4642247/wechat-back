import mysql.connector
import xmltodict
from datetime import datetime

MYSQL_HOST = "121.43.130.247"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Cnm.0001+"
MYSQL_DATABASE = "coding"

# 连接到数据库的函数
def connect_to_database():
    return  mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

# 保存用户信息    
def save_user_info(openid):
    try:
        # 使用上下文管理器管理数据库连接和游标
        with connect_to_database() as conn:
            with conn.cursor() as cursor:
                # 插入用户信息到数据库
                insert_query = "INSERT INTO users (openid) VALUES (%s)"
                cursor.execute(insert_query, (openid,))
                # 提交事务
                conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # 在这里添加更多的错误处理逻辑

# 将接收到的消息和回复消息记录到数据库中
def log_message(openid, received_msg, reply_msg):
    try:
        # 使用上下文管理器管理数据库连接和游标
        with connect_to_database() as conn:
            with conn.cursor() as cursor:
                # 构建插入消息日志的SQL语句
                sql = """INSERT INTO message_log 
                         (openid, received_message, reply_message, insert_time) 
                         VALUES (%s, %s, %s, %s)"""
                values = (openid, xmltodict.unparse({'xml': received_msg}), 
                          xmltodict.unparse({'xml': reply_msg}), datetime.now())

                # 执行SQL语句
                cursor.execute(sql, values)

                # 提交事务
                conn.commit()

    except mysql.connector.Error as err:
        print(f"Error logging message: {err}")
        # 在这里添加更多的错误处理逻辑