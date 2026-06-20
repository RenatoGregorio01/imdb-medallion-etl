import pandas as pd

df = pd.read_csv("data/raw/imdb_top_movies_1980_2026.csv")

print("\n===== INFO =====")
df.info()

print("\n===== NULOS =====")
print(df.isnull().sum())

print("\n===== DUPLICADOS =====")
print(df.duplicated(subset=["imdb_id"]).sum())

print("\n===== AMOSTRA =====")
print(df.head())
