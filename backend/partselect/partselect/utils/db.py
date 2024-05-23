# import os

# import psycopg2


# def get_db_conn():
#     return psycopg2.connect(
#         database=os.environ.get("DATABASE_NAME", "partselect"),
#         host=os.environ.get("DATABASE_URI", "localhost"),
#         user=os.environ.get("DATABASE_USER", "partselect"),
#         password=os.environ.get("DATABASE_PASSWORD", "partselect"),
#         port=os.environ.get("DATABASE_PORT", "5432"),
#     )
