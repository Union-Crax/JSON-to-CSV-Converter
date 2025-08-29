#!/usr/bin/env python3
"""
json2csv - A command-line tool to convert JSON to CSV

Supports JSON arrays, single objects, NDJSON, nested object flattening,
flexible list handling, and various output options.
"""

import argparse
import csv
import json
import sys
from typing import Any, Dict, List, Optional, Union, TextIO


class JSONToCSVConverter:
    """Main converter class for JSON to CSV conversion."""

    def __init__(self,
                 delimiter: str = ',',
                 fields: Optional[List[str]] = None,
                 no_header: bool = False,
                 list_handling: str = 'join',
                 join_string: str = '|'):
        """
        Initialize the converter with specified options.

        Args:
            delimiter: CSV field delimiter
            fields: List of fields to include (None for all)
            no_header: Whether to skip header row
            list_handling: How to handle lists ('join' or 'index')
            join_string: String to join list items with
        """
        self.delimiter = delimiter
        self.fields = fields
        self.no_header = no_header
        self.list_handling = list_handling
        self.join_string = join_string

    def convert(self, input_stream: TextIO, output_stream: TextIO) -> None:
        """
        Convert JSON from input stream to CSV on output stream.

        Args:
            input_stream: Input stream containing JSON
            output_stream: Output stream for CSV
        """
        json_data = self._parse_json(input_stream)

        records = self._json_to_records(json_data)

        if self.fields:
            records = self._filter_fields(records, self.fields)

        self._write_csv(records, output_stream)

    def _parse_json(self, input_stream: TextIO) -> Union[List[Dict], Dict]:
        """Parse JSON from input stream, handling arrays, objects, and NDJSON."""
        content = input_stream.read().strip()

        if not content:
            return []

        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ValueError("JSON must be an object or array")
        except json.JSONDecodeError:
            return self._parse_ndjson(content)

    def _parse_ndjson(self, content: str) -> List[Dict]:
        """Parse NDJSON (Newline Delimited JSON) content."""
        lines = content.strip().split('\n')
        records = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
                if isinstance(record, dict):
                    records.append(record)
                else:
                    raise ValueError(f"Line {line_num}: Expected JSON object")
            except json.JSONDecodeError as e:
                raise ValueError(f"Line {line_num}: Invalid JSON - {e}")

        return records

    def _json_to_records(self, json_data: List[Dict]) -> List[Dict]:
        """Convert JSON data to flattened records."""
        records = []

        for item in json_data:
            if isinstance(item, dict):
                flattened = self._flatten_object(item)
                records.append(flattened)
            else:
                records.append({'value': item})

        return records

    def _flatten_object(self, obj: Dict, prefix: str = '') -> Dict:
        """
        Flatten a nested object using dot notation.

        Args:
            obj: Object to flatten
            prefix: Current prefix for nested keys

        Returns:
            Flattened dictionary
        """
        flattened = {}

        for key, value in obj.items():
            new_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                nested = self._flatten_object(value, new_key)
                flattened.update(nested)
            elif isinstance(value, list):
                if self.list_handling == 'join':
                    flattened[new_key] = self.join_string.join(str(v) for v in value)
                elif self.list_handling == 'index':
                    for i, item in enumerate(value):
                        flattened[f"{new_key}.{i}"] = item
                else:
                    flattened[new_key] = value
            else:
                flattened[new_key] = value

        return flattened

    def _filter_fields(self, records: List[Dict], fields: List[str]) -> List[Dict]:
        """Filter records to include only specified fields."""
        filtered_records = []

        for record in records:
            filtered_record = {}
            for field in fields:
                if field in record:
                    filtered_record[field] = record[field]
                else:
                    filtered_record[field] = None
            filtered_records.append(filtered_record)

        return filtered_records

    def _write_csv(self, records: List[Dict], output_stream: TextIO) -> None:
        """Write records to CSV format."""
        if not records:
            return

        fieldnames = set()
        for record in records:
            fieldnames.update(record.keys())

        fieldnames = sorted(fieldnames)

        writer = csv.DictWriter(
            output_stream,
            fieldnames=fieldnames,
            delimiter=self.delimiter,
            quoting=csv.QUOTE_MINIMAL,
            escapechar=None,
            lineterminator='\n'
        )

        if not self.no_header:
            writer.writeheader()

        for record in records:
            writer.writerow(record)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert JSON to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json                    # Convert JSON file to CSV
  cat data.json | %(prog)s             # Convert from stdin
  %(prog)s --fields name,age data.json # Select specific fields
  %(prog)s --delimiter ';' data.json   # Use custom delimiter
  %(prog)s --no-header data.json       # Skip header row
  %(prog)s --list-handling index data.json  # Index list items
        """
    )

    parser.add_argument(
        'file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='JSON file to convert (reads from stdin if not provided)'
    )

    parser.add_argument(
        '-d', '--delimiter',
        default=',',
        help='CSV delimiter (default: ,)'
    )

    parser.add_argument(
        '-f', '--fields',
        help='Comma-separated list of fields to include'
    )

    parser.add_argument(
        '-n', '--no-header',
        action='store_true',
        help="Don't output CSV header"
    )

    parser.add_argument(
        '-l', '--list-handling',
        choices=['join', 'index'],
        default='join',
        help="How to handle lists: 'join' or 'index' (default: join)"
    )

    parser.add_argument(
        '-j', '--join-string',
        default='|',
        help='String to join list items with (default: |)'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    if args.fields:
        args.fields = [field.strip() for field in args.fields.split(',')]

    return args


def main():
    """Main entry point."""
    args = None
    try:
        args = parse_arguments()

        converter = JSONToCSVConverter(
            delimiter=args.delimiter,
            fields=args.fields,
            no_header=args.no_header,
            list_handling=args.list_handling,
            join_string=args.join_string
        )

        converter.convert(args.file, sys.stdout)

    except KeyboardInterrupt:
        sys.exit(1)
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if args is not None and hasattr(args, 'file') and args.file != sys.stdin:
            args.file.close()


if __name__ == '__main__':
    main()