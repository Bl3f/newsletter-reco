import warnings
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
from yato import Transformation


def clean_url(url) -> str:
    """
    Remove utm_* and ref GET param from URL.
    :param url: URL to be cleaned.
    :return: Cleaned URL.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_params = {key: value for key, value in query_params.items() if not key.startswith("utm_") and key != "ref"}
    filtered_query_string = urlencode(filtered_params, doseq=True)
    return urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            filtered_query_string,
            parsed_url.fragment,
        )
    )


class IntEvents(Transformation):
    @staticmethod
    def source_sql():
        return "SELECT * FROM stg_events"

    def run(self, context, *args, **kwargs) -> pd.DataFrame:
        df = self.get_source(context)

        df.loc[:, "link__to"] = df["link__to"].apply(clean_url)

        return df
