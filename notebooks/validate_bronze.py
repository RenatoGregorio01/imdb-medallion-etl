import pandas as pd

df = pd.read_parquet("data/bronze/movies_raw.parquet")

print(df.info())
print(df.head())
