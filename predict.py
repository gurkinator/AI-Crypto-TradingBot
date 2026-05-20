import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

def train_gpu_model(df):
    print("🧠 Initierar GPU-accelererad mönsteranalys via RTX 4070 Ti Super...")
    
    # Skapa tekniska särdrag (features) för din AI att lära sig av
    df['rsi'] = pd.Series(df['close']).diff().rolling(14).mean() # Enkel RSI-vektor
    df['price_change'] = df['close'].pct_change()
    
    # Skapa ett facit (Target): Gick priset upp nästa timme? (1 = Ja, 0 = Nej)
    df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    df = df.dropna()
    
    X = df[['rsi', 'price_change', 'open', 'high', 'low', 'close', 'volume']]
    y = df['target']
    
    # Dela upp i träningsdata och testdata
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Initiera XGBoost specifikt konfigurerat för Nvidias CUDA (GPU)
    model = XGBClassifier(
        tree_method='hist',
        device='cuda', # Tvingar beräkningen till ditt RTX 4070 Ti Super
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05
    )
    
    # Träna modellen blixtsnabbt på ditt VRAM
    model.fit(X_train, y_train)
    
    # Beräkna träffsäkerhet på testdatan
    accuracy = model.score(X_test, y_test) * 100
    print(f"✅ AI-Träning klar! Träffsäkerhet på historisk testdata: {accuracy:.2f}%")
    
    # Förutsäg nästa rörelse (Sannolikhet i procent)
    last_row = X.iloc[[-1]]
    prediction_proba = model.predict_proba(last_row)[0][1] * 100
    
    return prediction_proba