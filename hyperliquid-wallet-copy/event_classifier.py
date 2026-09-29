"""
Classifies position changes into trading events.

Public portfolio version.
Contains no wallet addresses, API keys,
account IDs, or private data.
"""

from enum import Enum


class PositionEvent(str, Enum):
    OPEN = "OPEN"
    ADD = "ADD"
    REDUCE = "REDUCE"
    CLOSE = "CLOSE"
    FLIP = "FLIP"
    NO_CHANGE = "NO_CHANGE"


def classify_position_change(
    previous_notional: float,
    current_notional: float,
    tolerance: float = 1e-9,
) -> PositionEvent:

    prev_zero = abs(previous_notional) <= tolerance
    curr_zero = abs(current_notional) <= tolerance

    if prev_zero and curr_zero:
        return PositionEvent.NO_CHANGE

    if prev_zero and not curr_zero:
        return PositionEvent.OPEN

    if not prev_zero and curr_zero:
        return PositionEvent.CLOSE

    if previous_notional * current_notional < 0:
        return PositionEvent.FLIP

    previous_size = abs(previous_notional)
    current_size = abs(current_notional)

    if current_size > previous_size + tolerance:
        return PositionEvent.ADD

    if current_size < previous_size - tolerance:
        return PositionEvent.REDUCE

    return PositionEvent.NO_CHANGE


if __name__ == "__main__":

    examples = [
        (0, 300),
        (300, 500),
        (500, 200),
        (200, 0),
        (300, -250),
        (-400, -600),
        (-600, -150),
    ]

    for previous, current in examples:
        event = classify_position_change(
            previous_notional=previous,
            current_notional=current,
        )

        print(
            f"{previous:>6} -> "
            f"{current:>6} : "
            f"{event.value}"
        )
