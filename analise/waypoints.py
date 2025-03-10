#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados
df_pathloss = pd.read_csv(r'C:\Users\Marcos Hiarley\Documents\GitHub\K-means_Ns-3\data\csv\DlPathlossTrace.csv')
group_1_pathloss = df_pathloss.groupby('IMSI').get_group(6).abs()

df_dist = pd.read_csv(r'C:\Users\Marcos Hiarley\Documents\GitHub\K-means_Ns-3\data\csv\Dist_users.csv')
group_1 = df_dist.groupby('UE_ID').get_group(6)

# Criar array de distâncias interpoladas
num_samples = len(group_1_pathloss)
arr = np.linspace(group_1['Distancia_Inicial'].values[0], group_1['Distancia_Final'].values[0], num_samples)

# Converter distâncias para km para os modelos ITU
arr_km = arr / 1000  

# Frequência de operação
freq_hz = 100e9  # 100 GHz
freq_ghz = freq_hz / 1e9  # Convertendo para GHz

# 1️ FSPL (Free Space Path Loss)
def calcular_fspl(distancia_m, frequencia_hz):
    c = 3e8  # Velocidade da luz (m/s)
    fspl_db = 20 * np.log10(distancia_m) + 20 * np.log10(frequencia_hz) + 20 * np.log10(4 * np.pi / c)
    return fspl_db

# 2️ ITU-R P.528 (propagação para ondas milimétricas)
def itu_r_p528(dist_km, freq_ghz):
    Afs = 20 * np.log10(dist_km) + 20 * np.log10(freq_ghz) + 92.45  # Perda no espaço livre
    return Afs

# 3️ ITU-R P.676 (Atenuação Atmosférica por Oxigênio e Vapor d’Água)
def itu_r_p676(dist_km, freq_ghz):
    gamma_o = 0.4  # dB/km (oxigênio)
    gamma_w = 0.05  # dB/km (vapor d'água)
    atenuacao_total = (gamma_o + gamma_w) * dist_km
    return atenuacao_total

# Calcular os valores de path loss
fspl_values = calcular_fspl(arr, freq_hz)
itu_p528_values = itu_r_p528(arr_km, freq_ghz)
itu_p676_values = itu_r_p676(arr_km, freq_ghz)

# Pegamos a coluna correta de Path Loss do dataset
pathloss_column = group_1_pathloss.iloc[:, -1]  # Última coluna assumindo que seja Path Loss

# Garantir que os tamanhos sejam iguais
if len(arr) > len(pathloss_column):
    arr = arr[:len(pathloss_column)]
    fspl_values = fspl_values[:len(pathloss_column)]
    itu_p528_values = itu_p528_values[:len(pathloss_column)]
    itu_p676_values = itu_p676_values[:len(pathloss_column)]
elif len(arr) < len(pathloss_column):
    pathloss_column = pathloss_column[:len(arr)]

# Plotando os modelos de Path Loss
plt.figure(figsize=(10, 6))
plt.plot(arr, fspl_values, color="b", linestyle="-", label="FSPL (100 GHz)")
plt.plot(arr, itu_p528_values, color="g", linestyle="--", label="ITU-R P.528")
plt.plot(arr, itu_p676_values, color="m", linestyle="-.", label="ITU-R P.676 (Atenuação Atmosférica)")
plt.scatter(arr, pathloss_column, color="r", s=10, label="Dados Simulados")

plt.xlabel("Distância (m)")
plt.ylabel("Path Loss (dB)")
plt.title("Path Loss vs Distância (100 GHz)")
plt.legend()
plt.grid()
plt.show()

# %%
