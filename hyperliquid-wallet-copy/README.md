# Hyperliquid Wallet Copy System

Research and automation system for identifying successful Hyperliquid wallets and reproducing their trading activity under realistic execution conditions.

## Project Overview

The project was built to answer a practical question:

Can profitable on-chain trading wallets be copied successfully when real execution delay, position sizing, and account-size differences are taken into account?

The research process included screening multiple wallets, analyzing their historical performance, measuring execution latency, and testing whether their trades could be reproduced realistically.

## Key Results

- Identified four wallets that passed the research criteria
- Measured realistic copy latency of approximately 1.5 seconds
- Compared different wallet risk and return profiles
- Tested whether delayed execution materially affected results
- Built a proportional copy-trading system for accounts of different sizes

## Proportional Position Sizing

The bot does not copy the source wallet's absolute dollar position.

Instead, it reproduces the same percentage exposure relative to the follower's own account balance.

Example:

If the source wallet has $30,000,000 and opens a position using 30% of its capital, while the follower account has $1,000, the follower opens a position using approximately 30% of its own capital.

This allows accounts of very different sizes to reproduce the same relative portfolio exposure.

## Trading Actions

The system tracks and reproduces the complete position lifecycle:

- OPEN
- ADD
- REDUCE
- CLOSE
- FLIP

This means the bot follows not only the initial entry but also subsequent changes to the source wallet's position.

## Execution Research

The project also focused on realistic execution conditions, including:

- Signal detection latency
- Copy delay
- Position-size normalization
- Account balance differences
- Changes in exposure after ADD and REDUCE events
- Direction changes through FLIP events
- Risk differences between selected wallets

## Objective

The goal of the project was not simply to identify profitable wallets, but to determine whether their trading behavior could be reproduced systematically and realistically through automation.

> This project is intended for research and educational purposes only.
