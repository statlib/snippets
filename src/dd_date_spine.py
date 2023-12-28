import ibis

con_dd = ibis.duckdb.connect()

# Assumes the existence of a memframe called `df_dates` 
df_spine = con_dd.sql(
    f"""    
    WITH RECURSIVE dates AS (
        SELECT
            DATE '2023-01-01' AS date
        UNION ALL
        SELECT
            date + INTERVAL 1 DAY
        FROM
            dates
        WHERE
            date < DATE '2024-01-01'
    )

    SELECT
        *
    FROM
        dates
    ORDER BY
        date DESC
    """
)
