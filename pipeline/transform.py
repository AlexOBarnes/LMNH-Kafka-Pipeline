'''Contains functions used for transforming the LMNH data'''
from datetime import datetime as dt

MISSING_KEY_ERROR = " No '{}' key."

def check_valid_site(site: str) -> str:
    '''Checks if the site is valid'''
    if site:
        if not site.isnumeric():
            return "'Site' value is not numeric"
        if int(site) > 5 or int(site) < 0:
            return "Invalid site value; must be between 0 and 6"
    return ""

def check_invalid_type(type_value: int) -> bool:
    '''Returns true if the type is invalid'''
    if type_value is None:
        return True

    if not isinstance(type_value,int):
        return True

    if type_value > 1 or type_value < 0:
        return True

    return False


def check_valid_value(data: dict) -> str:
    '''Checks if the given value is valid'''
    value = data.get("val",0)

    if value is None:
        return "Value column is not an integer"

    if value:
        if not isinstance(value,int):
            return "Value column is not an integer"
        if value > 4 or value < -1:
            return "Value is outside accepted range"

        if value == -1:
            is_invalid_type = check_invalid_type(data.get("type"))
            if is_invalid_type:
                return "Invalid type; must be either 1 or 0"
    return ""

def check_valid_date(entry_timestamp: dt.date) -> str:
    '''Checks if the data is in the correct format'''
    if entry_timestamp:
        try:
            time = dt.strptime(entry_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z").time()
        except ValueError as err:
            return f" {err} for 'at' data"

        opening_time = dt.strptime("08:45:00", "%H:%M:%S").time()
        closing_time = dt.strptime("18:15:00", "%H:%M:%S").time()
        if time < opening_time or time > closing_time:
            return " The entered time is outside of working hours."
    return ""

def check_valid_keys(data: dict,error_msg: str) -> str:
    '''Checks if all necessary keys are present'''
    for key in ['at', 'site', 'val']:
        if not key in data.keys():
            error_msg += MISSING_KEY_ERROR.format(key)
    return error_msg

def transform(data: dict) -> dict:
    '''Converts data for the lmnh schema'''
    if data.get("type") or data.get("type") == 0:
        return {"request":[data["at"], int(data['site'])+1, int(data["type"])+1]}

    return {"rating":[data["at"], int(data['site'])+1, int(data["val"])+1]}
