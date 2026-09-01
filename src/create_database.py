import sqlite3


conn = sqlite3.connect("data/demo.db")

cursor = conn.cursor()


# 创建销售表
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    category TEXT,
    sales REAL,
    year INTEGER
)
""")


# 清空旧数据，方便重复运行
cursor.execute("DELETE FROM sales")


# 插入测试数据
data = [
    (1, "工业传感器", "设备", 120000, 2025),
    (2, "工业机器人", "设备", 250000, 2025),
    (3, "边缘网关", "网络", 180000, 2025),
    (4, "工业软件平台", "软件", 320000, 2025),
    (5, "数据采集模块", "设备", 150000, 2025),
    (6, "工业机器人", "设备", 280000, 2026),
    (7, "边缘网关", "网络", 210000, 2026),
    (8, "工业软件平台", "软件", 350000, 2026),
]


cursor.executemany("""
INSERT INTO sales
(id, product, category, sales, year)
VALUES (?, ?, ?, ?, ?)
""", data)


conn.commit()
conn.close()


print("SQLite 数据库创建完成！")