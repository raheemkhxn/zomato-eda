from fpdf import FPDF
import pandas as pd

df = pd.read_csv('data/zomato_cleaned.csv')

class PDF(FPDF):
    def header(self):
        self.set_fill_color(231, 76, 60)
        self.rect(0, 0, 210, 18, 'F')
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 18, 'Zomato Bangalore - EDA Insights Report', 
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()} | Zomato EDA Project by Abdul Raheem Khan',
                  align='C')

    def section_title(self, title):
        self.ln(4)
        self.set_font('Helvetica', 'B', 13)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, title, new_x='LMARGIN', 
                  new_y='NEXT', fill=True)
        self.ln(2)

    def insight_text(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def stat_row(self, label, value):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)
        self.cell(90, 8, label)
        self.set_font('Helvetica', '', 11)
        self.set_text_color(231, 76, 60)
        self.cell(0, 8, str(value), 
                  new_x='LMARGIN', new_y='NEXT')

    def add_chart(self, path, title, w=180):
        self.ln(3)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        try:
            self.image(path, x=15, w=w)
        except:
            self.insight_text(f"[Chart: {title}]")
        self.ln(3)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(15, 22, 15)

# -- Page 1: Overview --
pdf.add_page()
pdf.ln(4)

pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(231, 76, 60)
pdf.cell(0, 12, 'Project Overview', 
         new_x='LMARGIN', new_y='NEXT')

pdf.insight_text(
    'This report presents a full exploratory data analysis of the Zomato '
    'Bangalore restaurant dataset containing 8,900+ restaurants across '
    '47+ areas. The analysis covers data cleaning, SQL querying, '
    'visualization, and statistical insights to understand restaurant '
    'trends, pricing patterns, cuisine popularity, and customer ratings '
    'across Bangalore.'
)

pdf.section_title('Key Statistics')
pdf.stat_row('Total Restaurants Analyzed',
             f"{len(df):,}")
pdf.stat_row('Unique Areas',
             f"{df['Area'].nunique()}")
pdf.stat_row('Unique Cuisines',
             f"{df['Cuisines'].str.split(',').explode().str.strip().nunique()}")
pdf.stat_row('Average Dinner Rating',
             f"{df['Dinner Ratings'].mean():.2f} / 5.0")
pdf.stat_row('Average Cost for Two',
             f"Rs {df['AverageCost'].mean():.0f}")
pdf.stat_row('Restaurants with Home Delivery',
             f"{df['IsHomeDelivery'].sum():,} ({df['IsHomeDelivery'].mean()*100:.1f}%)")
pdf.stat_row('Veg Only Restaurants',
             f"{df['isVegOnly'].sum():,} ({df['isVegOnly'].mean()*100:.1f}%)")

pdf.section_title('Data Cleaning Summary')
pdf.insight_text(
    '1. Removed URL and PhoneNumber columns (not useful for analysis).\n'
    '2. Removed duplicate restaurants based on Name and Full Address.\n'
    '3. Cleaned Area column by removing city suffix (Indiranagar, Bangalore -> Indiranagar).\n'
    '4. Fixed encoding issues in Timing column.\n'
    '5. Converted rating and cost columns to numeric types.\n'
    '6. Filled missing text fields with "Not Available".\n'
    '7. Added 3 new feature columns: Cuisine_Count, Rating_Category, Price_Category.'
)

# -- Page 2: Location Analysis --
pdf.add_page()
pdf.section_title('Location Analysis')
pdf.insight_text(
    'Whitefield, BTM Layout, and Koramangala are the top 3 areas by '
    'number of restaurants. These areas are major IT hubs and commercial '
    'zones, which explains the high restaurant density.'
)
pdf.add_chart('data/chart1_top_areas.png',
              'Top 10 Areas by Restaurant Count')
pdf.add_chart('data/chart8_area_ratings.png',
              'Top 10 Areas by Average Dinner Rating')

# -- Page 3: Rating Analysis --
pdf.add_page()
pdf.section_title('Rating Analysis')
pdf.insight_text(
    f"The average dinner rating across all restaurants is "
    f"{df['Dinner Ratings'].mean():.2f}. Most restaurants fall in the "
    f"3.5 to 4.5 range, indicating generally positive customer experiences. "
    f"Only a small percentage are rated below 3.0."
)
pdf.add_chart('data/chart2_rating_dist.png',
              'Dinner Rating Distribution')
pdf.add_chart('data/chart3_rating_categories.png',
              'Restaurants by Rating Category')

# -- Page 4: Cuisine & Service Analysis --
pdf.add_page()
pdf.section_title('Cuisine Analysis')
pdf.insight_text(
    'North Indian and Chinese cuisines dominate the Bangalore restaurant '
    'scene. Most restaurants serve multiple cuisines - the average '
    'restaurant offers 4-5 different cuisine types, showing high '
    'competition and diverse customer preferences.'
)
pdf.add_chart('data/chart5_top_cuisines.png',
              'Top 15 Most Popular Cuisines')
pdf.add_chart('data/chart9_cuisine_count.png',
              'Number of Cuisines per Restaurant')

# -- Page 5: Price Analysis --
pdf.add_page()
pdf.section_title('Price Analysis')
pdf.insight_text(
    f"The majority of Bangalore restaurants fall in the Budget "
    f"(under Rs 200) and Moderate (Rs 200-500) price range. "
    f"The average cost for two is Rs {df['AverageCost'].mean():.0f}. "
    f"Premium and Luxury restaurants tend to have slightly higher ratings."
)
pdf.add_chart('data/chart6_price_categories.png',
              'Restaurants by Price Category')
pdf.add_chart('data/chart15_rating_by_price.png',
              'Rating Distribution by Price Category')

# -- Page 6: Advanced Analysis --
pdf.add_page()
pdf.section_title('Correlation Analysis')
pdf.insight_text(
    'The correlation matrix reveals that Dinner Ratings and Delivery '
    'Ratings are strongly correlated - restaurants that perform well '
    'for dine-in also perform well for delivery. AverageCost shows '
    'a mild positive correlation with ratings.'
)
pdf.add_chart('data/chart12_correlation.png',
              'Correlation Matrix - All Features', w=170)

# -- Page 7: Key Insights --
pdf.add_page()
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(231, 76, 60)
pdf.cell(0, 12, 'Key Business Insights',
         new_x='LMARGIN', new_y='NEXT')

insights = [
    ("1. Location drives volume",
     "Whitefield, BTM Layout and Koramangala have the most restaurants "
     "due to high IT workforce density. These are prime areas for new "
     "restaurant launches."),
    ("2. North Indian dominates",
     "North Indian cuisine is served by the most restaurants, followed "
     "by Chinese and South Indian. Any new restaurant offering these "
     "cuisines faces high competition."),
    ("3. Delivery is mainstream",
     "Over 60% of restaurants offer home delivery, showing that online "
     "food ordering is now a standard expectation in Bangalore."),
    ("4. Budget segment is largest",
     "Most restaurants target the budget and moderate price segment "
     "(under Rs 500 for two), catering to the large working population."),
    ("5. Rating consistency",
     "Dinner and delivery ratings are strongly correlated - a restaurant "
     "that delivers quality dine-in experience also delivers quality food, "
     "suggesting that food quality is the primary driver of ratings."),
    ("6. Veg-only is a niche",
     "Only a small percentage of restaurants are veg-only, suggesting "
     "most restaurants cater to both veg and non-veg customers to "
     "maximize their customer base."),
]

for title, text in insights:
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 9, title, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 7, text)
    pdf.ln(3)

pdf.output('data/Zomato_EDA_Report.pdf')
print("PDF report saved to data/Zomato_EDA_Report.pdf")
print("Phase 5 Step 1 complete!")