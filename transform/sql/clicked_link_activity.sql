SELECT
    u.member_uuid AS user_uuid,
    l.blefapi_link_id AS url_id,
    COUNT() AS nb_clicks_emails,
    0 AS nb_click_others,
    MIN(clicked_at) AS clicked_at
FROM events e
LEFT JOIN stg_links l ON l.link__to = e.link__to
LEFT JOIN stg_members u ON e.member_id = u.member_id
WHERE l.blefapi_link_id IS NOT NULL
GROUP BY u.member_uuid, l.blefapi_link_id;
