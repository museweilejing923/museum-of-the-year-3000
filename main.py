#!/usr/bin/env python3
"""Museum label writer: an everyday object, catalogued in the year 3000.

LABEL describes a house key the way a future curator would: object,
year, then the baffled explanation. The guards in GUARDS are small
functions that answer True when the label is acceptable; check() runs
them in order and the label only reaches /output/entry.txt if all of
them say yes.
"""

import sys

LABEL = "House key, 2025. A small metal stick humans carried everywhere, terrified of being locked out of their own homes."
CHAR_LIMIT = 200
OUT_PATH = "/output/entry.txt"
CLOSING = (".", "!", "?")
PUNCT_CHARS = set(".,!?;:'\"-() ")


def refuse(note):
    print(f"invalid label: {note}", file=sys.stderr)
    raise SystemExit(1)


def guard_present(text):
    return bool(text and text.strip())


def guard_length(text):
    return len(text) <= CHAR_LIMIT


def guard_no_controls(text):
    return all(ord(mark) >= 32 for mark in text)


def guard_spacing(text):
    return text == text.strip() and "  " not in text and "\n" not in text


def guard_letters(text):
    return any(mark.isalpha() for mark in text)


def guard_not_punct(text):
    return not all(mark in PUNCT_CHARS for mark in text)


def guard_not_digits(text):
    return not text.strip().isdigit()


def guard_ending(text):
    return text.rstrip().endswith(CLOSING)


def guard_has_year(text):
    for word in text.replace(",", "").split():
        cleaned = word.strip(".,!?")
        if cleaned.isdigit() and len(cleaned) == 4:
            return True
    return False


def guard_no_edge_hyphen(text):
    # A label that opens or closes on a hyphen looks unfinished, like a
    # sentence the curator walked away from mid-word.
    return not text.startswith("-") and not text.rstrip().endswith("-")


GUARDS = [
    ("label is empty", guard_present),
    ("label is over the 200 character limit", guard_length),
    ("label has control characters", guard_no_controls),
    ("label has leading/trailing/double spaces or a newline", guard_spacing),
    ("label has no letters", guard_letters),
    ("label is only punctuation", guard_not_punct),
    ("label is only digits", guard_not_digits),
    ("label must end with punctuation", guard_ending),
    ("a museum label must carry the object's year", guard_has_year),
    ("a label must not start or end with a hyphen", guard_no_edge_hyphen),
]


def check(text):
    for note, guard in GUARDS:
        if not guard(text):
            refuse(note)


def main():
    check(LABEL)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(LABEL + "\n")


if __name__ == "__main__":
    main()
