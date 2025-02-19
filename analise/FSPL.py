import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Criando um DataFrame com os dados fictícios
data = {
    "ID": [f"Ue{i}" for i in range(10)],
    "Posição X": [38.56, 1.03, 31.68, 37.44, 24.92, 11.23, 9.90, 38.02, 8.45, 4.16],
    "Posição Y": [34.26, 47.66, 0.19, 25.60, 40.63, 30.62, 36.08, 14.59, 45.88, 35.72],
    "Distância": [15.74, 12.16, 19.06, 7.01, 14.97, 8.89, 3.35, 4.37, 6.63, 6.70]
}

df = pd.DataFrame(data)

# Definição de parâmetros para FSPL (supondo frequência de 3.5 GHz)
freq_Hz = 100e8  # 3.5 GHz
c = 3e8  # Velocidade da luz (m/s)
df["FSPL_dB"] = 20 * np.log10(df["Distância"]) + 20 * np.log10(freq_Hz) + 20 * np.log10(4 * np.pi / c)

# Plotando a posição das UEs
plt.figure(figsize=(8, 5))
plt.scatter(df["Posição X"], df["Posição Y"], c=df["Distância"], cmap="viridis", s=100, edgecolors='k')
for i, txt in enumerate(df["ID"]):
    plt.annotate(txt, (df["Posição X"][i], df["Posição Y"][i]), fontsize=12)

plt.xlabel("Posição X")
plt.ylabel("Posição Y")
plt.title("Distribuição das UEs")
plt.colorbar(label="Distância da BS (m)")
plt.grid()
plt.show()

# Plotando FSPL vs Distância
plt.figure(figsize=(8, 5))
plt.scatter(df["Distância"], df["FSPL_dB"], marker="o", color="r", label="FSPL (Modelo Livre)")
plt.plot(df["Distância"], df["FSPL_dB"], linestyle="dashed", color="b")

plt.xlabel("Distância (m)")
plt.ylabel("Path Loss (dB)")
plt.title("Path Loss (FSPL) vs Distância")
plt.legend()
plt.grid()
plt.show()
s