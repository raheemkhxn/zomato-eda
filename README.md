# 🍽️ Zomato Bangalore Restaurant Analysis

> End-to-end Data Science project analyzing **8,900+ restaurants** across Bangalore using Python, SQL, and data visualization.

---

## 📌 Project Overview

This project performs a full **Exploratory Data Analysis (EDA)** on the Zomato Bangalore dataset. It covers everything from raw data loading and SQL querying to professional PDF report generation — simulating a real-world data analyst workflow.

---

## 🚀 What I Built

| Phase | Description |
|-------|-------------|
| 📥 **Data Loading** | Loaded raw CSV into SQLite database using pandas |
| 🧹 **Data Cleaning** | Fixed encoding issues, standardized columns, handled 4,800+ missing values, engineered 3 new features |
| 🔍 **SQL Analysis** | Wrote 7 business queries to extract insights using SQLite |
| 📊 **Visualization** | Created 15 charts covering ratings, cuisines, pricing, location, and correlations |
| 🧠 **Advanced Analysis** | GroupBy aggregations, pivot tables, and statistical summaries |
| 📄 **PDF Report** | Auto-generated a professional 7-page insights report using fpdf2 |

---

## 💡 Key Findings

- 📍 **Whitefield** has the most restaurants — driven by the IT hub effect
- 🍛 **North Indian** is the most served cuisine across Bangalore
- 🛵 **60%+** of restaurants offer home delivery
- ⭐ Dinner and delivery ratings are **strongly correlated**
- 💰 Most restaurants target the **budget-to-moderate** price segment (under ₹500 for two)

---

## 🗂️ Project Structure

```
zomato-eda/
│
├── data/
│   ├── zomato_raw.csv           # Original dataset
│   ├── zomato_cleaned.csv       # Cleaned dataset
│   ├── zomato.db                # SQLite database
│   ├── chart1_top_areas.png     # Generated charts (15 total)
│   └── Zomato_EDA_Report.pdf    # Final PDF report
│
├── load_data.py                 # Load CSV into SQLite
├── sql_analysis.py              # 7 SQL business queries
├── data_cleaning.py             # Full data cleaning pipeline
├── eda_charts.py                # 15 EDA visualizations
├── advanced_analysis.py         # GroupBy, pivot tables, correlation
└── generate_report.py           # PDF insights report generator
```

---

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install pandas matplotlib seaborn fpdf2
```

### 2. Run each phase in order
```bash
python load_data.py          # Phase 1 - Load data
python sql_analysis.py       # Phase 2 - SQL queries
python data_cleaning.py      # Phase 3 - Clean data
python eda_charts.py         # Phase 4 - Generate charts
python advanced_analysis.py  # Phase 5 - Advanced analysis
python generate_report.py    # Phase 5 - Generate PDF report
```

> 📄 The final PDF report will be saved to `data/Zomato_EDA_Report.pdf`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Core language |
| **pandas** | Data loading, cleaning, analysis |
| **numpy** | Numerical operations |
| **matplotlib / seaborn** | Data visualization |
| **SQLite + SQL** | Database querying |
| **fpdf2** | PDF report generation |

---

## 📦 Dataset

- **Source:** [Kaggle](https://www.kaggle.com/)
- **Size:** 8,923 rows × 19 columns
- **Coverage:** Restaurants across 47+ areas in Bangalore

---

## 👤 Author

**Abdul Raheem Khan**  
*Data Science & Python Enthusiast*

---

*If you found this useful, consider giving it a ⭐ on GitHub!*
