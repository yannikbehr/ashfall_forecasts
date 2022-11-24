# Probabilistic ashfall forecasting with Latin Hypercube Sampling
This library provides the codes to prepare and analyse probabilistic
ashfall forecasts using Latin Hypercube Sampling and Numerical Weather Prediction Model ensembles. Producing the probabilistic forecasts requires
an ashfall forecasting model like [HYSPLIT](https://ready.arl.noaa.gov/HYSPLIT.php). Details on this work can be
found [here](https://link.springer.com/article/10.1186/s13617-022-00123-0).

## Installation
### Install the conda environment
```
cd ashfall_forecasts 
conda env create -f environment.yml
```

### Install package in new environment
```
conda activate lhs 
python setup.py develop
```

### Setup Jupyter notebook kernel:
```
python -m ipykernel install --user --name lhs
pip install kernda
kernda -o -y /path/to/jupyter/kernels/lhs/kernel.json
```

To find the path of your kernel.json file you can run:
```
jupyter --paths
```
