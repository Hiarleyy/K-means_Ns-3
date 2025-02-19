#%%
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Carregar os dados em um DataFrame
df = pd.read_csv('datasets/DlPathlossTrace.txt', sep="\t")

# Normalização Min-Max
scaler_minmax = MinMaxScaler()
df["pathLoss_MinMax"] = scaler_minmax.fit_transform(df[["pathLoss(dB)"]])

# Normalização Z-score
scaler_zscore = StandardScaler()
df["pathLoss_Zscore"] = scaler_zscore.fit_transform(df[["pathLoss(dB)"]])

# Exibir as primeiras linhas com os valores normalizados
df.head()

# %%
