from datetime import datetime

import pandas as pd

from transform.sql.recommendation import recommendation


def test_recommendation():
    df = pd.DataFrame(
        [
            {
                "member_id": 1,
                "item_1": None,
                "item_2": None,
                "item_3": 1,
                "item_4": 1,
                "item_5": 1,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 2,
                "item_1": None,
                "item_2": None,
                "item_3": 1,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 3,
                "item_1": 1,
                "item_2": None,
                "item_3": 1,
                "item_4": None,
                "item_5": 1,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 4,
                "item_1": 1,
                "item_2": 1,
                "item_3": None,
                "item_4": 1,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 5,
                "item_1": None,
                "item_2": 1,
                "item_3": None,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 6,
                "item_1": None,
                "item_2": 1,
                "item_3": None,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 7,
                "item_1": 1,
                "item_2": None,
                "item_3": None,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 8,
                "item_1": None,
                "item_2": None,
                "item_3": None,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 9,
                "item_1": 1,
                "item_2": 1,
                "item_3": None,
                "item_4": None,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
            {
                "member_id": 10,
                "item_1": None,
                "item_2": None,
                "item_3": None,
                "item_4": 1,
                "item_5": None,
                "already_recommended": ["item_3"],
            },
        ]
    )

    result = recommendation(df)
    expected = pd.DataFrame(
        {
            "member_id": [4, 9],
            "reco": ["item_5", "item_4"],
            "week_number": datetime.now().strftime("%Y-%W"),
        }
    )

    pd.testing.assert_frame_equal(result, expected)
