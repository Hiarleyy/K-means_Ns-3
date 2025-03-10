#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%
df = pd.read_csv(r'C:\Users\Marcos Hiarley\Documents\GitHub\K-means_Ns-3\data\csv\RxPacketTrace.csv')
df

#%%
df['rnti'].value_counts()

#%%
df['Time']
# %%
# Função para filtrar DataFrame por rnti
def filter_by_rnti(df, rnti_values):
    return {rnti: df[df['rnti'] == rnti] for rnti in rnti_values}

rnti_values = range(1,2,3)  # p/ 2 usuarios
filtered_dfs = filter_by_rnti(df, rnti_values)

plt.figure(figsize=(10, 6))

for rnti in rnti_values:
    user_df = filtered_dfs[rnti]
    plt.plot(user_df['Time'], user_df['SINR(dB)'], label=str(rnti))

plt.title('SINR rate (2 users)')
plt.xlabel('time(s)')
plt.ylabel('SINR(dB)')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize='medium', title='Users', title_fontsize='large')
plt.tight_layout()
plt.show()
# %%
plt.figure(figsize=(10, 6))

rnti_values = df['rnti'].unique()
for rnti in rnti_values:
    user_df = df[df['rnti'] == rnti]
    plt.plot(user_df['Time'], user_df['CQI'], label=f'RNTI {rnti}')

plt.title('CQI over time')
plt.xlabel('time(s)')
plt.ylabel('CQI')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
plt.tight_layout()
plt.show()
# %%
CQI_medio1 = df[df['cellId'] == 1].groupby('rnti')['CQI'].mean().reset_index()
CQI_medio1
#%%
CQI_medio2 = df[df['cellId'] == 3].groupby('rnti')['CQI'].mean().reset_index()
CQI_medio2
#%%
CQI_medio3 = df[df['cellId'] == 5].groupby('rnti')['CQI'].mean().reset_index()
CQI_medio3
#%%
CQI_medio4 = df[df['cellId'] == 7].groupby('rnti')['CQI'].mean().reset_index()
CQI_medio4
#%%
plt.plot(df['Time'], df['CQI']) 
plt.title('CQI over time')
plt.xlabel('time(s)')
plt.ylabel('CQI')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
plt.tight_layout()
plt.show()
#%%
df = pd.DataFrame(CQI_medio1)  # ou qualquer outro DataFrame correspondente

otimo = df[(df['CQI'] > 20)].shape[0]
bom = df[(df['CQI'] > 15) & (df['CQI'] < 25)].shape[0]
medio = df[(df['CQI'] < 15) & (df['CQI'] > 10)].shape[0]
ruim = df[(df['CQI'] < 10) & (df['CQI'] > 0)].shape[0]
pessimo = df[df['CQI'] < 0].shape[0]

# Listas originais de labels e sizes
labels = ['BOM(>15)', 'MÉDIO(15-10)', 'ÓTIMO(>20)', 'RUIM(<10)', 'PESSIMO(<0)']
sizes = [bom, medio, otimo, ruim, pessimo]

# Filtra apenas as categorias com valores > 0
filtered = [(label, size) for label, size in zip(labels, sizes) if size > 0]
if filtered:
    filtered_labels, filtered_sizes = zip(*filtered)
else:
    filtered_labels, filtered_sizes = [], []
# Cria o gráfico de setores usando as listas filtradas
plt.figure(figsize=(8, 6))
plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
plt.title('CQI MÉDIO POR RNTI - ENB1')
plt.show()
#%%
df = pd.DataFrame(CQI_medio2)  # ou qualquer outro DataFrame correspondente

otimo = df[(df['CQI'] > 20)].shape[0]
bom = df[(df['CQI'] > 15) & (df['CQI'] < 25)].shape[0]
medio = df[(df['CQI'] < 15) & (df['CQI'] > 10)].shape[0]
ruim = df[(df['CQI'] < 10) & (df['CQI'] > 0)].shape[0]
pessimo = df[df['CQI'] < 0].shape[0]

# Listas originais de labels e sizes
labels = ['BOM(>15)', 'MÉDIO(15-10)', 'ÓTIMO(>20)', 'RUIM(<10)', 'PESSIMO(<0)']
sizes = [bom, medio, otimo, ruim, pessimo]

# Filtra apenas as categorias com valores > 0
filtered = [(label, size) for label, size in zip(labels, sizes) if size > 0]
if filtered:
    filtered_labels, filtered_sizes = zip(*filtered)
else:
    filtered_labels, filtered_sizes = [], []
# Cria o gráfico de setores usando as listas filtradas
plt.figure(figsize=(8, 6))
plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
plt.title('CQI MÉDIO POR RNTI - ENB2')
plt.show()
# %%
df = pd.DataFrame(CQI_medio3)  # ou qualquer outro DataFrame correspondente

otimo = df[(df['CQI'] > 20)].shape[0]
bom = df[(df['CQI'] > 15) & (df['CQI'] < 25)].shape[0]
medio = df[(df['CQI'] < 15) & (df['CQI'] > 10)].shape[0]
ruim = df[(df['CQI'] < 10) & (df['CQI'] > 0)].shape[0]
pessimo = df[df['CQI'] < 0].shape[0]

# Listas originais de labels e sizes
labels = ['BOM(>15)', 'MÉDIO(15-10)', 'ÓTIMO(>20)', 'RUIM(<10)', 'PESSIMO(<0)']
sizes = [bom, medio, otimo, ruim, pessimo]

# Filtra apenas as categorias com valores > 0
filtered = [(label, size) for label, size in zip(labels, sizes) if size > 0]
if filtered:
    filtered_labels, filtered_sizes = zip(*filtered)
else:
    filtered_labels, filtered_sizes = [], []
# Cria o gráfico de setores usando as listas filtradas
plt.figure(figsize=(8, 6))
plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
plt.title('CQI MÉDIO POR RNTI - ENB3')
plt.show()
#%%
df = pd.DataFrame(CQI_medio4)  # ou qualquer outro DataFrame correspondente

otimo = df[(df['CQI'] > 20)].shape[0]
bom = df[(df['CQI'] > 15) & (df['CQI'] < 25)].shape[0]
medio = df[(df['CQI'] < 15) & (df['CQI'] > 10)].shape[0]
ruim = df[(df['CQI'] < 10) & (df['CQI'] > 0)].shape[0]
pessimo = df[df['CQI'] < 0].shape[0]

# Listas originais de labels e sizes
labels = ['BOM(>15)', 'MÉDIO(15-10)', 'ÓTIMO(>20)', 'RUIM(<10)', 'PESSIMO(<0)']
sizes = [bom, medio, otimo, ruim, pessimo]

# Filtra apenas as categorias com valores > 0
filtered = [(label, size) for label, size in zip(labels, sizes) if size > 0]
if filtered:
    filtered_labels, filtered_sizes = zip(*filtered)
else:
    filtered_labels, filtered_sizes = [], []
# Cria o gráfico de setores usando as listas filtradas
plt.figure(figsize=(8, 6))
plt.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
plt.title('CQI MÉDIO POR RNTI - ENB4')
plt.show()
# %%
