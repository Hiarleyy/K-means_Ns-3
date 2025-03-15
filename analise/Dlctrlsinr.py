#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog

def filter_by_rnti(df, rnti_values):
    return {rnti: df[df['RNTI'] == rnti] for rnti in rnti_values}

def analyze_dataframe(df, file_number, freq):
    print(f"\nAnalisando arquivo {file_number} (Frequência: {freq} GHz)...")
    
    # Adiciona a frequência caso não exista na coluna (para o plot, se necessário)
    if 'SignalFrequency' not in df.columns:
        df['SignalFrequency'] = freq
        
    # --- Gráfico 1: SINR UlTrace ---
    rnti_values = df['RNTI'].unique()
    filtered_dfs = filter_by_rnti(df, rnti_values)
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap('tab10', len(rnti_values))
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']
    for i, rnti in enumerate(rnti_values):
        user_df = filtered_dfs[rnti]
        plt.plot(user_df['Time'], user_df['SINR(dB)'],
                 label=f'RNTI {rnti}',
                 color=colors(i),
                 marker=markers[i % len(markers)],
                 linestyle='-', markersize=1)
    plt.title(f'SINR UlTrace - Arquivo {file_number}')
    plt.xlabel('Time')
    plt.ylabel('SINR (dB)')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Gráfico 2: Gráficos individuais para grupos de usuários ---
    num_users = len(rnti_values)
    users_per_plot = 5
    sorted_rnti_values = sorted(rnti_values)
    fixed_colors = ['b', 'g', 'r', 'c', 'm']
    
    for start in range(0, num_users, users_per_plot):
        end = min(start + users_per_plot, num_users)
        fig, axs = plt.subplots(end - start, 1, figsize=(12, 8), sharex=True)
        for i, rnti in enumerate(sorted_rnti_values[start:end]):
            user_df = filtered_dfs[rnti]
            color = fixed_colors[i % len(fixed_colors)]
            axs[i].plot(user_df['Time'], user_df['SINR(dB)'],
                        label=f'RNTI {rnti}', color=color,
                        marker=markers[i % len(markers)],
                        linestyle='-', markersize=1)
            axs[i].set_title(f'SINR Trace {rnti}')
            axs[i].set_ylabel('SINR (dB)')
            axs[i].legend()
            axs[i].grid(True)
            axs[i].set_ylim(user_df['SINR(dB)'].min() - 0.5,
                            user_df['SINR(dB)'].max() + 0.5)
            stats_text = f"Min: {user_df['SINR(dB)'].min():.2f}\nMax: {user_df['SINR(dB)'].max():.2f}\nMean: {user_df['SINR(dB)'].mean():.2f}"
            axs[i].text(1.01, 0.5, stats_text, transform=axs[i].transAxes,
                        verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))
        axs[-1].set_xlabel('Time')
        plt.tight_layout()
        plt.show()
    
    # --- Estatísticas descritivas ---
    df_grouped = df.groupby('RNTI')['SINR(dB)'].describe()
    print(df_grouped)
    
    # --- Gráfico 3: Primeiros e últimos valores de SINR por RNTI ---
    rows = []
    for rnti in rnti_values:
        user_df = filtered_dfs[rnti]
        first_time = user_df['Time'].iloc[0]
        first_sinr = user_df['SINR(dB)'].iloc[0]
        last_time = user_df['Time'].iloc[-1]
        last_sinr = user_df['SINR(dB)'].iloc[-1]
        change_percent = ((last_sinr - first_sinr) / first_sinr) * 100
        rows.append({
            'RNTI': rnti,
            'First Time': first_time,
            'First SINR (dB)': first_sinr,
            'Last Time': last_time,
            'Last SINR (dB)': last_sinr,
            'Change (%)': change_percent
        })
    first_last_sinr = pd.DataFrame(rows)
    print(first_last_sinr)
    
    plt.figure(figsize=(12, 8))
    plt.bar(first_last_sinr['RNTI'].astype(str), first_last_sinr['Change (%)'], color='skyblue')
    plt.title(f'Change in SINR for Each RNTI - Arquivo {file_number}')
    plt.xlabel('RNTI')
    plt.ylabel('Change in SINR (%)')
    plt.grid(True, axis='y')
    for i, row in first_last_sinr.iterrows():
        plt.text(i, row['Change (%)'] + 0.5, f"{row['Change (%)']:.2f}%", ha='center', va='bottom')
    plt.show()
    
    # --- Gráfico 4: Relação entre RNTI e CellId ao longo do tempo ---
    plt.figure(figsize=(12, 8))
    for rnti in rnti_values:
        user_df = filtered_dfs[rnti]
        plt.plot(user_df['Time'], user_df['CellId'],
                 label=f'RNTI {rnti}', marker='o', linestyle='-', markersize=1)
        cellid_changes = user_df['CellId'].diff().fillna(0) != 0
        plt.scatter(user_df['Time'][cellid_changes], user_df['CellId'][cellid_changes],
                    color='red', zorder=5)
    plt.title(f'RNTI to CellId Over Time - Arquivo {file_number}')
    plt.xlabel('Time')
    plt.ylabel('CellId')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Estatísticas de CellId ---
    print(df['CellId'].value_counts())
    cellid_rnti_grouped = df.groupby(['CellId', 'RNTI']).size().reset_index(name='Count')
    print(cellid_rnti_grouped)
    
    # --- Gráfico 5: SINR Trace para CellId 3 ---
    filtered_df_3 = df[df['CellId'] == 3]
    filtered_rnti_values_3 = filtered_df_3['RNTI'].unique()
    filtered_dfs_3 = filter_by_rnti(filtered_df_3, filtered_rnti_values_3)
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap('tab10', len(filtered_rnti_values_3))
    for i, rnti in enumerate(filtered_rnti_values_3):
        user_df = filtered_dfs_3[rnti]
        plt.plot(user_df['Time'], user_df['SINR(dB)'],
                 label=f'RNTI {rnti}', color=colors(i),
                 marker=markers[i % len(markers)], linestyle='-', markersize=1)
    plt.title(f'SINR for CellId 3 - Arquivo {file_number}')
    plt.xlabel('Time')
    plt.ylabel('SINR (dB)')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Gráfico 6: Primeiros e últimos valores de SINR para todos os CellId ---
    all_rows = []
    cellid_values = df['CellId'].unique()
    
    def calculate_first_last_sinr(cell_id, filtered_dfs):
        rows = []
        for rnti in filtered_dfs.keys():
            user_df = filtered_dfs[rnti]
            first_time = user_df['Time'].iloc[0]
            first_sinr = user_df['SINR(dB)'].iloc[0]
            last_time = user_df['Time'].iloc[-1]
            last_sinr = user_df['SINR(dB)'].iloc[-1]
            change_percent = ((last_sinr - first_sinr) / first_sinr) * 100
            rows.append({
                'CellId': cell_id,
                'RNTI': rnti,
                'First Time': first_time,
                'First SINR (dB)': first_sinr,
                'Last Time': last_time,
                'Last SINR (dB)': last_sinr,
                'Change (%)': change_percent
            })
        return rows

    for cell_id in cellid_values:
        filtered_df = df[df['CellId'] == cell_id]
        filtered_rnti_values = filtered_df['RNTI'].unique()
        filtered_dfs_temp = filter_by_rnti(filtered_df, filtered_rnti_values)
        all_rows.extend(calculate_first_last_sinr(cell_id, filtered_dfs_temp))
    
    first_last_sinr_all = pd.DataFrame(all_rows)
    
    plt.figure(figsize=(12, 8))
    for cell_id in cellid_values:
        cell_df = first_last_sinr_all[first_last_sinr_all['CellId'] == cell_id]
        plt.bar(cell_df['RNTI'].astype(str), cell_df['Change (%)'], label=f'CellId {cell_id}')
    plt.title(f'Change in SINR for Each RNTI (All CellId) - Arquivo {file_number}')
    plt.xlabel('RNTI')
    plt.ylabel('Change in SINR (%)')
    plt.legend(title='CellId')
    for i, row in first_last_sinr_all.iterrows():
        plt.text(i, row['Change (%)'] + 0.5, f"{row['Change (%)']:.2f}%", ha='center', va='bottom', fontsize=8)
    plt.show()

# Início do script de seleção de arquivos
root = tk.Tk()
root.withdraw()

num_files = simpledialog.askinteger("Input", "Quantos arquivos deseja selecionar?", minvalue=1)
data_frames = []
frequencies = []

for i in range(num_files):
    freq = simpledialog.askfloat("Input", f"Digite a frequência do sinal (GHz) para o arquivo {i+1}:")
    frequencies.append(freq)
    
    file_path = filedialog.askopenfilename(
        title=f"Selecione o arquivo {i+1}",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    
    if file_path:
        df_temp = pd.read_csv(file_path)
        df_temp['SignalFrequency'] = freq
        data_frames.append(df_temp)

if not data_frames:
    print("Nenhum arquivo foi selecionado.")
    exit()

# Processa cada arquivo separadamente
for idx, df in enumerate(data_frames, start=1):
    analyze_dataframe(df, file_number=idx, freq=frequencies[idx-1])

# %%
# Processa as médias de SINR por CellId para cada arquivo CSV selecionado
# Combina as médias de SINR por CellId de todos os arquivos em um único DataFrame
combined_means = pd.DataFrame()

for idx, df in enumerate(data_frames, start=1):
    antenna_means = df.groupby('CellId')['SINR(dB)'].mean().abs().sort_index()
    freq = frequencies[idx-1]
    combined_means[f'{freq} GHz'] = antenna_means

combined_means = combined_means.sort_index()
print("\nMédias Absolutas de SINR por Antena - Todos os Arquivos:")
print(combined_means)

# Plotagem do gráfico de barras agrupadas para todos os arquivos
combined_means.plot(kind='bar', figsize=(10,6))
plt.xlabel('Antena (CellId)')
plt.ylabel('Média Absoluta do SINR (dB)')
plt.title('Média Absoluta do SINR por Antena - Todos os Arquivos')
plt.grid(axis='y')
plt.legend(title='Frequência')
plt.show()
# %%
df = pd.read_csv("/home/br4b0/Desktop/PIBIC/K-means_Ns-3/analise/data/28GHZ/DlPathlossTrace.csv")
df['CellId'].value_counts()
# %%
