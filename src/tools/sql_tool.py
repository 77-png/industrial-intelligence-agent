import sqlite3


DB_PATH = "data/demo.db"


def sql_query(query: str) -> str:
    """
    Execute a read-only SQL query on the industrial demo database.

    Args:
        query: SQL SELECT query.

    Returns:
        Query result as text.
    """

    # 安全限制：只允许 SELECT
    if not query.strip().lower().startswith("select"):
        return "错误：只允许执行 SELECT 查询。"

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        conn.close()

        if not rows:
            return "查询成功，但没有找到数据。"

        result = []

        # 表头
        result.append(
            " | ".join(columns)
        )

        # 数据
        for row in rows:

            result.append(
                " | ".join(
                    str(value)
                    for value in row
                )
            )

        return "\n".join(result)

    except Exception as e:

        return f"SQL执行失败：{str(e)}"