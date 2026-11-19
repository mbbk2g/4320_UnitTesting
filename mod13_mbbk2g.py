import unittest
from datetime import datetime
import re
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import get_user_input, get_valid_date


class TestStockVisualizerInputs(unittest.TestCase):
    #Unit tests for the five inputs from the stock visualizer challenge.

    # ==================== SYMBOL TESTS ====================

    def test_symbol_is_capitalized(self):
        #Test that the symbol is converted to uppercase.
        # Simulate user input: lowercase symbol
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertEqual(symbol, 'AAPL', "Symbol should be capitalized")

    def test_symbol_length_1_to_7(self):
        #Test that the symbol is between 1 and 7 characters.
        # Test valid length
        with unittest.mock.patch('builtins.input', side_effect=['AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertTrue(1 <= len(symbol) <= 7, "Symbol length should be 1-7 characters")

        # Test too short (empty)
        with unittest.mock.patch('builtins.input', side_effect=['', 'AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertEqual(symbol, 'AAPL')

        # Test too long (8 characters)
        with unittest.mock.patch('builtins.input', side_effect=['LONGSYMB', 'AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertEqual(symbol, 'AAPL')

    def test_symbol_is_alphabetic(self):
        #Test that the symbol contains only alphabetic characters.
        # Test valid alphabetic symbol
        with unittest.mock.patch('builtins.input', side_effect=['AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertTrue(symbol.isalpha(), "Symbol should contain only alphabetic characters")

        # Test invalid symbol with numbers
        with unittest.mock.patch('builtins.input', side_effect=['A1PL', 'AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertEqual(symbol, 'AAPL')

    def test_symbol_is_not_empty(self):
        #Test that the symbol is not empty.
        with unittest.mock.patch('builtins.input', side_effect=['', 'AAPL', '\n']):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertTrue(len(symbol) > 0, "Symbol should not be empty")

    # ==================== CHART TYPE TESTS ====================

    def test_chart_type_is_numeric(self):
        #Test that the chart type is a numeric character.
        # Test valid numeric input
        with unittest.mock.patch('builtins.input', side_effect=['1', '\n']):
            _, chart_type, _, _, _, _ = get_user_input()
            self.assertTrue(chart_type.isdigit(), "Chart type should be numeric")

    def test_chart_type_is_1_or_2(self):
        #Test that the chart type is either 1 or 2.
        # Test valid choice 1
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '\n']):
            _, chart_type, _, _, _, _ = get_user_input()
            self.assertEqual(chart_type, '1', "Chart type should be 1 or 2")

        # Test valid choice 2
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '2', '\n']):
            _, chart_type, _, _, _, _ = get_user_input()
            self.assertEqual(chart_type, '2', "Chart type should be 1 or 2")

        # Test invalid choice
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '3', '1', '\n']):
            _, chart_type, _, _, _, _ = get_user_input()
            self.assertEqual(chart_type, '1', "Invalid chart type should be rejected")

    # ==================== TIME SERIES TESTS ====================

    def test_time_series_is_numeric(self):
        #Test that the time series choice is a numeric character.
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '\n']):
            _, _, function, _, _, _ = get_user_input()
            self.assertTrue(function.isdigit(), "Time series should be numeric")

    def test_time_series_is_1_to_4(self):
        #Test that the time series choice is between 1 and 4.
        # Test valid choice 1
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '1', '\n']):
            _, _, function, _, _, _ = get_user_input()
            self.assertEqual(function, '1', "Time series should be 1-4")

        # Test valid choice 4
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '4', '\n']):
            _, _, function, _, _, _ = get_user_input()
            self.assertEqual(function, '4', "Time series should be 1-4")

        # Test invalid choice
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '5', '2', '\n']):
            _, _, function, _, _, _ = get_user_input()
            self.assertEqual(function, '2', "Invalid time series should be rejected")

    # ==================== START DATE TESTS ====================

    def test_start_date_format(self):
        #Test that the start date is in YYYY-MM-DD format.
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '2023-01-01', '\n']):
            _, _, _, start_date, _, _ = get_user_input()
            # Verify the date can be parsed
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                self.assertTrue(True, "Start date should be in YYYY-MM-DD format")
            except ValueError:
                self.fail("Start date format is invalid")

    def test_start_date_is_valid_date(self):
        #Test that the start date is a valid date.
        # Test invalid date format
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '01-01-2023', '2023-01-01', '\n']):
            _, _, _, start_date, _, _ = get_user_input()
            self.assertEqual(start_date, '2023-01-01', "Invalid date format should be rejected")

        # Test invalid date (February 30)
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '2023-02-30', '2023-01-01', '\n']):
            _, _, _, start_date, _, _ = get_user_input()
            self.assertEqual(start_date, '2023-01-01', "Invalid date should be rejected")

    # ==================== END DATE TESTS ====================

    def test_end_date_format(self):
        #Test that the end date is in YYYY-MM-DD format.
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '2023-01-01', '2023-12-31', '\n']):
            _, _, _, _, end_date, _ = get_user_input()
            # Verify the date can be parsed
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
                self.assertTrue(True, "End date should be in YYYY-MM-DD format")
            except ValueError:
                self.fail("End date format is invalid")

    def test_end_date_is_valid_date(self):
        #Test that the end date is a valid date.
        # Test invalid date format
        with unittest.mock.patch('builtins.input', side_effect=['aapl', '1', '2', '2023-01-01', '31-12-2023', '2023-12-31', '\n']):
            _, _, _, _, end_date, _ = get_user_input()
            self.assertEqual(end_date, '2023-12-31', "Invalid date format should be rejected")

    def test_end_date_not_before_start_date(self):
        #Test that the end date is not before the start date.
        # Test end date before start date
        with unittest.mock.patch('builtins.input', side_effect=[
            'aapl', '1', '2', '2023-06-01', '2023-01-01', '2023-12-31', '\n'
        ]):
            _, _, _, start_date, end_date, _ = get_user_input()
            self.assertGreaterEqual(end_date, start_date, "End date should not be before start date")

    # ==================== COMBINED INPUT TESTS ====================

    def test_complete_valid_input(self):
        #Test a complete set of valid inputs.
        inputs = [
            'aapl',      # symbol
            '1',         # chart type (Bar)
            '2',         # time series (Daily)
            '2023-01-01', # start date
            '2023-12-31'  # end date
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            symbol, chart_type, function, start_date, end_date, interval = get_user_input()
            
            self.assertEqual(symbol, 'AAPL')
            self.assertEqual(chart_type, '1')
            self.assertEqual(function, '2')
            self.assertEqual(start_date, '2023-01-01')
            self.assertEqual(end_date, '2023-12-31')
            self.assertIsNone(interval)  # No interval for non-intraday

    def test_complete_valid_intraday_input(self):
        #Test a complete set of valid inputs including intraday interval.
        inputs = [
            'tsla',      # symbol
            '2',         # chart type (Line)
            '1',         # time series (Intraday)
            '2',         # interval (5min)
            '2023-06-01', # start date
            '2023-06-30'  # end date
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            symbol, chart_type, function, start_date, end_date, interval = get_user_input()
            
            self.assertEqual(symbol, 'TSLA')
            self.assertEqual(chart_type, '2')
            self.assertEqual(function, '1')
            self.assertEqual(interval, '5min')
            self.assertEqual(start_date, '2023-06-01')
            self.assertEqual(end_date, '2023-06-30')

    def test_invalid_symbol_retries(self):
        #Test that invalid symbols are rejected and user is prompted again.
        inputs = [
            '',          # empty symbol
            'A1',        # symbol with number
            'TOOLONGSY', # symbol too long (8 chars)
            'MSFT'       # valid symbol
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            symbol, _, _, _, _, _ = get_user_input()
            self.assertEqual(symbol, 'MSFT')

    def test_invalid_chart_type_retries(self):
        #Test that invalid chart types are rejected.
        inputs = [
            'aapl', '3', '1', '2', '2023-01-01', '2023-12-31'
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            _, chart_type, _, _, _, _ = get_user_input()
            self.assertEqual(chart_type, '1')

    def test_invalid_time_series_retries(self):
        #Test that invalid time series choices are rejected.
        inputs = [
            'aapl', '1', '5', '2', '2023-01-01', '2023-12-31'
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            _, _, function, _, _, _ = get_user_input()
            self.assertEqual(function, '2')

    def test_invalid_start_date_retries(self):
        #Test that invalid start dates are rejected.
        inputs = [
            'aapl', '1', '2', 'not-a-date', '2023-01-01', '2023-12-31'
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            _, _, _, start_date, _, _ = get_user_input()
            self.assertEqual(start_date, '2023-01-01')

    def test_invalid_end_date_retries(self):
        #Test that invalid end dates are rejected.
        inputs = [
            'aapl', '1', '2', '2023-01-01', 'not-a-date', '2023-12-31'
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            _, _, _, _, end_date, _ = get_user_input()
            self.assertEqual(end_date, '2023-12-31')

    def test_end_date_before_start_date_retries(self):
        #Test that end date before start date is rejected.
        inputs = [
            'aapl', '1', '2', '2023-06-01', '2023-01-01', '2023-12-31'
        ]
        
        with unittest.mock.patch('builtins.input', side_effect=inputs):
            _, _, _, start_date, end_date, _ = get_user_input()
            self.assertGreaterEqual(end_date, start_date)


class TestGetValidDate(unittest.TestCase):
    #Unit tests for the get_valid_date helper function.

    def test_valid_date_format(self):
        #Test that valid dates in YYYY-MM-DD format are accepted.
        with unittest.mock.patch('builtins.input', side_effect=['2023-01-15']):
            result = get_valid_date("Enter date: ")
            self.assertEqual(result, '2023-01-15')

    def test_invalid_date_format(self):
        #Test that invalid date formats are rejected.
        with unittest.mock.patch('builtins.input', side_effect=['01-15-2023', '2023-01-15']):
            result = get_valid_date("Enter date: ")
            self.assertEqual(result, '2023-01-15')

    def test_invalid_date_value(self):
        #Test that invalid date values are rejected.
        with unittest.mock.patch('builtins.input', side_effect=['2023-02-30', '2023-01-15']):
            result = get_valid_date("Enter date: ")
            self.assertEqual(result, '2023-01-15')

    def test_leap_year_date(self):
        #Test that leap year dates are handled correctly.
        with unittest.mock.patch('builtins.input', side_effect=['2024-02-29']):
            result = get_valid_date("Enter date: ")
            self.assertEqual(result, '2024-02-29')

    def test_non_leap_year_date(self):
        #Test that non-leap year Feb 29 is rejected.
        with unittest.mock.patch('builtins.input', side_effect=['2023-02-29', '2023-01-15']):
            result = get_valid_date("Enter date: ")
            self.assertEqual(result, '2023-01-15')


if __name__ == '__main__':
    unittest.main()