import unittest
import json
from datetime import datetime
from unbabel_cli import parse_input, calculate_moving_average, output_moving_average
import os
import filecmp

EXAMPLE_INPUT = 'inputs/example_input.json'
EXAMPLE_OUTPUT = 'outputs/example_output.json'
TEMP_INPUT = 'temp_input.json'
TEMP_OUTPUT = 'temp_output.json'

class TestTranslationApp(unittest.TestCase):

    def create_temp_input_file(self, data):
        with open(TEMP_INPUT, 'w') as file:
            file.write(data)
   
    def test_parse_example_file(self):
        '''
        This validates that parse_input() correctly parses a valid input file
        using the given example
        '''

        # Create temporary file with the given example
        translations = parse_input(EXAMPLE_INPUT)
        self.assertEqual(len(translations), 3)
        self.assertEqual(translations[0]['translation_id'], "5aa5b2f39f7254a75aa5")


    def test_parse_input_valid_file(self):
        '''
        This validates that parse_input() correctly parses a valid input file.
        '''

        # Create a temporary input file for testing
        temp_input_file = TEMP_INPUT

        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')

            expected_output = [
                {"timestamp": datetime.strptime("2018-12-26 18:11:08.509654", "%Y-%m-%d %H:%M:%S.%f"), "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}
            ]
            self.assertEqual(parse_input(temp_input_file), expected_output)

        finally:
            # Clean the temporary file
            os.remove(temp_input_file)
    
    def test_parse_input_empty_file(self):
        '''
        This validates that parse_input() handles an empty input file 
        gracefully by returning an empty list or None.
        '''

        # Create a temporary empty input file for testing
        temp_input_file = TEMP_INPUT

        try:
            self.create_temp_input_file("")

            # Expecting parse_input to return an empty list or None, 
            self.assertTrue(parse_input(temp_input_file) in [None, []])

        finally:
            # Clean the temporary file
            os.remove(temp_input_file)
    
    def test_parse_input_invalid_file(self):
        '''
        This validates that parse_input() handles invalid file paths 
        gracefully by returning None.
        '''
        self.assertIsNone(parse_input('invalid_path.json'))
    
    def test_parse_input_invalid_timestamp(self):
        try:
            self.create_temp_input_file('{"timestamp": "invalid_timestamp","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_missing_key(self):
        try:
            self.create_temp_input_file('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_invalid_data_type(self):
        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": "30", "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)
    
    def test_parse_input_additional_key(self):
        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20, "extra_key": "extra_value"}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_invalid_json(self):
        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654" "translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)
    
    def test_calculate_moving_average_valid_data(self):
        '''
        Tests calculate_moving_average() with valid input data.

        This validates that calculate_moving_average() functions as
        expected for a basic valid input.
        '''
        translations = [
            {"timestamp": datetime.strptime("2018-12-26 18:11:08.509654", "%Y-%m-%d %H:%M:%S.%f"), "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}
        ]
        window_size = 10
        expected_output = [
            {"date": "2018-12-26 18:11:00", "average_delivery_time": "0"},
            {"date": "2018-12-26 18:12:00", "average_delivery_time": "20"}
        ]
        self.assertEqual(calculate_moving_average(translations, window_size), expected_output)


    def test_calculate_moving_average_example(self):
        '''
        Tests calculate_moving_average() on example input.

        This provides integration and boundary testing of 
        calculate_moving_average().
        '''
        # Integration Test: Ensure that the function interacts with the parsed input correctly
        translations = parse_input(EXAMPLE_INPUT)
        moving_averages = calculate_moving_average(translations, 10)
        self.assertEqual(len(moving_averages), 14)
        self.assertEqual(moving_averages[0]['average_delivery_time'], '0')
        
        # Boundary Test: Ensure that the function handles boundary data correctly
        self.assertEqual(moving_averages[-1]['average_delivery_time'], '42.5')

    
    def test_output_moving_average(self):
        '''
        This validates that output_moving_average() correctly 
        writes the expected output to a file.
        '''
        moving_averages = [
            {"date": "2018-12-26 18:11:00", "average_delivery_time": "20"}
        ]

        output_file = TEMP_OUTPUT

        try:
            output_moving_average(moving_averages, output_file)
            output_file_path = os.path.join('outputs/',output_file)
            # Validate the output file
            with open(output_file_path, 'r') as file:
                line = file.readline().strip()
                self.assertEqual(json.loads(line), moving_averages[0])

        finally:    
            # Clean up the temporary file
            os.remove(output_file_path)
    

    def test_full_integration_example(self):
        translations = parse_input(EXAMPLE_INPUT)
        moving_averages = calculate_moving_average(translations, 10)

        output_file=TEMP_OUTPUT

        try:
            output_moving_average(moving_averages, output_file)
            output_file_path = os.path.join('outputs/',output_file)

            # Validate the output file
            self.assertTrue(filecmp.cmp(output_file_path, EXAMPLE_OUTPUT))

        finally:
            # Clean up the temporary file
            os.remove(output_file_path)


if __name__ == '__main__':
    unittest.main()
