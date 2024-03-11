SELECT user_id AS member_id, ARRAY_AGG(url_id) as already_recommended
FROM pg_prod.public.ghostapi_recommendation
GROUP BY member_id;