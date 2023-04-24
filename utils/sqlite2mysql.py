# 依赖pymysql还没有写在requments，请注意添加
import sqlite3
import pymysql

# 连接到SQLite3数据库
sqlite_con = sqlite3.connect('../db.sqlite3')

# 连接到MySQL数据库
mysql_con = pymysql.connect(
    host='your_mysql_host',
    user='your_mysql_user',
    password='your_mysql_password',
    database='your_mysql_db',
    charset='utf8mb4',
)

# 创建一个游标对象以执行SQL命令
sqlite_cur = sqlite_con.cursor()
mysql_cur = mysql_con.cursor()

# 查询SQLite3数据库中的所有表
sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = sqlite_cur.fetchall()

# 遍历每个表
for table in tables:
    table_name = table[0]

    # 获取SQLite3表结构
    sqlite_cur.execute(f"PRAGMA table_info({table_name})")
    columns_info = sqlite_cur.fetchall()

    # 创建MySQL表
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in columns_info:
        col_name = column[1]
        col_type = column[2]
        create_table_sql += f"{col_name} {col_type}, "
    create_table_sql = create_table_sql[:-2] + ")"
    mysql_cur.execute(create_table_sql)

    # 查询SQLite3表中的所有数据
    sqlite_cur.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cur.fetchall()

    # 将数据插入到MySQL表中
    for row in rows:
        placeholders = ", ".join(["%s"] * len(row))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        mysql_cur.execute(insert_sql, row)

    # 提交更改并关闭游标
    mysql_con.commit()

# 关闭数据库连接
sqlite_cur.close()
sqlite_con.close()
mysql_cur.close()
mysql_con.close()