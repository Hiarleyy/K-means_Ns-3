#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog

#%%
# Carregar os dados em DataFrames separados e associar a respectiva frequência
root = tk.Tk()
root.withdraw()  # Esconde a janela principal do tkinter

num_files = simpledialog.askinteger("Input", "Quantos arquivos deseja selecionar?", minvalue=1)

data_frames = []
frequencies = []

for i in range(num_files):
    freq = simpledialog.askfloat("Input", f"Digite a frequência do sinal para o arquivo {i+1}:")
    frequencies.append(freq)
    
    file_path = filedialog.askopenfilename(
        title=f"Selecione o arquivo {i+1}",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    
    if file_path:
        df_temp = pd.read_csv(file_path)
        df_temp['SignalFrequency'] = freq
        data_frames.append(df_temp)

# Verifica se há dados para analisar
if not data_frames:
    print("Nenhum arquivo foi selecionado.")
    exit()

#%%
# Loop para realizar a análise para cada arquivo separadamente
for idx, df in enumerate(data_frames):
    freq = frequencies[idx]
    
    # Análise 1: Gráfico de barras para pathLoss inicial e final por CellId
    # Calcula o valor absoluto do pathLoss e obtém os CellIds únicos
    df['pathLoss_abs'] = df['pathLoss(dB)'].abs()
    unique_cellids = sorted(df['CellId'].unique())
    
    initial_pathloss = []
    final_pathloss = []
    
    for cell_id in unique_cellids:
        filtered_df = df[df['CellId'] == cell_id].copy()
        filtered_df['pathLoss_abs'] = filtered_df['pathLoss(dB)'].abs()
        initial_pathloss.append(filtered_df['pathLoss_abs'].iloc[0])
        final_pathloss.append(filtered_df['pathLoss_abs'].iloc[-1])
    
    x = np.arange(len(unique_cellids))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, initial_pathloss, width, label='PathLoss Inicial')
    rects2 = ax.bar(x + width/2, final_pathloss, width, label='PathLoss Final')

    ax.set_xticks(x)
    ax.set_xticklabels(unique_cellids)
    ax.set_xlabel('CellId')
    ax.set_ylabel('PathLoss (dB, valor absoluto)')
    ax.set_title(f'PathLoss Inicial e Final para cada CellId | Frequência: {freq} MHz')
    ax.legend()
    ax.grid(True)
    
    plt.show()
    
    #%%
    # Análise 2: Média do pathLoss_abs por IMSI agrupado por CellId
    group_df = df.groupby(['IMSI', 'CellId'])['pathLoss_abs'].mean().reset_index()
    group_df.sort_values(['CellId', 'IMSI'], inplace=True)
    group_df.reset_index(drop=True, inplace=True)
    
    x = np.arange(len(group_df))
    
    unique_cellids_group = group_df['CellId'].unique()
    cmap = plt.cm.get_cmap('tab10', len(unique_cellids_group))
    cellid_colors = {cellid: cmap(i) for i, cellid in enumerate(unique_cellids_group)}
    bar_colors = group_df['CellId'].map(cellid_colors)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(x, group_df['pathLoss_abs'], color=bar_colors)
    
    ax.set_xticks(x)
    ax.set_xticklabels(group_df['IMSI'])
    ax.set_xlabel('IMSI')
    ax.set_ylabel('Mean PathLoss (dB, valor absoluto)')
    ax.set_title(f'Mean PathLoss por IMSI agrupados por CellId | Frequência: {freq} MHz')
    
    y_max = group_df['pathLoss_abs'].max() * 1.3
    ax.set_ylim(0, y_max)
    
    legend_patches = [patches.Patch(color=cellid_colors[cid], label=f'Antena {cid}') for cid in unique_cellids_group]
    ax.legend(handles=legend_patches, title='Antena', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    ax.grid(True)
    plt.tight_layout()
    plt.show()
# %%
