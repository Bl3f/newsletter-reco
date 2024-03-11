ATTACH 'host={{ DB_HOST }} port={{ DB_PORT }} dbname={{ DB_NAME }} password={{ DB_PASSWORD }} user={{ DB_USER }}' AS pg_prod (TYPE postgres);

SELECT 'ok' ;