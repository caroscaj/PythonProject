import argparse
import csv
import os
import re
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clean up a CSV file by removing duplicates and fixing formatting."
    )

    parser.add_argument("-i", "--input", required=True,
                        help="Input CSV file")
    parser.add_argument("-o", "--output", required=True,
                        help="Output cleaned CSV file")

    parser.add_argument("-c", "--column", required=False,
                        help="Column name to check formatting (regex applied)")

    parser.add_argument("-r", "--regex", required=False,
                        help="Regular expression to filter rows in the specified column")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")

    return parser.parse_args()


def read_csv(file_path):
    if not os.path.exists(file_path):
        print(f"ERROR: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def write_csv(file_path, rows, headers):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def clean_csv(rows, column=None, regex=None, verbose=False):
    cleaned = []
    seen = set()

    pattern = re.compile(regex) if regex else None

    for row in rows:
        row_tuple = tuple(row.items())


        if row_tuple in seen:
            continue
        seen.add(row_tuple)

        if pattern and column:
            value = row.get(column, "")
            if not pattern.search(value):
                continue

        cleaned.append(row)

    if verbose:
        print(f"Original rows: {len(rows)}")
        print(f"Cleaned rows:  {len(cleaned)}")

    return cleaned

def main():
    args = parse_arguments()

    rows, headers = read_csv(args.input)

    cleaned_rows = clean_csv(
        rows,
        column=args.column,
        regex=args.regex,
        verbose=args.verbose
    )

    write_csv(args.output, cleaned_rows, headers)

    if args.verbose:
        print(f"Cleaned CSV saved to: {args.output}")


if __name__ == "__main__":
    main()
