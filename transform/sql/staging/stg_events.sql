WITH delivered_events AS (
    SELECT
        member_id,
        created_at,
        email_post_id,
    FROM ghost.activities
    WHERE
        type = 'email_delivered_event'
        AND member_id IS NOT NULL
),

opened_events AS (
    SELECT
        member_id,
        created_at,
        email_post_id,
    FROM ghost.activities
    WHERE
        type = 'email_opened_event'
        AND member_id IS NOT NULL
),

feedback_events AS (
    SELECT
        member_id,
        created_at,
        post__id,
        score,
    FROM ghost.activities
    WHERE
        type = 'feedback_event'
        AND member_id IS NOT NULL
),

delays AS (
    SELECT
        id,
        a.member_id,
        de.created_at AS delivered_at,
        oe.created_at AS opened_at,
        a.created_at AS clicked_at,
        oe.created_at - de.created_at AS delay_delivered_opened,
        a.created_at - de.created_at AS delay_delivered_clicked,
        a.created_at - oe.created_at AS delay_opened_clicked,
        (opened_at is not null AND delay_opened_clicked <= '00:00:00') OR (delay_delivered_clicked <= '00:00:05') AS is_fake_click,
        fe.score AS feedback_multiplier,
        a.post__id,
        a.link__to,
    FROM ghost.activities a
    LEFT JOIN delivered_events de ON a.post__id = de.email_post_id AND a.member_id = de.member_id
    LEFT JOIN opened_events oe ON a.post__id = oe.email_post_id AND a.member_id = oe.member_id
    LEFT JOIN feedback_events fe ON a.post__id = fe.post__id AND a.member_id = fe.member_id
    WHERE
        a.type = 'click_event'
        AND NOT CONTAINS(link__to, 'https://www.blef.fr')
        AND NOT CONTAINS(link__to, 'unsplash.com')
        AND NOT CONTAINS(link__to, 'mailto:')
)

SELECT *
FROM delays
