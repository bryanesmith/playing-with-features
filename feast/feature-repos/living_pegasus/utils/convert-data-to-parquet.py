import pandas as pd

csv_file = "/Users/bryan/Developer/playing-with-features/feast/data/us-covid.csv"
parquet_file = "/Users/bryan/Developer/playing-with-features/feast/data/us-covid.parquet"

def convert():
    # load CSV
    df = pd.read_csv(csv_file, chunksize=100_000, low_memory=False) \
      .read() \

    # convert date to timestamp
    #print('before', df['date'].head(5))
    df['date'] = df['date'].astype('datetime64[ns]')
    #print('after', df['date'].head(5))

    # write to Parquet
    df.to_parquet(parquet_file)

if __name__ == "__main__":
    convert()
