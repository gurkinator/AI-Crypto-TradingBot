import ccxt
import pandas as pd
import ta
import numpy as np

def run_backtest():
    # --- MAXIMERADE INSTÄLLNINGAR ---
    symbol = 'XRP/USDT'
    timeframe = '15m'      
    start_balance = 100.0  
    low_risk_size = 1.00   # BOOST: Satsar 100% av saldot för maximal avkastning!
    
    print(f"Hämtar data för {symbol} ({timeframe})...")
    exchange = ccxt.kucoin({'enableRateLimit': True})
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1500)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    except Exception as e:
        print(f"Fel vid datahämtning: {e}")
        return

    print("Beräknar indikatorer...")
    df['rsi_14'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    df = df.dropna().reset_index(drop=True)
    
    balance_usdt = start_balance
    crypto_held = 0.0
    trades_count = 0
    winning_trades = 0
    peak_balance = start_balance
    max_drawdown = 0.0
    balance_history = []

    print("Kör historisk simulering (MAX POWER)...")
    
    for i in range(1, len(df)):
        current_price = df['close'].iloc[i]
        rsi_val = df['rsi_14'].iloc[i]
        
        total_portfolio_value = balance_usdt + (crypto_held * current_price)
        balance_history.append(total_portfolio_value)
        
        if total_portfolio_value > peak_balance:
            peak_balance = total_portfolio_value
            
        drawdown = (peak_balance - total_portfolio_value) / peak_balance * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        # KÖP: RSI under 45
        if crypto_held == 0.0 and rsi_val < 45:
            usdt_to_spend = balance_usdt * low_risk_size
            if usdt_to_spend > 1.0:
                buy_price = current_price
                crypto_held = usdt_to_spend / buy_price
                balance_usdt -= usdt_to_spend
                trades_count += 1

        # SÄLJ: RSI över 55
        elif crypto_held > 0.0 and rsi_val > 55:
            sell_price = current_price
            returned_usdt = crypto_held * sell_price
            balance_usdt += returned_usdt
            crypto_held = 0.0
            if sell_price > buy_price:
                winning_trades += 1

    if crypto_held > 0.0:
        balance_usdt += crypto_held * df['close'].iloc[-1]
        if df['close'].iloc[-1] > buy_price:
            winning_trades += 1
        crypto_held = 0.0

    final_balance = balance_usdt
    total_return_pct = ((final_balance - start_balance) / start_balance) * 100
    win_rate = (winning_trades / trades_count * 100) if trades_count > 0 else 0.0

    print("\n" + "="*40)
    print("📋 SLUTRAPPORT: MAXIMERAD AVKASTNING")
    print("="*40)
    print(f"Handelspar:          {symbol}")
    print(f"Startbalans:         {start_balance:.2f} USDT")
    print(f"Slutbalans:          {final_balance:.2f} USDT ({total_return_pct:+.2f}%)")
    print(f"Totalt antal affärer: {trades_count}")
    print(f"Vinstprocent (Win Rate): {win_rate:.1f}%")
    print(f"Maximal svacka (Max Drawdown): {max_drawdown:.2f}%")
    print("="*40)

if __name__ == "__main__":
    run_backtest()