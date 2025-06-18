import csv

def load_csv_to_memory(file_path: str) -> list[dict]:
    """
    Loads a CSV file into a list of dictionaries.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A list of dictionaries, where each dictionary represents a row
        and keys are column headers.

    Raises:
        FileNotFoundError: If the CSV file is not found.
        ValueError: If the CSV file is invalid or improperly formatted.
    """
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
            if not data and reader.fieldnames is None: # Check for empty or invalid CSV
                raise ValueError(f"CSV file at {file_path} is empty or has no headers.")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {file_path}")
    except Exception as e: # Catch other potential CSV parsing errors
        raise ValueError(f"Error parsing CSV file at {file_path}: {e}")

def query_data(data: list[dict], column_name: str, value: str) -> list[dict]:
    """
    Queries a list of dictionaries for rows where a specific column matches a given value.

    Args:
        data: A list of dictionaries (e.g., loaded from a CSV).
        column_name: The name of the column to query.
        value: The value to match in the specified column.

    Returns:
        A new list of dictionaries containing only the matching rows.
        Returns an empty list if the column_name is not found or no rows match.
    """
    matching_rows = []
    for row in data:
        if column_name in row and row[column_name] == value:
            matching_rows.append(row)
    return matching_rows

def display_data(data: list[dict]):
    """
    Displays a list of dictionaries in a basic tabular format.

    Args:
        data: A list of dictionaries to display.
    """
    if not data:
        print("No data to display.")
        return

    # Assume all dictionaries have the same keys as the first one
    headers = list(data[0].keys())

    # Determine column widths (optional, for better alignment)
    # For simplicity, we'll use a fixed separator (tab) for now
    # A more advanced version might calculate max width for each column

    # Print headers
    print("\t".join(headers))
    print("-" * (len(headers) * 10)) # Simple separator line

    # Print rows
    for row in data:
        # Ensure all header keys are present, print empty string if not
        print("\t".join(str(row.get(header, "")) for header in headers))

if __name__ == '__main__':
    # --- Test load_csv_to_memory ---
    print("--- Testing load_csv_to_memory ---")
    # Create a dummy CSV file for testing load_csv_to_memory
    dummy_load_file_path = 'dummy_load_data.csv'
    with open(dummy_load_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'value'])
        writer.writerow(['1', 'itemA', '100'])
        writer.writerow(['2', 'itemB', '200'])
        writer.writerow(['3', 'itemC', '300'])

    try:
        print(f"Attempting to load: {dummy_load_file_path}")
        loaded_dummy_data = load_csv_to_memory(dummy_load_file_path)
        print("Successfully loaded dummy data:")
        for row in loaded_dummy_data:
            print(row)
    except (FileNotFoundError, ValueError) as e:
        print(e)

    print("\nAttempting to load non_existent_file.csv:")
    try:
        load_csv_to_memory('non_existent_file.csv')
    except (FileNotFoundError, ValueError) as e:
        print(e)

    empty_file_path = 'empty_data.csv'
    with open(empty_file_path, 'w', newline='') as f:
        pass
    print(f"\nAttempting to load empty CSV: {empty_file_path}")
    try:
        load_csv_to_memory(empty_file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)

    invalid_csv_path = 'invalid_data.bin'
    with open(invalid_csv_path, 'wb') as f:
        f.write(b"\x00\x01\x02\x03\x04")
    print(f"\nAttempting to load invalid CSV: {invalid_csv_path}")
    try:
        load_csv_to_memory(invalid_csv_path)
    except (FileNotFoundError, ValueError) as e:
        print(e) # This was missing

    # --- Test query_data ---
    print("\n--- Testing query_data ---")
    sample_csv_path = 'data/sample.csv' # Using the one created in data/ directory

    # For query testing, we'll load the previously created data/sample.csv
    # This assumes data/sample.csv was created in a previous step or exists
    # If running this script standalone, ensure data/sample.csv is present.
    print(f"\nLoading data from {sample_csv_path} for query tests...")
    try:
        main_data = load_csv_to_memory(sample_csv_path)
        if not main_data:
            print(f"Warning: {sample_csv_path} loaded no data. Query tests might not be meaningful.")
        else:
            print(f"Successfully loaded {len(main_data)} rows from {sample_csv_path}")

        # Test 1: Query for Source_IP 192.168.1.10
        print("\nQuery 1: Source_IP = '192.168.1.10'")
        results1 = query_data(main_data, 'Source_IP', '192.168.1.10')
        for row in results1:
            print(row)
        print(f"Found {len(results1)} matching rows.")

        # Test 2: Query for Protocol TCP
        print("\nQuery 2: Protocol = 'TCP'")
        results2 = query_data(main_data, 'Protocol', 'TCP')
        for row in results2:
            print(row)
        print(f"Found {len(results2)} matching rows.")

        # Test 3: Query for a value that doesn't exist
        print("\nQuery 3: Destination_IP = '1.2.3.4'")
        results3 = query_data(main_data, 'Destination_IP', '1.2.3.4')
        for row in results3:
            print(row) # Should not print anything
        print(f"Found {len(results3)} matching rows (expected 0).")

        # Test 4: Query for a column that doesn't exist
        print("\nQuery 4: NonExistentColumn = 'any_value'")
        results4 = query_data(main_data, 'NonExistentColumn', 'any_value')
        for row in results4:
            print(row) # Should not print anything
        print(f"Found {len(results4)} matching rows (expected 0).")

        # Test 5: Query on empty data
        print("\nQuery 5: Query on empty data list")
        results5 = query_data([], 'Source_IP', '192.168.1.10')
        print(f"Found {len(results5)} matching rows (expected 0).")

    except FileNotFoundError:
        print(f"ERROR: Test data file {sample_csv_path} not found. Skipping query tests.")
        main_data = [] # Ensure main_data is defined for display tests if file not found
    except ValueError as e:
        print(f"ERROR: Could not process {sample_csv_path} for query tests: {e}")
        main_data = [] # Ensure main_data is defined for display tests if error

    # --- Test display_data ---
    print("\n--- Testing display_data ---")

    # Test 1: Display data from a query
    print("\nDisplay 1: Results from 'Query 1: Source_IP = 192.168.1.10'")
    if 'main_data' in locals() and main_data: # Check if main_data was loaded
        results_for_display = query_data(main_data, 'Source_IP', '192.168.1.10')
        display_data(results_for_display)
    else:
        print("Skipping display test as main_data is not available.")

    # Test 2: Display data from another query (e.g., all TCP traffic)
    print("\nDisplay 2: Results from 'Query 2: Protocol = TCP'")
    if 'main_data' in locals() and main_data:
        tcp_results_for_display = query_data(main_data, 'Protocol', 'TCP')
        display_data(tcp_results_for_display)
    else:
        print("Skipping display test as main_data is not available.")

    # Test 3: Display empty list
    print("\nDisplay 3: Displaying an empty list")
    display_data([])

    # Test 4: Display data with a single row
    print("\nDisplay 4: Displaying a single row of data")
    if 'main_data' in locals() and main_data:
        single_row_data = query_data(main_data, 'Timestamp', '2023-10-26T10:05:00Z') # Assuming this timestamp is unique
        display_data(single_row_data)
    else:
        print("Skipping display test as main_data is not available.")

    # Test 5: Display all loaded sample data
    print("\nDisplay 5: Displaying all loaded sample data")
    if 'main_data' in locals() and main_data:
        display_data(main_data)
    else:
        print("Skipping display test as main_data is not available or empty.")


    # Clean up dummy files created for load_csv_to_memory tests
    import os
    if os.path.exists(dummy_load_file_path):
        os.remove(dummy_load_file_path)
    if os.path.exists(empty_file_path):
        os.remove(empty_file_path)
    if os.path.exists(invalid_csv_path):
        os.remove(invalid_csv_path)
# The following __main__ block was removed as per subtask instructions.
# if __name__ == '__main__':
#     # --- Test load_csv_to_memory ---
#     print("--- Testing load_csv_to_memory ---")
#     # Create a dummy CSV file for testing load_csv_to_memory
#     dummy_load_file_path = 'dummy_load_data.csv'
#     with open(dummy_load_file_path, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['id', 'name', 'value'])
#         writer.writerow(['1', 'itemA', '100'])
#         writer.writerow(['2', 'itemB', '200'])
#         writer.writerow(['3', 'itemC', '300'])
#
#     try:
#         print(f"Attempting to load: {dummy_load_file_path}")
#         loaded_dummy_data = load_csv_to_memory(dummy_load_file_path)
#         print("Successfully loaded dummy data:")
#         for row in loaded_dummy_data:
#             print(row)
#     except (FileNotFoundError, ValueError) as e:
#         print(e)
#
#     print("\nAttempting to load non_existent_file.csv:")
#     try:
#         load_csv_to_memory('non_existent_file.csv')
#     except (FileNotFoundError, ValueError) as e:
#         print(e)
#
#     empty_file_path = 'empty_data.csv'
#     with open(empty_file_path, 'w', newline='') as f:
#         pass
#     print(f"\nAttempting to load empty CSV: {empty_file_path}")
#     try:
#         load_csv_to_memory(empty_file_path)
#     except (FileNotFoundError, ValueError) as e:
#         print(e)
#
#     invalid_csv_path = 'invalid_data.bin'
#     with open(invalid_csv_path, 'wb') as f:
#         f.write(b"\x00\x01\x02\x03\x04")
#     print(f"\nAttempting to load invalid CSV: {invalid_csv_path}")
#     try:
#         load_csv_to_memory(invalid_csv_path)
#     except (FileNotFoundError, ValueError) as e:
#         print(e) # This was missing
#
#     # --- Test query_data ---
#     print("\n--- Testing query_data ---")
#     sample_csv_path = 'data/sample.csv' # Using the one created in data/ directory
#
#     # For query testing, we'll load the previously created data/sample.csv
#     # This assumes data/sample.csv was created in a previous step or exists
#     # If running this script standalone, ensure data/sample.csv is present.
#     print(f"\nLoading data from {sample_csv_path} for query tests...")
#     try:
#         main_data = load_csv_to_memory(sample_csv_path)
#         if not main_data:
#             print(f"Warning: {sample_csv_path} loaded no data. Query tests might not be meaningful.")
#         else:
#             print(f"Successfully loaded {len(main_data)} rows from {sample_csv_path}")
#
#         # Test 1: Query for Source_IP 192.168.1.10
#         print("\nQuery 1: Source_IP = '192.168.1.10'")
#         results1 = query_data(main_data, 'Source_IP', '192.168.1.10')
#         for row in results1:
#             print(row)
#         print(f"Found {len(results1)} matching rows.")
#
#         # Test 2: Query for Protocol TCP
#         print("\nQuery 2: Protocol = 'TCP'")
#         results2 = query_data(main_data, 'Protocol', 'TCP')
#         for row in results2:
#             print(row)
#         print(f"Found {len(results2)} matching rows.")
#
#         # Test 3: Query for a value that doesn't exist
#         print("\nQuery 3: Destination_IP = '1.2.3.4'")
#         results3 = query_data(main_data, 'Destination_IP', '1.2.3.4')
#         for row in results3:
#             print(row) # Should not print anything
#         print(f"Found {len(results3)} matching rows (expected 0).")
#
#         # Test 4: Query for a column that doesn't exist
#         print("\nQuery 4: NonExistentColumn = 'any_value'")
#         results4 = query_data(main_data, 'NonExistentColumn', 'any_value')
#         for row in results4:
#             print(row) # Should not print anything
#         print(f"Found {len(results4)} matching rows (expected 0).")
#
#         # Test 5: Query on empty data
#         print("\nQuery 5: Query on empty data list")
#         results5 = query_data([], 'Source_IP', '192.168.1.10')
#         print(f"Found {len(results5)} matching rows (expected 0).")
#
#     except FileNotFoundError:
#         print(f"ERROR: Test data file {sample_csv_path} not found. Skipping query tests.")
#         main_data = [] # Ensure main_data is defined for display tests if file not found
#     except ValueError as e:
#         print(f"ERROR: Could not process {sample_csv_path} for query tests: {e}")
#         main_data = [] # Ensure main_data is defined for display tests if error
#
#     # --- Test display_data ---
#     print("\n--- Testing display_data ---")
#
#     # Test 1: Display data from a query
#     print("\nDisplay 1: Results from 'Query 1: Source_IP = 192.168.1.10'")
#     if 'main_data' in locals() and main_data: # Check if main_data was loaded
#         results_for_display = query_data(main_data, 'Source_IP', '192.168.1.10')
#         display_data(results_for_display)
#     else:
#         print("Skipping display test as main_data is not available.")
#
#     # Test 2: Display data from another query (e.g., all TCP traffic)
#     print("\nDisplay 2: Results from 'Query 2: Protocol = TCP'")
#     if 'main_data' in locals() and main_data:
#         tcp_results_for_display = query_data(main_data, 'Protocol', 'TCP')
#         display_data(tcp_results_for_display)
#     else:
#         print("Skipping display test as main_data is not available.")
#
#     # Test 3: Display empty list
#     print("\nDisplay 3: Displaying an empty list")
#     display_data([])
#
#     # Test 4: Display data with a single row
#     print("\nDisplay 4: Displaying a single row of data")
#     if 'main_data' in locals() and main_data:
#         single_row_data = query_data(main_data, 'Timestamp', '2023-10-26T10:05:00Z') # Assuming this timestamp is unique
#         display_data(single_row_data)
#     else:
#         print("Skipping display test as main_data is not available.")
#
#     # Test 5: Display all loaded sample data
#     print("\nDisplay 5: Displaying all loaded sample data")
#     if 'main_data' in locals() and main_data:
#         display_data(main_data)
#     else:
#         print("Skipping display test as main_data is not available or empty.")
#
#
#     # Clean up dummy files created for load_csv_to_memory tests
#     import os
#     if os.path.exists(dummy_load_file_path):
#         os.remove(dummy_load_file_path)
#     if os.path.exists(empty_file_path):
#         os.remove(empty_file_path)
#     if os.path.exists(invalid_csv_path):
#         os.remove(invalid_csv_path)
