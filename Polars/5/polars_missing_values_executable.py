"""
================================================================================
מדריך Polars: טיפול בערכים חסרים (Missing Values)
================================================================================

קובץ זה מכיל את כל דוגמאות הקוד מה-Notebook, עם הסברים מפורטים בעברית.
הקוד מוכן להרצה מיידית!

דרישות:
    pip install polars numpy --break-system-packages

מחבר: נוצר אוטומטית מ-Jupyter Notebook
תאריך: 2025
================================================================================
"""

import polars as pl
from datetime import date
import numpy as np

# ==============================================================================
# חלק 1: זיהוי ערכים חסרים (Identifying Missing Values)
# ==============================================================================

print("=" * 80)
print("חלק 1: זיהוי ערכים חסרים")
print("=" * 80)

# יצירת DataFrame לדוגמה עם ערכים חסרים
print("\n1.1 יצירת נתונים לדוגמה")
print("-" * 40)

date_col = pl.date_range(date(2023, 1, 1), date(2023, 1, 15), '1d', eager=True)
avg_temp_c_list = [-3, None, 6, -1, np.nan, 6, 4, None, 1, 2, np.nan, 7, 9, -2, None]

df = pl.DataFrame({
    'date': date_col,
    'avg_temp_celsius': avg_temp_c_list
}, strict=False)

print("DataFrame שנוצר:")
print(df.head())
print(f"\nמספר שורות: {len(df)}")
print(f"סוגי העמודות: {df.dtypes}")

# ספירת ערכים חסרים
print("\n1.2 שימוש ב-null_count()")
print("-" * 40)

print("ספירת nulls בכל העמודות:")
print(df.null_count())

print("\nספירת nulls בעמודה אחת בלבד:")
print(df.select('avg_temp_celsius').null_count())

print("\nספירת nulls עם pl.col():")
print(df.select(pl.col('avg_temp_celsius').null_count()))

# שימוש ב-is_null()
print("\n1.3 שימוש ב-is_null()")
print("-" * 40)

print("ספירה עם is_null() + sum():")
result = df.select(
    pl.col('avg_temp_celsius')
    .is_null()
    .sum()
)
print(result)

print("\nסינון שורות עם null:")
null_rows = (
    df
    .filter(pl.col('avg_temp_celsius').is_null())
    .select(pl.len())
)
print(f"מספר שורות עם null: {null_rows.item()}")

print("\nשימוש ב-shape:")
null_rows_count = df.filter(pl.col('avg_temp_celsius').is_null()).shape[0]
print(f"מספר שורות עם null (דרך shape): {null_rows_count}")

# זיהוי NaN
print("\n1.4 זיהוי ערכי NaN")
print("-" * 40)

print("ספירת NaN:")
nan_count = df.select(
    pl.col('avg_temp_celsius')
    .is_nan()
    .sum()
)
print(nan_count)

print("\nסינון שורות עם NaN:")
nan_rows = (
    df
    .filter(pl.col('avg_temp_celsius').is_nan())
    .select(pl.len())
)
print(f"מספר שורות עם NaN: {nan_rows.item()}")

print("\n📊 סיכום:")
print(f"  • סה\"כ שורות: {len(df)}")
print(f"  • שורות עם null: {null_rows_count}")
print(f"  • שורות עם NaN: {nan_rows.item()}")
print(f"  • שורות עם נתונים תקינים: {len(df) - null_rows_count - nan_rows.item()}")

# ==============================================================================
# חלק 2: מחיקת ערכים חסרים (Deleting Missing Values)
# ==============================================================================

print("\n\n" + "=" * 80)
print("חלק 2: מחיקת שורות ועמודות עם ערכים חסרים")
print("=" * 80)

# יצירת DataFrame חדש (או טעינת קובץ CSV)
print("\n2.1 הכנת הנתונים")
print("-" * 40)

# אם יש קובץ CSV, אפשר לטעון אותו:
# df = pl.read_csv('../data/temperatures.csv')

# אחרת, נשתמש בנתונים שיצרנו:
print("משתמש בנתונים מהדוגמה הקודמת:")
print(df.head())

# מחיקת שורות עם null
print("\n2.2 שימוש ב-drop_nulls()")
print("-" * 40)

print("לפני מחיקה:")
print(f"  • סה\"כ שורות: {len(df)}")
print(f"  • nulls בטמפרטורה: {df.null_count()['avg_temp_celsius'][0]}")

df_no_nulls = df.drop_nulls()
print("\nאחרי drop_nulls():")
print(f"  • סה\"כ שורות: {len(df_no_nulls)}")
print(df_no_nulls.null_count())

print("\n⚠️ שימו לב: drop_nulls() לא מוחק NaN!")
print(f"  • NaN שנשארו: {df_no_nulls.select(pl.col('avg_temp_celsius').is_nan().sum()).item()}")

# מחיקת גם NaN
print("\n2.3 מחיקת null + NaN")
print("-" * 40)

# המרת NaN ל-null ואז מחיקה
df_fully_clean = (
    df
    .with_columns(pl.col('avg_temp_celsius').fill_nan(None))
    .drop_nulls()
)

print(f"לפני ניקוי: {len(df)} שורות")
print(f"אחרי ניקוי מלא: {len(df_fully_clean)} שורות")
print(f"נמחקו: {len(df) - len(df_fully_clean)} שורות")

print("\nהנתונים המנוקים:")
print(df_fully_clean)

# מחיקת עמודה
print("\n2.4 מחיקת עמודות")
print("-" * 40)

# דוגמה: יצירת DataFrame עם עמודה נוספת
df_with_extra_col = df.with_columns(
    pl.lit(None).alias('empty_column')
)

print("לפני מחיקת עמודה:")
print(df_with_extra_col.columns)

df_dropped = df_with_extra_col.drop('empty_column')
print("\nאחרי מחיקת העמודה 'empty_column':")
print(df_dropped.columns)

# ==============================================================================
# חלק 3: מילוי ערכים חסרים (Filling Missing Values)
# ==============================================================================

print("\n\n" + "=" * 80)
print("חלק 3: מילוי ערכים חסרים")
print("=" * 80)

# נחזור לנתונים המקוריים
df = pl.DataFrame({
    'date': date_col,
    'avg_temp_celsius': avg_temp_c_list
}, strict=False)

# המרת NaN ל-null כדי שהפונקציות יעבדו
df = df.with_columns(
    pl.col('avg_temp_celsius').fill_nan(None)
)

print("\n3.1 מילוי בערך קבוע")
print("-" * 40)

df_filled_zero = df.with_columns(
    pl.col('avg_temp_celsius').fill_null(0).alias('filled_with_zero')
)

print("מילוי באפס:")
print(df_filled_zero.select(['avg_temp_celsius', 'filled_with_zero']))

# מילוי באסטרטגיות סטטיסטיות
print("\n3.2 אסטרטגיות מילוי סטטיסטיות")
print("-" * 40)

df_strategies = df.select(
    pl.col('avg_temp_celsius'),
    mean_filled=pl.col('avg_temp_celsius').fill_null(strategy='mean'),
    min_filled=pl.col('avg_temp_celsius').fill_null(strategy='min'),
    max_filled=pl.col('avg_temp_celsius').fill_null(strategy='max'),
)

print("השוואת אסטרטגיות מילוי:")
print(df_strategies)

print("\n📊 ערכים שנוצרו:")
print(f"  • ממוצע: {df.select(pl.col('avg_temp_celsius').mean()).item():.2f}")
print(f"  • מינימום: {df.select(pl.col('avg_temp_celsius').min()).item():.2f}")
print(f"  • מקסימום: {df.select(pl.col('avg_temp_celsius').max()).item():.2f}")

# אינטרפולציה
print("\n3.3 אינטרפולציה (Interpolation)")
print("-" * 40)

df_interpolated = df.select(
    'avg_temp_celsius',
    interpolated_linear=pl.col('avg_temp_celsius').interpolate(),
    interpolated_nearest=pl.col('avg_temp_celsius').interpolate(method='nearest')
)

print("אינטרפולציה לינארית vs. nearest:")
print(df_interpolated)

# מילוי מותאם אישית
print("\n3.4 מילוי מותאם אישית")
print("-" * 40)

df_custom = df.select(
    'avg_temp_celsius',
    avg_temp_median=pl.col('avg_temp_celsius')
        .fill_null(
            pl.col('avg_temp_celsius').median()
        ),
    avg_temp_max_minus_min=pl.col('avg_temp_celsius')
        .fill_null(
            pl.col('avg_temp_celsius').max() - pl.col('avg_temp_celsius').min()
        )
)

print("מילוי בחציון ובטווח (max-min):")
print(df_custom)

median_val = df.select(pl.col('avg_temp_celsius').median()).item()
range_val = (df.select(pl.col('avg_temp_celsius').max()).item() - 
             df.select(pl.col('avg_temp_celsius').min()).item())

print(f"\n📊 חציון: {median_val:.1f}")
print(f"📊 טווח (max-min): {range_val:.1f}")

# ==============================================================================
# חלק 4: Forward Fill ו-Backward Fill
# ==============================================================================

print("\n\n" + "=" * 80)
print("חלק 4: Forward Fill ו-Backward Fill")
print("=" * 80)

# יצירת דוגמה פשוטה יותר
print("\n4.1 יצירת נתונים לדוגמה")
print("-" * 40)

df_fills = pl.DataFrame({
    'values': [1, 2, None, None, None, 3, 4, None, 5]
})

print("DataFrame עם ערכים חסרים:")
print(df_fills)

# השוואת שיטות מילוי
print("\n4.2 השוואת שיטות Forward ו-Backward Fill")
print("-" * 40)

df_fills_result = df_fills.select(
    'values',
    forward_fill=pl.col('values').forward_fill(),
    forward_fill_1=pl.col('values').forward_fill(limit=1),
    backward_fill=pl.col('values').backward_fill(),
    backward_fill_2=pl.col('values').backward_fill(limit=2),
)

print("תוצאות:")
print(df_fills_result)

print("\n📝 הסבר:")
print("  • forward_fill: ממלא את כל ה-nulls בערך הקודם")
print("  • forward_fill(limit=1): ממלא רק null אחד אחרי כל ערך")
print("  • backward_fill: ממלא את כל ה-nulls בערך הבא")
print("  • backward_fill(limit=2): ממלא רק 2 nulls לפני כל ערך")

# ==============================================================================
# סיכום כללי
# ==============================================================================

print("\n\n" + "=" * 80)
print("✅ סיכום")
print("=" * 80)

print("""
בקובץ זה למדנו:

1️⃣ זיהוי ערכים חסרים:
   • null_count() - ספירת nulls
   • is_null() - זיהוי שורות
   • is_nan() - זיהוי NaN

2️⃣ מחיקת ערכים חסרים:
   • drop_nulls() - מחיקת שורות
   • drop() - מחיקת עמודות
   • המרת NaN ל-null

3️⃣ מילוי ערכים חסרים:
   • fill_null() - מילוי בערך קבוע
   • אסטרטגיות: mean, min, max
   • interpolate() - אינטרפולציה
   • מילוי מותאם אישית

4️⃣ Forward/Backward Fill:
   • forward_fill() - מילוי קדימה
   • backward_fill() - מילוי אחורה
   • שימוש ב-limit

🎯 מה הלאה?
   • התנסו עם הנתונים שלכם
   • נסו אסטרטגיות מילוי שונות
   • השוו ביצועים
   • קראו את המדריך המקיף!

בהצלחה! 🐻‍❄️
""")

# הרצה של הקובץ
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("הקובץ הסתיים בהצלחה! ✨")
    print("=" * 80)
