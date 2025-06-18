import sys
from siem_core.csv_handler import load_csv_to_memory, query_data, display_data

# Global variables to store data
original_data = []
current_data = []

def main():
    """
    Main function to run the command-line interface.
    """
    global original_data, current_data

    while True:
        print("\nSIEM Core CLI")
        print("Commands:")
        print("  load <file_path>     - Loads data from a CSV file.")
        print("  query <column> <value> - Queries the current data.")
        print("  display              - Displays the current data.")
        print("  reset                - Resets current data to the original loaded data.")
        print("  exit                 - Exits the application.")

        try:
            raw_input = input("> ").strip()
            if not raw_input:
                continue

            parts = raw_input.split(maxsplit=1) # Split command from arguments
            command = parts[0].lower()
            args_str = parts[1] if len(parts) > 1 else ""

        except EOFError: # Handle Ctrl+D as exit
            print("\nExiting...")
            break
        except KeyboardInterrupt: # Handle Ctrl+C as exit
            print("\nExiting...")
            break

        if command == "load":
            if not args_str:
                print("Error: Missing file path for 'load' command.")
                continue
            file_path = args_str
            try:
                original_data = load_csv_to_memory(file_path)
                current_data = list(original_data) # Make a copy
                print(f"Successfully loaded {len(original_data)} rows from {file_path}.")
            except FileNotFoundError:
                print(f"Error: File not found at '{file_path}'.")
            except ValueError as e:
                print(f"Error loading CSV: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during load: {e}")

        elif command == "query":
            if not original_data:
                print("Error: No data loaded. Use 'load <file_path>' first.")
                continue

            query_parts = args_str.split(maxsplit=1)
            if len(query_parts) < 2:
                print("Error: 'query' command requires <column> and <value> arguments.")
                print("Usage: query <column_name> <value_to_search>")
                continue

            column_name, value = query_parts[0], query_parts[1]
            current_data = query_data(current_data, column_name, value)
            print(f"Query executed. {len(current_data)} rows match the criteria.")
            if not current_data:
                 print(f"(No results for '{column_name}' = '{value}' in the current view. Use 'reset' to see all loaded data again)")


        elif command == "display":
            if not original_data: # Check if any data has ever been loaded
                print("Error: No data loaded. Use 'load <file_path>' first.")
                continue
            display_data(current_data)

        elif command == "reset":
            if not original_data:
                print("Error: No data loaded to reset. Use 'load <file_path>' first.")
                continue
            current_data = list(original_data) # Reset to a fresh copy of original
            print("Data view has been reset to the original loaded data.")

        elif command == "exit":
            print("Exiting...")
            break

        else:
            print(f"Error: Unknown command '{command}'. Type one of the listed commands.")

if __name__ == '__main__':
    # Check if siem_core is importable, otherwise guide user
    try:
        from siem_core import csv_handler
    except ImportError:
        print("Error: Could not import 'siem_core.csv_handler'.")
        print("Please ensure that the 'siem_core' directory is in your Python path,")
        print("or that you are running this script from the project's root directory.")
        sys.exit(1)
    main()
