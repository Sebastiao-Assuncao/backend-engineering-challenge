import unittest
import json
from datetime import datetime
from unbabel_cli import parse_input, calculate_moving_average, output_moving_average
from collections import deque
import os
import filecmp

EXAMPLE_INPUT = 'inputs/example_input.json'
EXAMPLE_OUTPUT = 'outputs/example_output.json'
LARGE_INPUT = 'inputs/large_input.json'
LARGE_OUTPUT = 'outputs/large_output.json'
TEMP_INPUT = 'temp_input.json'
TEMP_OUTPUT = 'temp_output.json'

class TestTranslationApp(unittest.TestCase):

    def create_temp_input_file(self, data):
        '''
        Auxilary function that creates an input file given the desired data to be written in it
        '''
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

            expected_output = deque([
                {"timestamp": datetime.strptime("2018-12-26 18:11:08.509654", "%Y-%m-%d %H:%M:%S.%f"), "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}
            ])
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

            # Expecting parse_input to return an empty deque 
            self.assertFalse(parse_input(temp_input_file))

        finally:
            # Clean the temporary file
            os.remove(temp_input_file)
    
    def test_parse_input_duplicate_translation(self):
        '''
        This validates that any repeated translation will be ignored in parse_input()
        '''

        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n\
                                    {"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}\n\
                                    {"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}\n\
                                    {"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}\n')

            expected_output = deque([{'timestamp': datetime.strptime("2018-12-26 18:11:08.509654", "%Y-%m-%d %H:%M:%S.%f"), 'translation_id': '5aa5b2f39f7254a75aa5', 'source_language': 'en', 'target_language': 'fr', 'client_name': 'airliberty', 'event_name': 'translation_delivered', 'nr_words': 30, 'duration': 20},
                            {'timestamp': datetime.strptime("2018-12-26 18:15:19.903159", "%Y-%m-%d %H:%M:%S.%f"), 'translation_id': '5aa5b2f39f7254a75aa4', 'source_language': 'en', 'target_language': 'fr', 'client_name': 'airliberty', 'event_name': 'translation_delivered', 'nr_words': 30, 'duration': 31},
                            {'timestamp': datetime.strptime("2018-12-26 18:23:19.903159", "%Y-%m-%d %H:%M:%S.%f"), 'translation_id': '5aa5b2f39f7254a75bb3', 'source_language': 'en', 'target_language': 'fr', 'client_name': 'taxi-eats', 'event_name': 'translation_delivered', 'nr_words': 100, 'duration': 54}])

            self.assertEqual(parse_input(TEMP_INPUT), expected_output)

        finally:
            os.remove(TEMP_INPUT)
    
    def test_parse_input_invalid_file(self):
        '''
        This validates that parse_input() handles invalid file paths 
        gracefully by returning None.
        '''
        self.assertIsNone(parse_input('invalid_path.json'))
    
    def test_parse_input_invalid_timestamp(self):
        '''
        This validates that parse_input() handles invalid timestamps
        gracefully by returning None.
        '''
        try:
            self.create_temp_input_file('{"timestamp": "invalid_timestamp","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_missing_key(self):
        '''
        This validates that parse_input() handles missing keys in translations
        gracefully by returning None.
        '''
        try:
            self.create_temp_input_file('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_invalid_data_type(self):
        '''
        This validates that parse_input() handles invalid data types in translations
        gracefully by returning None.
        '''
        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": "30", "duration": 20}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)
    
    def test_parse_input_additional_key(self):
        '''
        This validates that parse_input() handles additional keys in translations
        gracefully by returning None.
        '''
        try:
            self.create_temp_input_file('{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20, "extra_key": "extra_value"}\n')
            self.assertIsNone(parse_input(TEMP_INPUT))
        finally:
            os.remove(TEMP_INPUT)

    def test_parse_input_invalid_json(self):
        '''
        This validates that parse_input() handles invalid JSON formats
        gracefully by returning None.
        '''
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
        translations = deque([
            {"timestamp": datetime.strptime("2018-12-26 18:11:08.509654", "%Y-%m-%d %H:%M:%S.%f"), "translation_id": "5aa5b2f39f7254a75aa5", "source_language": "en", "target_language": "fr", "client_name": "airliberty", "event_name": "translation_delivered", "nr_words": 30, "duration": 20}
        ])
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
    
    def test_calculate_moving_average_window_one(self):
        '''
        This is a window size edge case where window_size equals 1
        
        This also validates that calculate_moving_average() deals well with intervals with no data
        '''

        expected_moving_averages = ['0', '20', '0', '0', '0', '31', '0', '0', '0', '0', '0', '0', '0', '54']

        translations = parse_input(EXAMPLE_INPUT)
        moving_averages = calculate_moving_average(translations, 1)

        # !!! Ideally change this, loops should not be used in testing
        for i in range(len(expected_moving_averages)):
            self.assertEqual(moving_averages[i]['average_delivery_time'], expected_moving_averages[i])

    def test_calculate_moving_average_max_window(self):
        '''
        This is a window size edge case where window_size equals the total number of minutes        
        '''

        expected_moving_averages = ['0', '20', '20', '20', '20', '25.5', '25.5', '25.5', '25.5', '25.5', '25.5', '25.5', '25.5', '35']

        translations = parse_input(EXAMPLE_INPUT)
        moving_averages = calculate_moving_average(translations, 14)

        # !!! Ideally change this, loops should not be used in testing
        for i in range(len(expected_moving_averages)):
            self.assertEqual(moving_averages[i]['average_delivery_time'], expected_moving_averages[i])

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
        '''
        This validates that the 3 functions integrate well with each other with the example input
        '''
        translations = parse_input(EXAMPLE_INPUT)
        moving_averages = calculate_moving_average(translations, 10)

        try:
            output_moving_average(moving_averages, TEMP_OUTPUT)
            output_file_path = os.path.join('outputs/',TEMP_OUTPUT)

            # Validate the output file
            self.assertTrue(filecmp.cmp(output_file_path, EXAMPLE_OUTPUT))

        finally:
            # Clean up the temporary file
            os.remove(output_file_path)
    
    # Comment out this test if running tests.py takes too long
    def test_full_integration_large_file(self):
        '''
        This validates that the program works well with large files.
        '''
        translations = parse_input(LARGE_INPUT)
        moving_averages = calculate_moving_average(translations, 15)

        try:
            output_moving_average(moving_averages, TEMP_OUTPUT)
            output_file_path = os.path.join('outputs/', TEMP_OUTPUT)

            # This is more of a stress test given that large_output.json was outputted by the program itself
            self.assertTrue(filecmp.cmp(output_file_path, LARGE_OUTPUT))
        
        finally:
            os.remove(output_file_path)


if __name__ == '__main__':
    unittest.main()
