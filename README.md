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