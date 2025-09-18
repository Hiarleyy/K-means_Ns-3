# K-means NS-3: 5G Antenna Positioning Optimization

## 📋 Description

This project implements an optimization solution for antenna positioning in 5G networks using the K-means algorithm. The system combines NS-3 (Network Simulator 3) simulations with Python data analysis to optimize the location of base stations (eNodeB/gNodeB) based on user distribution and signal quality metrics.

## 🎯 Objective

The project aims to improve 5G network efficiency through antenna positioning optimization, considering:
- Spatial distribution of users
- Signal quality metrics (CQI, SINR)
- Path loss at different frequencies (3.5 GHz, 28 GHz, 100 GHz)
- Minimization of distance between users and antennas

## 🏗️ Project Structure

```
K-means_Ns-3/
├── README.md                 # This file
├── Code/                     # NS-3 Code
│   └── packet_5G.cc         # Main 5G/NR simulation
├── ml-python/               # Machine Learning algorithms
│   ├── K-Means-Optmize.py   # K-means optimization
│   └── K-means-Positions_Manual.py
├── analise/                 # Data analysis scripts
│   ├── Rx-Analise.py        # Received packets analysis
│   ├── boxplot_waypoints.py # Waypoints visualization
│   ├── Dlctrlsinr.py        # Downlink SINR analysis
│   ├── DlDataSinr.py        # Downlink SINR data
│   ├── dlpathloss.py        # Downlink path loss
│   └── waypoints.py         # Route points analysis
├── data/                    # Simulation data
│   ├── csv/                 # Data converted to CSV
│   └── *.txt               # NS-3 trace files
├── Simulações/             # Results from different scenarios
│   ├── 3.5GHZ/            # 3.5 GHz simulations
│   ├── 28GHZ/             # 28 GHz simulations
│   ├── 100GHZ/            # 100 GHz simulations
│   └── ...                # Other scenarios
├── tratamento/             # Processing utilities
│   └── txt-csv.py         # TXT to CSV conversion
└── docs/                   # Documentation
    └── K-means.md         # Specific documentation
```

## 🚀 Features

### 1. NS-3 Simulation
- **File**: `Code/packet_5G.cc`
- 5G/NR network simulation with multiple antennas and users
- Metrics collection: CQI, SINR, Path Loss, positions
- Support for different frequencies (3.5, 28, 100 GHz)

### 2. K-means Optimization
- **File**: `ml-python/K-Means-Optmize.py`
- User clustering for positioning optimization
- Hungarian algorithm for optimal pairing
- Optimization results visualization

### 3. Data Analysis
- **Files**: `analise/*.py`
- Signal quality analysis (CQI/SINR)
- Comparative visualizations between frequencies
- Pie charts for quality categorization
- Temporal analysis of metrics

### 4. Data Processing
- **File**: `tratamento/txt-csv.py`
- Automatic conversion of NS-3 traces to CSV
- Graphical interface for file selection

## 📊 Analyzed Metrics

### Channel Quality Indicator (CQI)
- **Excellent**: CQI > 20
- **Good**: CQI 15-20
- **Average**: CQI 10-15
- **Poor**: CQI 0-10
- **Very Poor**: CQI < 0

### Signal-to-Interference-plus-Noise Ratio (SINR)
- Temporal SINR analysis per user
- Comparison between different cells

### Path Loss
- Analysis at multiple frequencies
- Normalization and comparison

## 🛠️ Prerequisites

### Required Software
- **NS-3**: Network Simulator 3 (NR-compatible version)
- **Python 3.7+**
- **Python Libraries**:
  ```
  pandas
  numpy
  matplotlib
  scikit-learn
  scipy
  tkinter
  ```

### Recommended Hardware
- RAM: 8GB+ (for complex simulations)
- CPU: Multi-core (parallel simulations)
- Disk space: 2GB+ (trace data)

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Hiarleyy/K-means_Ns-3.git
cd K-means_Ns-3
```

### 2. Install Python dependencies
```bash
pip install pandas numpy matplotlib scikit-learn scipy
```

### 3. Configure NS-3
- Install NS-3 with NR module
- Compile the code `Code/packet_5G.cc`

## 🚀 Usage

### 1. Run NS-3 Simulation
```bash
cd Code/
# Compile and run the simulation
./Ns3 --run scratch/packet_5G
```

### 2. Convert Data to CSV
```python
python tratamento/txt-csv.py
```

### 3. Optimize Positioning
```python
python ml-python/K-Means-Optmize.py
```

### 4. Analyze Results
```python
python analise/Rx-Analise.py
```

## 📈 Example Results

### Antenna Optimization
The K-means algorithm repositions antennas to minimize total distance to users:

**Before Optimization:**
- Antenna 1: [0, 50]
- Antenna 2: [0, 500]
- Antenna 3: [500, 500]
- Antenna 4: [500, 50]

**After Optimization:**
- Optimized positions based on actual user distribution

### Quality Analysis
- Comparative CQI charts by frequency
- Quality distribution per antenna
- Temporal evolution of metrics

## 🔧 Configuration

### Simulation Parameters
In the `packet_5G.cc` file, you can configure:
- Number of users
- Number of antennas
- Operating frequencies
- Mobility models
- Channel parameters

### K-means Parameters
In the `K-Means-Optmize.py` file:
- `n_users`: Number of users
- `n_antennas`: Number of antennas
- `random_seed`: Seed for reproducibility

## 📊 Data Structure

### NS-3 Trace Files
- `RxPacketTrace.txt`: Received packets
- `DlCtrlSinr.txt`: Downlink control SINR
- `DlPathlossTrace.txt`: Downlink path loss
- `waypoint_positions.txt`: Waypoint positions

### Processed CSV Data
- Standardized structure for analysis
- Columns: Time, cellId, rnti, CQI, SINR, etc.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 👥 Authors

- **Marcos Hiarley** - *Main Development* - [GitHub](https://github.com/Hiarleyy)
- **Robert Gabriel** - *Data Analysis and ML* - [GitHub](https://github.com/r0bertgabriel)

## 🙏 Acknowledgments

- NS-3 Community
- NR module developers for NS-3
- Python libraries used

## 📞 Support

For questions or issues:
- Open an [Issue](https://github.com/Hiarleyy/K-means_Ns-3/issues)
- Contact via email

## 🔄 Versions

- **v1.0**: Initial implementation with basic K-means
- **v2.0**: Addition of multi-frequency analysis
- **v3.0**: TXT-CSV conversion interface

---

*This project is part of research in 5G network optimization using Machine Learning techniques.*

## 📚 Related Research Projects

### 2024 - Current: A Study on Applications and Challenges of Aerial Networks in Sixth Generation (6G) Networks
**Coordinator**: José Jailton Henrique Ferreira Junior  
**Status**: In progress
**Authors**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Description**: This project conducts an in-depth study on the use of aerial platforms, such as drones and stratospheric balloons, in sixth-generation (6G) networks. The research analyzes potential applications, such as coverage in remote areas and support for temporary events, in addition to the main challenges related to mobility, interference, energy consumption and integration with terrestrial networks, contributing to the advancement of connectivity in dynamic and hard-to-reach scenarios.

### 2023 - 2024: High-Frequency Wireless Transmission for 6G Networks
**Coordinator**: José Jailton Henrique Ferreira Junior  
**Status**: Completed
**Authors**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Description**: The project studies the feasibility of high-frequency wireless transmission, such as terahertz (THz) waves, for sixth-generation (6G) mobile networks. The research focuses on performance analysis in terms of data rate, latency and reliability, in addition to proposing solutions to propagation challenges, beam steering and energy consumption, aiming to support advanced applications such as holography, extended reality and real-time communication.

### 2022 - 2023: Millimeter Waves from 5G Networks for the Amazon Region
**Coordinator**: José Jailton Henrique Ferreira Junior  
**Status**: Completed
**Authors**: Marcos Hiarley Lima Silva, Robert Gabriel  
**Description**: The project investigates the use of millimeter waves (mmWave) in 5G networks as an alternative to expand connectivity access in the Amazon Region. The research considers the environmental, logistical and infrastructure challenges of the region, evaluating technical feasibility, signal range, transmission capacity and interference mitigation mechanisms to provide high-speed internet in remote areas.