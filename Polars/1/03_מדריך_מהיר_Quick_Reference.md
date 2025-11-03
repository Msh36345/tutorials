# ⚡ Python Polars - מדריך מהיר (Quick Reference)

> **Cheat Sheet** מקיף לעבודה עם Polars - כל מה שצריך במסך אחד!

---

## 📦 התקנה והתחלה

```bash
# התקנה
pip install polars

# ייבוא
import polars as pl
```

---

## 🏗️ יצירה וקריאה

### יצירת DataFrame

```python
# מ-Dictionary
df = pl.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c']
})

# מ-List of Dicts
df = pl.DataFrame([
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30}
])
```

### קריאה מקבצים

| פורמט | Eager (מיידי) | Lazy (עצל) |
|-------|---------------|-----------|
| CSV | `pl.read_csv('file.csv')` | `pl.scan_csv('file.csv')` |
| Parquet | `pl.read_parquet('file.parquet')` | `pl.scan_parquet('file.parquet')` |
| JSON | `pl.read_json('file.json')` | - |
| Excel | `pl.read_excel('file.xlsx')` | - |

```python
# קריאה עם אפשרויות
df = pl.read_csv(
    'data.csv',
    columns=['col1', 'col2'],    # עמודות ספציפיות
    n_rows=1000,                  # מספר שורות
    skip_rows=5,                  # דילוג על שורות
    has_header=True,              # יש כותרת
    separator=';'                 # מפריד
)
```

---

## 🔍 בחינת DataFrame

### מידע בסיסי

```python
df.shape              # (rows, cols) - מימדים
df.height             # מספר שורות
df.width              # מספר עמודות
df.columns            # רשימת שמות עמודות
df.dtypes             # רשימת טיפוסי נתונים
df.schema             # Dictionary של עמודות וטיפוסים

df.head(n=5)          # n שורות ראשונות
df.tail(n=5)          # n שורות אחרונות
df.sample(n=10)       # n שורות אקראיות
df.describe()         # סטטיסטיקות תיאוריות
df.glimpse()          # סקירה מהירה
```

### בדיקת נתונים חסרים

```python
df.null_count()                    # ספירת null בכל עמודה
df.select(pl.all().is_null().sum())  # סה"כ null per column
```

---

## 📊 בחירת עמודות (Select)

### בחירה בסיסית

```python
# עמודה אחת
df.select('col1')
df.select(pl.col('col1'))

# מספר עמודות
df.select(['col1', 'col2', 'col3'])
df.select(pl.col('col1'), pl.col('col2'))

# כל העמודות חוץ מ...
df.select(pl.exclude('col1'))
df.select(pl.exclude(['col1', 'col2']))
```

### בחירה מתקדמת

```python
# לפי דפוס שם
df.select(pl.col('^col.*$'))           # Regex
df.select(pl.col('*_name'))            # wildcard

# לפי טיפוס
df.select(pl.col(pl.Int64))            # רק Int64
df.select(pl.col(pl.Utf8))             # רק String
df.select(pl.col([pl.Int64, pl.Float64]))  # מספרים

# כל העמודות המספריות
df.select(pl.col(pl.NUMERIC_DTYPES))
```

---

## 🔎 סינון שורות (Filter)

### סינון בסיסי

```python
# תנאי יחיד
df.filter(pl.col('age') > 30)
df.filter(pl.col('name') == 'Alice')
df.filter(pl.col('city').is_in(['NY', 'LA']))

# תנאים מרובים
df.filter((pl.col('age') > 30) & (pl.col('city') == 'NY'))
df.filter((pl.col('age') < 20) | (pl.col('age') > 60))
```

### אופרטורים

| אופרטור | משמעות | דוגמה |
|---------|--------|-------|
| `==` | שווה | `pl.col('x') == 5` |
| `!=` | לא שווה | `pl.col('x') != 5` |
| `>` | גדול מ | `pl.col('x') > 5` |
| `<` | קטן מ | `pl.col('x') < 5` |
| `>=` | גדול או שווה | `pl.col('x') >= 5` |
| `<=` | קטן או שווה | `pl.col('x') <= 5` |
| `&` | AND | `(cond1) & (cond2)` |
| `\|` | OR | `(cond1) \| (cond2)` |
| `~` | NOT | `~pl.col('x').is_null()` |

### פונקציות סינון שימושיות

```python
# null values
df.filter(pl.col('age').is_null())
df.filter(pl.col('age').is_not_null())

# השתייכות לרשימה
df.filter(pl.col('city').is_in(['NY', 'LA', 'SF']))

# בין ערכים
df.filter(pl.col('age').is_between(18, 65))

# מחרוזות
df.filter(pl.col('name').str.contains('Alice'))
df.filter(pl.col('name').str.starts_with('A'))
df.filter(pl.col('name').str.ends_with('son'))
```

---

## ✏️ יצירה ושינוי עמודות

### הוספת/שינוי עמודה

```python
# עמודה חדשה
df.with_columns([
    (pl.col('age') * 2).alias('age_doubled')
])

# עמודות מרובות
df.with_columns([
    (pl.col('age') >= 18).alias('is_adult'),
    (pl.col('salary') * 1.1).alias('new_salary')
])

# שינוי עמודה קיימת
df.with_columns([
    (pl.col('age') + 1).alias('age')  # אותו שם = החלפה
])
```

### פעולות נפוצות על עמודות

```python
# מתמטיות
pl.col('x') + 10
pl.col('x') * 2
pl.col('price') * pl.col('quantity')

# תנאים (if-else)
pl.when(pl.col('age') >= 18).then('Adult').otherwise('Minor')

# מילוי ערכים חסרים
pl.col('age').fill_null(0)
pl.col('name').fill_null('Unknown')

# המרת טיפוס
pl.col('age').cast(pl.Float64)
pl.col('date').cast(pl.Date)
```

---

## 🗑️ מחיקה ושינוי שם

### מחיקת עמודות

```python
# עמודה אחת
df.drop('col1')

# מספר עמודות
df.drop(['col1', 'col2', 'col3'])
```

### שינוי שמות

```python
# שינוי שם עמודה
df.rename({'old_name': 'new_name'})

# מספר עמודות
df.rename({
    'old1': 'new1',
    'old2': 'new2'
})
```

---

## 📈 מיון (Sort)

```python
# מיון בסיסי
df.sort('age')                              # עולה
df.sort('age', descending=True)             # יורד

# מיון לפי מספר עמודות
df.sort(['city', 'age'])
df.sort(['city', 'age'], descending=[False, True])

# מיון עם null בהתחלה/סוף
df.sort('age', nulls_last=True)
```

---

## 🔢 אגרגציות (Aggregations)

### אגרגציות פשוטות

```python
# על כל ה-DataFrame
df.select([
    pl.col('age').mean().alias('avg_age'),
    pl.col('salary').sum().alias('total_salary'),
    pl.count().alias('count')
])

# פונקציות אגרגציה נפוצות
.mean()         # ממוצע
.sum()          # סכום
.min()          # מינימום
.max()          # מקסימום
.median()       # חציון
.std()          # סטיית תקן
.var()          # שונות
.count()        # ספירה
.n_unique()     # ערכים ייחודיים
```

### Group By

```python
# קיבוץ בסיסי
df.group_by('city').agg([
    pl.count().alias('count'),
    pl.col('age').mean().alias('avg_age')
])

# קיבוץ לפי מספר עמודות
df.group_by(['city', 'gender']).agg([
    pl.col('salary').mean().alias('avg_salary'),
    pl.col('salary').sum().alias('total_salary')
])

# עם סינון לאחר קיבוץ
df.group_by('city').agg([
    pl.count().alias('count')
]).filter(pl.col('count') > 100)
```

---

## ⛓️ Method Chaining - שרשור פעולות

```python
# דוגמה מורכבת
result = (
    df
    .filter(pl.col('age').is_not_null())        # סינון
    .with_columns([                              # הוספת עמודות
        (pl.col('age') >= 18).alias('is_adult')
    ])
    .filter(pl.col('is_adult'))                  # סינון נוסף
    .select(['name', 'age', 'city'])             # בחירה
    .sort('age', descending=True)                # מיון
    .head(10)                                    # 10 ראשונים
)
```

**💡 טיפ:** השתמשו בסוגריים ומעברי שורה לקריאות!

---

## ⚡ LazyFrame - עיבוד עצל

### יצירה והרצה

```python
# המרה ל-LazyFrame
lazy_df = df.lazy()

# או סריקה ישירה
lazy_df = pl.scan_csv('large_file.csv')

# ביצוע פעולות - לא מבוצע עדיין!
result_lazy = (
    lazy_df
    .filter(pl.col('age') > 30)
    .select(['name', 'age'])
    .sort('age')
)

# ביצוע בפועל
result = result_lazy.collect()

# עם streaming (לקבצים ענקיים)
result = result_lazy.collect(streaming=True)
```

### הצגת תוכנית ביצוע

```python
# לפני אופטימיזציה
print(lazy_df.explain(optimized=False))

# אחרי אופטימיזציה
print(lazy_df.explain(optimized=True))
```

---

## 🔗 Joins - איחוד טבלאות

```python
# Inner Join (ברירת מחדל)
df1.join(df2, on='id')

# Left Join
df1.join(df2, on='id', how='left')

# Right Join
df1.join(df2, on='id', how='right')

# Outer Join
df1.join(df2, on='id', how='outer')

# Join עם עמודות שונות
df1.join(df2, left_on='id1', right_on='id2')

# Join עם מספר עמודות
df1.join(df2, on=['id', 'date'])
```

---

## 💾 שמירה לקבצים

```python
# CSV
df.write_csv('output.csv')

# Parquet (מומלץ!)
df.write_parquet('output.parquet')

# JSON
df.write_json('output.json')

# Excel
df.write_excel('output.xlsx')

# עם אפשרויות
df.write_csv(
    'output.csv',
    separator=';',
    has_header=True,
    quote_style='necessary'
)
```

---

## 🎯 טיפים ו-Best Practices

### ✅ עשו (DO)

1. **השתמשו ב-LazyFrame** לקבצים גדולים
   ```python
   pl.scan_csv('big.csv').filter(...).collect()
   ```

2. **סננו מוקדם** - הפחיתו נתונים בהקדם
   ```python
   df.filter(...).select(...) # ✅
   # לא df.select(...).filter(...) # פחות יעיל
   ```

3. **השתמשו ב-`pl.col()`** לבהירות
   ```python
   pl.col('age') > 18  # ✅ ברור
   ```

4. **שרשרו פעולות** עם מעברי שורה
   ```python
   result = (
       df
       .filter(...)
       .select(...)
       .sort(...)
   )  # ✅ קריא
   ```

### ❌ אל תעשו (DON'T)

1. ❌ לא להשתמש ב-`and`/`or` של Python
   ```python
   # ❌ שגוי
   df.filter(pl.col('age') > 18 and pl.col('city') == 'NY')
   
   # ✅ נכון
   df.filter((pl.col('age') > 18) & (pl.col('city') == 'NY'))
   ```

2. ❌ לא לשכוח סוגריים בתנאים
   ```python
   # ❌ עלול לגרום לשגיאות
   df.filter(pl.col('age') > 18 & pl.col('city') == 'NY')
   
   # ✅ תמיד עם סוגריים
   df.filter((pl.col('age') > 18) & (pl.col('city') == 'NY'))
   ```

3. ❌ לא לשכוח `.collect()` ב-LazyFrame
   ```python
   # ❌ לא יבוצע
   result = df.lazy().filter(...)
   
   # ✅ יבוצע
   result = df.lazy().filter(...).collect()
   ```

---

## 🐛 פתרון בעיות נפוצות

### שגיאה: "TypeError: unsupported operand"
**פתרון:** השתמשו ב-`&`, `|` במקום `and`, `or`

### שגיאה: "ColumnNotFoundError"
**פתרון:** בדקו `df.columns` לראות שמות נכונים

### שגיאה: "InvalidOperationError"
**פתרון:** בדקו ערכי null עם `.is_null()` ו-`.is_not_null()`

### LazyFrame לא מחזיר נתונים
**פתרון:** הוסיפו `.collect()` בסוף!

---

## 📚 משאבים נוספים

- 🌐 [Polars Docs](https://pola-rs.github.io/polars/)
- 📖 [User Guide](https://pola-rs.github.io/polars-book/)
- 🔗 [API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/)
- 💬 [Discord](https://discord.gg/4UfP5cfBE7)
- 🐙 [GitHub](https://github.com/pola-rs/polars)

---

## 🚀 סיכום מהיר

```python
import polars as pl

# קריאה
df = pl.read_csv('data.csv')
# או
df = pl.scan_csv('big_data.csv')

# עיבוד
result = (
    df
    .filter((pl.col('age') > 18) & (pl.col('city') == 'NY'))
    .with_columns([
        (pl.col('salary') * 1.1).alias('new_salary')
    ])
    .select(['name', 'age', 'new_salary'])
    .sort('new_salary', descending=True)
    .collect()  # אם LazyFrame
)

# שמירה
result.write_parquet('output.parquet')
```

---

<div align="center">

**⚡ Python Polars - מהיר, יעיל, מודרני! ⚡**

Made with ❤️ for the Polars community

</div>
