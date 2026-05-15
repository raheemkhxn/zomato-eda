import pandas as pd
import sqlite3

# 1. Load the dataset
df = pd.read_csv('data/zomato.csv', encoding='latin-1')

# 2. Basic info
print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFirst 3 rows:")
print(df.head(3))
print("\nMissing values:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)

# 3. Save to SQLite
conn = sqlite3.connect('data/zomato.db')
df.to_sql('restaurants', conn, if_exists='replace', index=False)
conn.close()

print("\nDatabase saved to data/zomato.db")
print("Phase 1 Step 1 complete!")