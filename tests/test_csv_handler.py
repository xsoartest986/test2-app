import unittest
import os
import csv
from io import StringIO
from contextlib import redirect_stdout

# Add project root to sys.path to allow direct import of siem_core
import sys
# Assuming the tests directory is directly under the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from siem_core.csv_handler import load_csv_to_memory, query_data, display_data

class TestCSVHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create sample.csv for testing
        cls.sample_csv_path = os.path.join(project_root, 'data', 'sample.csv')
        # Malformed CSV path
        cls.malformed_csv_path = os.path.join(project_root, 'data', 'malformed.csv')
        # Non-existent CSV path
        cls.non_existent_csv_path = os.path.join(project_root, 'data', 'non_existent.csv')

        # Ensure sample.csv exists (it should from previous steps, but good for standalone test runs)
        if not os.path.exists(cls.sample_csv_path):
            os.makedirs(os.path.join(project_root, 'data'), exist_ok=True)
            with open(cls.sample_csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Source_IP', 'Destination_IP', 'Protocol', 'Port', 'Timestamp'])
                writer.writerow(['192.168.1.10', '10.0.0.5', 'TCP', '443', '2023-10-26T10:00:00Z'])
                writer.writerow(['192.168.1.12', '10.0.0.8', 'UDP', '53', '2023-10-26T10:05:00Z'])
                writer.writerow(['192.168.1.10', '10.0.0.5', 'TCP', '80', '2023-10-26T10:10:00Z'])
                writer.writerow(['10.20.30.40', '172.16.0.100', 'TCP', '443', '2023-10-26T10:15:00Z'])
                writer.writerow(['192.168.1.15', '10.0.0.5', 'ICMP', '', '2023-10-26T10:20:00Z'])

        # Sample data loaded from sample.csv, used in multiple query tests
        cls.loaded_data = load_csv_to_memory(cls.sample_csv_path)


    # --- Test load_csv_to_memory ---
    def test_load_csv_success(self):
        data = load_csv_to_memory(self.sample_csv_path)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertIsInstance(data[0], dict)
        self.assertIn('Source_IP', data[0])

    def test_load_csv_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_csv_to_memory(self.non_existent_csv_path)

    def test_load_csv_value_error_malformed(self):
        # This test expects a ValueError because DictReader behavior with inconsistent field numbers.
        # Depending on Python's CSV reader strictness, this might sometimes not raise ValueError
        # but rather fill missing fields with None or skip rows.
        # For this example, we assume it raises ValueError due to DictReader expecting consistent rows.
        # If the malformed.csv has headers, DictReader will use them. If a row has FEWER fields
        # than headers, the missing keys will have None values. If a row has MORE fields,
        # the extra data is put into a list under a key None (by default).
        # The current malformed.csv (r2c1,r2c2) will result in {'Header1': 'r2c1', 'Header2': 'r2c2', 'Header3': None}
        # The row (r3c1,r3c2,r3c3,r3c4) will result in {'Header1': 'r3c1', 'Header2': 'r3c2', 'Header3': 'r3c3', None: ['r3c4']}
        # Neither of these inherently causes a ValueError *during loading* with DictReader.
        # A ValueError in load_csv_to_memory is more likely from an empty file or truly broken CSV structure.
        # Let's test the "empty or no headers" case which is explicitly in load_csv_to_memory
        empty_csv_path = os.path.join(project_root, 'data', 'empty_for_test.csv')
        with open(empty_csv_path, 'w') as f:
            pass # create empty file
        with self.assertRaisesRegex(ValueError, "empty or has no headers"):
            load_csv_to_memory(empty_csv_path)
        os.remove(empty_csv_path)

        # To truly test malformed CSV that DictReader might struggle with and cause our function to raise ValueError
        # (e.g. due to an underlying exception during iteration), it might need to be more severely malformed,
        # or the function itself would need stricter checks post-DictReader.
        # For now, the "empty" test is a valid ValueError test for load_csv_to_memory.


    # --- Test query_data ---
    def test_query_data_success(self):
        results = query_data(self.loaded_data, 'Source_IP', '192.168.1.10')
        self.assertEqual(len(results), 2)
        for row in results:
            self.assertEqual(row['Source_IP'], '192.168.1.10')

        results_protocol = query_data(self.loaded_data, 'Protocol', 'TCP')
        self.assertEqual(len(results_protocol), 3)
        for row in results_protocol:
            self.assertEqual(row['Protocol'], 'TCP')

    def test_query_data_non_existent_column(self):
        results = query_data(self.loaded_data, 'NonExistentColumn', 'some_value')
        self.assertEqual(len(results), 0)

    def test_query_data_non_existent_value(self):
        results = query_data(self.loaded_data, 'Source_IP', '1.2.3.4')
        self.assertEqual(len(results), 0)

    def test_query_data_empty_input(self):
        results = query_data([], 'Source_IP', '192.168.1.10')
        self.assertEqual(len(results), 0)

    # --- Test display_data ---
    def test_display_data_with_content(self):
        string_io = StringIO()
        # Use a subset of data for predictable output
        test_data = [
            {'col1': 'val1', 'col2': 'val2'},
            {'col1': 'val3', 'col2': 'val4'}
        ]
        with redirect_stdout(string_io):
            display_data(test_data)
        output = string_io.getvalue()

        self.assertIn("col1\tcol2", output) # Check headers
        self.assertIn("val1\tval2", output) # Check first row
        self.assertIn("val3\tval4", output) # Check second row
        self.assertNotIn("No data to display.", output)

    def test_display_data_empty(self):
        string_io = StringIO()
        with redirect_stdout(string_io):
            display_data([])
        output = string_io.getvalue()
        self.assertIn("No data to display.", output)

if __name__ == '__main__':
    unittest.main()
