# CSV Input Lookup Tool

## Description

This project implements a simple command-line tool that mimics the basic `inputlookup` functionality found in SIEM systems like Splunk. It allows users to load data from a CSV file, perform simple equality-based queries on that data, and display the results.

All data is currently processed and stored in memory.

## Project Structure

```
.project-root/
├── app.py            # Main CLI application script
├── data/
│   ├── sample.csv      # Sample CSV data for testing
│   └── malformed.csv   # Malformed CSV for error handling tests (currently tests empty CSV)
├── siem_core/
│   ├── __init__.py
│   └── csv_handler.py  # Core logic for CSV loading, querying, and display
├── tests/
│   ├── __init__.py
│   └── test_csv_handler.py # Unit tests for csv_handler.py
└── README.md         # This file
```

## Setup

This project uses only standard Python libraries. No special setup is required beyond having a Python 3 environment.

1.  Clone the repository (or ensure all files are present in a local directory).
2.  Navigate to the project's root directory in your terminal.

## Usage

To start the application, run:

```bash
python app.py
```

Once the application is running, you will see a prompt. The following commands are available:

*   `load <file_path>`: Loads a CSV file into memory.
    *   Example: `load data/sample.csv`
*   `query <column_name> <value>`: Filters the currently loaded data. The query is performed on the results of the previous query if multiple queries are chained.
    *   Example: `query Source_IP 192.168.1.10`
*   `display`: Shows the current data (either full loaded data or filtered data) in a tabular format.
*   `reset`: Resets the current data view to the originally loaded CSV data, discarding any query results.
*   `exit`: Exits the application.

## Running Tests

Unit tests are located in the `tests/` directory and use Python's `unittest` module.

To run the tests, navigate to the project's root directory and execute:

```bash
python -m unittest discover tests
```

This will automatically discover and run all tests in the `tests` directory.
