# ⚡ מדריך מהיר: טיפול בערכים חסרים ב-Polars

<div dir="rtl">

> **סיכום תמציתי** של כל הפקודות והדפוסים החשובים לטיפול בערכים חסרים ב-Polars

---

## 📋 תוכן עניינים מהיר

- [זיהוי ערכים חסרים](#זיהוי-ערכים-חסרים)
- [מחיקת ערכים חסרים](#מחיקת-ערכים-חסרים)
- [מילוי ערכים חסרים](#מילוי-ערכים-חסרים)
- [טבלאות השוואה](#טבלאות-השוואה)
- [דפוסים נפוצים](#דפוסים-נפוצים)
- [טיפים ודיבאג](#טיפים-ודיבאג)

---

## 🔍 זיהוי ערכים חסרים

### פקודות בסיסיות

```python
# ספירת nulls בכל העמודות
df.null_count()

# ספירת nulls בעמודה אחת
df.select(pl.col('column').null_count())

# ספירת NaN
df.select(pl.col('column').is_nan().sum())

# בדיקה אם יש nulls
df.select(pl.col('column').is_null().any())

# אחוז ערכים חסרים
(df.null_count() / len(df) * 100)
```

### זיהוי שורות

```python
# שורות עם null
df.filter(pl.col('column').is_null())

# שורות ללא null
df.filter(pl.col('column').is_not_null())

# שורות עם NaN
df.filter(pl.col('column').is_nan())

# מספר שורות עם null
df.filter(pl.col('column').is_null()).shape[0]
```

---

## 🗑️ מחיקת ערכים חסרים

### מחיקת שורות

```python
# מחיקת כל השורות עם null בכל עמודה
df.drop_nulls()

# מחיקת שורות עם null בעמודות ספציפיות
df.drop_nulls(subset=['col1', 'col2'])

# מחיקת null + NaN
df.with_columns(pl.all().fill_nan(None)).drop_nulls()
```

### מחיקת עמודות

```python
# מחיקת עמודה אחת
df.drop('column_name')

# מחיקת מספר עמודות
df.drop(['col1', 'col2'])

# מחיקת עמודות עם יותר מ-X% nulls
threshold = 0.5
cols_to_drop = [
    col for col in df.columns
    if df.select(pl.col(col).null_count()).item() / len(df) > threshold
]
df.drop(cols_to_drop)
```

---

## 📝 מילוי ערכים חסרים

### מילוי בערכים קבועים

```python
# מילוי באפס
df.with_columns(pl.col('column').fill_null(0))

# מילוי בערך מותאם
df.with_columns(pl.col('column').fill_null(999))

# מילוי במחרוזת
df.with_columns(pl.col('column').fill_null('לא ידוע'))
```

### אסטרטגיות סטטיסטיות

```python
# ממוצע
pl.col('column').fill_null(strategy='mean')

# מינימום
pl.col('column').fill_null(strategy='min')

# מקסימום
pl.col('column').fill_null(strategy='max')

# אפס
pl.col('column').fill_null(strategy='zero')

# אחד
pl.col('column').fill_null(strategy='one')
```

### מילוי מותאם אישית

```python
# חציון
pl.col('column').fill_null(pl.col('column').median())

# ממוצע משוקלל
pl.col('column').fill_null(
    pl.col('column').mean() * 0.5 + pl.col('column').median() * 0.5
)

# טווח (max - min)
pl.col('column').fill_null(
    pl.col('column').max() - pl.col('column').min()
)

# ממוצע נע (rolling mean)
pl.col('column').rolling_mean(window_size=3)
```

### אינטרפולציה

```python
# לינארית (ברירת מחדל)
pl.col('column').interpolate()

# nearest (הקרוב ביותר)
pl.col('column').interpolate(method='nearest')
```

### Forward/Backward Fill

```python
# Forward fill (מילוי קדימה)
pl.col('column').forward_fill()

# Forward fill עם הגבלה
pl.col('column').forward_fill(limit=2)

# Backward fill (מילוי אחורה)
pl.col('column').backward_fill()

# Backward fill עם הגבלה
pl.col('column').backward_fill(limit=2)
```

---

## 📊 טבלאות השוואה

### מתי להשתמש בכל שיטה?

| שיטה | מתאים ל... | דוגמאות | יתרונות | חסרונות |
|------|------------|----------|---------|----------|
| **drop_nulls** | מעט ערכים חסרים | אימות נתונים | פשוט, מהיר | אובדן נתונים |
| **fill_null(0)** | ערכי ברירת מחדל | כמות גשמים, ספירות | ברור, עקבי | לא תמיד הגיוני |
| **mean/median** | נתונים סטטיסטיים | סקרים, מדידות | שומר על התפלגות | לא לסדרות זמן |
| **interpolate** | סדרות זמן רציפות | טמפרטורות, מחירים | מעבר חלק | דורש סדר |
| **forward_fill** | נתונים קבועים עד לשינוי | מלאי, סטטוס | הגיוני לזמן | לא למדידות |
| **backward_fill** | תחזיות, לוח זמנים | אירועים מתוכננים | שימושי לעתיד | פחות נפוץ |

### השוואה: null vs NaN

| תכונה | `null` | `NaN` |
|-------|--------|-------|
| **מקור** | היעדר מידע | פעולה מתמטית לא חוקית |
| **ייצוג** | `None` | `np.nan` |
| **זיהוי** | `is_null()` | `is_nan()` |
| **ספירה** | `null_count()` | `is_nan().sum()` |
| **מילוי** | `fill_null()` | `fill_nan()` |
| **מחיקה** | `drop_nulls()` | המרה ל-null תחילה |

---

## 🎯 דפוסים נפוצים

### דפוס 1: ניקוי מלא

```python
# ניקוי מקיף של DataFrame
df_clean = (
    df
    # המרת NaN ל-null
    .with_columns(pl.all().fill_nan(None))
    # מחיקת שורות עם nulls
    .drop_nulls()
)
```

### דפוס 2: מילוי חכם לפי סוג עמודה

```python
# מילוי מספרים בממוצע, טקסט בערך ברירת מחדל
df_filled = df.with_columns([
    # עמודות מספריות
    pl.col(pl.NUMERIC_DTYPES).fill_null(strategy='mean'),
    # עמודות טקסט
    pl.col(pl.Utf8).fill_null('לא ידוע')
])
```

### דפוס 3: טיפול בסדרות זמן

```python
# טיפול אופטימלי בנתוני זמן
df_time = (
    df
    # המרת NaN
    .with_columns(pl.col('value').fill_nan(None))
    # אינטרפולציה
    .with_columns(pl.col('value').interpolate().alias('value_filled'))
    # מילוי פערים שנשארו בקצוות
    .with_columns(pl.col('value_filled').forward_fill())
)
```

### דפוס 4: דיווח על ערכים חסרים

```python
# יצירת דוח מקיף
missing_report = pl.DataFrame({
    'column': df.columns,
    'null_count': [df[col].null_count() for col in df.columns],
    'null_percent': [df[col].null_count() / len(df) * 100 for col in df.columns]
}).sort('null_percent', descending=True)

print(missing_report)
```

### דפוס 5: מילוי לפי קבוצות

```python
# מילוי ערכים חסרים לפי קבוצות
df_grouped = df.with_columns(
    pl.col('value')
      .fill_null(pl.col('value').mean())
      .over('category')  # לפי קטגוריה
)
```

---

## 🔧 טיפים ודיבאג

### בעיות נפוצות ופתרונות

#### ❌ בעיה 1: `drop_nulls()` לא עובד על NaN

```python
# ❌ לא עובד
df.drop_nulls()  # NaN נשארים

# ✅ פתרון
df.with_columns(pl.all().fill_nan(None)).drop_nulls()
```

#### ❌ בעיה 2: אסטרטגיות fill_null לא עובדות

```python
# ❌ שגיאה
df.select(pl.col('column').fill_null(strategy='mean'))

# ✅ צריך with_columns
df.with_columns(pl.col('column').fill_null(strategy='mean'))
```

#### ❌ בעיה 3: אינטרפולציה לא עובדת היטב

```python
# ⚠️ צריך סדר
# אינטרפולציה עובדת לפי הסדר בטבלה

# ✅ מיינו לפני אינטרפולציה
df.sort('date').with_columns(
    pl.col('value').interpolate()
)
```

### טיפים לביצועים

```python
# ✅ השתמשו ב-lazy evaluation למהירות
(
    pl.scan_csv('data.csv')
    .with_columns(pl.all().fill_nan(None))
    .drop_nulls()
    .collect()  # מבצע רק בסוף
)

# ✅ מלאו רק את מה שצריך
df.with_columns(
    pl.col(['col1', 'col2']).fill_null(0)
)
# במקום
# df.with_columns(pl.all().fill_null(0))
```

### בדיקות לפני עיבוד

```python
# בדיקה מהירה
def check_missing(df):
    """בדיקת ערכים חסרים מקיפה"""
    print("=== דוח ערכים חסרים ===")
    print(f"שורות: {len(df)}")
    print(f"עמודות: {len(df.columns)}")
    print("\nלפי עמודה:")
    
    for col in df.columns:
        nulls = df[col].null_count()
        nans = df[col].is_nan().sum() if df[col].dtype in [pl.Float32, pl.Float64] else 0
        total_missing = nulls + nans
        percent = total_missing / len(df) * 100
        
        if total_missing > 0:
            print(f"  {col}: {total_missing} ({percent:.1f}%) - null:{nulls}, NaN:{nans}")

# שימוש
check_missing(df)
```

---

## ⚡ Cheat Sheet - פקודות מהירות

```python
# זיהוי
df.null_count()                              # ספירת nulls
df.select(pl.col('x').is_nan().sum())        # ספירת NaN
df.filter(pl.col('x').is_null())             # שורות עם null

# מחיקה
df.drop_nulls()                              # מחיקת שורות עם null
df.drop('col')                               # מחיקת עמודה

# מילוי - קבוע
pl.col('x').fill_null(0)                    # מילוי באפס
pl.col('x').fill_nan(None)                  # המרת NaN ל-null

# מילוי - סטטיסטי
pl.col('x').fill_null(strategy='mean')      # ממוצע
pl.col('x').fill_null(strategy='min')       # מינימום
pl.col('x').fill_null(strategy='max')       # מקסימום

# מילוי - מתקדם
pl.col('x').interpolate()                   # אינטרפולציה
pl.col('x').forward_fill()                  # מילוי קדימה
pl.col('x').backward_fill()                 # מילוי אחורה
pl.col('x').fill_null(pl.col('x').median()) # חציון

# שרשור
df.with_columns(pl.all().fill_nan(None)).drop_nulls()
```

---

## 🎓 זכרו!

**✅ עשו:**
- בדקו את הנתונים לפני עיבוד (`null_count()`)
- המירו NaN ל-null לפני `drop_nulls()`
- בחרו אסטרטגיה מתאימה לסוג הנתונים
- השתמשו ב-`with_columns()` לשמירת כל העמודות

**❌ אל תעשו:**
- אל תמחקו נתונים בלי בדיקה
- אל תשתמשו באותה שיטת מילוי לכל העמודות
- אל תשכחו NaN (הם לא null!)
- אל תמלאו ערכים חסרים אם המשמעות היא "לא קיים"

---

## 📚 קישורים מהירים

- [תיעוד מלא של Polars](https://pola-rs.github.io/polars/py-polars/html/reference/)
- [API Reference - Missing Data](https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/index.html#missing-data)
- [מדריך משתמש](https://pola-rs.github.io/polars-book/)

---

**🐻‍❄️ בהצלחה עם Polars!**

</div>
