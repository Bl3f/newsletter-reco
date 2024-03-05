ATTACH 'host={{ DB_HOST }} port={{ DB_PORT }} dbname={{ DB_NAME }} password={{ DB_PASSWORD }} user={{ DB_USER }}' AS pg_prod (TYPE postgres);

SELECT
    link__to,
    cl.id AS blefapi_link_id,
    MIN(post__id),
    MIN(delivered_at) as first_click
FROM int_events
LEFT JOIN pg_prod.public.ghostapi_ghostlink cl ON link__to = url
GROUP BY link__to, cl.id