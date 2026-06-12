import argparse

from product.storage import write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--shape", default="cube")
    parser.add_argument("--output", required=True)
    parser.add_argument("--state", default="runtime/state.json")
    parser.add_argument("--trace", default="runtime/trace.log")
    args = parser.parse_args()
    write_json(
        args.output,
        {"name": args.name, "shape": args.shape, "version": 1},
    )


if __name__ == "__main__":
    main()
