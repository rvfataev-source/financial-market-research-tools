"""
Proportional position sizing for copy-trading research.

Public portfolio version.
Contains no wallet addresses, API keys,
account IDs, or private data.
"""


def calculate_exposure_ratio(
    source_equity: float,
    source_position_usd: float,
) -> float:
    """
    Calculates what share of the source account
    is allocated to the position.
    """

    if source_equity <= 0:
        raise ValueError(
            "source_equity must be greater than zero"
        )

    return source_position_usd / source_equity


def calculate_target_position(
    source_equity: float,
    source_position_usd: float,
    follower_equity: float,
) -> float:
    """
    Converts the source account exposure
    into a proportional position size
    for the follower account.
    """

    if follower_equity < 0:
        raise ValueError(
            "follower_equity cannot be negative"
        )

    exposure_ratio = calculate_exposure_ratio(
        source_equity=source_equity,
        source_position_usd=source_position_usd,
    )

    return follower_equity * exposure_ratio


def calculate_position_adjustment(
    current_follower_position_usd: float,
    target_follower_position_usd: float,
) -> float:
    """
    Calculates how much the follower position
    needs to change.

    Positive result -> increase
    Negative result -> reduce
    """

    return (
        target_follower_position_usd
        - current_follower_position_usd
    )


if __name__ == "__main__":

    source_equity = 30_000_000
    source_position = 9_000_000

    follower_equity = 1_000
    current_follower_position = 150

    target_position = calculate_target_position(
        source_equity=source_equity,
        source_position_usd=source_position,
        follower_equity=follower_equity,
    )

    adjustment = calculate_position_adjustment(
        current_follower_position_usd=current_follower_position,
        target_follower_position_usd=target_position,
    )

    exposure_percent = (
        calculate_exposure_ratio(
            source_equity,
            source_position,
        )
        * 100
    )

    print(
        f"Source exposure: "
        f"{exposure_percent:.2f}%"
    )

    print(
        f"Follower target position: "
        f"${target_position:.2f}"
    )

    print(
        f"Required adjustment: "
        f"${adjustment:.2f}"
    )
