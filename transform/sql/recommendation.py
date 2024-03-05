from datetime import datetime

import numpy as np
import pandas as pd
from yato import Transformation


def recommendation(df):
    member_ids = df.member_id.unique()

    def find_member_id(value):
        return np.where(member_ids == value)[0][0]

    df.member_id = df.member_id.apply(find_member_id)

    user_similarity = df.T.corr()

    results = {}
    for i, member_id in enumerate(member_ids):
        # Make the recommendation for this member
        # Get the similar users
        similar_users = user_similarity[user_similarity[i] == 1][i].sort_values(ascending=False)
        if len(similar_users) < 10:
            threshold = 0.3
            similar_users = user_similarity[user_similarity[i] > threshold][i].sort_values(ascending=False)

        if len(similar_users) < 5:
            continue

        # Get what the user already clicked
        picked_user_clicked = df[df.index == i].dropna(axis=1, how="all").columns[1:]

        # Find the clicks the similar users did
        similar_clicks = (
            df[df.index.isin(similar_users.index)]
            .dropna(axis=1, how="all")
            .drop(picked_user_clicked, axis=1, errors="ignore")
            .iloc[:, 1:]
        )

        # Sort the clicks by percentage of clicked over the similar users
        reco = (similar_clicks.sum() / len(similar_clicks)).sort_values(ascending=False)[:1]
        results[member_id] = reco.index[0]

    output = pd.DataFrame(results.items(), columns=["member_id", "reco"])
    output["week_number"] = datetime.now().strftime("%Y-%W")

    return output


class Recommendation(Transformation):
    @staticmethod
    def source_sql():
        return "SELECT * FROM pivoted_matrix"

    def run(self, context, *args, **kwargs) -> pd.DataFrame:
        df = self.get_source(context)

        return recommendation(df)
