import urllib
from datetime import datetime

import dlt
import jwt
from dlt.sources.helpers import requests


@dlt.source
def ghost_source(admin_api_key=dlt.secrets.value):
    return get_activities(admin_api_key)


def _get_jwt_token(admin_api_key):
    id, secret = admin_api_key.split(":")

    # Prepare header and payload
    iat = int(datetime.now().timestamp())

    header = {"alg": "HS256", "typ": "JWT", "kid": id}
    payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/admin/"}

    # Create the token (including decoding secret)
    return jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)


def _create_auth_headers(admin_api_key):
    """Constructs Bearer type authorization header which is the most common authorization method"""
    token = _get_jwt_token(admin_api_key)
    headers = {"Authorization": f"Ghost {token}"}
    return headers


@dlt.resource(table_name="activities", write_disposition="merge", primary_key="id")
def get_activities(
    admin_api_key=dlt.secrets.value,
    created_at=dlt.sources.incremental("$.data.created_at"),
):
    headers = _create_auth_headers(admin_api_key)
    base_url = "https://christopheblefari.ghost.io/ghost/api/admin/members/events"
    types = ["aggregated_click_event"]

    keep_going = True
    cursor = datetime.now()
    limit = 2000

    while keep_going:
        params = {
            "filter": f"data.created_at:<'{cursor.strftime('%Y-%m-%d %H:%M:%S')}'+type:-[{','.join(types)}]",
            "limit": limit,
            # This is not working I don't know why
            # "order": f"created_at ASC",
        }
        url = f"{base_url}/?{urllib.parse.urlencode(params)}"

        print(url)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as er:
            headers = _create_auth_headers(admin_api_key)
            response = requests.get(url, headers=headers)
            response.raise_for_status()

        activities = response.json()["events"]

        for activity in activities:
            activity["id"] = activity["data"]["id"]

            cursor = min(
                [
                    datetime.strptime(
                        activity["data"]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    cursor,
                ]
            )
            yield activity

        if len(activities) < limit or (
            created_at.start_value is not None
            and cursor
            < datetime.strptime(created_at.start_value, "%Y-%m-%dT%H:%M:%S.%fZ")
        ):
            keep_going = False


def remove_columns(doc):
    return {
        "id": doc["id"],
        "type": doc["type"],
        "member_id": (
            doc["data"]["member"].get("id") if "member" in doc["data"] else None
        ),
        "created_at": doc["data"]["created_at"],
        "score": doc["data"]["score"] if "score" in doc else None,
        "post": doc["data"]["post"] if "post" in doc["data"] else None,
        "link": doc["data"]["link"] if "link" in doc["data"] else None,
        "email_post_id": (
            doc["data"]["email"]["post_id"] if "email" in doc["data"] else None
        ),
    }


if __name__ == "__main__":
    # configure the pipeline with your destination details
    pipeline = dlt.pipeline(
        pipeline_name="ghostdb",
        destination="duckdb",
        dataset_name="ghost",
        # loader_file_format="parquet",
    )

    data = ghost_source()
    data = data.get_activities.add_map(remove_columns)

    # run the pipeline with your parameters
    load_info = pipeline.run(data)

    # pretty print the information on data that was loaded
    print(load_info)
