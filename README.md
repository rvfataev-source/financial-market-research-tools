# Financial Market Research Tools

Python-based research and automation projects focused on cryptocurrency market structure, wallet analysis, copy-trading automation, backtesting, and execution research.

## Featured Projects

### Hyperliquid Wallet Copy System

Built a research and automation system for identifying successful Hyperliquid wallets and reproducing their trading activity under realistic execution conditions.

The project included:

- Screening and comparing active trading wallets
- Analyzing wallet performance and risk profiles
- Measuring realistic copy latency of approximately 1.5 seconds
- Replaying wallet activity with execution-delay constraints
- Identifying four wallets that passed the research criteria
- Comparing higher-return and lower-risk trading profiles

### Proportional Copy-Trading Bot

Developed a bot that automatically mirrors the full trading cycle of a selected wallet while adapting position size to the follower's own account balance.

Instead of copying absolute dollar amounts, the system calculates exposure proportionally.

Example:

If the source wallet allocates 30% of its capital to a position, the follower account also allocates approximately 30% of its available capital.

The system tracks and reproduces trading actions including:

- OPEN
- ADD
- REDUCE
- CLOSE
- FLIP

Position sizing is dynamically adjusted to the follower's deposit, allowing accounts of very different sizes to follow the same relative exposure model.

The project focused on preserving the source wallet's trading behavior while accounting for realistic latency, execution constraints, and account-size differences.

---

### OI + FLOW BUILD_CONT

Developed and tested a Binance Futures continuation model based on the interaction between:

- Price shocks
- Open Interest expansion
- Aggressive taker flow

The system was designed to identify situations where positioning and order flow supported continuation after an abnormal market move.

Research included:

- Historical market-data processing
- Open Interest analysis
- Taker-flow analysis
- Automated signal generation
- Out-of-sample backtesting
- Transaction-cost modeling
- Execution-delay testing
- Risk and performance analysis
- Shadow monitoring of live market conditions

The model retained positive performance in historical out-of-sample testing under delayed-entry and transaction-cost assumptions.

## Additional Research

Other research and automation work includes:

- Cryptocurrency market-data collection through exchange APIs
- Strategy backtesting
- Technical indicator research
- Risk and leverage analysis
- Automated performance analysis
- Exchange announcement monitoring
- Market-event research
- AI-assisted strategy development
- Rapid prototyping of research tools and trading automation

## Tech

Python · Exchange APIs · Market Data · Backtesting · Automation · Data Analysis · AI-Assisted Development

## Research Approach

My approach is focused on turning a trading or market hypothesis into a measurable workflow:

Idea → Data Collection → Automation → Historical Testing → Latency & Cost Modeling → Risk Analysis → Validation

The objective is to determine whether a strategy or automation concept remains viable under realistic execution conditions rather than relying only on theoretical results.

> This repository is intended for research and educational purposes only. It does not provide financial advice.
