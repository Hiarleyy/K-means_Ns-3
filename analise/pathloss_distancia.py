#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%
df = pd.read_csv(r'../data/csv/DlPathlossTrace.csv',usecols=['IMSI','pathLoss(dB)'])
df
# %%
df_last = df.groupby('IMSI', as_index=False).last()
df_last = df_last.abs()
df_last
# %%
df_first = df.groupby('IMSI', as_index=False).first()
df_first = df_first.abs()
df_last
# %%
distancias_iniciais = [
    217.89, 56.98, 501.99, 400.82, 116.27, 397.65, 264.28, 253.77, 375.25, 449.51,
    210.32, 224.24, 400.50, 425.48, 160.27, 517.97, 456.28, 428.09, 389.09, 387.18]
#%%
distancias_finais =[
    59.90, 120.12, 373.31, 338.54, 103.86, 268.10, 81.10, 91.47, 248.48, 299.47,
    22.81, 82.07, 312.06, 374.43, 43.34, 375.03, 330.78, 299.14, 273.63, 262.60
]
#%%
Dist_users = pd.DataFrame({
    'UE_ID': range(1, len(distancias_iniciais) + 1),
    'Distancia_Inicial': distancias_iniciais,
    'Distancia_Final': distancias_finais
})
Dist_users.to_csv(r'../data/csv/Dist_users.csv', index=False)
#%%
freq_Hz = 28e9  # 100Ghz
c = 3e8  # Velocidade da luz (m/s)
pathloss_inicial_esperado = []

for distancia in distancias_iniciais:
    pathloss = 20 * np.log10(distancia) + 20 * np.log10(freq_Hz) + 20 * np.log10(4 * np.pi / c)
    pathloss_inicial_esperado.append(pathloss)
    print(pathloss)
# %%
freq_Hz = 28e9  # 100Ghz
c = 3e8  # Velocidade da luz (m/s)
pathloss_final_esperado = []

for distancia in distancias_finais:
    pathloss = 20 * np.log10(distancia) + 20 * np.log10(freq_Hz) + 20 * np.log10(4 * np.pi / c)
    pathloss_final_esperado.append(pathloss)
    print(pathloss)
# %%
df_first['Índice'] = range(1, len(df_first) + 1)
indices = np.arange(1, len(df_first) + 1)  # Garantir que os índices sejam compatíveis

# Definir a largura das barras para evitar sobreposição total
largura_barra = 0.4  

# Criar a figura
plt.figure(figsize=(8, 6))

# Plotar Pathloss Simulado (df_first) com um deslocamento para a esquerda
plt.bar(indices - largura_barra/2, df_first['pathLoss(dB)'], width=largura_barra, color='red', label='Pathloss Simulado')

# Plotar Pathloss Esperado (pathloss_inicial_esperado) com um deslocamento para a direita
plt.bar(indices + largura_barra/2, pathloss_inicial_esperado, width=largura_barra, color='blue', label='Pathloss Esperado')

# Adicionar rótulos e título
plt.xlabel('Índice')
plt.ylabel('Pathloss (dB)')
plt.title('Comparação de Pathloss: Simulado vs Esperado (Antenas Iniciais)')
plt.xticks(indices)
plt.legend()  # Adicionar legenda para diferenciar os conjuntos de dados
plt.grid(True)

# Mostrar o gráfico
plt.show()

# %%
df_last['Índice'] = range(1, len(df_last) + 1)
indices = np.arange(1, len(df_last) + 1)  # Garantir que os índices sejam compatíveis

# Definir a largura das barras para evitar sobreposição total
largura_barra = 0.4  

# Criar a figura
plt.figure(figsize=(8, 6))

# Plotar Pathloss Simulado (df_last) com um deslocamento para a esquerda
plt.bar(indices - largura_barra/2, df_last['pathLoss(dB)'], width=largura_barra, color='red', label='Pathloss Simulado')

# Plotar Pathloss Esperado (pathloss_final_esperado) com um deslocamento para a direita
plt.bar(indices + largura_barra/2, pathloss_final_esperado, width=largura_barra, color='blue', label='Pathloss Esperado')

# Adicionar rótulos e título
plt.xlabel('Índice')
plt.ylabel('Pathloss (dB)')
plt.title('Comparação de Pathloss: Simulado vs Esperado (Antenas Otimizadas)')
plt.xticks(indices)
plt.legend()  # Adicionar legenda para diferenciar os conjuntos de dados
plt.grid(True)

# Mostrar o gráfico
plt.show()
# %%
