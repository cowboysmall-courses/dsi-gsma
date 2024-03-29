
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
import numpy as np

from gsma import INDICES, COLUMNS

from gsma.data.file import read_master_file
from gsma.plots import plt, sns



# %% 2 -
master = read_master_file()

master["NSEI_OPEN_DIR"] = np.where(master["NSEI_OPEN"] > master["NSEI_CLOSE"].shift(), 1, 0)

for index, column in zip(INDICES, COLUMNS):
    plt.plot_setup()
    sns.sns_setup()
    sns.box_plot(master["NSEI_OPEN_DIR"], master[column].shift(), column, "Daily Returns", "NSEI_OPEN_DIR", "NSEI Open Direction", index, "phase_02")
