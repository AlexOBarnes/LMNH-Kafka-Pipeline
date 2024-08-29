'''Contains fixtures for test_pipeline.py'''
#pylint: skip-file
import pytest

@pytest.fixture
def valid_date():
    '''Returns a date that is valid'''
    return "2024-08-28T11:54:41.460887+01:00"

@pytest.fixture
def invalid_date_1():
    '''Returns a date in the wrong format'''
    return '2024-08-28'

@pytest.fixture
def invalid_date_2():
    '''Returns a date that is too late for entry'''
    return "2024-08-28T20:54:41.460887+01:00"

@pytest.fixture
def invalid_date_3():
    '''Date that is too early for entry'''
    return "2024-08-28T7:54:41.460887+01:00"

@pytest.fixture
def valid_keys():
    '''A correctly formatted data entry'''
    return {'at':1,'site':0,'val':0}

@pytest.fixture
def invalid_keys_1():
    '''Returns a dictionary missing one of the keys'''
    return {'at': 1, 'site': 0}

@pytest.fixture
def invalid_keys_2():
    '''Returns an empty dictionary'''
    return {}

@pytest.fixture
def valid_value():
    '''Returns a valid ratings entry'''
    return {'at': 1,'site':0,'val':3}

@pytest.fixture
def valid_value_2():
    '''Returns a valid entry'''
    return {'at': 1, 'site':0,'val':-1,'type':1}

@pytest.fixture
def invalid_value_1():
    '''Returns a null value in the value column'''
    return {'at': 1, 'site': 0,'val':None}

@pytest.fixture
def invalid_value_2():
    '''Returns an invalid value string'''
    return {'at': 1, 'site': 0, 'val': "1"}

@pytest.fixture
def invalid_value_3():
    '''Returns an invalid value out of range'''
    return {'at': 1, 'site': 0, 'val': 7}
