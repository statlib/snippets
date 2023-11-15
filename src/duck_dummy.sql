/*
    1. Subtly wrong
    2. Provide dataset

    Example query with a mistake in it
    Extend to do a next task
    Open source data set  

    1. Do yourself
    2. Correct
    3. Extend one of the two

    Learned recently
    Want to learn
*/

SELECT
    setseed(123);

CREATE OR REPLACE TABLE dummy AS (
    WITH RECURSIVE
        spine AS (
            SELECT
                DATE '2022-01-01' AS statement_date,
                random() / random() AS financial_metric
            UNION ALL
            SELECT
                statement_date + INTERVAL 1 MONTH,
                financial_metric + .25 * random()
            FROM 
                spine
            WHERE
                statement_date < DATE '2023-12-01'            
        ),
        ids AS (
            SELECT
                range + 1 id
            FROM    
                range(50000)
        ),
        flags AS (
            SELECT
                id,
                statement_date,
                financial_metric,
                round(random() / 1.25) = 1 flag_null,
                MONTH(statement_date) IN (3, 6, 9, 12) flag_season
            FROM
                spine
            CROSS JOIN
                ids
        ),
        cte AS (
            SELECT
                id,
                IF(flag_null, NULL, statement_date) statement_date,
                IF(flag_season, financial_metric * 2.5, financial_metric) financial_metric
            FROM
                flags
        ),
        final AS (
            SELECT
                *
            FROM
                cte 
            WHERE
                statement_date IS NOT NULL
        )
    SELECT 
        *
    FROM
        final
    ORDER BY
        id,
        statement_date
);

SELECT * FROM dummy;

CREATE OR REPLACE VIEW grid AS (
    SELECT DISTINCT
        id,
        month_end
    FROM (
        SELECT DISTINCT
            last_day(statement_date) month_end
        FROM
            dummy
        WHERE
            statement_date IS NOT NULL
    ) dates
    CROSS JOIN (
        SELECT DISTINCT
            id
        FROM
            dummy
    ) ids  
    ORDER BY
        id,
        month_end
);

CREATE OR REPLACE VIEW final AS (
    WITH cte AS (
        SELECT
            d.id,
            d.financial_metric,
            g.month_end,
            d.statement_date,
            row_number() OVER (
                PARTITION BY
                    d.id,
                    g.month_end
                ORDER BY
                    d.statement_date DESC
            ) n
        FROM    
            grid g
        LEFT JOIN
            dummy d
        ON  
            g.id = d.id
        AND 
            d.statement_date <= g.month_end
        ORDER BY
            d.id,
            g.month_end,
            n
    )
    SELECT
        * EXCLUDE (n)
    FROM
        cte
    WHERE   
        n = 1
);

COPY dummy TO 'interview_task_data.csv.gz' (
        HEADER, 
        COMPRESSION 'gzip',
        DELIMITER ','
);
