INSERT INTO pg_prod.public.ghostapi_ghostlink BY NAME (
    SELECT link__to AS url, false AS is_excluded, false AS is_matched FROM stg_links WHERE blefapi_link_id IS NULL
);

SELECT 'ok';