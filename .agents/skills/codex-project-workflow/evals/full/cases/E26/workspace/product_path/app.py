import argparse

from product.commands import create_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--shape", default="cube")
    parser.add_argument("--output", required=True)
    parser.add_argument("--state", default="runtime/state.json")
    parser.add_argument("--trace", default="runtime/trace.log")
    args = parser.parse_args()
    create_model(
        name=args.name,
        shape=args.shape,
        output=args.output,
        state_path=args.state,
        trace_path=args.trace,
    )


if __name__ == "__main__":
    main()
