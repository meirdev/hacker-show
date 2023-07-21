import argparse
import random
import sys
import time
from dataclasses import dataclass

import blessed

MASK_CHAR_TABLE = [
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "\u00c7",
    "\u00fc",
    "\u00e9",
    "\u00e2",
    "\u00e4",
    "\u00e0",
    "\u00e5",
    "\u00e7",
    "\u00ea",
    "\u00eb",
    "\u00e8",
    "\u00ef",
    "\u00ee",
    "\u00ec",
    "\u00c4",
    "\u00c5",
    "\u00c9",
    "\u00e6",
    "\u00c6",
    "\u00f4",
    "\u00f6",
    "\u00f2",
    "\u00fb",
    "\u00f9",
    "\u00ff",
    "\u00d6",
    "\u00dc",
    "\u00a2",
    "\u00a3",
    "\u00a5",
    "\u20a7",
    "\u0192",
    "\u00e1",
    "\u00ed",
    "\u00f3",
    "\u00fa",
    "\u00f1",
    "\u00d1",
    "\u00aa",
    "\u00ba",
    "\u00bf",
    "\u2310",
    "\u00ac",
    "\u00bd",
    "\u00bc",
    "\u00a1",
    "\u00ab",
    "\u00bb",
    "\u2591",
    "\u2592",
    "\u2593",
    "\u2502",
    "\u2524",
    "\u2561",
    "\u2562",
    "\u2556",
    "\u2555",
    "\u2563",
    "\u2551",
    "\u2557",
    "\u255d",
    "\u255c",
    "\u255b",
    "\u2510",
    "\u2514",
    "\u2534",
    "\u252c",
    "\u251c",
    "\u2500",
    "\u253c",
    "\u255e",
    "\u255f",
    "\u255a",
    "\u2554",
    "\u2569",
    "\u2566",
    "\u2560",
    "\u2550",
    "\u256c",
    "\u2567",
    "\u2568",
    "\u2564",
    "\u2565",
    "\u2559",
    "\u2558",
    "\u2552",
    "\u2553",
    "\u256b",
    "\u256a",
    "\u2518",
    "\u250c",
    "\u2588",
    "\u2584",
    "\u258c",
    "\u2590",
    "\u2580",
    "\u03b1",
    "\u00df",
    "\u0393",
    "\u03c0",
    "\u03a3",
    "\u03c3",
    "\u00b5",
    "\u03c4",
    "\u03a6",
    "\u0398",
    "\u03a9",
    "\u03b4",
    "\u221e",
    "\u03c6",
    "\u03b5",
    "\u2229",
    "\u2261",
    "\u00b1",
    "\u2265",
    "\u2264",
    "\u2320",
    "\u2321",
    "\u00f7",
    "\u2248",
    "\u00b0",
    "\u2219",
    "\u00b7",
    "\u221a",
    "\u207f",
    "\u00b2",
    "\u25a0",
]

TYPE_EFFECT_SPEED = 0.004
JUMBLE_SECONDS = 2.0
JUMBLE_LOOP_SPEED = 0.035
REVEAL_LOOP_SPEED = 0.050


@dataclass
class Char:
    source: str
    mask: str
    time: float
    is_space: bool = False


def rand() -> int:
    return random.randint(0, sys.maxsize)


def put(ch: str) -> None:
    print(ch, end="", flush=True)


def rand_mask() -> str:
    return random.choice(MASK_CHAR_TABLE)


def sneakers_effect(
    text: str,
    type_effect_speed: float,
    jumble_seconds: float,
    jumble_loop_speed: float,
    reveal_loop_speed: float,
) -> None:
    chars = [
        Char(
            source=ch,
            mask=rand_mask(),
            time=float(random.randint(0, 5)),
            is_space=ch.isspace(),
        )
        for ch in text
    ]

    term = blessed.Terminal()

    with term.fullscreen(), term.hidden_cursor():
        put(term.home + term.clear_eos)

        for char in chars:
            if char.is_space:
                put(char.source)
            else:
                put(char.mask)
                time.sleep(type_effect_speed)

        term.getch()

        for _ in range(int(jumble_seconds // jumble_loop_speed)):
            put(term.home + term.clear_eos)

            for char in chars:
                put(char.source if char.is_space else rand_mask())

            time.sleep(jumble_loop_speed)

        revealed = False

        while not revealed:
            put(term.home + term.clear_eos)

            revealed = True

            for char in chars:
                if char.is_space:
                    put(char.source)
                    continue

                if char.time > 0:
                    if char.time < 0.5 and rand() % 3 == 0 or rand() % 10 == 0:
                        put(rand_mask())
                    else:
                        put(char.mask)

                    char.time -= reveal_loop_speed
                    revealed = False
                else:
                    put(f"{term.bold}{term.blue}{char.source}{term.normal}")

            time.sleep(reveal_loop_speed)

        term.getch()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType())
    parser.add_argument(
        "--type-effect-speed", "-s", type=float, default=TYPE_EFFECT_SPEED
    )
    parser.add_argument("--jumble-seconds", "-j", type=float, default=JUMBLE_SECONDS)
    parser.add_argument(
        "--jumble-loop-speed", "-l", type=float, default=JUMBLE_LOOP_SPEED
    )
    parser.add_argument(
        "--reveal-loop-speed", "-r", type=float, default=REVEAL_LOOP_SPEED
    )

    args = parser.parse_args()

    sneakers_effect(
        args.file.read(),
        args.type_effect_speed,
        args.jumble_seconds,
        args.jumble_loop_speed,
        args.reveal_loop_speed,
    )


if __name__ == "__main__":
    main()
