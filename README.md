# Gurks Advanced AI Trading Bot

> Early beta KuCoin trading bot. Use at your own risk. Never trade with money you are not prepared to lose.

Gurks Advanced AI Trading Bot is a Streamlit-based crypto trading dashboard for KuCoin spot trading. It combines live monitoring, Swing/Day trading modes, strategy scanning, Top 3 strategy suggestions, Telegram reporting, persistent position memory and risk-aware optimization.

This project is in active beta. Unknown bugs can exist. Start with tiny amounts, test in simulation/mock mode first, and review every setting before enabling live trading.

## Exchange Support

- Supported now: KuCoin spot trading through `ccxt`.
- Planned later: Binance and other major exchanges.

## Main Features

- Streamlit web UI with English/Swedish language switching.
- KuCoin API integration for balances, market data and live spot orders.
- Swing Trading and Day Trading modes with separate capital frames and position memory.
- Independent Swing/Day live control, so one mode or both modes can run.
- Persistent open-position tracking through `open_positions.json`, designed to survive hard restarts.
- Compact active holdings/open positions panel under the System Event Log.
- Live market watcher with RSI, EMA, Bollinger Bands, MACD, volume, ATR, regime/sentiment filters, grid logic, trailing stop loss, cooldowns and max-position checks.
- Time-exit protection that can block fee-eating exits near break-even.
- Background strategy scanner with rolling Top 250 leaderboard and Top 3 strategy cards.
- Bayesian/Optuna-ready optimization support.
- Walk-Forward Analysis and risk-adjusted metrics: Fitness, Sharpe, Sortino, Max Drawdown and out-of-sample result.
- Weighted/randomized scan variation, designed to add exploration without ignoring relevance and scoring.
- Telegram status reports, trade alerts, scan summaries, strategy alerts and optional notification controls.
- Optional login wall with PBKDF2-SHA256 hashed passwords. Login is off by default unless the user enables it.
- KCS fee-model support for KuCoin fee discount modeling.
- Runtime files are auto-created on first startup when missing.

## Current UI Panels

- Simulator and controls.
- Live configuration.
- System Event Log.
- Active holdings / open positions.
- Historical Profit Chart.
- Market Chart.
- ROI Dashboard.
- Time-of-day performance.
- False Positive Analyzer.
- Advanced AI Market Optimization.
- Telegram alert configuration.
- Swing/Day Top 3 strategy cards.
- Settings and Strategy dialog.
- Help section.

## Active Holdings / Open Positions

The active holdings panel is placed directly under the System Event Log. It is intentionally lightweight.

It shows, per open bot position:

- Symbol/pair.
- Entry price.
- Current cached price.
- PnL in percent and USDT.
- Time since buy.
- Trading mode and strategy/version.
- Current trend/regime.
- Confidence/score.
- Stop loss and take profit levels.
- Trailing stop status.
- Grid sell level.
- Time-exit status.
- Latest important signal.
- Next expected exit signal.
- Why the bot is still holding the position.
- Sell conditions required for exit.

The panel does not fetch KuCoin data during UI rendering. It uses cached live watcher data and `open_positions.json` so it should not materially affect scan throughput or UI responsiveness.

## KCS Fee Discount Model

KuCoin can reduce trading fees if your KuCoin account is configured to pay fees with KCS.

What you must do manually:

1. Log in to KuCoin.
2. Enable KuCoin's account setting for paying trading fees with KCS.
3. Keep a small KCS balance on the account.
4. In the bot, enable the KCS fee model only if your KuCoin account actually uses KCS fee deduction.

Suggested reserve:

- Light testing: about 5-10 USDT worth of KCS.
- Active day trading: about 10-25+ USDT worth of KCS.

What the bot does:

- Models scans, backtests, Top 3, mock tests and PnL using the configured fee model.
- Tries to read actual fee information from KuCoin orders when the API returns it.
- Can warn when the estimated KCS reserve is low.

What the bot cannot guarantee:

- It cannot force KuCoin to use KCS for fees per order through `ccxt`.
- If your KCS reserve runs out, KuCoin may charge normal fees instead.
- Changing the fee model later does not rewrite old exchange fills.

## Important Risk Notice

This bot can place real orders when live trading is enabled and valid KuCoin API keys are configured.

You are responsible for:

- API key permissions and IP restrictions.
- Exchange account security.
- Understanding the strategy settings.
- Monitoring open positions.
- KuCoin fees, spread, slippage and liquidity.
- Verifying behavior with small amounts before using meaningful capital.

Recommended first run:

1. Start without API keys, or with read-only keys if you only want to inspect UI behavior.
2. Use mock/simulation mode first.
3. Configure Telegram and send a test message.
4. Run Test Live Settings.
5. Run a small background scan.
6. Review Top 3 and active holdings behavior.
7. Only then enable live trading with very small capital.

## Hardware Requirements

The bot can start on small machines, but strategy scanning is CPU-heavy. Weak hardware can make the UI feel slow.

Practical minimum worth using:

- CPU: 4 vCPU / 4 logical cores.
- RAM: 8 GB.
- Storage: 30+ GB SSD/NVMe.
- OS: Ubuntu 24.04 VPS or Windows 10/11.
- Network: stable internet connection.

Recommended for live trading plus normal scanning:

- CPU: 8 vCPU.
- RAM: 16-24 GB.
- Storage: 80+ GB NVMe preferred.
- Network: stable VPS connection, ideally accessed through Tailscale/VPN.

Recommended for heavy/Brutal VPS scanning:

- CPU: 16 vCPU.
- RAM: 32-64 GB.
- Storage: 150+ GB NVMe.
- Network: stable 1 Gbit/s VPS network.

More CPU mainly improves background scanning. It does not guarantee better trades. Always reserve enough CPU for Streamlit, live watcher, balance updates and order handling.

## Installation

### Windows

1. Download or clone this folder.
2. Open the folder containing `bot.py`.
3. Double-click `install_dependencies.bat`.
4. Copy `example.env` to `.env`.
5. Fill in your own KuCoin and Telegram values.
6. Start the bot:

```bat
venv\Scripts\activate
streamlit run bot.py --server.address 0.0.0.0 --server.port 8501
```

### Ubuntu 24.04 VPS

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git screen

cd /path/to/your/bot/folder
chmod +x install_dependencies.sh
./install_dependencies.sh

cp example.env .env
nano .env

screen -S tradingbot
source venv/bin/activate
streamlit run bot.py --server.address 0.0.0.0 --server.port 8501
```

Detach from `screen` with `CTRL+A`, then `D`.

## Environment Variables

Required for live KuCoin trading:

- `KUCOIN_API_KEY`
- `KUCOIN_SECRET` or `KUCOIN_API_SECRET`
- `KUCOIN_PASSPHRASE`, `KUCOIN_API_PASSWORD` or `KUCOIN_PASSWORD`

Required for Telegram:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Optional runtime/performance controls:

- `BOT_UI_RESERVED_CORES`
- `BOT_OPT_MAX_WORKERS`
- `BOT_OPT_WORKERS_FORCE`
- `BOT_DISABLE_LOGIN`
- `BOT_DISABLE_AUTORUN`

## Files Safe To Commit

- `bot.py`
- `predict.py`
- `backtest.py`
- `README.md`
- `requirements.txt`
- `DEPENDENCIES.txt`
- `HOW_TO_GET_STARTED.txt`
- `HARDWARE_REQUIREMENTS.txt`
- `FILES_TO_UPLOAD.txt`
- `example.env`
- `install_dependencies.bat`
- `install_dependencies.sh`
- `.gitignore`

## Do Not Commit Private Or Runtime Files

- `.env`
- `secure_auth.json`
- `secure_keys.json`
- `bot_config.json`
- `trade_history.csv`
- `event_logs.txt`
- `open_positions.json`
- `optimization_results.csv`
- `opt_progress.txt`
- `opt_stop.txt`
- `opt_engine_status.json`
- `opt_processpool_errors.txt`
- `analysis_status.json`
- `telegram_report_state.json`
- `portfolio_snapshots.json`
- `strategy_alert_snapshot.json`
- `live_strategy_baseline.json`
- `strategy_live_performance.json`
- `mode_capital_state.json`
- `last_trade_state.json`
- `trade_reasons.jsonl`
- `bot_runtime_state.json`
- `strategy_versions.json`
- `missed_opportunities.jsonl`
- `data_quality_report.json`
- `false_positive_report.json`
- `suppressed_errors.log`
- `__pycache__/`
- `venv/`

## Upcoming Development Roadmap

Planned future work discussed for the project:

- Stronger multiprocessing/shared-memory scan engine.
- More advanced RAM-accelerated indicator cache.
- Smarter AI market-regime models.
- Better portfolio/risk engine.
- More exchange connectors, starting with Binance.
- More robust mobile UI and lighter live-refresh paths.
- Expanded KCS fee monitoring and optional cautious KCS top-up logic.
- More strategy analytics and scan-quality diagnostics.

Feedback and bug reports are appreciated. This is beta software and real user testing is valuable.
