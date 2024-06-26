
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
import numpy as np

from cowboysmall.feature import INDICES, COLUMNS

from cowboysmall.data.file import read_master_file
from cowboysmall.plots import plt, sns



# %% 1 -
plt.plot_setup()
sns.sns_setup()



# %% 2 - read master data
master = read_master_file()



# %% 3 -
master["NSEI_OPEN_DIR"] = np.where(master["NSEI_OPEN"] > master["NSEI_CLOSE"].shift(), 1, 0)



# %% 3 - prepare master data
CONDITIONS = [(master.index <= '2020-01-30'), ('2022-05-05' <= master.index)]
CHOICES    = ['PRE_COVID', 'POST_COVID']

master['PANDEMIC'] = np.select(CONDITIONS, CHOICES, 'COVID')
master['PANDEMIC'] = pd.Categorical(master['PANDEMIC'], categories = ['PRE_COVID', 'COVID', 'POST_COVID'], ordered = True)



# %% 4 - performance analytics function
def performance_analytics(data, indices, columns, groupBy, groupByName):
    for index, column in zip(indices, columns):
        table = data.groupby(groupBy, observed = False)[column].agg(['count', 'mean', 'std', 'var'])
        print(f"\n{index}\n\n{table}\n\n")
        sns.box_plot(data[groupBy], data[column], groupByName, "Daily Returns", index)

        table = data.groupby(groupBy, observed = False)[column].agg(['median'])
        sns.bar_plot(table.index, table["median"], groupByName, "Median Daily Return", index)

        table = pd.pivot_table(data, values = column, index = [groupBy], columns = ["QUARTER"], aggfunc = "mean", observed = False)
        sns.heat_map(table, index)

        table = pd.pivot_table(data, values = column, index = [groupBy], columns = ["QUARTER"], aggfunc = "median", observed = False)
        sns.heat_map(table, index)




# %% 5 - global indices 5 years performance analytics
print("\n5 Years Performance Analytics\n")
performance_analytics(master['2018-01-02':'2022-12-30'], INDICES[:-1], COLUMNS[:-1], "YEAR", "Year")




# %% 6 - global indices correlation analysis
matrix = master[COLUMNS]['2018-01-02':'2022-12-30'].corr()
sns.correlation_matrix(matrix, "Daily Returns - 2018-2022")

matrix = master[COLUMNS]['2023-01-02':'2023-12-29'].corr()
sns.correlation_matrix(matrix, "Daily Returns - 2023-2023")




# %% 7 - pre-post covid performance analytics
print("\nPre-Post Covid Performance Analytics\n")
performance_analytics(master, INDICES[:-1], COLUMNS[:-1], "PANDEMIC", "Pandemic")




# %% 8 - 
for index, column in zip(INDICES[:-1], COLUMNS[:-1]):
    pre_covid  = master.loc[(master['PANDEMIC'] == 'PRE_COVID'),  [column]]
    post_covid = master.loc[(master['PANDEMIC'] == 'POST_COVID'), [column]]

    mean_pre   = pre_covid.values.mean()
    post_count = np.where(post_covid[column].ge(mean_pre).values == True)[0][0]
    post_date  = post_covid.index[post_covid[column].ge(mean_pre)][0].date()

    print(f"{index.rjust(5)} returned to pre-covid levels (mean {mean_pre: 2.4f}) on {post_date} after {post_count} trading day(s)")




# %% 9 - nifty fifty daily movement - pre-modeling
table1 = master.groupby("YEAR", observed = False)[["NSEI_OPEN_DIR"]].sum()
table2 = master.groupby("YEAR", observed = False)[["NSEI_OPEN_DIR"]].count()
table  = ((table1["NSEI_OPEN_DIR"] / table2["NSEI_OPEN_DIR"]) * 100).round(2)

print("\nNifty Fifty Daily Movement\n")
print(f"\n{table}\n")




# %% 10 - 
for index, column in zip(INDICES, COLUMNS):
    sns.box_plot(master["NSEI_OPEN_DIR"], master[column].shift(), "NSEI Open Direction", "Daily Returns", index)
