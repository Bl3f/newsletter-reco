SELECT
    member_id AS user_id,
    link__to AS item_id,
    LEAST(CAST(score AS INTEGER), 5) AS rating,
FROM scores