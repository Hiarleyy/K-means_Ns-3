# K-means Algorithm Documentation

## Overview

This document provides detailed information about the K-means algorithm implementation used in the 5G antenna positioning optimization project.

## Algorithm Description

K-means is an unsupervised machine learning algorithm used for clustering data points into k clusters. In this project, it's used to optimize the positioning of 5G antennas based on user distribution.

## Implementation Details

The K-means algorithm in this project:

1. **Input**: User positions in 2D space (x, y coordinates)
2. **Process**: Groups users into clusters and finds optimal antenna positions
3. **Output**: Optimized antenna positions that minimize total distance to users

## Usage

The main implementation can be found in `ml-python/K-Means-Optmize.py`.

### Key Parameters

- `n_clusters`: Number of antenna clusters (equals number of antennas)
- `random_state`: Seed for reproducible results
- `max_iter`: Maximum number of iterations for convergence

### Optimization Process

1. **User Data Collection**: Extract user positions from simulation data
2. **Clustering**: Apply K-means to group users
3. **Assignment**: Use Hungarian algorithm to assign new positions to existing antennas
4. **Visualization**: Generate plots showing before/after optimization

## Benefits

- Reduces average distance between users and antennas
- Improves signal quality and coverage
- Optimizes network resource utilization
- Provides visual feedback on optimization effectiveness

## Integration with NS-3

The optimized antenna positions can be fed back into NS-3 simulations to validate the improvements in network performance metrics such as:

- Channel Quality Indicator (CQI)
- Signal-to-Interference-plus-Noise Ratio (SINR)
- Path Loss
- Throughput

## Future Enhancements

Potential improvements to the current implementation:

- Dynamic clustering based on user mobility patterns
- Multi-objective optimization considering multiple metrics
- Integration with other clustering algorithms (DBSCAN, hierarchical clustering)
- Real-time optimization capabilities