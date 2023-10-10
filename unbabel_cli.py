import argparse
import json
from datetime import datetime, timedelta
from collections import deque
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

def parse_input(file_path):
    '''
    Parse the input JSON file and convert it into a list of event dictionaries.
    
    Parameters:
        file_path -> str: The path to the input file.
        
    Returns:
        translations -> list: A list of dictionaries, each representing an event.
    '''

    translations = []

    try:    
        with open(file_path, 'r') as input_file:
            for line in input_file:
                translation = json.loads(line.strip())
                # Convert timestamp to datetime objects for easier comparsion and calculation
                translation['timestamp'] = datetime.strptime(translation['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                translations.append(translation)

    except Exception as e:
        logging.error(f"Error parsing input file: {str(e)}")
        return None
    
    return translations

def calculate_moving_average(translations, window_size):
    '''
    Calculate the moving average of translation delivery times per minute for a specified window size.
    
    Parameters:
        translations -> list: A list of translations, each represented as a dictionary.
        window_size -> int: The size of the window for which the moving average is to be calculated.
        
    Returns:
        moving_averages -> list: A list of dictionaries, each containing a minute and the corresponding moving average.
    '''

    moving_averages = []
    window_queue = deque()
    window_sum = 0

    current_minute = translations[0]['timestamp'].replace(second=0, microsecond=0)
    last_minute = translations[-1]['timestamp'].replace(second=0, microsecond=0) + timedelta(minutes=1)
    
    # Iterate through each minute from the first to the last translation
    while current_minute <= last_minute:
        average = 0

        # Check for new translations that fall within the new window with the added minute
        while translations and translations[0]['timestamp'] < current_minute:    
            translation = translations.pop(0)
            window_sum += translation['duration']
            window_queue.append(translation)

        # Remove translations from the window that are older than the current minute minus the window_size   
        while window_queue and window_queue[0]['timestamp'] <= current_minute - timedelta(minutes=window_size):
            window_sum -= window_queue.popleft()['duration']
        
        # Calculate the average for the current minute
        if window_queue:
            average = window_sum / len(window_queue)
        
        # Store the average for the current minute
        moving_averages.append({
        "date": current_minute.strftime("%Y-%m-%d %H:%M:%S"),
        "average_delivery_time": f'{average:g}'
        })

        current_minute += timedelta(minutes=1)
    
    return moving_averages

def output_moving_average(moving_averages, output_file):
    '''
    Output the calculated moving averages to a file in the desired format.
    
    Parameters:
        moving_averages -> list: A list of dictionaries, each containing a minute and the corresponding moving average.
        output_file -> strS: The path to the file where the output should be written.
    '''
    try:
        output_file_path = os.path.join('outputs/',output_file)
        with open(output_file_path, 'w') as file:
            for avg in moving_averages:
                file.write(f'{json.dumps(avg)}\n')
    
    except IOError as e:
        logging.error(f'"File write error: {str(e)}')



def main():

    # Argument parser for CLI
    parser = argparse.ArgumentParser(description="Calculate moving average of translation delivery times.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing translations.")
    parser.add_argument("--window_size", required=True, type=int, help="The window size in minutes for moving average calculation.")
    parser.add_argument("--output_file", default="output.txt", help="Path to desired output file (optional).")
    args = parser.parse_args()

    # Window size validation
    if args.window_size <= 0:
        logging.error("Error: Window size must be a positive integer")
        return
    
    translations = parse_input(args.input_file)

    if not translations:
        return

    moving_averages = calculate_moving_average(translations, args.window_size)
    output_moving_average(moving_averages, args.output_file)

if __name__ == "__main__":
    main()
