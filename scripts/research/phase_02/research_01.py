
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
from cowboysmall.data.file import read_master_file
from cowboysmall.plots import plt, sns
from cowboysmall.feature import INDICES, COLUMNS



# %% 2 - plot daily returns
master = read_master_file()['2018-01-02':'2022-12-30']



# %% 3 - 
plt.plot_setup()
sns.sns_setup()

for index, column in zip(INDICES[:-1], COLUMNS[:-1]):
    sns.box_plot(master["YEAR"].values, master[column].values, "Daily Returns", "Years", index)
