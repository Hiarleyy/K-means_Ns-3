#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
#%%
# Carregar os dados em um DataFrame
df = pd.read_csv(r'C:\Users\Marcos Hiarley\Documents\GitHub\K-means_Ns-3\data\csv\DlPathlossTrace.csv')
df.head()
# %%
# Obtém os CellIds únicos e ordena-os
unique_cellids = sorted(df['CellId'].unique())

# Listas para armazenar os valores absolutos do pathLoss inicial e final para cada CellId
initial_pathloss = []
final_pathloss = []

for cell_id in unique_cellids:
    # Filtra os registros para o CellId atual e cria cópia para evitar warnings
    filtered_df = df[df['CellId'] == cell_id].copy()
    # Calcula o valor absoluto do pathLoss
    filtered_df['pathLoss_abs'] = filtered_df['pathLoss(dB)'].abs()
    
    # Armazena o primeiro e o último valor de pathLoss_abs
    initial_pathloss.append(filtered_df['pathLoss_abs'].iloc[0])
    final_pathloss.append(filtered_df['pathLoss_abs'].iloc[-1])

# Configurar o gráfico de barras agrupadas
x = np.arange(len(unique_cellids))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, initial_pathloss, width, label='PathLoss Inicial')
rects2 = ax.bar(x + width/2, final_pathloss, width, label='PathLoss Final')

ax.set_xticks(x)
ax.set_xticklabels(unique_cellids)
ax.set_xlabel('CellId')
ax.set_ylabel('PathLoss (dB, valor absoluto)')
ax.set_title('PathLoss Inicial e Final para cada CellId')
ax.legend()
ax.grid(True)

plt.show()
# %%
df['pathLoss_abs'] = df['pathLoss(dB)'].abs()

# Supondo que cada IMSI esteja associado a um único CellId, agrupe e calcule a média do pathLoss_abs para cada IMSI
group_df = df.groupby(['IMSI', 'CellId'])['pathLoss_abs'].mean().reset_index()

# Ordena os dados por CellId (para agrupar visualmente os IMSI de mesmo CellId)
group_df.sort_values(['CellId', 'IMSI'], inplace=True)
group_df.reset_index(drop=True, inplace=True)

# Cria o eixo x como o índice da tabela agrupada
x = np.arange(len(group_df))

# Use um colormap para definir uma cor única para cada CellId
unique_cellids = group_df['CellId'].unique()
cmap = plt.cm.get_cmap('tab10', len(unique_cellids))
# Mapeia cada CellId para uma cor
cellid_colors = {cellid: cmap(i) for i, cellid in enumerate(unique_cellids)}

# Cria um vetor de cores para cada barra, de acordo com o CellId do IMSI
bar_colors = group_df['CellId'].map(cellid_colors)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(x, group_df['pathLoss_abs'], color=bar_colors)

# Configura o eixo x para mostrar o índice de IMSI (ou o próprio identificador de IMSI, se preferir)
ax.set_xticks(x)
ax.set_xticklabels(group_df['IMSI'])
ax.set_xlabel('IMSI')
ax.set_ylabel('Mean PathLoss (dB, valor absoluto)')
ax.set_title('Mean PathLoss por IMSI agrupados por CellId')

# Define um limite superior para o eixo Y
y_max = group_df['pathLoss_abs'].max() * 1.3
ax.set_ylim(0, y_max)

# Cria uma legenda para identificar as cores conforme o CellId
legend_patches = [patches.Patch(color=cellid_colors[cid], label=f'Antena {cid}') for cid in unique_cellids]
ax.legend(handles=legend_patches, title='Antena', bbox_to_anchor=(1.05, 1), loc='upper left')

ax.grid(True)
plt.tight_layout()
plt.show()
# %%
