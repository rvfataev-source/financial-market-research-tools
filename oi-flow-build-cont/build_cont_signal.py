"""
Public portfolio version of an OI + Flow continuation signal.

The original research combined:
- abnormal price movement
- Open Interest expansion
- aggressive taker flow

This public version demonstrates the signal structure without exposing
private production thresholds, datasets, credentials, or execution logic.
"""

from dataclasses import dataclass
from enum import Enum


class Signal(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NONE = "NONE"


@dataclass
class MarketSnapshot:
    price_change_pct: float
    oi_change_pct: float

    # Positive values = aggressive buying
    # Negative values = aggressive selling
    taker_flow_ratio: float


@dataclass
class SignalConfig:
    """
    Illustrative thresholds for the public version.

    These values are examples and are not intended to represent
    private production parameters from the research system.
    """

    min_price_shock_pct: float = 0.75
    min_oi_expansion_pct: float = 1.00
    min_taker_flow_ratio: float = 0.20


def detect_build_cont_signal(
    snapshot: MarketSnapshot,
    config: SignalConfig,
) -> Signal:

    oi_expanding = (
        snapshot.oi_change_pct
        >= config.min_oi_expansion_pct
    )

    if not oi_expanding:
        return Signal.NONE

    long_setup = (
        snapshot.price_change_pct
        >= config.min_price_shock_pct
        and snapshot.taker_flow_ratio
        >= config.min_taker_flow_ratio
    )

    short_setup = (
        snapshot.price_change_pct
        <= -config.min_price_shock_pct
        and snapshot.taker_flow_ratio
        <= -config.min_taker_flow_ratio
    )

    if long_setup:
        return Signal.LONG

    if short_setup:
        return Signal.SHORT

    return Signal.NONE


if __name__ == "__main__":

    config = SignalConfig()

    examples = [
        MarketSnapshot(
            price_change_pct=1.20,
            oi_change_pct=1.80,
            taker_flow_ratio=0.35,
        ),
        MarketSnapshot(
            price_change_pct=-1.10,
            oi_change_pct=1.60,
            taker_flow_ratio=-0.30,
        ),
        MarketSnapshot(
            price_change_pct=0.30,
            oi_change_pct=0.40,
            taker_flow_ratio=0.10,
        ),
    ]

    for index, snapshot in enumerate(
        examples,
        start=1,
    ):
        signal = detect_build_cont_signal(
            snapshot=snapshot,
            config=config,
        )

        print(
            f"Example {index}: "
            f"price={snapshot.price_change_pct:+.2f}% | "
            f"OI={snapshot.oi_change_pct:+.2f}% | "
            f"flow={snapshot.taker_flow_ratio:+.2f} | "
            f"signal={signal.value}"
        )
