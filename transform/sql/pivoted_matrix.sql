WITH pivoted AS (
    PIVOT scores
    ON link__to
    USING SUM(score)
    GROUP BY member_id
)

SELECT p.*, r.already_recommended
FROM pivoted p
LEFT JOIN stg_reco r USING(member_id)

