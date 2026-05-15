import pandas as pd

df = pd.read_csv('data/zomato.csv', encoding='latin-1')
print("Shape:", df.shape)
print("\nExact column names:")
for i, col in enumerate(df.columns):
    print(f"  {i}: '{col}'")
print("\nFirst row sample:")
print(df.head(1).to_string())