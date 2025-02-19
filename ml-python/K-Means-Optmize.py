#%%
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment
#%%
# Gerando dados simulados para a localização de usuários
n_users = 20
np.random.seed(20) ## NAO TIRAR A SEED PELO AMOR DE DEUS
x_users = np.random.uniform(0, 500, n_users)  # Coordenada X dos usuários
y_users = np.random.uniform(0, 500, n_users)  # Coordenada Y dos usuários
user_locations = np.array(list(zip(x_users, y_users)))
user_ids = [f'Ue{i}' for i in range(n_users)]
user_positions_df = pd.DataFrame(user_locations, columns=['Posição X', 'Posição Y'])
user_positions_df['ID'] = user_ids
user_positions_df = user_positions_df[['ID', 'Posição X', 'Posição Y']]
user_positions_df[['Posição X', 'Posição Y']] = user_positions_df[['Posição X', 'Posição Y']].round(2)

user_positions_df.to_csv('user_positions.csv', index=False)

antenna_positions_before = np.array([[0,50],[500,500]])

n_antennas = antenna_positions_before.shape[0]
kmeans = KMeans(n_clusters=n_antennas)
kmeans.fit(user_locations)

antenna_positions_after = kmeans.cluster_centers_
labels = kmeans.labels_

# Calcula a matriz de custo (distâncias Euclidianas) entre as posições iniciais e os centros dos clusters
cost_matrix = np.linalg.norm(antenna_positions_before[:, np.newaxis] - antenna_positions_after, axis=2)
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Reordena os centros dos clusters para que cada antena inicial (por índice) receba a posição otimizada correspondente
antenna_positions_after_ordered = np.empty_like(antenna_positions_after)
for r, c in zip(row_ind, col_ind):
    antenna_positions_after_ordered[r] = antenna_positions_after[c]

print('Posicionamento das antenas antes da otimização:')
for i, pos in enumerate(antenna_positions_before):
    print(f'Antena {i+1}: {pos}')
print('=====================================')
print('Posicionamento otimizado das antenas (pareado):')
for i, pos in enumerate(antenna_positions_after_ordered):
    print(f'Antena {i+1}: {pos}')
#%%
plt.figure(figsize=(10, 8))
plt.scatter(x_users, y_users, c=labels, cmap='viridis', s=50, label="Usuários")
for i, (x, y) in enumerate(zip(x_users, y_users)):
    plt.text(x, y, f'UE {i}', fontsize=9, ha='right')  # Alterado de i+1 para i

# Visualizando os resultados
plt.figure(figsize=(10, 8))
plt.scatter(x_users, y_users, c=labels, cmap='viridis', s=50, label="Usuários")
for i, (x, y) in enumerate(zip(x_users, y_users)):
    plt.text(x, y, f'UE {i}', fontsize=9, ha='right')  # Alterado de i+1 para i
plt.scatter(antenna_positions_before[:, 0], antenna_positions_before[:, 1], edgecolors='black', c='orange', s=200, marker='o', label="Antenas Iniciais")
for i, (x, y) in enumerate(antenna_positions_before):
    plt.text(x, y, f'ENB {i+1}', fontsize=9, ha='right')
plt.scatter(antenna_positions_after_ordered[:, 0], antenna_positions_after_ordered[:, 1], edgecolors='black', c='red', s=200, marker='o', label="Antenas Otimizadas")
for i, (x, y) in enumerate(antenna_positions_after_ordered):
    plt.text(x, y, f'ENB {i+1}', fontsize=9, ha='right')

plt.title("Otimização de Antenas com K-Means", fontsize=16)
plt.xlabel("X", fontsize=12)
plt.ylabel("Y", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
# %%
