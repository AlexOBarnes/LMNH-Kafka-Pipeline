'''Uses psycopg2 to load data to a database'''
#pylint: disable=import-error
from os import environ as ENV
import logging
from dotenv import load_dotenv
from psycopg2 import extras, connect


def insert_review(review_data: list) -> list:
    '''Inserts the review data into a given database'''
    query = """INSERT INTO rating_interaction
                (created_at,exhibition_id,rating_id)
                 VALUES (%s,%s,%s)
                 RETURNING *"""

    with connect(f"""dbname={ENV["DATABASE"]} user={ENV["USER1"]}
                 host={ENV["HOST"]} password={ENV["PASSWORD1"]} port={ENV["PORT"]}""") as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, review_data)
            inserted_data = cur.fetchall()
            conn.commit()

    return inserted_data


def insert_request(request_data: list) -> list:
    '''Inserts the request data into a given database'''
    query = """INSERT INTO request_interaction
                (created_at,exhibition_id,request_id)
                 VALUES (%s,%s,%s)
                 RETURNING *"""

    with connect(f"""dbname={ENV["DATABASE"]} user={ENV["USER1"]}
                host={ENV["HOST"]} password={ENV["PASSWORD1"]} port={ENV["PORT"]}""") as conn:
        with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
            cur.execute(query, request_data)
            inserted_data = cur.fetchall()

    return inserted_data

def load_data(data: dict, log: logging.Logger) -> None:
    '''Calls the appropriate load function'''
    load_dotenv()
    returned_data = []

    if data.get("request"):
        returned_data = insert_request(data["request"])
    else:
        returned_data = insert_review(data["rating"])

    if returned_data:
        logging.info("Inserted %s successfully!",returned_data)
    else:
        logging.warning("Failed to insert data, no data returned.")
