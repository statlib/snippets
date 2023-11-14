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

CREATE OR REPLACE TABLE dummy AS (
    WITH RECURSIVE
        spine AS (
            SELECT
                DATE '2021-01-01' AS statement_date
            UNION ALL
            SELECT
                statement_date + INTERVAL 1 MONTH
            FROM 
                spine
            WHERE
                statement_date < DATE '2023-12-01'            
        ),
        ids AS (
            SELECT
                range + 1 id
            FROM    
                range(46000)
        ),
        cte AS (
            SELECT
                id,
                round(random() / random(), 4) financial_metric,
                IF(round(random() / 1.25) = 1, NULL, statement_date) statement_date            
            FROM
                spine
            CROSS JOIN
                ids
        )
    SELECT
        *
    FROM
        cte
    WHERE
        statement_date IS NOT NULL
);

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

-- COPY dat TO 'data.csv' (HEADER, DELIMITER ',');

-- Q1
SELECT
    id,
    round(sum(financial_metric), 2) total_financial_metric,
    round(avg(financial_metric), 2) avg_financial_metric
FROM
    dummy
GROUP BY
    1
ORDER BY
    1;

-- Q2
SELECT 
    last_day(statement_date) month_end,
    count(id) id_count,
    round(sum(financial_metric), 2) total_financial_metric,
    round(avg(financial_metric), 2) avg_financial_metric
FROM
    dummy
WHERE
    month_end IS NOT NULL
GROUP BY
    1
ORDER BY
    1;

-- Q3

-- 1. Do yourself
-- 2. Correct
-- 3. Extend one of the two


-- Identify which months of data are missing
-- Count ranges exceeding thresh for each ID
-- Months where I > J
-- Top 3 metrics by month
-- What kinds of analysis could you run

SELECT
    COUNT(*)
FROM
    dummy;
