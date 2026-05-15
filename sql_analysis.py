import sqlite3
import pandas as pd

conn = sqlite3.connect('data/zomato.db')

# Query 1 — Total restaurants
q1 = """
SELECT COUNT(*) AS total_restaurants
FROM restaurants;
"""

# Query 2 — Top 10 areas with most restaurants
q2 = """
SELECT Area,
       COUNT(*) AS total
FROM restaurants
WHERE Area IS NOT NULL
GROUP BY Area
ORDER BY total DESC
LIMIT 10;
"""

# Query 3 — Most popular cuisines
q3 = """
SELECT Cuisines,
       COUNT(*) AS total
FROM restaurants
WHERE Cuisines IS NOT NULL
GROUP BY Cuisines
ORDER BY total DESC
LIMIT 10;
"""

# Query 4 — Home delivery vs not
q4 = """
SELECT IsHomeDelivery,
       COUNT(*) AS total,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM restaurants), 2) AS percentage
FROM restaurants
GROUP BY IsHomeDelivery;
"""

# Query 5 — Veg only restaurants
q5 = """
SELECT isVegOnly,
       COUNT(*) AS total,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM restaurants), 2) AS percentage
FROM restaurants
GROUP BY isVegOnly;
"""

# Query 6 — Top 10 areas by average cost
q6 = """
SELECT Area,
       ROUND(AVG(AverageCost), 0) AS avg_cost
FROM restaurants
WHERE AverageCost IS NOT NULL
AND Area IS NOT NULL
GROUP BY Area
ORDER BY avg_cost DESC
LIMIT 10;
"""

# Query 7 — Top 10 highest dinner rated restaurants
q7 = """
SELECT Name,
       Area,
       "Dinner Ratings",
       "Dinner Reviews"
FROM restaurants
WHERE "Dinner Ratings" IS NOT NULL
ORDER BY "Dinner Ratings" DESC,
         "Dinner Reviews" DESC
LIMIT 10;
"""

queries = [
    ("Total restaurants", q1),
    ("Top areas", q2),
    ("Popular cuisines", q3),
    ("Home delivery breakdown", q4),
    ("Veg only breakdown", q5),
    ("Avg cost by area", q6),
    ("Top rated restaurants", q7),
]

for name, query in queries:
    print(f"\n{'='*55}")
    print(f"  {name}")
    print('='*55)
    print(pd.read_sql_query(query, conn).to_string(index=False))

conn.close()
print("\nPhase 1 complete!")