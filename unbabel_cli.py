import argparse
import json
from datetime import datetime

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


def main():
    parser = argparse.ArgumentParser(description="Calculate moving average of translation delivery times.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing translations.")
    parser.add_argument("--window_size", required=True, type=int, help="The window size in minutes for moving average calculation.")
    parser.add_argument("--output_file", default="output.txt", help="Path to desired output file (optional).")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
