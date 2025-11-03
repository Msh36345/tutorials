# 📖 מדריך מהיר: Polars Python

> **מדריך ייחוס מהיר (Quick Reference)** לניתוח נתונים עם Polars

---

## 📑 תוכן עניינים

1. [התקנה ויבוא](#1-התקנה-ויבוא)
2. [יצירה וטעינה](#2-יצירה-וטעינה)
3. [בדיקת DataFrame](#3-בדיקת-dataframe)
4. [המרת סוגי נתונים](#4-המרת-סוגי-נתונים)
5. [בחירה וסינון](#5-בחירה-וסינון)
6. [כפילויות](#6-כפילויות)
7. [ערכים חסרים](#7-ערכים-חסרים)
8. [צבירה וקיבוץ](#8-צבירה-וקיבוץ)
9. [מיזוג וחיבור](#9-מיזוג-וחיבור)
10. [ויזואליזציה](#10-ויזואליזציה)
11. [ערכים חריגים](#11-ערכים-חריגים)
12. [טיפים מתקדמים](#12-טיפים-מתקדמים)

---

## 1. התקנה ויבוא

### 💻 התקנה

```bash
# התקנה בסיסית
pip install polars

# עם תכונות נוספות
pip install 'polars[all]'

# עם Plotly לויזואליזציה
pip install polars plotly
```

### 📦 יבוא

```python
import polars as pl
import polars.selectors as cs  # לבחירת עמודות
import plotly.express as px    # לגרפים
```

---

## 2. יצירה וטעינה

### 📄 טעינה מקבצים

```python
# CSV
df = pl.read_csv('file.csv')
df = pl.read_csv('file.csv', separator=';')  # עם מפריד אחר

# Excel
df = pl.read_excel('file.xlsx')

# JSON
df = pl.read_json('file.json')

# Parquet (מומלץ!)
df = pl.read_parquet('file.parquet')
```

### 🏗️ יצירה ידנית

```python
# מ-dictionary
df = pl.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Tel Aviv', 'Haifa', 'Jerusalem']
})

# מ-lists
df = pl.DataFrame([
    ['Alice', 25],
    ['Bob', 30]
], schema=['name', 'age'], orient='row')
```

### ⚡ LazyFrame (עיבוד עצל)

```python
# טעינה עצלה (לא טוען מיד לזיכרון)
lf = pl.scan_csv('large_file.csv')

# עיבוד
result = (
    lf
    .filter(pl.col('age') > 25)
    .select(['name', 'age'])
    .collect()  # רק כאן נטענים הנתונים!
)
```

---

## 3. בדיקת DataFrame

### 👀 תצוגה בסיסית

```python
df.head()           # 5 שורות ראשונות
df.head(10)         # 10 שורות ראשונות
df.tail()           # 5 שורות אחרונות
df.sample(10)       # 10 שורות אקראיות
```

### 📊 מידע על המבנה

```python
df.shape            # (שורות, עמודות)
df.columns          # רשימת שמות עמודות
df.dtypes           # סוגי הנתונים
df.schema           # מבנה מפורט

df.glimpse()        # סקירה מהירה
df.describe()       # סטטיסטיקות
```

### 🔍 מידע נוסף

```python
df.estimated_size('mb')    # גודל בזיכרון
df.null_count()            # ערכים חסרים
df.is_empty()              # האם ריק?
len(df)                    # מספר שורות
```

---

## 4. המרת סוגי נתונים

### 🔄 המרות בסיסיות

```python
# המרה פשוטה
df = df.with_columns(
    pl.col('age').cast(pl.Int64),
    pl.col('salary').cast(pl.Float64)
)

# המרה למחרוזת
df = df.with_columns(
    pl.col('id').cast(pl.Utf8)
)
```

### 📅 המרה לתאריכים

```python
# מ-string לתאריך
df = df.with_columns(
    pl.col('date_str').str.strptime(pl.Date, '%Y-%m-%d')
)

# שיטה פשוטה יותר
df = df.with_columns(
    pl.col('date_str').str.to_date('%d/%m/%Y')
)

# לזמן (datetime)
df = df.with_columns(
    pl.col('datetime_str').str.strptime(pl.Datetime, '%Y-%m-%d %H:%M:%S')
)
```

### 📋 פורמטי תאריך נפוצים

| פורמט | דוגמה | קוד |
|-------|--------|-----|
| ISO | 2023-12-31 | `%Y-%m-%d` |
| ישראלי | 31/12/2023 | `%d/%m/%Y` |
| אמריקאי | 12/31/2023 | `%m/%d/%Y` |
| עם זמן | 2023-12-31 14:30 | `%Y-%m-%d %H:%M` |

---

## 5. בחירה וסינון

### 🎯 בחירת עמודות

```python
# עמודה אחת
df.select('name')

# מספר עמודות
df.select(['name', 'age'])

# כל העמודות חוץ מ...
df.select(pl.exclude('name'))

# לפי סוג
df.select(cs.numeric())    # מספריות
df.select(cs.string())     # מחרוזות
df.select(cs.temporal())   # תאריכים
```

### 🔍 סינון שורות

```python
# תנאי בסיסי
df.filter(pl.col('age') > 25)

# מספר תנאים (AND)
df.filter(
    (pl.col('age') > 25) & 
    (pl.col('city') == 'Tel Aviv')
)

# תנאי OR
df.filter(
    (pl.col('age') > 60) | 
    (pl.col('age') < 18)
)

# שימוש ב-is_in
df.filter(pl.col('city').is_in(['Tel Aviv', 'Haifa']))

# ערכים לא חסרים
df.filter(pl.col('age').is_not_null())
```

### 🔤 חיפוש במחרוזות

```python
# מכיל
df.filter(pl.col('name').str.contains('Al'))

# מתחיל ב...
df.filter(pl.col('name').str.starts_with('A'))

# מסתיים ב...
df.filter(pl.col('name').str.ends_with('e'))

# case insensitive
df.filter(pl.col('name').str.to_lowercase().str.contains('alice'))
```

---

## 6. כפילויות

### 🔍 זיהוי

```python
# שורות כפולות
df.is_duplicated().sum()

# שורות ייחודיות
df.is_unique().sum()

# מספר ערכים ייחודיים בכל עמודה
df.select(pl.all().n_unique())

# לפי עמודות ספציפיות
df.n_unique(subset=['name', 'age'])
```

### 🗑️ הסרה

```python
# הסרת כפילויות (כל העמודות)
df.unique()

# לפי עמודות ספציפיות
df.unique(subset=['name'], keep='first')  # או 'last', 'none'

# שמירה רק של שורות ייחודיות
unique_rows = df.select(['name', 'age']).is_unique()
df.filter(unique_rows)
```

---

## 7. ערכים חסרים

### 🔍 זיהוי

```python
# ספירת null בכל עמודה
df.null_count()

# אחוז null
df.null_count() / len(df) * 100

# האם יש null?
df.select(pl.col('age').is_null())
```

### 🔧 טיפול

```python
# הסרת שורות עם null
df.drop_nulls()                    # כל העמודות
df.drop_nulls(subset=['age'])      # עמודות ספציפיות

# מילוי ב-0
df.fill_null(0)

# מילוי לפי עמודה
df.with_columns(
    pl.col('age').fill_null(pl.col('age').mean())
)

# forward fill (השתמש בערך הקודם)
df.with_columns(
    pl.col('age').forward_fill()
)

# backward fill
df.with_columns(
    pl.col('age').backward_fill()
)
```

---

## 8. צבירה וקיבוץ

### 📊 פונקציות צבירה

```python
# בסיסי
df.select(
    pl.col('age').mean().alias('avg_age'),
    pl.col('age').sum().alias('total_age'),
    pl.col('age').min().alias('min_age'),
    pl.col('age').max().alias('max_age'),
    pl.col('age').std().alias('std_age'),
    pl.col('age').median().alias('median_age')
)
```

### 👥 קיבוץ (Group By)

```python
# קיבוץ פשוט
df.group_by('city').agg(
    pl.col('age').mean().alias('avg_age'),
    pl.col('age').count().alias('count')
)

# קיבוץ מרובה
df.group_by(['city', 'gender']).agg(
    pl.col('salary').mean(),
    pl.col('salary').median()
)

# מיון לפי תוצאה
df.group_by('city').agg(
    pl.col('age').mean()
).sort('age', descending=True)
```

---

## 9. מיזוג וחיבור

### 🔗 Join (מיזוג)

```python
# Inner join
df1.join(df2, on='id', how='inner')

# Left join
df1.join(df2, on='id', how='left')

# Right join
df1.join(df2, on='id', how='right')

# Outer join (full)
df1.join(df2, on='id', how='outer')

# מספר עמודות
df1.join(df2, on=['id', 'date'])

# שמות שונים
df1.join(df2, left_on='emp_id', right_on='employee_id')
```

### ⬆️ חיבור אנכי (Concat)

```python
# הוספת שורות
pl.concat([df1, df2], how='vertical')

# הוספת עמודות
pl.concat([df1, df2], how='horizontal')
```

---

## 10. ויזואליזציה

### 📊 תרשימים בסיסיים

```python
import plotly.express as px

# Bar Chart
fig = px.bar(df, x='category', y='value', title='כותרת')
fig.show()

# Line Chart
fig = px.line(df, x='date', y='value', color='group')
fig.show()

# Scatter Plot
fig = px.scatter(df, x='x', y='y', size='size', color='category')
fig.show()

# Box Plot
fig = px.box(df, y='value')
fig.show()
```

### 🎨 התאמה אישית

```python
fig = px.bar(df, x='x', y='y')

# שינוי עיצוב
fig.update_traces(
    marker_color='#FF6B6B',
    width=0.5
)

# שינוי layout
fig.update_layout(
    title='כותרת',
    xaxis_title='ציר X',
    yaxis_title='ציר Y',
    font=dict(size=14)
)

fig.show()
```

---

## 11. ערכים חריגים

### 📦 שיטת IQR (מומלצת)

```python
# חישוב גבולות
q1 = pl.col('value').quantile(0.25)
q3 = pl.col('value').quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

# זיהוי חריגים
is_outlier = (pl.col('value') < lower) | (pl.col('value') > upper)

# הסרה
df.filter(is_outlier.not_())

# החלפה בחציון
df.with_columns(
    pl.when(is_outlier)
      .then(pl.col('value').median())
      .otherwise(pl.col('value'))
      .alias('value')
)
```

### 📊 שיטת Z-Score

```python
# חישוב Z-Score
df = df.with_columns(
    ((pl.col('value') - pl.col('value').mean()) / pl.col('value').std())
    .alias('zscore')
)

# זיהוי חריגים (|Z| > 3)
is_outlier = (pl.col('zscore').abs() > 3)

# הסרה
df.filter(is_outlier.not_())
```

---

## 12. טיפים מתקדמים

### ⚡ ביצועים

```python
# שימוש ב-LazyFrame
lf = pl.scan_csv('file.csv')
result = lf.filter(...).select(...).collect()

# קריאה חלקית
df = pl.read_csv('file.csv', n_rows=1000)

# שימוש ב-streaming (קבצים ענקיים)
result = (
    pl.scan_csv('huge.csv')
    .filter(...)
    .collect(streaming=True)
)
```

### 🔄 שרשרת פעולות (Method Chaining)

```python
result = (
    df
    .filter(pl.col('age') > 25)
    .with_columns(
        (pl.col('salary') * 1.1).alias('new_salary')
    )
    .group_by('department')
    .agg(pl.col('new_salary').mean())
    .sort('new_salary', descending=True)
)
```

### 🎭 Expressions מתקדמות

```python
# When-Then-Otherwise
df.with_columns(
    pl.when(pl.col('age') < 18)
      .then(pl.lit('minor'))
      .when(pl.col('age') < 65)
      .then(pl.lit('adult'))
      .otherwise(pl.lit('senior'))
      .alias('age_group')
)

# חישובים מתקדמים
df.with_columns(
    (pl.col('price') * pl.col('quantity')).alias('total'),
    pl.col('name').str.to_uppercase().alias('name_upper')
)
```

### 📝 Window Functions

```python
# Rank
df.with_columns(
    pl.col('score').rank().over('group').alias('rank')
)

# Rolling mean
df.with_columns(
    pl.col('value').rolling_mean(window_size=3).alias('rolling_avg')
)

# Cumulative sum
df.with_columns(
    pl.col('value').cum_sum().alias('cumsum')
)
```

---

## 🆚 Polars vs Pandas: השוואה מהירה

| תכונה | Polars | Pandas |
|-------|---------|---------|
| **מהירות** | ⚡⚡⚡ מהיר מאוד | ⚡ רגיל |
| **זיכרון** | 💾 יעיל | 💾💾 צורך הרבה |
| **API** | 🎯 אקספרסיבי | 🔧 גמיש |
| **Lazy Evaluation** | ✅ כן | ❌ לא |
| **Null Handling** | ✅ טוב | ⚠️ מסובך |
| **קהילה** | 🌱 צעירה | 🌳 ענקית |

### 📋 תרגום פקודות: Pandas → Polars

| Pandas | Polars |
|--------|---------|
| `df.head()` | `df.head()` |
| `df['col']` | `df.select('col')` |
| `df[df['age'] > 25]` | `df.filter(pl.col('age') > 25)` |
| `df.groupby('col').mean()` | `df.group_by('col').agg(pl.all().mean())` |
| `df.merge(df2, on='id')` | `df.join(df2, on='id')` |
| `df.fillna(0)` | `df.fill_null(0)` |
| `df.drop_duplicates()` | `df.unique()` |

---

## 🐛 פתרון בעיות נפוצות

### ❌ שגיאה: "column not found"

```python
# ✅ פתרון: ודא שמות עמודות
print(df.columns)

# או השתמש ב-select עם regex
df.select(pl.col('^col.*'))  # כל העמודות שמתחילות ב-col
```

### ❌ שגיאה: "TypeError: ... is not a valid type"

```python
# ✅ פתרון: המר סוג
df.with_columns(pl.col('col').cast(pl.Float64))
```

### ❌ ביצועים איטיים

```python
# ✅ פתרון: השתמש ב-LazyFrame
lf = pl.scan_csv('file.csv')
result = lf.filter(...).collect()
```

### ❌ זיכרון נגמר

```python
# ✅ פתרון: streaming
result = (
    pl.scan_csv('huge.csv')
    .filter(...)
    .collect(streaming=True)
)
```

---

## 📊 Cheat Sheet ויזואלי

```
┌─────────────────────────────────────────┐
│         POLARS WORKFLOW                 │
├─────────────────────────────────────────┤
│                                         │
│  1. טעינה → pl.read_csv()              │
│            pl.scan_csv() (lazy)        │
│                                         │
│  2. בדיקה → .glimpse()                 │
│            .describe()                 │
│                                         │
│  3. ניקוי → .drop_nulls()              │
│            .unique()                   │
│                                         │
│  4. המרה → .cast()                     │
│            .str.strptime()             │
│                                         │
│  5. סינון → .filter()                  │
│                                         │
│  6. צבירה → .group_by().agg()          │
│                                         │
│  7. ויזואליזציה → plotly               │
│                                         │
│  8. שמירה → .write_csv()               │
│            .write_parquet()            │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎓 עצות לתרגול

### ✅ המלצות

1. **התחל קטן** - תרגל על DataFrame קטן קודם
2. **שימוש ב-LazyFrame** - לקבצים גדולים תמיד
3. **קרא שגיאות** - הן מסבירות בדיוק מה הבעיה
4. **תעד קוד** - הוסף הערות לקוד שלך
5. **השתמש ב-glimpse()** - לפני כל פעולה חשובה

### ❌ טעויות נפוצות

1. **אל תשכח `.collect()`** - ב-LazyFrame
2. **אל תשתמש ב-loops** - השתמש ב-expressions
3. **אל תטען קובץ שלם** - אם צריך רק חלק
4. **אל תשכח null handling** - תמיד בדוק ערכים חסרים

---

## 🔗 קישורים שימושיים

### תיעוד

- 📚 [Polars Official Docs](https://pola-rs.github.io/polars/)
- 📚 [Plotly Python Docs](https://plotly.com/python/)
- 📚 [Python Data Types](https://docs.python.org/3/library/datatypes.html)

### מדריכים

- 🎥 [YouTube: Polars Tutorial](https://www.youtube.com/results?search_query=polars+tutorial)
- 📝 [Real Python Articles](https://realpython.com/)
- 💻 [Kaggle Learn](https://www.kaggle.com/learn)

### נתונים לתרגול

- 📊 [Kaggle Datasets](https://www.kaggle.com/datasets)
- 📊 [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- 📊 [Data.gov.il](https://data.gov.il/)

---

## 📝 תבנית קוד להעתקה

```python
"""
תבנית סטנדרטית לניתוח נתונים
"""

import polars as pl
import polars.selectors as cs
import plotly.express as px

# 1. טעינה
df = pl.read_csv('data.csv')

# 2. בדיקה ראשונית
print(f"Shape: {df.shape}")
print(df.glimpse())

# 3. ניקוי
df = (
    df
    .drop_nulls()
    .unique()
    .with_columns(
        # המרות
        pl.col('date').str.to_date('%Y-%m-%d'),
        pl.col('value').cast(pl.Float64)
    )
)

# 4. ניתוח
result = (
    df
    .filter(pl.col('value') > 0)
    .group_by('category')
    .agg(
        pl.col('value').mean().alias('avg'),
        pl.col('value').count().alias('count')
    )
    .sort('avg', descending=True)
)

# 5. ויזואליזציה
fig = px.bar(result, x='category', y='avg')
fig.show()

# 6. שמירה
result.write_csv('output.csv')
```

---

## 💡 עצה אחרונה

> **"הדרך הטובה ביותר ללמוד Polars היא לתרגל עם נתונים אמיתיים!"**

התחל עם dataset קטן, נסה את כל הפונקציות, ואז עבור לפרויקטים גדולים יותר.

**בהצלחה! 🚀**

---

*מדריך זה עודכן לאחרונה: נובמבר 2025*
