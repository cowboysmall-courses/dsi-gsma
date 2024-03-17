
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



# %% 0 - import required libraries
import pandas as pd
import numpy as np

from gsma.data.file import read_master_file


# %% 1 - list of indices
indices = ['NSEI', 'DJI', 'IXIC', 'HSI', 'N225', 'GDAXI', 'VIX']


# %% 2 -
master = read_master_file()

master['PANDEMIC'] = np.select(
    [
        master.index <= '2020-01-30',
        ('2020-01-31' <= master.index) & (master.index <= '2022-05-04'),
        '2022-05-05' <= master.index
    ], 
    ['PRE_COVID', 'COVID', 'POST_COVID']
)

master['PANDEMIC'] = pd.Categorical(master['PANDEMIC'], categories = ['PRE_COVID', 'COVID', 'POST_COVID'], ordered = True)

for index in indices[:-1]:
    returns = f"{index}_DAILY_RETURNS"

    table   = master.groupby("PANDEMIC", observed = False)[returns].agg(['count', 'mean', 'std', 'var'])

    print()
    print(index)
    print()
    print(table)
    print()
