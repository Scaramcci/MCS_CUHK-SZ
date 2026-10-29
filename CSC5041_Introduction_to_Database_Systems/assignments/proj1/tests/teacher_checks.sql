\set ON_ERROR_STOP on
\pset pager off
SET statement_timeout = '120s';
\timing on
CREATE TEMP TABLE actual_checks AS SELECT * FROM check_all();
TABLE actual_checks;
SELECT 1 / CASE WHEN count(*) = 10 AND bool_and(result = 'correct')
                THEN 1 ELSE 0 END AS all_ten_checks_passed
FROM actual_checks;

-- Retrieve each full result, not just an optimizable COUNT(*), for timing.
SELECT * FROM Q1;
SELECT * FROM Q2;
SELECT * FROM Q3;
SELECT * FROM Q4;
SELECT * FROM Q5;
SELECT * FROM Q6;
SELECT * FROM Q7;
SELECT * FROM Q8;
SELECT * FROM Q9;
SELECT * FROM Q10;

SELECT c.relname AS view_name, a.attnum AS column_number, a.attname,
       format_type(a.atttypid, a.atttypmod) AS column_type
FROM pg_class AS c
JOIN pg_namespace AS n ON n.oid = c.relnamespace
JOIN pg_attribute AS a ON a.attrelid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'v'
  AND c.relname ~ '^q([1-9]|10)$' AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY substring(c.relname FROM 2)::integer, a.attnum;
