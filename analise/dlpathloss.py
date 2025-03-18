#%%
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, simpledialog

def filter_by_rnti(df, imsi_values):
    return {imsi: df[df['IMSI'] == imsi] for imsi in imsi_values}

def analyze_dataframe(df, file_number, freq):
    print(f"\nAnalisando arquivo {file_number} (Frequência: {freq} GHz)...")
    
    # Adiciona a frequência caso não exista na coluna (para o plot, se necessário)
    if 'SignalFrequency' not in df.columns:
        df['SignalFrequency'] = freq
        
    # --- Gráfico 1: Path Loss UlPathlossTrace ---
    imsi_values = df['IMSI'].unique()
    filtered_dfs = filter_by_rnti(df, imsi_values)
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap('tab10', len(imsi_values))
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']
    for i, imsi in enumerate(imsi_values):
        user_df = filtered_dfs[imsi]
        plt.plot(user_df['Time(sec)'], user_df['pathLoss(dB)'],
                 label=f'IMSI {imsi}',
                 color=colors(i),
                 marker=markers[i % len(markers)],
                 linestyle='-', markersize=1)
    plt.title(f'Path Loss UlPathlossTrace - Arquivo {file_number}')
    plt.xlabel('Time (sec)')
    plt.ylabel('Path Loss (dB)')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Gráfico 2: Gráficos individuais para grupos de usuários ---
    num_users = len(imsi_values)
    users_per_plot = 5
    sorted_imsi_values = sorted(imsi_values)
    fixed_colors = ['b', 'g', 'r', 'c', 'm']
    
    for start in range(0, num_users, users_per_plot):
        end = min(start + users_per_plot, num_users)
        fig, axs = plt.subplots(end - start, 1, figsize=(12, 8), sharex=True)
        for i, imsi in enumerate(sorted_imsi_values[start:end]):
            user_df = filtered_dfs[imsi]
            color = fixed_colors[i % len(fixed_colors)]
            axs[i].plot(user_df['Time(sec)'], user_df['pathLoss(dB)'],
                        label=f'IMSI {imsi}', color=color,
                        marker=markers[i % len(markers)],
                        linestyle='-', markersize=1)
            axs[i].set_title(f'Path Loss UlPathlossTrace {imsi}')
            axs[i].set_ylabel('Path Loss (dB)')
            axs[i].legend()
            axs[i].grid(True)
            axs[i].set_ylim(user_df['pathLoss(dB)'].min() - 0.5,
                            user_df['pathLoss(dB)'].max() + 0.5)
            stats_text = f"Min: {user_df['pathLoss(dB)'].min():.2f}\nMax: {user_df['pathLoss(dB)'].max():.2f}\nMean: {user_df['pathLoss(dB)'].mean():.2f}"
            axs[i].text(1.01, 0.5, stats_text, transform=axs[i].transAxes,
                        verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))
        axs[-1].set_xlabel('Time (sec)')
        plt.tight_layout()
        plt.show()
    
    # --- Estatísticas descritivas ---
    df_grouped = df.groupby('IMSI')['pathLoss(dB)'].describe()
    print(df_grouped)
    
    # --- Gráfico 3: Primeiros e últimos valores de pathLoss por IMSI ---
    rows = []
    for imsi in imsi_values:
        user_df = filtered_dfs[imsi]
        first_time = user_df['Time(sec)'].iloc[0]
        first_path_loss = user_df['pathLoss(dB)'].iloc[0]
        last_time = user_df['Time(sec)'].iloc[-1]
        last_path_loss = user_df['pathLoss(dB)'].iloc[-1]
        change_percent = ((last_path_loss - first_path_loss) / first_path_loss) * 100
        rows.append({
            'IMSI': imsi,
            'First Time (sec)': first_time,
            'First Path Loss (dB)': first_path_loss,
            'Last Time (sec)': last_time,
            'Last Path Loss (dB)': last_path_loss,
            'Change (%)': change_percent
        })
    first_last_pathloss = pd.DataFrame(rows)
    print(first_last_pathloss)
    
    plt.figure(figsize=(12, 8))
    plt.bar(first_last_pathloss['IMSI'].astype(str), first_last_pathloss['Change (%)'], color='skyblue')
    plt.title(f'Change in Path Loss for Each IMSI - Arquivo {file_number}')
    plt.xlabel('IMSI')
    plt.ylabel('Change in Path Loss (%)')
    plt.grid(True, axis='y')
    for i, row in first_last_pathloss.iterrows():
        plt.text(i, row['Change (%)'] + 0.5, f"{row['Change (%)']:.2f}%", ha='center', va='bottom')
    plt.show()
    
    # --- Gráfico 4: Relação entre IMSI e CellId ao longo do tempo ---
    plt.figure(figsize=(12, 8))
    for imsi in imsi_values:
        user_df = filtered_dfs[imsi]
        plt.plot(user_df['Time(sec)'], user_df['CellId'],
                 label=f'IMSI {imsi}', marker='o', linestyle='-', markersize=1)
        cellid_changes = user_df['CellId'].diff().fillna(0) != 0
        plt.scatter(user_df['Time(sec)'][cellid_changes], user_df['CellId'][cellid_changes],
                    color='red', zorder=5)
    plt.title(f'IMSI to CellId Over Time - Arquivo {file_number}')
    plt.xlabel('Time (sec)')
    plt.ylabel('CellId')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Estatísticas de CellId ---
    print(df['CellId'].value_counts())
    cellid_imsi_grouped = df.groupby(['CellId', 'IMSI']).size().reset_index(name='Count')
    print(cellid_imsi_grouped)
    
    # --- Gráfico 5: Path Loss UlPathlossTrace para CellId 3 ---
    filtered_df_3 = df[df['CellId'] == 3]
    filtered_imsi_values_3 = filtered_df_3['IMSI'].unique()
    filtered_dfs_3 = filter_by_rnti(filtered_df_3, filtered_imsi_values_3)
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap('tab10', len(filtered_imsi_values_3))
    for i, imsi in enumerate(filtered_imsi_values_3):
        user_df = filtered_dfs_3[imsi]
        plt.plot(user_df['Time(sec)'], user_df['pathLoss(dB)'],
                 label=f'IMSI {imsi}', color=colors(i),
                 marker=markers[i % len(markers)], linestyle='-', markersize=1)
    plt.title(f'Path Loss for CellId 3 - Arquivo {file_number}')
    plt.xlabel('Time (sec)')
    plt.ylabel('Path Loss (dB)')
    plt.legend(title='Users')
    plt.grid(True)
    plt.show()
    
    # --- Gráfico 6: Primeiros e últimos valores de pathLoss para todos os CellId ---
    all_rows = []
    cellid_values = df['CellId'].unique()
    
    def calculate_first_last_pathloss(cell_id, filtered_dfs):
        rows = []
        for imsi in filtered_dfs.keys():
            user_df = filtered_dfs[imsi]
            first_time = user_df['Time(sec)'].iloc[0]
            first_path_loss = user_df['pathLoss(dB)'].iloc[0]
            last_time = user_df['Time(sec)'].iloc[-1]
            last_path_loss = user_df['pathLoss(dB)'].iloc[-1]
            change_percent = ((last_path_loss - first_path_loss) / first_path_loss) * 100
            rows.append({
                'CellId': cell_id,
                'IMSI': imsi,
                'First Time (sec)': first_time,
                'First Path Loss (dB)': first_path_loss,
                'Last Time (sec)': last_time,
                'Last Path Loss (dB)': last_path_loss,
                'Change (%)': change_percent
            })
        return rows

    for cell_id in cellid_values:
        filtered_df = df[df['CellId'] == cell_id]
        filtered_imsi_values = filtered_df['IMSI'].unique()
        filtered_dfs_temp = filter_by_rnti(filtered_df, filtered_imsi_values)
        all_rows.extend(calculate_first_last_pathloss(cell_id, filtered_dfs_temp))
    
    first_last_pathloss_all = pd.DataFrame(all_rows)
    
    plt.figure(figsize=(12, 8))
    for cell_id in cellid_values:
        cell_df = first_last_pathloss_all[first_last_pathloss_all['CellId'] == cell_id]
        plt.bar(cell_df['IMSI'].astype(str), cell_df['Change (%)'], label=f'CellId {cell_id}')
    plt.title(f'Change in Path Loss for Each IMSI (All CellId) - Arquivo {file_number}')
    plt.xlabel('IMSI')
    plt.ylabel('Change in Path Loss (%)')
    plt.legend(title='CellId')
    for i, row in first_last_pathloss_all.iterrows():
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
# Processa as médias de pathLoss por CellId para cada arquivo CSV selecionado
# Combina as médias de pathLoss por CellId de todos os arquivos em um único DataFrame
combined_means = pd.DataFrame()

for idx, df in enumerate(data_frames, start=1):
    # Get unique CellIds and sort them
    cell_ids = sorted(df['CellId'].unique())
    
    # Create a mapping from actual CellIds to sequential numbers (1, 2, 3...)
    cell_id_mapping = {cell_id: i+1 for i, cell_id in enumerate(cell_ids)}
    
    # Calculate means by actual CellId
    antenna_means = df.groupby('CellId')['pathLoss(dB)'].mean().abs()
    
    # Create a new Series with sequential indices
    sequential_means = pd.Series(index=range(1, len(cell_ids)+1))
    for cell_id in cell_ids:
        sequential_means[cell_id_mapping[cell_id]] = antenna_means[cell_id]
    
    freq = frequencies[idx-1]
    combined_means[f'{freq} GHz'] = sequential_means

print("\nMédias de PathLoss Absolutas por Antena")
print(combined_means)

# Plotagem do gráfico de barras agrupadas para todos os arquivos
ax = combined_means.plot(kind='bar', figsize=(12, 7))
plt.xlabel('Antenas')
plt.ylabel('Média Absoluta do Pathloss (dB)')
plt.title('Média Absoluta do Pathloss por Antena')
plt.grid(axis='y')

# Centraliza a legenda abaixo do gráfico com tamanho reduzido
plt.legend(title='Frequência', 
           loc='upper center', 
           bbox_to_anchor=(0.5, -0.12),
           ncol=min(len(frequencies), 3),  # Distribui as frequências em até 3 colunas
           fontsize='small',
           frameon=True,
           framealpha=0.7)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # Ajusta o layout para acomodar a legenda
plt.show()
# %%
df = pd.read_csv("/home/br4b0/Desktop/PIBIC/K-means_Ns-3/analise/data/28GHZ/DlPathlossTrace.csv")
df['CellId'].value_counts()
# %%
