import pandas as pd
import matplotlib as plt
plt.use('TkAgg')

ldf_regular = pd.read_csv('./LDF_REGULAR.csv', sep=';')
ldf_optimised = pd.read_csv('./LDF_REGULAR.csv', sep=';')

ldf_regular['mean number of rejected'].plot()