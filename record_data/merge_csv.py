import pandas as pd
import glob
import os

path = r'data/' # use your path
all_files = glob.glob(os.path.join(path, "recorded_data*.csv"))

df = pd.concat((pd.read_csv(f, sep='\s*;\s*', engine='python') for f in all_files))

df.to_csv('data/sum_csv.csv')
