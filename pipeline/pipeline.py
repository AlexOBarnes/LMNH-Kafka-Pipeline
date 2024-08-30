'''Parses arguments and calls the extract function'''
import argparse
import logging
from datetime import datetime as dt
from extract import extract

def parse_arguments() -> None:
    '''Parses CL arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l", action='store_true')
    args = parser.parse_args()

    log = args.log
    if log:
        config_log()
    else:
        logging.basicConfig(level=logging.INFO)

def config_log() -> None:
    '''Configures the log'''
    date = get_date()
    logging.basicConfig(filename=f'pipeline_{date}_log.txt',\
                         encoding='UTF-8', level=logging.WARNING)

def get_date() -> str:
    '''Returns the current date'''
    return dt.now().strftime('%d-%m-%Y_%H:%M:%S')

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parse_arguments()
    extract(logger)
