import argparse
import json
from datetime import datetime, timedelta
from collections import deque

def parse_input(file_path):
    translations = []

    try:    
        with open(file_path, 'r') as input_file:
            for line in input_file:
                translation = json.loads(line.strip())
                # Convert timestamp to datetime objects for easier comparsion and calculation
                translation['timestamp'] = datetime.strptime(translation['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                translations.append(translation)

    except Exception as e:
        print(f"Error parsing input file: {str(e)}")
        return None
    
    return translations

def calculate_moving_average(translations, window_size):
    moving_averages = []
    window_queue = deque()
    window_sum = 0

    current_minute = translations[0]['timestamp'].replace(second=0, microsecond=0)
    last_minute = translations[-1]['timestamp'].replace(second=0, microsecond=0)

    while current_minute <= last_minute + timedelta(minutes=1):
        average = 0

        # Check for new translations that fall within the new window with the added minute
        while translations and translations[0]['timestamp'] < current_minute:    
            translation = translations.pop(0)
            window_sum += translation['duration']
            window_queue.append(translation)

        # Remove translations from the window that are older than the current minute minus the window_size   
        while window_queue and window_queue[0]['timestamp'] <= current_minute - timedelta(minutes=window_size):
            window_sum -= window_queue.popleft()['duration']
        
        if window_queue:
            average = window_sum / len(window_queue)
        
        moving_averages.append({
        "date": current_minute.strftime("%Y-%m-%d %H:%M:%S"),
        "average_delivery_time": f'{average:g}'
        })

        current_minute += timedelta(minutes=1)
    
    return moving_averages

def output_moving_average(moving_averages, output_file):
    with open(output_file, 'w') as file:
        for avg in moving_averages:
            file.write(f'{json.dumps(avg)}\n')



def main():
    parser = argparse.ArgumentParser(description="Calculate moving average of translation delivery times.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing translations.")
    parser.add_argument("--window_size", required=True, type=int, help="The window size in minutes for moving average calculation.")
    parser.add_argument("--output_file", default="output.txt", help="Path to desired output file (optional).")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
