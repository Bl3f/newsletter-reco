SELECT DISTINCT member_id, member_uuid
FROM ghost.activities
WHERE member_id IS NOT NULL and member_uuid IS NOT NULL