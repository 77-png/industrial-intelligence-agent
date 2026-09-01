from tools.sql_tool import sql_query


result = sql_query(
    """
    SELECT product, sales, year
    FROM sales
    WHERE year = 2026
    """
)

print(result)