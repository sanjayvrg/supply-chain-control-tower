import pandas as pd
import sqlite3


df = pd.read_csv('scd.csv', encoding='latin-1')


conn = sqlite3.connect('supply_chain.db')


df.to_sql('orders', conn, if_exists='replace', index=False)

print(f"Done. {len(df)} rows loaded.")
print(df.columns.tolist())
conn.close()