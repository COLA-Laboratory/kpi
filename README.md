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
