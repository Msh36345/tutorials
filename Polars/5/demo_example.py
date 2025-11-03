"""
דוגמה מהירה - טיפול בערכים חסרים ב-Polars
הרצה: python demo_example.py
"""

import polars as pl
from datetime import date
import numpy as np

print("🐻‍❄️ ברוכים הבאים ל-Polars!")
print("=" * 60)

# 1. יצירת נתונים
print("\n📊 שלב 1: יצירת נתונים עם ערכים חסרים")
date_col = pl.date_range(date(2023, 1, 1), date(2023, 1, 10), '1d', eager=True)
temps = [-3, None, 6, -1, np.nan, 6, 4, None, 1, 2]

df = pl.DataFrame({
    'date': date_col,
    'temp': temps
}, strict=False)

print(df)

# 2. זיהוי
print("\n🔍 שלב 2: זיהוי ערכים חסרים")
print(f"Nulls: {df.select(pl.col('temp').is_null().sum()).item()}")
print(f"NaN: {df.select(pl.col('temp').is_nan().sum()).item()}")

# 3. מחיקה
print("\n🗑️  שלב 3: מחיקת שורות עם ערכים חסרים")
df_clean = df.with_columns(pl.col('temp').fill_nan(None)).drop_nulls()
print(f"לפני: {len(df)} שורות → אחרי: {len(df_clean)} שורות")

# 4. מילוי
print("\n📝 שלב 4: מילוי ערכים חסרים")
df_filled = df.with_columns([
    pl.col('temp').fill_nan(None),
    pl.col('temp').fill_nan(None).interpolate().alias('temp_filled')
])
print(df_filled.select(['temp', 'temp_filled']))

print("\n✅ הדגמה הושלמה! קראו את המדריך המקיף ללמידה נוספת.")
