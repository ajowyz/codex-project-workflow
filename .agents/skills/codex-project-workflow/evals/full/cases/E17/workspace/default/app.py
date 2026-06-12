import argparse

from reading_list import ReadingList


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    add = subparsers.add_parser("add")
    add.add_argument("url")
    subparsers.add_parser("list")
    return parser


def main():
    args = build_parser().parse_args()
    reading_list = ReadingList()
    if args.command == "add":
        reading_list.add(args.url)
        print(f"added: {args.url}")
    else:
        for item in reading_list.items():
            print(item)


if __name__ == "__main__":
    main()
