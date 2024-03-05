INSERT INTO pg_prod.public.ghostapi_clickedlinkactivity BY NAME (
    SELECT cla.*, uuid() AS tracking_uuid,
    FROM clicked_link_activity AS cla
    LEFT JOIN pg_prod.public.ghostapi_clickedlinkactivity AS gcla
        ON cla.user_uuid = gcla.user_uuid
        AND cla.url_id = gcla.url_id
    WHERE gcla.url_id IS NULL
);

SELECT 'ok';