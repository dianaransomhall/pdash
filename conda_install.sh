#!/usr/bin/env bash
# assume anaconda is installed
conda install haversine
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx

# conda install osmnx
# conda install fiona

#conda create -n verge_conda
# conda activate verge_conda
# conda install rpy2
# conda install pandas
# conda install