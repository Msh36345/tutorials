# 📋 מדריך מהיר - Polars: טרנספורמציה של נתונים

> **Cheat Sheet מקיף** לעבודה עם Polars - טכניקות טרנספורמציה של נתונים

---

## 🚀 התחלה מהירה

### ייבוא והגדרות בסיסיות

```python
import polars as pl
from polars import selectors as cs
from datetime import date
import os

# הגדרות תצוגה
os.environ['POLARS_FMT_STR_LEN'] = '50'
```

### טעינת נתונים

```python
# Eager (מיידי)
df = pl.read_csv('file.csv', try_parse_dates=True)

# Lazy (אופטימיזציה אוטומטית)
lf = pl.scan_csv('file.csv', try_parse_dates=True)
result = lf.select(...).filter(...).collect()
```

---

## 📊 1. צברים פשוטים (Simple Aggregations)

### פונקציות צבירה בסיסיות

| פונקציה | תיאור | דוגמה |
|---------|-------|-------|
| `sum()` | סכום | `df.select(pl.col('price').sum())` |
| `mean()` | ממוצע | `df.select(pl.col('age').mean())` |
| `median()` | חציון | `df.select(pl.col('score').median())` |
| `min()` / `max()` | מינימום/מקסימום | `df.select(pl.col('temp').max())` |
| `count()` | ספירה | `df.select(pl.col('id').count())` |
| `std()` | סטיית תקן | `df.select(pl.col('values').std())` |
| `var()` | שונות | `df.select(pl.col('values').var())` |
| `first()` / `last()` | ראשון/אחרון | `df.select(pl.col('name').first())` |

### בחירת עמודות לפי טיפוס

```python
# כל העמודות המספריות
df.select(cs.numeric()).sum()

# כל העמודות מסוג String
df.select(cs.string())

# כל העמודות מסוג Date/Datetime
df.select(cs.temporal())
```

### צבירה מותנית

```python
# ספירת ערכים שעומדים בתנאי
df.select((pl.col('quantity') >= 4).sum())

# סכום עם סינון
df.select(
    pl.col('quantity')
      .filter(pl.col('store') == 'Online')
      .sum()
)
```

### describe() - סטטיסטיקה מהירה

```python
df.select(cs.numeric()).describe()
# מחזיר: count, null_count, mean, std, min, 25%, 50%, 75%, max
```

---

## 👥 2. קיבוץ וצבירה (Group By)

### תבנית בסיסית

```python
df.group_by('column').agg(
    pl.col('value').sum().alias('total'),
    pl.col('value').mean().alias('average')
)
```

### דוגמאות שימושיות

```python
# קיבוץ פשוט
df.group_by('brand').agg(pl.col('sales').sum())

# קיבוץ מרובה עמודות
df.group_by('category', 'brand').agg(
    pl.col('price').mean().alias('avg_price'),
    pl.len().alias('count')
)

# קיבוץ עם שמירת סדר
df.group_by('brand', maintain_order=True).agg(...)

# קיבוץ עם חישוב
df.group_by(
    pl.col('date').dt.year().alias('year')
).agg(pl.col('sales').sum())
```

### פעולות מתקדמות

```python
# חישובים מרובים
df.group_by('brand').agg(
    pl.col('price').mean().round(2).alias('avg_price'),
    (pl.col('price').sum() / pl.len()).alias('avg_price2'),
    pl.col('customer').first(),
    pl.col('category').n_unique()  # ספירת ערכים ייחודיים
)

# קיבוץ עם איסוף ערכים לרשימה
df.group_by('brand').agg(pl.col('products'))
```

### איטרציה על קבוצות

```python
for name, data in df.group_by('brand'):
    print(f"Brand: {name[0]}")
    print(data.head())
```

---

## ↔️ 3. צבירה אופקית (Horizontal Aggregations)

### פונקציות אופקיות בסיסיות

| פונקציה | תיאור | דוגמה |
|---------|-------|-------|
| `sum_horizontal()` | סכום אופקי | `pl.sum_horizontal('a', 'b', 'c')` |
| `mean_horizontal()` | ממוצע אופקי | `pl.mean_horizontal('x', 'y', 'z')` |
| `max_horizontal()` | מקסימום אופקי | `pl.max_horizontal(cols)` |
| `min_horizontal()` | מינימום אופקי | `pl.min_horizontal(cols)` |
| `all_horizontal()` | AND לוגי | `pl.all_horizontal(pl.col(cols) > 0)` |
| `any_horizontal()` | OR לוגי | `pl.any_horizontal(pl.col(cols) > 100)` |

### דוגמאות שימוש

```python
# סכום מספר עמודות
df.with_columns(
    pl.sum_horizontal('price', 'tax', 'shipping').alias('total')
)

# ממוצע
df.select(
    pl.mean_horizontal('score1', 'score2', 'score3').alias('avg_score')
)

# סינון לפי תנאי על כל העמודות
df.filter(pl.all_horizontal(pl.col(['a', 'b', 'c']) > 10))
```

### concat_list

```python
# יצירת רשימות מעמודות
df.with_columns(
    pl.concat_list('hp', 'attack', 'defense')
      .list.sum()
      .alias('total_stats')
)

# שרשור מחרוזות
df.select(
    pl.concat_str(['first_name', 'last_name'], separator=' ')
      .alias('full_name')
)
```

### reduce ו-fold

```python
# reduce - התחלה מהעמודה הראשונה
cols = ['a', 'b', 'c', 'd']
df.with_columns(
    pl.reduce(
        function=lambda acc, col: acc + col,
        exprs=pl.col(cols)
    ).alias('sum')
)

# fold - עם ערך התחלתי
df.with_columns(
    pl.fold(
        acc=pl.lit(0),
        function=lambda acc, col: acc + col,
        exprs=pl.col(cols)
    ).alias('sum_from_zero')
)

# שרשור תנאים עם AND
df.filter(
    pl.fold(
        acc=pl.lit(True),
        function=lambda acc, col: acc & col,
        exprs=pl.col(cols) > 10
    )
)
```

---

## 🪟 4. פונקציות חלון (Window Functions)

### תבנית בסיסית - over()

```python
df.select(
    'category',
    pl.col('sales').sum().over('category').alias('total_by_category')
)
```

### ההבדל בין group_by ל-over()

```python
# group_by - שורה אחת לקבוצה
df.group_by('category').agg(pl.col('sales').sum())
# Output: n_categories שורות

# over() - שומר כל השורות
df.select(pl.col('sales').sum().over('category'))
# Output: n_rows שורות
```

### דוגמאות שימושיות

```python
# ממוצע לפי קבוצה
df.with_columns(
    pl.col('price').mean().over('brand').alias('avg_brand_price')
)

# קיבוץ מרובה
df.select(
    pl.col('sales').sum().over('category', 'region').alias('sales_by_cat_region')
)

# חישוב אחוז
df.with_columns(
    (pl.col('sales') / pl.col('sales').sum().over('category') * 100)
      .alias('percent_of_category')
)

# עם חישובים מורכבים
df.select(
    pl.col('sales').mean().over('brand', pl.col('date').dt.year())
)
```

### דירוג (Ranking)

```python
# דירוג גלובלי
df.with_columns(
    pl.col('sales').rank(descending=True).alias('rank')
)

# דירוג בתוך קבוצות
df.with_columns(
    pl.col('sales')
      .rank(descending=True)
      .over('category')
      .alias('rank_in_category')
)

# שיטות דירוג
# 'average' - ברירת מחדל, ממוצע לערכים שווים
# 'min' - דירוג מינימלי
# 'max' - דירוג מקסימלי
# 'dense' - ללא פערים
# 'ordinal' - סדר הופעה
df.with_columns(
    pl.col('score').rank(method='dense').alias('rank')
)
```

### אסטרטגיות Mapping

```python
# join (ברירת מחדל) - שומר רק שורות מתאימות
df.with_columns(
    pl.col('name')
      .sort_by('score')
      .head(3)
      .over('team', mapping_strategy='join')
)

# explode - משכפל שורות
df.with_columns(
    pl.col('name')
      .sort_by('score')
      .over('team', mapping_strategy='explode')
)
```

### פונקציות שימושיות עם over()

```python
# shift - הזזה
df.with_columns(
    pl.col('sales').shift(1).over('category').alias('previous_sales')
)

# diff - הפרש
df.with_columns(
    pl.col('sales').diff().over('category').alias('sales_change')
)

# cumsum - סכום מצטבר
df.with_columns(
    pl.col('sales').cum_sum().over('category').alias('cumulative_sales')
)

# pct_change - אחוז שינוי
df.with_columns(
    pl.col('sales').pct_change().over('category').alias('sales_pct_change')
)
```

---

## 🔧 5. פונקציות מוגדרות משתמש (UDFs)

### map_elements - תבנית בסיסית

```python
def my_function(value: str) -> str:
    return value.upper()

df.select(
    pl.col('name').map_elements(
        lambda x: my_function(x),
        return_dtype=pl.String
    ).alias('name_upper')
)
```

### ⚠️ חשוב - UDFs איטיים!

```python
# ❌ איטי - UDF
df.select(
    pl.col('name').map_elements(
        lambda x: x.split(' ')[0],
        return_dtype=pl.String
    )
)

# ✅ מהיר - פונקציה מובנית
df.select(
    pl.col('name').str.split(' ').list.first()
)
```

### טיפוסי return_dtype נפוצים

```python
pl.String    # מחרוזת
pl.Int64     # מספר שלם
pl.Float64   # מספר עשרוני
pl.Boolean   # אמת/שקר
pl.Date      # תאריך
pl.List      # רשימה
```

### אלטרנטיבות מומלצות

```python
# במקום UDF למיפוי ערכים
# ❌ איטי
df.select(pl.col('status').map_elements(lambda x: status_map[x], ...))

# ✅ מהיר
df.select(pl.col('status').replace(status_map))

# במקום UDF לתנאים
# ❌ איטי
df.select(pl.col('age').map_elements(lambda x: 'child' if x < 18 else 'adult', ...))

# ✅ מהיר
df.select(
    pl.when(pl.col('age') < 18)
      .then(pl.lit('child'))
      .otherwise(pl.lit('adult'))
)
```

---

## 🗄️ 6. SQL ב-Polars

### התחלת עבודה

```python
# Eager mode
ctx = pl.SQLContext(eager=True)
ctx.register('my_table', df)

result = ctx.execute("""
    SELECT * FROM my_table WHERE price > 100
""")

# Lazy mode
result = pl.SQLContext(lf=df.lazy()).execute("""
    SELECT * FROM lf LIMIT 10
""").collect()
```

### תחביר SQL נפוץ

```python
# SELECT בסיסי
"""
SELECT 
    column1,
    column2,
    column3 as alias
FROM table_name
WHERE condition
ORDER BY column1 DESC
LIMIT 10
"""

# GROUP BY
"""
SELECT 
    category,
    AVG(price) as avg_price,
    COUNT(*) as count
FROM sales
GROUP BY category
HAVING avg_price > 50
ORDER BY count DESC
"""

# JOIN
"""
SELECT 
    a.id,
    a.name,
    b.value
FROM table_a as a
LEFT JOIN table_b as b
    ON a.id = b.id
"""
```

### טיפים חשובים

```python
# שמות עמודות עם רווחים - השתמש ב-backticks
"""
SELECT `Customer Name`, `Order Date` FROM df
"""

# רישום מספר טבלאות
ctx.register('sales', sales_df)
ctx.register('products', products_df)
ctx.execute("""
    SELECT * FROM sales s
    JOIN products p ON s.product_id = p.id
""")
```

---

## 🎯 טיפים לפתרון בעיות נפוצות

### Debug וטיפול בשגיאות

```python
# הצגת query plan
lf.show_graph()

# בדיקת schema
df.schema

# בדיקת nulls
df.null_count()

# הצגה מפורטת יותר
df.describe()

# בדיקת duplicates
df.is_duplicated().sum()
df.unique()
```

### בעיות ביצועים

```python
# ✅ טוב - Lazy evaluation
pl.scan_csv('file.csv').filter(...).select(...).collect()

# ❌ רע - Eager
pl.read_csv('file.csv').filter(...).select(...)

# ✅ טוב - פונקציות מובנות
df.select(pl.col('name').str.to_uppercase())

# ❌ רע - UDF
df.select(pl.col('name').map_elements(lambda x: x.upper(), ...))

# ✅ טוב - filter לפני select
df.filter(...).select(...)

# ❌ רע - select לפני filter
df.select(...).filter(...)
```

### טיפים לזיכרון

```python
# streaming mode לקבצים ענקיים
lf.collect(streaming=True)

# קריאה בחלקים
for batch in pl.read_csv_batched('huge.csv', batch_size=10000):
    process(batch)

# שימוש בטיפוסים קטנים יותר
df.with_columns(pl.col('age').cast(pl.UInt8))
```

---

## 📊 טבלאות עזר

### המרות טיפוסים (Casting)

```python
pl.Int8, pl.Int16, pl.Int32, pl.Int64       # שלמים
pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64   # שלמים חיוביים
pl.Float32, pl.Float64                       # עשרוניים
pl.Boolean                                   # בוליאני
pl.String, pl.Utf8                          # מחרוזות
pl.Date, pl.Datetime                        # תאריכים
pl.List, pl.Struct                          # מורכבים
```

### פעולות על מחרוזות

```python
.str.to_uppercase()          # אותיות גדולות
.str.to_lowercase()          # אותיות קטנות
.str.strip_chars()           # הסרת תווים
.str.replace('old', 'new')   # החלפה
.str.contains('pattern')     # בדיקת תוכן
.str.starts_with('prefix')   # מתחיל ב
.str.ends_with('suffix')     # מסתיים ב
.str.split(' ')              # פיצול
.str.slice(0, 5)             # חיתוך
.str.lengths()               # אורכים
```

### פעולות על תאריכים

```python
.dt.year()                   # שנה
.dt.month()                  # חודש
.dt.day()                    # יום
.dt.hour()                   # שעה
.dt.weekday()                # יום בשבוע
.dt.strftime('%Y-%m-%d')     # פורמט
.dt.timestamp()              # Unix timestamp
.dt.truncate('1d')           # עיגול
```

### פעולות על רשימות

```python
.list.len()                  # אורך
.list.sum()                  # סכום
.list.mean()                 # ממוצע
.list.first()                # ראשון
.list.last()                 # אחרון
.list.get(0)                 # גישה לאינדקס
.list.slice(0, 3)            # חיתוך
.list.unique()               # ייחודיים
.list.sort()                 # מיון
.list.reverse()              # הפוך
```

---

## 🚀 דפוסי קוד נפוצים

### טעינה ועיבוד בסיסי

```python
# קריאה, סינון, בחירה
df = (
    pl.read_csv('data.csv')
    .filter(pl.col('age') > 18)
    .select(['name', 'age', 'city'])
    .head(100)
)
```

### צינור עיבוד מלא

```python
result = (
    pl.scan_csv('data.csv', try_parse_dates=True)
    .filter(pl.col('status') == 'active')
    .with_columns([
        (pl.col('price') * pl.col('quantity')).alias('total'),
        pl.col('date').dt.year().alias('year')
    ])
    .group_by('category', 'year')
    .agg([
        pl.col('total').sum().alias('revenue'),
        pl.col('customer_id').n_unique().alias('unique_customers')
    ])
    .sort('revenue', descending=True)
    .collect()
)
```

### ניתוח מהיר

```python
# סטטיסטיקה מהירה
df.select(cs.numeric()).describe()

# חלוקה לפי קבוצה
df.group_by('category').agg([
    pl.col('price').mean(),
    pl.col('price').std(),
    pl.len()
])

# Top N
df.sort('sales', descending=True).head(10)
```

### ניקוי נתונים

```python
df_clean = (
    df
    .drop_nulls()                                    # הסרת nulls
    .unique()                                        # הסרת כפולים
    .with_columns(
        pl.col('price').fill_null(0),               # מילוי nulls
        pl.col('name').str.strip_chars().str.to_uppercase()
    )
)
```

---

## ⚡ Best Practices

### ✅ עשה

1. **השתמש ב-Lazy evaluation** לקבצים גדולים
2. **השתמש בפונקציות מובנות** במקום UDFs
3. **סנן מוקדם** ככל האפשר
4. **השתמש ב-expressions** במקום לולאות
5. **קרא את הדוקומנטציה** - יש הרבה פונקציות!

### ❌ אל תעשה

1. **אל תשתמש ב-UDFs** אלא אם אין ברירה
2. **אל תטען הכל לזיכרון** - השתמש ב-scan במקום read
3. **אל תעשה iterrows()** - זה איטי מאוד
4. **אל תשכח את return_dtype** ב-map_elements
5. **אל תשתמש ב-pandas habits** - Polars שונה!

---

## 🆘 פתרון בעיות נפוצות

### שגיאה: ColumnNotFoundError

```python
# בדוק שמות עמודות
print(df.columns)

# שימוש ב-try-except
try:
    df.select('colum')  # שם שגוי
except pl.ColumnNotFoundError:
    print("העמודה לא קיימת!")
```

### שגיאה: SchemaError

```python
# וודא שהטיפוסים תואמים
df.schema  # בדוק טיפוסים נוכחיים
df = df.cast({'age': pl.Int64})  # המר טיפוס
```

### ביצועים איטיים

```python
# השתמש ב-lazy
lf = pl.scan_csv('file.csv')

# הפעל אופטימיזציה
lf = lf.filter(...).select(...)
result = lf.collect()

# או streaming
result = lf.collect(streaming=True)
```

### בעיות זיכרון

```python
# קרא בחלקים
reader = pl.read_csv_batched('huge.csv', batch_size=10000)
for batch in reader:
    process(batch)

# או השתמש בטיפוסים קטנים
df = df.with_columns(
    pl.col('age').cast(pl.UInt8),
    pl.col('status').cast(pl.Categorical)
)
```

---

## 📚 משאבים נוספים

### קישורים שימושיים

- [תיעוד רשמי](https://pola-rs.github.io/polars/)
- [API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/)
- [GitHub](https://github.com/pola-rs/polars)
- [Discord Community](https://discord.gg/4UfP5cfBE7)

### ספרים ומדריכים

- [Polars Cookbook](https://pola-rs.github.io/polars-book/)
- [User Guide](https://pola-rs.github.io/polars/user-guide/)

---

## 🎓 לסיום

זכור:
- 📖 **תיעוד** - תמיד קרא את התיעוד
- 🧪 **נסה** - התנסה עם דוגמאות קטנות
- ⚡ **אופטימיזציה** - השתמש ב-lazy evaluation
- 🎯 **פשטות** - פונקציות מובנות > UDFs
- 💡 **למידה** - Polars מתפתח - עקוב אחר עדכונים!

**בהצלחה! 🚀**

---

*מדריך מהיר זה מכסה את העיקר - לפרטים נוספים, עיין במחברת המקיפה!*
