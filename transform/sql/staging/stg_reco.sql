SELECT user_id AS member_id, ARRAY_AGG(link__to) as already_recommended
FROM pg_prod.public.ghostapi_recommendation
LEFT JOIN stg_links ON blefapi_link_id = url_id
GROUP BY member_id;