import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned data
df = pd.read_csv('data/zomato_cleaned.csv')
print("Data loaded:", df.shape)

sns.set_theme(style="whitegrid")
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', 
          '#9b59b6', '#1abc9c', '#e67e22', '#34495e']

# ── Chart 1: Top 10 Areas by restaurant count ─────────────
plt.figure(figsize=(12, 6))
top_areas = df['Area'].value_counts().head(10)
bars = plt.barh(top_areas.index[::-1], top_areas.values[::-1], 
                color='#e74c3c', edgecolor='white')
for bar, val in zip(bars, top_areas.values[::-1]):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontweight='bold', fontsize=11)
plt.title('Top 10 Areas by Number of Restaurants', 
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Number of Restaurants')
plt.tight_layout()
plt.savefig('data/chart1_top_areas.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 1 saved")

# ── Chart 2: Dinner Rating Distribution ───────────────────
plt.figure(figsize=(10, 6))
df['Dinner Ratings'].dropna().hist(bins=20, color='#3498db', 
                                    edgecolor='white', linewidth=1.2)
plt.axvline(df['Dinner Ratings'].mean(), color='#e74c3c', 
            linestyle='--', linewidth=2,
            label=f"Mean: {df['Dinner Ratings'].mean():.2f}")
plt.title('Dinner Rating Distribution', 
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Rating')
plt.ylabel('Number of Restaurants')
plt.legend()
plt.tight_layout()
plt.savefig('data/chart2_rating_dist.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 2 saved")

# ── Chart 3: Rating Category Breakdown ────────────────────
plt.figure(figsize=(10, 6))
order = ['Excellent', 'Very Good', 'Good', 
         'Average', 'Below Average', 'No Rating']
cat_colors = ['#2ecc71', '#27ae60', '#f39c12', 
              '#e67e22', '#e74c3c', '#95a5a6']
rating_counts = df['Rating_Category'].value_counts()
rating_counts = rating_counts.reindex(
    [o for o in order if o in rating_counts.index])
bars = plt.bar(rating_counts.index, rating_counts.values, 
               color=cat_colors[:len(rating_counts)], edgecolor='white')
for bar, val in zip(bars, rating_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             str(val), ha='center', fontweight='bold')
plt.title('Restaurants by Rating Category', 
          fontsize=16, fontweight='bold', pad=15)
plt.ylabel('Number of Restaurants')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('data/chart3_rating_categories.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 3 saved")

# ── Chart 4: Home Delivery vs Dine-in ─────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Restaurant Service Types', 
             fontsize=16, fontweight='bold')

for ax, col, title in zip(
    axes,
    ['IsHomeDelivery', 'isTakeaway', 'isIndoorSeating'],
    ['Home Delivery', 'Takeaway', 'Indoor Seating']
):
    counts = df[col].value_counts()
    labels = ['Yes' if i == 1 else 'No' for i in counts.index]
    ax.pie(counts.values, labels=labels, autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c'], startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title(title, fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('data/chart4_service_types.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 4 saved")

# ── Chart 5: Top 15 Cuisines ──────────────────────────────
plt.figure(figsize=(12, 7))
all_cuisines = df['Cuisines'].dropna().str.split(',').explode()
all_cuisines = all_cuisines.str.strip()
top_cuisines = all_cuisines.value_counts().head(15)
bars = plt.barh(top_cuisines.index[::-1], top_cuisines.values[::-1],
                color='#9b59b6', edgecolor='white')
for bar, val in zip(bars, top_cuisines.values[::-1]):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontweight='bold', fontsize=10)
plt.title('Top 15 Most Popular Cuisines in Bangalore',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Number of Restaurants')
plt.tight_layout()
plt.savefig('data/chart5_top_cuisines.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 5 saved")

# ── Chart 6: Price Category Distribution ──────────────────
plt.figure(figsize=(10, 6))
price_order = ['Budget', 'Moderate', 'Premium', 'Luxury', 'Unknown']
price_colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#95a5a6']
price_counts = df['Price_Category'].value_counts()
price_counts = price_counts.reindex(
    [p for p in price_order if p in price_counts.index])
bars = plt.bar(price_counts.index, price_counts.values,
               color=price_colors[:len(price_counts)], edgecolor='white')
for bar, val in zip(bars, price_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(val), ha='center', fontweight='bold')
plt.title('Restaurants by Price Category',
          fontsize=16, fontweight='bold', pad=15)
plt.ylabel('Number of Restaurants')
plt.tight_layout()
plt.savefig('data/chart6_price_categories.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 6 saved")

# ── Chart 7: Average Cost vs Dinner Rating ────────────────
plt.figure(figsize=(10, 6))
clean = df[['AverageCost', 'Dinner Ratings']].dropna()
clean = clean[clean['AverageCost'] < 3000]
plt.scatter(clean['AverageCost'], clean['Dinner Ratings'],
            alpha=0.4, color='#e74c3c', edgecolor='white', s=30)
z = np.polyfit(clean['AverageCost'], clean['Dinner Ratings'], 1)
p = np.poly1d(z)
x_line = np.linspace(clean['AverageCost'].min(), 
                     clean['AverageCost'].max(), 100)
plt.plot(x_line, p(x_line), color='#2c3e50', 
         linewidth=2, linestyle='--', label='Trend line')
plt.title('Average Cost vs Dinner Rating',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Average Cost for Two (₹)')
plt.ylabel('Dinner Rating')
plt.legend()
plt.tight_layout()
plt.savefig('data/chart7_cost_vs_rating.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 7 saved")

# ── Chart 8: Top 10 Areas by Average Rating ───────────────
plt.figure(figsize=(12, 6))
area_rating = df.groupby('Area')['Dinner Ratings'].agg(
    ['mean', 'count']).reset_index()
area_rating = area_rating[area_rating['count'] >= 10]
area_rating = area_rating.sort_values('mean', ascending=False).head(10)
bars = plt.barh(area_rating['Area'][::-1], 
                area_rating['mean'][::-1],
                color='#1abc9c', edgecolor='white')
for bar, val in zip(bars, area_rating['mean'][::-1]):
    plt.text(bar.get_width() + 0.01, 
             bar.get_y() + bar.get_height()/2,
             f'{val:.2f}', va='center', fontweight='bold')
plt.title('Top 10 Areas by Average Dinner Rating\n(min 10 restaurants)',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Average Rating')
plt.xlim(0, 5)
plt.tight_layout()
plt.savefig('data/chart8_area_ratings.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 8 saved")

# ── Chart 9: Number of Cuisines per Restaurant ────────────
plt.figure(figsize=(10, 6))
cuisine_dist = df['Cuisine_Count'].value_counts().sort_index().head(10)
plt.bar(cuisine_dist.index, cuisine_dist.values,
        color='#f39c12', edgecolor='white')
for i, val in zip(cuisine_dist.index, cuisine_dist.values):
    plt.text(i, val + 20, str(val), ha='center', fontweight='bold')
plt.title('How Many Cuisines Does Each Restaurant Serve?',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Number of Cuisines')
plt.ylabel('Number of Restaurants')
plt.tight_layout()
plt.savefig('data/chart9_cuisine_count.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 9 saved")

# ── Chart 10: Veg vs Non-veg by Area (top 8) ─────────────
plt.figure(figsize=(14, 7))
top8_areas = df['Area'].value_counts().head(8).index
area_veg = df[df['Area'].isin(top8_areas)].groupby(
    ['Area', 'isVegOnly']).size().unstack(fill_value=0)
area_veg.columns = ['Non-Veg', 'Veg Only']
area_veg.plot(kind='bar', color=['#e74c3c', '#2ecc71'], 
              edgecolor='white', ax=plt.gca())
plt.title('Veg vs Non-Veg Restaurants in Top 8 Areas',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Area')
plt.ylabel('Number of Restaurants')
plt.xticks(rotation=30, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('data/chart10_veg_nonveg.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 10 saved")

# ── Chart 11: Dinner vs Delivery Rating Comparison ────────
plt.figure(figsize=(10, 6))
both = df[['Dinner Ratings', 'Delivery Ratings']].dropna()
plt.scatter(both['Dinner Ratings'], both['Delivery Ratings'],
            alpha=0.4, color='#3498db', edgecolor='white', s=30)
plt.plot([1, 5], [1, 5], color='#e74c3c', 
         linestyle='--', linewidth=2, label='Perfect match line')
plt.title('Dinner Rating vs Delivery Rating',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Dinner Rating')
plt.ylabel('Delivery Rating')
plt.legend()
plt.tight_layout()
plt.savefig('data/chart11_dinner_vs_delivery.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart 11 saved")

print("\n" + "="*50)
print("All 11 charts saved to data/ folder!")
print("="*50)
print("\nPhase 3 complete!")