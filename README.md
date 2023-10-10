# Translation Delivery Time Averager

This command-line application calculates the moving average of translation delivery times per minute over a specified window of minutes, given a stream of translation delivery events.

## Usage

To use the application, run the following command in your terminal:

```sh
python3 unbabel_cli.py --input_file [INPUT_FILE_PATH] --window_size [WINDOW_SIZE] --output_file [OUTPUT_FILE_PATH]
```

- `[INPUT_FILE_PATH]`: Path to the input JSON file containing translation events.
- `[WINDOW_SIZE]`: The window size in minutes for calculating the moving average.
- `[OUTPUT_FILE_PATH]`: (Optional) Path to the desired output file. If not provided, defaults to `output.txt`.


## Input Format

The input file should contain translation events in JSON format, one per line. Example:

```json
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```

Note: The example above is contained in the 'inputs/' folder

## Output Format

The output file will be located in the 'outputs/' folder and will contain the moving average per minute in JSON format. Example:

```json
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

## Optimizations

Given the ordered nature of the input lines (by timestamp), the application leverages this to optimize the calculation of the moving average by:
- Utilizing a queue to efficiently add and remove translations from the window, ensuring O(1) time complexity for these operations.
- Avoiding recalculating the sum of durations in the window from scratch for each minute by maintaining a running total.
