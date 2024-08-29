'''Tests for pipeline python scripts'''
#pylint: skip-file
from datetime import datetime as dt
from unittest.mock import patch,MagicMock
import pytest
from extract import get_consumer,check_data
from pipeline import get_date,config_log,parse_arguments
from load import insert_request, load_data, insert_review
from transform import check_valid_date, check_valid_keys,\
                      check_valid_site, check_valid_value, check_invalid_type,transform

class TestCheckValidDate:
    '''Tests for the check valid date function'''

    def test_valid_input(self,valid_date):
        '''Asserts that valid dates return an empty string'''
        assert check_valid_date(valid_date) == ""

    def test_invalid_date(self,invalid_date_1,invalid_date_2,invalid_date_3):
        '''Asserts that depending on error an appropriate error is returned'''
        assert 'at' in check_valid_date(invalid_date_1)
        assert check_valid_date(invalid_date_2) == " The entered time is outside of working hours."
        assert check_valid_date(invalid_date_3) == " The entered time is outside of working hours."

class TestCheckValidKeys:
    '''Tests for the check valid keys function '''

    def test_valid_input(self,valid_keys):
        '''Tests that valid inputs return nothing'''
        assert not check_valid_keys(valid_keys,"")

    def test_invalid_input(self,invalid_keys_1,invalid_keys_2):
        '''Checks that invalid inputs return error messages'''
        assert 'val' in check_valid_keys(invalid_keys_1," ")
        assert all(key in check_valid_keys(invalid_keys_2, " ")for key in ('at', 'site', 'val'))

class TestCheckValidSite:
    '''Tests for the check valid site funciton'''

    def test_valid_input(self):
        '''Checks that a valid input is accepted'''
        assert not check_valid_site("1")

    def test_invalid_input(self):
        '''Checks that an invalid input returns an error msg'''
        assert check_valid_site("10")


class TestCheckValidValue:
    '''Tests for the check valid value function'''

    def test_valid_input(self, valid_value):
        '''Tests that valid inputs are accepted'''
        assert check_valid_value(valid_value) == ''

    @patch('transform.check_invalid_type')
    def test_valid_input_negative(self,mock_check, valid_value_2):
        '''Asserts negative numbers are accepted'''
        mock_check.return_value = False
        assert check_valid_value(valid_value_2) == ''

    def test_invalid_input(self, invalid_value_1, invalid_value_2, invalid_value_3):
        '''Checks that invalid values return the correct error'''
        assert check_valid_value(invalid_value_1) == "Value column is not an integer"
        assert check_valid_value(invalid_value_2) == "Value column is not an integer"
        assert check_valid_value(invalid_value_3) == "Value is outside accepted range"

class TestCheckInvalidType:
    '''Tests the invalid type function'''

    def test_valid_input(self):
        '''Checks valid inputs return False'''
        assert not check_invalid_type(1)
        assert not check_invalid_type(0)

    def test_invalid_input(self):
        '''Checks that invalid inputs return True'''
        assert check_invalid_type(None)
        assert check_invalid_type("1")
        assert check_invalid_type(3)

class TestTransform:
    '''Tests for the transform function'''

    def test_valid_input(self, valid_keys):
        '''Tests that data is returned correctly'''
        assert transform(valid_keys) == {"rating":[1,1,1]}

    def test_invalid_input(self, valid_value_2):
        '''Tests that data is returned correctly'''
        assert transform(valid_value_2) == {"request":[1,1,2]}

class TestPipeline:
    '''Tests for pipeline.py functions'''

    def test_valid(self):
        '''Tests that the data is returned in the valid format'''
        assert isinstance(get_date(),str)
        assert dt.strptime(get_date(),'%d-%m-%Y_%H:%M:%S')

    @patch('pipeline.logging.basicConfig')
    def test_config(self,mock_config):
        '''Tests that config function is called appropriately'''
        config_log()
        assert mock_config.called

    @patch('pipeline.logging.basicConfig')
    def test_basic_config(self,mock_config):
        '''Tests that config function is called appropriately'''
        parse_arguments()
        assert mock_config.called

class TestLoad:
    '''Tests that check the load function'''

    @patch('load.insert_review')
    def test_rating(self, mock_insert):
        '''Tests that the correct function is called'''
        load_data({"rating": [1, 1, 1]},"")
        assert mock_insert.called

    @patch('load.insert_request')
    def test_request(self, mock_insert):
        '''Tests that the correct function is called'''
        load_data({"request": [1, 1, 1]}, "")
        assert mock_insert.called

    def test_invalid(self):
        '''Tests that when data is not valid an error is raised'''
        with pytest.raises(KeyError):
            load_data({"fake": [1, 1, 1]}, "")

class TestInsert:
    '''Tests to check the insertion functions '''

    @patch('load.connect')
    def test_insert_review(self, mock_connect):
        '''Tests that when the function is called a psycopg2 connection is established'''
        mock_connect.cursor.fetchall.return_value = [1]
        assert isinstance(insert_review([1]), MagicMock)

    @patch('load.connect')
    def test_insert_request(self, mock_connect):
        '''Tests that when the function is called a psycopg2 connection is established'''
        mock_connect.cursor.fetchall.return_value = [1]
        assert isinstance(insert_request([1]), MagicMock)

class TestExtract:
    '''Tests functions within the extract.py file'''

    @patch('extract.Consumer')
    def test_consumer_made(self,mock_consumer):
        '''Checks that a consumer is made upon calling this function'''
        get_consumer()
        assert mock_consumer.called

    @patch('extract.check_valid_value')
    @patch('extract.check_valid_site')
    @patch('extract.check_valid_keys')
    @patch('extract.check_valid_date')
    def test_check_data(self,mock_1,mock_2,mock_3,mock_4):
        '''Tests that all data checks were performed.'''
        mock_1.return_value = ""
        mock_2.return_value = ""
        mock_3.return_value = ""
        mock_4.return_value = ""
        assert check_data({" ":[]}) == ""
        assert mock_1.called
        assert mock_2.called
        assert mock_3.called
        assert mock_4.called
