import argparse
import io
from contextlib import contextmanager
from typing import Iterator, TextIO

import readchar
import requests


def print_with_speed(text: TextIO, speed: int) -> None:
    while readchar.readchar():
        chars = text.read(speed)
        if not chars:
            break

        print(chars, end="", flush=True)


@contextmanager
def open_file(file: str) -> Iterator[TextIO]:
    if file.startswith("http://") or file.startswith("https://"):
        response = requests.get(file)
        response.raise_for_status()

        yield io.StringIO(response.text)
    else:
        with open(file) as f:
            yield f


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("--speed", "-s", type=int, default=1)

    args = parser.parse_args()

    with open_file(args.file) as f:
        print_with_speed(f, args.speed)


if __name__ == "__main__":
    main()
