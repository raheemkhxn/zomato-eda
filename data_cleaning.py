import pandas as pd
import numpy as np
import sqlite3

# ── 1. Load raw data ──────────────────────────────────────
df = pd.read_csv('data/zomato.csv', encoding='latin-1')
print("Original shape:", df.shape)
print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

# ── 2. Drop useless columns ───────────────────────────────
# URL and PhoneNumber are not useful for analysis
df.drop(columns=['URL', 'PhoneNumber'], inplace=True)
print("\nDropped URL and PhoneNumber columns")

# ── 3. Remove duplicate restaurants ───────────────────────
before = len(df)
df.drop_duplicates(subset=['Name', 'Full_Address'], inplace=True)
after = len(df)
print(f"\nRemoved {before - after} duplicate rows")

# ── 4. Clean the Area column ──────────────────────────────
# "Indiranagar, Bangalore" → "Indiranagar"
df['Area'] = df['Area'].str.split(',').str[0].str.strip()
print("\nArea column cleaned — removed city suffix")

# ── 5. Clean the Timing column ────────────────────────────
# Remove "(Today)", fix encoding issues
df['Timing'] = df['Timing'].str.replace(r'\(.*?\)', '', regex=True)
df['Timing'] = df['Timing'].str.replace('â', '-', regex=False)
df['Timing'] = df['Timing'].str.strip()
print("Timing column cleaned")

# ── 6. Clean Dinner Ratings ───────────────────────────────
df['Dinner Ratings'] = pd.to_numeric(df['Dinner Ratings'], errors='coerce')
print("Dinner Ratings converted to numeric")

# ── 7. Clean Delivery Ratings ─────────────────────────────
df['Delivery Ratings'] = pd.to_numeric(df['Delivery Ratings'], errors='coerce')
print("Delivery Ratings converted to numeric")

# ── 8. Clean Dinner Reviews ───────────────────────────────
# Some values might have commas like "1,000" → remove and convert
df['Dinner Reviews'] = df['Dinner Reviews'].astype(str)
df['Dinner Reviews'] = df['Dinner Reviews'].str.replace(',', '', regex=False)
df['Dinner Reviews'] = pd.to_numeric(df['Dinner Reviews'], errors='coerce')
print("Dinner Reviews converted to numeric")

# ── 9. Clean Delivery Reviews ─────────────────────────────
df['Delivery Reviews'] = df['Delivery Reviews'].astype(str)
df['Delivery Reviews'] = df['Delivery Reviews'].str.replace(',', '', regex=False)
df['Delivery Reviews'] = pd.to_numeric(df['Delivery Reviews'], errors='coerce')
print("Delivery Reviews converted to numeric")

# ── 10. Clean AverageCost ─────────────────────────────────
df['AverageCost'] = pd.to_numeric(df['AverageCost'], errors='coerce')
print("AverageCost converted to numeric")

# ── 11. Fix boolean columns ───────────────────────────────
bool_cols = ['IsHomeDelivery', 'isTakeaway', 'isIndoorSeating', 'isVegOnly']
for col in bool_cols:
    df[col] = df[col].fillna(0).astype(int)
print("Boolean columns fixed")

# ── 12. Fill missing text columns ─────────────────────────
text_cols = ['KnownFor', 'PopularDishes', 'PeopleKnownFor']
for col in text_cols:
    df[col] = df[col].fillna('Not Available')
print("Missing text columns filled")

# ── 13. Clean Cuisines column ─────────────────────────────
# Strip extra spaces around commas
df['Cuisines'] = df['Cuisines'].str.strip()
df['Cuisines'] = df['Cuisines'].str.replace(' ,', ',', regex=False)
df['Cuisines'] = df['Cuisines'].str.replace(',  ', ', ', regex=False)
print("Cuisines column cleaned")

# ── 14. Add useful new columns ────────────────────────────
# Number of cuisines each restaurant serves
df['Cuisine_Count'] = df['Cuisines'].str.split(',').str.len()

# Rating category
def rate_category(r):
    if pd.isna(r): return 'No Rating'
    elif r >= 4.5: return 'Excellent'
    elif r >= 4.0: return 'Very Good'
    elif r >= 3.5: return 'Good'
    elif r >= 3.0: return 'Average'
    else: return 'Below Average'

df['Rating_Category'] = df['Dinner Ratings'].apply(rate_category)

# Price category
def price_category(cost):
    if pd.isna(cost): return 'Unknown'
    elif cost <= 200: return 'Budget'
    elif cost <= 500: return 'Moderate'
    elif cost <= 1000: return 'Premium'
    else: return 'Luxury'

df['Price_Category'] = df['AverageCost'].apply(price_category)
print("New columns added: Cuisine_Count, Rating_Category, Price_Category")

# ── 15. Final check ───────────────────────────────────────
print("\n" + "="*50)
print("AFTER CLEANING")
print("="*50)
print("Shape:", df.shape)
print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)
print("\nSample cleaned data:")
print(df[['Name', 'Area', 'Dinner Ratings', 
          'AverageCost', 'Rating_Category', 
          'Price_Category']].head(5).to_string())

# ── 16. Save cleaned data ─────────────────────────────────
df.to_csv('data/zomato_cleaned.csv', index=False)

conn = sqlite3.connect('data/zomato.db')
df.to_sql('restaurants_clean', conn, 
          if_exists='replace', index=False)
conn.close()

print("\nCleaned data saved to:")
print("  data/zomato_cleaned.csv")
print("  data/zomato.db → table: restaurants_clean")
print("\nPhase 2 complete!")