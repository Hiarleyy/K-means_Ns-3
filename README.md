# K-means NS-3: Otimização de Posicionamento de Antenas 5G

## 📋 Descrição

Este projeto implementa uma solução de otimização para posicionamento de antenas em redes 5G utilizando o algoritmo K-means. O sistema combina simulações NS-3 (Network Simulator 3) com análise de dados em Python para otimizar a localização de estações base (eNodeB/gNodeB) baseada na distribuição de usuários e métricas de qualidade de sinal.

## 🎯 Objetivo

O projeto visa melhorar a eficiência de redes 5G através da otimização do posicionamento de antenas, considerando:
- Distribuição espacial dos usuários
- Métricas de qualidade de sinal (CQI, SINR)
- Path loss em diferentes frequências (3.5 GHz, 28 GHz, 100 GHz)
- Minimização da distância entre usuários e antenas

## 🏗️ Estrutura do Projeto

```
K-means_Ns-3/
├── README.md                 # Este arquivo
├── Code/                     # Código NS-3
│   └── packet_5G.cc         # Simulação principal 5G/NR
├── ml-python/               # Algoritmos de Machine Learning
│   ├── K-Means-Optmize.py   # Otimização com K-means
│   └── K-means-Positions_Manual.py
├── analise/                 # Scripts de análise de dados
│   ├── Rx-Analise.py        # Análise de pacotes recebidos
│   ├── boxplot_waypoints.py # Visualização waypoints
│   ├── Dlctrlsinr.py        # Análise SINR downlink
│   ├── DlDataSinr.py        # Dados SINR downlink
│   ├── dlpathloss.py        # Path loss downlink
│   └── waypoints.py         # Análise de pontos de rota
├── data/                    # Dados de simulação
│   ├── csv/                 # Dados convertidos para CSV
│   └── *.txt               # Arquivos de trace NS-3
├── Simulações/             # Resultados de diferentes cenários
│   ├── 3.5GHZ/            # Simulações em 3.5 GHz
│   ├── 28GHZ/             # Simulações em 28 GHz
│   ├── 100GHZ/            # Simulações em 100 GHz
│   └── ...                # Outros cenários
├── tratamento/             # Utilitários de processamento
│   └── txt-csv.py         # Conversão TXT para CSV
└── docs/                   # Documentação
    └── K-means.md         # Documentação específica
```

## 🚀 Funcionalidades

### 1. Simulação NS-3
- **Arquivo**: `Code/packet_5G.cc`
- Simulação de rede 5G/NR com múltiplas antenas e usuários
- Coleta de métricas: CQI, SINR, Path Loss, posições
- Suporte a diferentes frequências (3.5, 28, 100 GHz)

### 2. Otimização K-means
- **Arquivo**: `ml-python/K-Means-Optmize.py`
- Clustering de usuários para otimização de posicionamento
- Algoritmo Hungarian para pareamento otimizado
- Visualização dos resultados de otimização

### 3. Análise de Dados
- **Arquivos**: `analise/*.py`
- Análise de qualidade de sinal (CQI/SINR)
- Visualizações comparativas entre frequências
- Gráficos de pizza para categorização de qualidade
- Análise temporal de métricas

### 4. Processamento de Dados
- **Arquivo**: `tratamento/txt-csv.py`
- Conversão automática de traces NS-3 para CSV
- Interface gráfica para seleção de arquivos

## 📊 Métricas Analisadas

### Channel Quality Indicator (CQI)
- **Ótimo**: CQI > 20
- **Bom**: CQI 15-20
- **Médio**: CQI 10-15
- **Ruim**: CQI 0-10
- **Péssimo**: CQI < 0

### Signal-to-Interference-plus-Noise Ratio (SINR)
- Análise temporal do SINR por usuário
- Comparação entre diferentes células

### Path Loss
- Análise em múltiplas frequências
- Normalização e comparação

## 🛠️ Pré-requisitos

### Software Necessário
- **NS-3**: Network Simulator 3 (versão compatível com NR)
- **Python 3.7+**
- **Bibliotecas Python**:
  ```
  pandas
  numpy
  matplotlib
  scikit-learn
  scipy
  tkinter
  ```

### Hardware Recomendado
- RAM: 8GB+ (para simulações complexas)
- CPU: Multi-core (simulações paralelas)
- Espaço em disco: 2GB+ (dados de trace)

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/K-means_Ns-3.git
cd K-means_Ns-3
```

### 2. Instale as dependências Python
```bash
pip install pandas numpy matplotlib scikit-learn scipy
```

### 3. Configure o NS-3
- Instale o NS-3 com módulo NR
- Compile o código `Code/packet_5G.cc`

## 🚀 Como Usar

### 1. Executar Simulação NS-3
```bash
cd Code/
# Compile e execute a simulação
./waf --run "packet_5G --param1=value1 --param2=value2"
```

### 2. Converter Dados para CSV
```python
python tratamento/txt-csv.py
```

### 3. Otimizar Posicionamento
```python
python ml-python/K-Means-Optmize.py
```

### 4. Analisar Resultados
```python
python analise/Rx-Analise.py
```

## 📈 Exemplos de Resultados

### Otimização de Antenas
O algoritmo K-means reposiciona as antenas para minimizar a distância total aos usuários:

**Antes da Otimização:**
- Antena 1: [0, 50]
- Antena 2: [0, 500]
- Antena 3: [500, 500]
- Antena 4: [500, 50]

**Após Otimização:**
- Posições otimizadas baseadas na distribuição real dos usuários

### Análise de Qualidade
- Gráficos comparativos de CQI por frequência
- Distribuição de qualidade por antena
- Evolução temporal das métricas

## 🔧 Configuração

### Parâmetros de Simulação
No arquivo `packet_5G.cc`, você pode configurar:
- Número de usuários
- Número de antenas
- Frequências de operação
- Modelos de mobilidade
- Parâmetros de canal

### Parâmetros K-means
No arquivo `K-Means-Optmize.py`:
- `n_users`: Número de usuários
- `n_antennas`: Número de antenas
- `random_seed`: Semente para reprodutibilidade

## 📊 Estrutura de Dados

### Arquivos de Trace NS-3
- `RxPacketTrace.txt`: Pacotes recebidos
- `DlCtrlSinr.txt`: SINR de controle downlink
- `DlPathlossTrace.txt`: Path loss downlink
- `waypoint_positions.txt`: Posições dos waypoints

### Dados CSV Processados
- Estrutura padronizada para análise
- Colunas: Time, cellId, rnti, CQI, SINR, etc.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Marcos Hiarley** - *Desenvolvimento principal* - [GitHub](https://github.com/Hiarleyy)
- **Robert Gabriel** - *Análise de Dados e ML* - [GitHub](https://github.com/r0bertgabriel)

## 🙏 Agradecimentos

- Comunidade NS-3
- Desenvolvedores do módulo NR para NS-3
- Bibliotecas Python utilizadas

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma [Issue](https://github.com/seu-usuario/K-means_Ns-3/issues)
- Entre em contato via email

## 🔄 Versões

- **v1.0**: Implementação inicial com K-means básico
- **v2.0**: Adição de análise multi-frequência
- **v3.0**: Interface de conversão TXT-CSV

---

*Este projeto faz parte de pesquisas em otimização de redes 5G utilizando técnicas de Machine Learning.*

## 📚 Projetos de Pesquisa Relacionados

### 2024 - Atual: Um Estudo Sobre as Aplicações e Desafios de Redes Aéreas em Redes da Sexta Geração (6G)
**Coordenador**: José Jailton Henrique Ferreira Junior  
**Situação**: Em andamento
**Escritores**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Descrição**: Este projeto realiza um estudo aprofundado sobre o uso de plataformas aéreas, como drones e balões estratosféricos, em redes da sexta geração (6G). A pesquisa analisa aplicações potenciais, como cobertura em áreas remotas e suporte a eventos temporários, além dos principais desafios relacionados à mobilidade, interferência, consumo energético e integração com redes terrestres, contribuindo para o avanço da conectividade em cenários dinâmicos e de difícil acesso.

### 2023 - 2024: Transmissão Sem Fio em Altas Frequências para Rede 6G
**Coordenador**: José Jailton Henrique Ferreira Junior  
**Situação**: Concluído
**Escritores**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Descrição**: O projeto estuda a viabilidade da transmissão sem fio em altas frequências, como ondas terahertz (THz), para redes móveis de sexta geração (6G). A pesquisa foca na análise do desempenho em termos de taxa de dados, latência e confiabilidade, além de propor soluções para os desafios de propagação, direcionamento de feixes e consumo energético, visando suportar aplicações avançadas como holografia, realidade estendida e comunicação em tempo real.

### 2022 - 2023: Ondas Milimétricas de Redes 5G para Região Amazônica
**Coordenador**: José Jailton Henrique Ferreira Junior  
**Situação**: Concluído
**Escritores**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Descrição**: O projeto investiga o uso de ondas milimétricas (mmWave) em redes 5G como alternativa para ampliar o acesso à conectividade na Região Amazônica. A pesquisa considera os desafios ambientais, logísticos e de infraestrutura da região, avaliando a viabilidade técnica, o alcance do sinal, a capacidade de transmissão e os mecanismos de mitigação de interferência para fornecer internet de alta velocidade em áreas remotas.
