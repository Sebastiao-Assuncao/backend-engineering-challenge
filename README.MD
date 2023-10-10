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