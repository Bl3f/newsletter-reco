import os

import dlt
from yato import Yato

from ghost import ghost_source, remove_columns

if __name__ == "__main__":
    DATABASE_FILE_NAME = "ghostdb.duckdb"

    yato = Yato(
        database_path="ghostdb.duckdb",
        sql_folder="transform/sql/",
        s3_bucket=os.getenv("S3_BUCKET"),
        s3_access_key=os.getenv("S3_ACCESS_KEY"),
        s3_secret_key=os.getenv("S3_SECRET_KEY"),
        s3_endpoint_url=os.getenv("S3_ENDPOINT"),
        s3_region_name=os.getenv("S3_REGION_NAME"),
    )

    yato.restore(overwrite=True)

    pipeline = dlt.pipeline(
        pipeline_name="ghostdb",
        destination=dlt.destinations.duckdb(credentials=DATABASE_FILE_NAME),
        dataset_name="ghost",
    )

    data = ghost_source()
    data = data.get_activities.add_map(remove_columns)

    load_info = pipeline.run(data)

    print(load_info)

    yato.backup()

    db = yato.run()
