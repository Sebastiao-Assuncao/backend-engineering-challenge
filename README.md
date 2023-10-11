# Translation Delivery Time Averager

This command-line application calculates the moving average of translation delivery times per minute over a specified window of minutes, given a stream of translation delivery events.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Input Format](#input-format)
- [Output Format](#output-format)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Optimizations](#optimizations)


## Prerequisites

- Python 3.x
- All imported modules come built into python, no further requirements


## Usage

To use the application, run the following command in your terminal:

```sh
python3 unbabel_cli.py --input_file [INPUT_FILE_PATH] --window_size [WINDOW_SIZE] --output_file [OUTPUT_FILE_PATH]
```

- `[INPUT_FILE_PATH]`: Path to the input JSON file containing translation events.
- `[WINDOW_SIZE]`: The window size in minutes for calculating the moving average.
- `[OUTPUT_FILE_PATH]`: (Optional) Path to the desired output file. If not provided, defaults to `outputs/output.txt`.

Example:

```sh
python3 unbabel_cli.py --input_file events.json --window_size 10 --output_file output.json
```

## Input Format

The input file should contain translation events in JSON format, one per line. Example:

```json
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```


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

## Error Handling

In the `unbabel_cli.py` script, various error scenarios are anticipated and handled. Below are the types of errors that are handled and how the application responds:

#### 1. File Not Found Error
- **Scenario:** When the provided input file path does not point to an existing file.
- **Response:** The application logs an error message: "File [file_path] not found." and terminates gracefully.

#### 2. Invalid Timestamp Format
- **Scenario:** When the timestamp in the input JSON data is not in the expected format.
- **Response:** Logs an error message: "Invalid timestamp format in [file_path]." and terminates the application.

#### 3. Validation Error
- **Scenario:** When the input JSON data does not adhere to the expected schema (missing keys, incorrect data types, etc.).
- **Response:** Logs specific error messages detailing the validation failure and terminates the application.

#### 4. I/O Error
- **Scenario:** When the application cannot write the output to the specified file.
- **Response:** Logs an error message: "File write error: [error_detail]" and terminates the application.

#### 5. CLI Argument Error
- **Scenario:** When the window size provided via CLI is not a positive integer.
- **Response:** Logs an error message: "Error: Window size must be a positive integer" and terminates the application.


## Testing

To run the tests, execute the following command:

```sh
python3 tests.py
```

The folders inputs/ and outputs/ contain 2 files each, one relative to the example given and the other relative to testing with large amounts of data.


## Optimizations

Given the ordered nature of the input lines (by timestamp), the application leverages this to optimize the calculation of the moving average by:
- Utilizing a queue to efficiently add and remove translations from the window, ensuring O(1) time complexity for these operations.
- Avoiding recalculating the sum of durations in the window from scratch for each minute by maintaining a running total.
