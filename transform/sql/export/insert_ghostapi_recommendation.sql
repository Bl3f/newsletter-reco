DELETE FROM pg_prod.public.ghostapi_recommendation
WHERE week_number = (SELECT MAX(week_number) FROM recommendation);

INSERT INTO pg_prod.public.ghostapi_recommendation BY NAME (
    SELECT
        r.member_id AS user_id,
        u.member_uuid AS user_uuid,
        uuid() AS tracking_uuid,
        l.blefapi_link_id AS url_id,
        0 AS nb_click_others,
        week_number,
        NOW() AS created_at,
        NOW() AS updated_at
    FROM recommendation r
    LEFT JOIN stg_links l ON r.reco = l.link__to
    LEFT JOIN stg_members u ON r.member_id = u.member_id
);

SELECT 'ok';