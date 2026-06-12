import argparse
import json

from src.report import render_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--include-zero", action="store_true")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as handle:
        records = json.load(handle)
    print(render_report(records, include_zero=args.include_zero))


if __name__ == "__main__":
    main()
