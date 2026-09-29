"""
Public portfolio version of a Hyperliquid wallet-copy latency simulation.

This file contains no wallet addresses, API keys, account IDs,
private endpoints, or live order execution.

The simulation models:
- OPEN
- ADD
- REDUCE
- CLOSE
- FLIP
- proportional position sizing
- 1500 ms execution latency
- taker fees

Historical delayed execution prices are expected to be prepared
from public market data before running the simulation.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


LATENCY_MS = 1500
INITIAL_FOLLOWER_EQUITY = 1_000.0

# Example fee only.
# Replace with the fee assumption used in a specific research run.
TAKER_FEE_RATE = 0.0005


@dataclass
class LeaderEvent:
    observed_ts_ms: int
    symbol: str
    action: str

    # Leader account value near the event.
    leader_equity_usd: float

    # Signed position notional AFTER the leader action.
    # Positive = long
    # Negative = short
    # Zero = closed
    leader_position_after_usd: float

    # Historical executable price measured around T + 1500 ms.
    delayed_exec_price: float


@dataclass
class Position:
    qty: float = 0.0
    avg_price: float = 0.0
    realized_pnl: float = 0.0
    fees_paid: float = 0.0

    def unrealized_pnl(self, mark_price: float) -> float:
        if self.qty == 0:
            return 0.0

        return self.qty * (mark_price - self.avg_price)

    def apply_trade(
        self,
        delta_qty: float,
        price: float,
        fee_rate: float,
    ) -> None:
        if delta_qty == 0:
            return

        trade_notional = abs(delta_qty * price)
        self.fees_paid += trade_notional * fee_rate

        # No existing position -> open.
        if self.qty == 0:
            self.qty = delta_qty
            self.avg_price = price
            return

        old_qty = self.qty
        new_qty = old_qty + delta_qty

        # Same direction -> ADD.
        if old_qty * delta_qty > 0:
            old_notional = abs(old_qty) * self.avg_price
            added_notional = abs(delta_qty) * price

            self.qty = new_qty
            self.avg_price = (
                old_notional + added_notional
            ) / abs(new_qty)

            return

        # Trade is reducing, closing, or flipping.
        closing_qty = min(abs(old_qty), abs(delta_qty))

        if old_qty > 0:
            # Closing/reducing a long.
            self.realized_pnl += closing_qty * (
                price - self.avg_price
            )
        else:
            # Closing/reducing a short.
            self.realized_pnl += closing_qty * (
                self.avg_price - price
            )

        self.qty = new_qty

        # Fully closed.
        if self.qty == 0:
            self.avg_price = 0.0
            return

        # FLIP: remaining position is now in opposite direction.
        if old_qty * self.qty < 0:
            self.avg_price = price


class LatencyCopySimulator:
    def __init__(
        self,
        initial_equity: float = INITIAL_FOLLOWER_EQUITY,
        latency_ms: int = LATENCY_MS,
        fee_rate: float = TAKER_FEE_RATE,
    ):
        self.initial_equity = initial_equity
        self.latency_ms = latency_ms
        self.fee_rate = fee_rate

        self.position = Position()
        self.last_mark_price = 0.0

    def follower_equity(self, mark_price: float) -> float:
        return (
            self.initial_equity
            + self.position.realized_pnl
            + self.position.unrealized_pnl(mark_price)
            - self.position.fees_paid
        )

    def target_notional(
        self,
        event: LeaderEvent,
        follower_equity: float,
    ) -> float:
        if event.leader_equity_usd <= 0:
            raise ValueError("leader_equity_usd must be positive")

        exposure_ratio = (
            event.leader_position_after_usd
            / event.leader_equity_usd
        )

        return follower_equity * exposure_ratio

    def process_event(self, event: LeaderEvent) -> dict:
        action = event.action.upper()

        if action not in {
            "OPEN",
            "ADD",
            "REDUCE",
            "CLOSE",
            "FLIP",
        }:
            raise ValueError(f"Unsupported action: {action}")

        exec_ts_ms = (
            event.observed_ts_ms
            + self.latency_ms
        )

        price = event.delayed_exec_price

        if price <= 0:
            raise ValueError(
                "delayed_exec_price must be positive"
            )

        self.last_mark_price = price

        equity_before = self.follower_equity(price)

        # The follower mirrors the leader's relative exposure,
        # not the leader's absolute dollar size.
        target_notional_usd = self.target_notional(
            event,
            equity_before,
        )

        current_notional_usd = (
            self.position.qty * price
        )

        notional_change_usd = (
            target_notional_usd
            - current_notional_usd
        )

        delta_qty = (
            notional_change_usd / price
        )

        qty_before = self.position.qty

        self.position.apply_trade(
            delta_qty=delta_qty,
            price=price,
            fee_rate=self.fee_rate,
        )

        equity_after = self.follower_equity(price)

        return {
            "symbol": event.symbol,
            "action": action,
            "observed_ts_ms": event.observed_ts_ms,
            "simulated_exec_ts_ms": exec_ts_ms,
            "latency_ms": self.latency_ms,
            "exec_price": round(price, 6),
            "follower_equity_before": round(
                equity_before,
                2,
            ),
            "target_notional_usd": round(
                target_notional_usd,
                2,
            ),
            "qty_before": round(qty_before, 8),
            "qty_after": round(
                self.position.qty,
                8,
            ),
            "realized_pnl": round(
                self.position.realized_pnl,
                2,
            ),
            "fees_paid": round(
                self.position.fees_paid,
                2,
            ),
            "follower_equity_after": round(
                equity_after,
                2,
            ),
        }


def load_events(csv_path: str) -> list[LeaderEvent]:
    """
    Expected CSV columns:

    observed_ts_ms
    symbol
    action
    leader_equity_usd
    leader_position_after_usd
    delayed_exec_price

    No wallet address is required.
    """

    events: list[LeaderEvent] = []

    with open(
        csv_path,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            events.append(
                LeaderEvent(
                    observed_ts_ms=int(
                        row["observed_ts_ms"]
                    ),
                    symbol=row["symbol"],
                    action=row["action"],
                    leader_equity_usd=float(
                        row["leader_equity_usd"]
                    ),
                    leader_position_after_usd=float(
                        row[
                            "leader_position_after_usd"
                        ]
                    ),
                    delayed_exec_price=float(
                        row["delayed_exec_price"]
                    ),
                )
            )

    return events


def run_simulation(csv_path: str) -> None:
    simulator = LatencyCopySimulator()

    events = load_events(csv_path)

    print(
        f"Loaded {len(events)} anonymized events"
    )
    print(
        f"Fixed execution latency: "
        f"{LATENCY_MS} ms"
    )
    print()

    for event in events:
        result = simulator.process_event(event)
        print(result)

    if simulator.last_mark_price:
        final_equity = simulator.follower_equity(
            simulator.last_mark_price
        )
    else:
        final_equity = simulator.initial_equity

    print()
    print("Simulation complete")
    print(
        f"Initial equity: "
        f"${simulator.initial_equity:,.2f}"
    )
    print(
        f"Realized PnL: "
        f"${simulator.position.realized_pnl:,.2f}"
    )
    print(
        f"Fees paid: "
        f"${simulator.position.fees_paid:,.2f}"
    )
    print(
        f"Final simulated equity: "
        f"${final_equity:,.2f}"
    )


if __name__ == "__main__":
    INPUT_FILE = Path(
        "anonymized_events.csv"
    )

    if not INPUT_FILE.exists():
        print(
            "No anonymized_events.csv found."
        )
        print()
        print(
            "Create an anonymized historical event "
            "file before running the simulation."
        )
        print(
            "Do not include wallet addresses, "
            "API keys, or private account data."
        )
    else:
        run_simulation(str(INPUT_FILE))
