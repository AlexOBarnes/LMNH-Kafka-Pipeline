'''Extracts data from a kafka cluster before sending it to be transformed and loaded'''
import json
import logging
from os import environ as ENV
from dotenv import load_dotenv
from confluent_kafka import Consumer
from transform import check_valid_keys, check_valid_date, check_valid_site,\
                      check_valid_value,transform
from load import load_data


def check_data(data: dict) -> str:
    '''Checks whether data is in the right format
    Returns a string containing info for each invalid field'''
    error_msg = ""
    error_msg += check_valid_keys(data,error_msg)
    error_msg += check_valid_date(data.get("at"))
    error_msg += check_valid_site(data.get("site"))
    error_msg += check_valid_value(data)
    return error_msg

def consume_data(con: Consumer, logger: logging.Logger) -> None:
    '''A loop that consumes data from a kafka cluster'''
    try:
        while True:
            msg = con.poll(timeout=1.0)

            if msg:
                if msg.error():
                    logging.warning("Error: %s",msg.error().str())
                else:
                    logging.info("Consumed event from %s: key= %s, value= %s", ENV["TOPIC"],
                                str(msg.key())[1:], str(msg.value())[1:])
                    error_msg = check_data(json.loads(msg.value().decode()))
                    if error_msg:
                        logging.warning(error_msg)
                    else:
                        clean_data = transform(json.loads(msg.value().decode()))
                        load_data(clean_data,logger)
    except KeyboardInterrupt:
        pass
    finally:
        con.close()

def get_consumer() -> Consumer:
    '''Configures the confluent_kafka consumer'''
    kafka_config = {
        'bootstrap.servers': ENV["BOOTSTRAP_SERVERS"],
        'security.protocol': ENV["SECURITY_PROTOCOL"],
        'sasl.mechanisms': ENV["SASL_MECHANISM"],
        'sasl.username': ENV["USERNAME"],
        'sasl.password': ENV["PASSWORD"],
        'group.id': ENV["GROUPID"],
        'auto.offset.reset': 'earliest'
    }
    return Consumer(kafka_config)

def extract(log: logging.Logger) -> None:
    '''Extracts data from given kafka cluster and topic'''
    load_dotenv()
    con = get_consumer()
    con.subscribe([ENV["TOPIC"]])
    consume_data(con,log)

if __name__ == "__main__":
    logs = logging.getLogger(__name__)
    consumer = get_consumer()
    consumer.subscribe([ENV["TOPIC"]])
    consume_data(consumer,logs)
