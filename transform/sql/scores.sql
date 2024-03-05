SELECT
    member_id,
    link__to,
    COUNT(DISTINCT clicked_at) * COALESCE(CASE WHEN MAX(feedback_multiplier) == 0 THEN -1 ELSE MAX(feedback_multiplier) * 3 END, 1) AS score,
FROM events
WHERE 1 = 1
    AND is_fake_click IS FALSE
GROUP BY member_id, link__to