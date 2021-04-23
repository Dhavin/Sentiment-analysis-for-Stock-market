import glob
import pandas as pd

# get data file names
path =r'C:\Users\Admin\PycharmProjects\test1.py\tweetdata'
filenames = glob.glob(path + "/*.csv")

dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename))

# Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True)