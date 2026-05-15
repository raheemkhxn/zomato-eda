import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Load cleaned data
df = pd.read_csv('data/zomato_cleaned.csv')
print("Data loaded:", df.shape)
sns.set_theme(style="whitegrid")

# ══════════════════════════════════════════════
# PART 1 — GroupBy Analysis
# ══════════════════════════════════════════════

print("\n" + "="*55)
print("  PART 1 — GroupBy Analysis")
print("="*55)

# 1a. Area wise summary
area_summary = df.groupby('Area').agg(
    Total_Restaurants=('Name', 'count'),
    Avg_Dinner_Rating=('Dinner Ratings', 'mean'),
    Avg_Cost=('AverageCost', 'mean'),
    Delivery_Available=('IsHomeDelivery', 'sum'),
    Veg_Only=('isVegOnly', 'sum')
).round(2).sort_values('Total_Restaurants', ascending=False)

print("\nTop 10 Areas — Full Summary:")
print(area_summary.head(10).to_string())

# 1b. Price category wise rating
price_rating = df.groupby('Price_Category').agg(
    Count=('Name', 'count'),
    Avg_Rating=('Dinner Ratings', 'mean'),
    Avg_Cost=('AverageCost', 'mean'),
    Avg_Reviews=('Dinner Reviews', 'mean')
).round(2)
print("\nPrice Category vs Rating:")
print(price_rating.to_string())

# 1c. Rating category wise cost
rating_cost = df.groupby('Rating_Category').agg(
    Count=('Name', 'count'),
    Avg_Cost=('AverageCost', 'mean'),
    Avg_Delivery_Rating=('Delivery Ratings', 'mean')
).round(2)
print("\nRating Category vs Cost:")
print(rating_cost.to_string())

# ══════════════════════════════════════════════
# PART 2 — Pivot Tables
# ══════════════════════════════════════════════

print("\n" + "="*55)
print("  PART 2 — Pivot Tables")
print("="*55)

# 2a. Area vs Price Category pivot
top10_areas = df['Area'].value_counts().head(10).index
df_top = df[df['Area'].isin(top10_areas)]

pivot1 = pd.pivot_table(
    df_top,
    values='Name',
    index='Area',
    columns='Price_Category',
    aggfunc='count',
    fill_value=0
)
print("\nPivot — Area vs Price Category (restaurant count):")
print(pivot1.to_string())

# 2b. Rating Category vs Service type pivot
pivot2 = pd.pivot_table(
    df,
    values='Name',
    index='Rating_Category',
    columns='IsHomeDelivery',
    aggfunc='count',
    fill_value=0
)
pivot2.columns = ['No Delivery', 'Has Delivery']
print("\nPivot — Rating Category vs Home Delivery:")
print(pivot2.to_string())

# 2c. Area vs Average cost pivot (heatmap ready)
pivot3 = pd.pivot_table(
    df_top,
    values='AverageCost',
    index='Area',
    columns='Price_Category',
    aggfunc='mean',
    fill_value=0
).round(0)
print("\nPivot — Area vs Avg Cost by Price Category:")
print(pivot3.to_string())

# ══════════════════════════════════════════════
# PART 3 — Correlation Matrix
# ══════════════════════════════════════════════

print("\n" + "="*55)
print("  PART 3 — Correlation Matrix")
print("="*55)

num_cols = ['Dinner Ratings', 'Dinner Reviews',
            'Delivery Ratings', 'Delivery Reviews',
            'AverageCost', 'Cuisine_Count',
            'IsHomeDelivery', 'isTakeaway',
            'isIndoorSeating', 'isVegOnly']

corr = df[num_cols].corr().round(2)
print("\nCorrelation Matrix:")
print(corr.to_string())

# ══════════════════════════════════════════════
# PART 4 — Statistical Summary
# ══════════════════════════════════════════════

print("\n" + "="*55)
print("  PART 4 — Key Statistical Insights")
print("="*55)

print(f"""
Total restaurants analyzed : {len(df):,}
Unique areas               : {df['Area'].nunique()}
Unique cuisines            : {df['Cuisines'].str.split(',').explode().str.strip().nunique()}

Dinner Ratings:
  Mean     : {df['Dinner Ratings'].mean():.2f}
  Median   : {df['Dinner Ratings'].median():.2f}
  Std Dev  : {df['Dinner Ratings'].std():.2f}
  Min      : {df['Dinner Ratings'].min():.1f}
  Max      : {df['Dinner Ratings'].max():.1f}

Average Cost for Two:
  Mean     : ₹{df['AverageCost'].mean():.0f}
  Median   : ₹{df['AverageCost'].median():.0f}
  Min      : ₹{df['AverageCost'].min():.0f}
  Max      : ₹{df['AverageCost'].max():.0f}

Service Availability:
  Home Delivery : {df['IsHomeDelivery'].sum():,} restaurants ({df['IsHomeDelivery'].mean()*100:.1f}%)
  Takeaway      : {df['isTakeaway'].sum():,} restaurants ({df['isTakeaway'].mean()*100:.1f}%)
  Indoor Seating: {df['isIndoorSeating'].sum():,} restaurants ({df['isIndoorSeating'].mean()*100:.1f}%)
  Veg Only      : {df['isVegOnly'].sum():,} restaurants ({df['isVegOnly'].mean()*100:.1f}%)
""")

# ══════════════════════════════════════════════
# PART 5 — Advanced Charts
# ══════════════════════════════════════════════

# Chart 12 — Correlation Heatmap
plt.figure(figsize=(12, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
            mask=mask, center=0, square=True,
            linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix — Zomato Features',
          fontsize=16, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('data/chart12_correlation.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 12 — Correlation heatmap saved")

# Chart 13 — Pivot heatmap: Area vs Price Category
plt.figure(figsize=(12, 7))
sns.heatmap(pivot1, annot=True, fmt='g', cmap='YlOrRd',
            linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Restaurant Count — Area vs Price Category',
          fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('data/chart13_area_price_pivot.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 13 — Area vs Price pivot heatmap saved")

# Chart 14 — Top 10 restaurants by dinner reviews
plt.figure(figsize=(13, 7))
top_reviewed = df.nlargest(10, 'Dinner Reviews')[
    ['Name', 'Area', 'Dinner Ratings', 'Dinner Reviews', 'AverageCost']]
bars = plt.barh(top_reviewed['Name'][::-1],
                top_reviewed['Dinner Reviews'][::-1],
                color='#3498db', edgecolor='white')
for bar, val in zip(bars, top_reviewed['Dinner Reviews'][::-1]):
    plt.text(bar.get_width() + 50,
             bar.get_y() + bar.get_height()/2,
             f'{int(val):,}', va='center', fontweight='bold')
plt.title('Top 10 Most Reviewed Restaurants',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Number of Dinner Reviews')
plt.tight_layout()
plt.savefig('data/chart14_most_reviewed.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 14 — Most reviewed restaurants saved")

# Chart 15 — Box plot: Rating by Price Category
plt.figure(figsize=(12, 6))
price_order = ['Budget', 'Moderate', 'Premium', 'Luxury']
df_box = df[df['Price_Category'].isin(price_order)]
sns.boxplot(data=df_box, x='Price_Category', y='Dinner Ratings',
            order=price_order, hue='Price_Category',
            palette=['#2ecc71', '#f39c12', '#e67e22', '#e74c3c'],
            legend=False)
plt.title('Dinner Rating Distribution by Price Category',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Price Category')
plt.ylabel('Dinner Rating')
plt.tight_layout()
plt.savefig('data/chart15_rating_by_price.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 15 — Rating by price boxplot saved")

# Save area summary to CSV for report
area_summary.to_csv('data/area_summary.csv')
print("\nArea summary saved to data/area_summary.csv")

print("\n" + "="*55)
print("Phase 4 complete! 4 more charts saved.")
print("="*55)