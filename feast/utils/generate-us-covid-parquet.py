import pandas as pd

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))

csv_file = "%s/data/us-covid.csv"%d
parquet_file = "%s/data/us-covid.parquet"%d

def convert():
    # load CSV
    df = pd.read_csv(csv_file, chunksize=100_000, low_memory=False) \
      .read()

    # convert date to timestamp
    #print('before', df['date'].head(5))
    df['date'] = df['date'].astype('datetime64[ns]')
    #print('after', df['date'].head(5))

    # write to Parquet
    df.to_parquet(parquet_file)

if __name__ == "__main__":
    convert()
