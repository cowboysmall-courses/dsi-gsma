
"""

Global market indices of interest:

    NSEI:  Nifty 50
    DJI:   Dow Jones Index
    IXIC:  Nasdaq
    HSI:   Hang Seng
    N225:  Nikkei 225
    GDAXI: Dax
    VIX:   Volatility Index

"""



# %% 1 - import required libraries
import pandas as pd

from gsma import INDICES, COLUMNS

from gsma.data.file import read_master_file
from gsma.plots import plt, sns



# %% 2 -
master = read_master_file()['2018-01-02':'2022-12-30']

for index, column in zip(INDICES[:-1], COLUMNS[:-1]):
    table = pd.pivot_table(master, values = column, index = ["YEAR"], columns = ["QUARTER"], aggfunc = "mean")
    plt.plot_setup()
    sns.sns_setup()
    sns.heat_map(table, column, "MEAN", "YEAR", index, "phase_02")

    table = pd.pivot_table(master, values = column, index = ["YEAR"], columns = ["QUARTER"], aggfunc = "median")
    plt.plot_setup()
    sns.sns_setup()
    sns.heat_map(table, column, "MEDIAN", "YEAR", index, "phase_02")
