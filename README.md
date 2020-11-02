# Knee Point Identification Based on Trade-Off Utility
![Python package](https://github.com/stanfordmlgroup/ngboost/workflows/Python%20package/badge.svg)
[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation guide
* `Python version should be 3.6`
* Install thrid-party packages (In `Anacaonda` environment)
    * `pip install sklearn`
    * `pip install pandas`

## A quick start to run experiments
* Run `code\main.py` to get files about knee points identified by all six KPI methods. The files are stored by default in `code\results` after run `main.py`.
* Run `code\algorithms\KPITU.py` to observe the results of KPITU on the specified test problem separately. Other `.py` files in `code\algorithms` can be run separately like this to get the corresponding results.

## Examples of the search dynamics of KPITU for identifying knee point(s).
- Example of a problem with only one knee point
<p align="center">
    <img src="https://github.com/COLA-Laboratory/kpi/blob/master/gif/PMOP1_M2_A2.gif" width="400"/><img src="https://github.com/COLA-Laboratory/kpi/blob/master/gif/PMOP1_M3_A2.gif" width="400"/>
</p>

- Example of a problem with more than one knee point
<p align="center">
    <img src="https://github.com/COLA-Laboratory/kpi/blob/master/gif/PMOP1_M2_A4.gif" width="400"/><img src="https://github.com/COLA-Laboratory/kpi/blob/master/gif/PMOP1_M3_A4.gif" width="400"/>
</p>

## Reference
K. Li, H. Nie, H. Gao and X. Yao, "Posterior Decision-Making Based on Decomposition-Driven Knee Point Identification", submitted for peer review, May, 2020.
