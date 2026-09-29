"""
Public portfolio backtest engine for the OI + Flow BUILD_CONT research.

Demonstrates:
- delayed execution assumptions
- transaction costs
- net returns
- win rate
- profit factor
- maximum drawdown

Example trades below are illustrative only.
No private datasets, production thresholds, or credentials are included.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Trade:
    side: str
    entry_price: float
    exit_price: float
    delay_ms: int = 1500


@dataclass
class BacktestConfig:
    starting_equity: float = 10_000.0
    fee_rate: float = 0.0005


def calculate_trade_return(
    trade: Trade,
    fee_rate: float,
) -> float:

    side = trade.side.upper()

    if trade.entry_price <= 0:
        raise ValueError("entry_price must be positive")

    if trade.exit_price <= 0:
        raise ValueError("exit_price must be positive")

    if side == "LONG":
        gross_return = (
            trade.exit_price - trade.entry_price
        ) / trade.entry_price

    elif side == "SHORT":
        gross_return = (
            trade.entry_price - trade.exit_price
        ) / trade.entry_price

    else:
        raise ValueError(
            "side must be LONG or SHORT"
        )

    round_trip_cost = fee_rate * 2

    return gross_return - round_trip_cost


def calculate_max_drawdown(
    equity_curve: List[float],
) -> float:

    if not equity_curve:
        return 0.0

    peak = equity_curve[0]
    max_drawdown = 0.0

    for equity in equity_curve:

        if equity > peak:
            peak = equity

        drawdown = (
            peak - equity
        ) / peak

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def run_backtest(
    trades: List[Trade],
    config: BacktestConfig,
) -> dict:

    equity = config.starting_equity
    equity_curve = [equity]

    wins = 0
    losses = 0

    gross_profit = 0.0
    gross_loss = 0.0

    results = []

    for trade in trades:

        net_return = calculate_trade_return(
            trade=trade,
            fee_rate=config.fee_rate,
        )

        pnl = equity * net_return

        if pnl > 0:
            wins += 1
            gross_profit += pnl

        elif pnl < 0:
            losses += 1
            gross_loss += abs(pnl)

        equity += pnl
        equity_curve.append(equity)

        results.append(
            {
                "side": trade.side,
                "delay_ms": trade.delay_ms,
                "entry_price": trade.entry_price,
                "exit_price": trade.exit_price,
                "net_return_pct": round(
                    net_return * 100,
                    4,
                ),
                "pnl": round(pnl, 2),
                "equity": round(equity, 2),
            }
        )

    total_trades = len(trades)

    win_rate = (
        wins / total_trades
        if total_trades
        else 0.0
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else float("inf")
    )

    max_drawdown = calculate_max_drawdown(
        equity_curve
    )

    total_return = (
        equity / config.starting_equity
    ) - 1

    return {
        "starting_equity": config.starting_equity,
        "final_equity": round(equity, 2),
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate_pct": round(
            win_rate * 100,
            2,
        ),
        "profit_factor": round(
            profit_factor,
            2,
        ),
        "max_drawdown_pct": round(
            max_drawdown * 100,
            2,
        ),
        "total_return_pct": round(
            total_return * 100,
            2,
        ),
        "trades": results,
    }


if __name__ == "__main__":

    config = BacktestConfig(
        starting_equity=10_000,
        fee_rate=0.0005,
    )

    example_trades = [
        Trade(
            side="LONG",
            entry_price=100.0,
            exit_price=102.0,
            delay_ms=1500,
        ),
        Trade(
            side="SHORT",
            entry_price=105.0,
            exit_price=103.5,
            delay_ms=1500,
        ),
        Trade(
            side="LONG",
            entry_price=98.0,
            exit_price=97.0,
            delay_ms=1500,
        ),
    ]

    report = run_backtest(
        trades=example_trades,
        config=config,
    )

    print("BUILD_CONT BACKTEST")
    print("-------------------")

    print(
        f"Trades: "
        f"{report['total_trades']}"
    )

    print(
        f"Win rate: "
        f"{report['win_rate_pct']}%"
    )

    print(
        f"Profit factor: "
        f"{report['profit_factor']}"
    )

    print(
        f"Max drawdown: "
        f"{report['max_drawdown_pct']}%"
    )

    print(
        f"Total return: "
        f"{report['total_return_pct']}%"
    )

    print(
        f"Final equity: "
        f"${report['final_equity']:,.2f}"
    )
