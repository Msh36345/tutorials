# 📖 מדריך מהיר: Polars - Reshaping & Tidying Data

## 🎯 סיכום תמציתי

מדריך זה מכיל את כל הפקודות והדפוסים החשובים לעיצוב וארגון נתונים ב-Polars.

---

## 📑 תוכן עניינים

1. [Unpivot (Melt)](#unpivot)
2. [Pivot](#pivot)
3. [Join](#join)
4. [Concatenation](#concatenation)
5. [טכניקות נוספות](#additional)
6. [Selectors](#selectors)
7. [טיפים ודיבאג](#tips)

---

<a id="unpivot"></a>
## 🔄 Unpivot (Melt) - הפיכת עמודות לשורות

### תחביר בסיסי

```python
df.unpivot(
    index='column_to_keep',      # עמודות שנשארות קבועות
    on=['col1', 'col2', ...],    # עמודות להפוך לשורות
    variable_name='category',    # שם לעמודת הקטגוריות
    value_name='value'           # שם לעמודת הערכים
)
```

### דוגמאות מהירות

```python
# דוגמה 1: Unpivot בסיסי
df.unpivot(
    index='year',
    on=['sales', 'profit', 'costs']
)

# דוגמה 2: עם Selectors
df.unpivot(
    index='id',
    on=cs.numeric()  # כל העמודות המספריות
)

# דוגמה 3: עם LazyFrame (מהיר יותר)
df.lazy().unpivot(
    index='id',
    on=cs.numeric()
).collect()
```

### מתי להשתמש?
- ✅ כאשר יש עמודות רבות של אותו סוג מדידה
- ✅ לפני ויזואליזציה או ניתוח לפי קטגוריה
- ✅ לפני group_by על משתנה קטגורי

---

<a id="pivot"></a>
## 🔁 Pivot - הפיכת שורות לעמודות

### תחביר בסיסי

```python
df.pivot(
    index='key_column',          # עמודת המפתח
    values='value_column',       # הערכים למלא
    on='pivot_column',           # העמודה שתהפוך לעמודות
    aggregate_function='sum'     # פונקציית אגרגציה (אם יש כפילויות)
)
```

### דוגמאות מהירות

```python
# דוגמה 1: Pivot פשוט
df.pivot(
    index='year',
    values='count',
    on='category'
)

# דוגמה 2: עם כפילויות - חובה aggregate_function
df.pivot(
    index='date',
    values='sales',
    on='product',
    aggregate_function='sum'
)

# דוגמה 3: שמירת רשימות
df.pivot(
    index='id',
    values='score',
    on='subject',
    aggregate_function=pl.element()
)
```

### פונקציות אגרגציה נפוצות
| פונקציה | תיאור | דוגמה |
|---------|--------|-------|
| `'sum'` | סכום | `aggregate_function='sum'` |
| `'mean'` | ממוצע | `aggregate_function='mean'` |
| `'min'` | מינימום | `aggregate_function='min'` |
| `'max'` | מקסימום | `aggregate_function='max'` |
| `'count'` | ספירה | `aggregate_function='count'` |
| `pl.element()` | רשימה | `aggregate_function=pl.element()` |

### אלטרנטיבה: Group By

```python
# Pivot עם group_by (יותר שליטה)
df.group_by('id').agg(
    pl.col('value').filter(pl.col('type') == 'A').sum().alias('A'),
    pl.col('value').filter(pl.col('type') == 'B').sum().alias('B')
)
```

---

<a id="join"></a>
## 🔗 Join - חיבור טבלאות

### תחביר בסיסי

```python
df1.join(
    df2,
    left_on='key1',       # מפתח בטבלה שמאלית
    right_on='key2',      # מפתח בטבלה ימנית
    how='inner',          # סוג Join
    validate='1:m'        # אופציונלי: וולידציה
)
```

### סוגי Join

| סוג | תיאור | שימוש |
|-----|--------|-------|
| `'inner'` | רק שורות משותפות | `how='inner'` |
| `'left'` | כל השמאליות | `how='left'` |
| `'right'` | כל הימניות | `how='right'` |
| `'outer'` | כל השורות | `how='outer'` |
| `'semi'` | שורות שמאליות עם התאמה | `how='semi'` |
| `'anti'` | שורות שמאליות ללא התאמה | `how='anti'` |
| `'cross'` | מכפלה קרטזית | `how='cross'` |

### וולידציה

```python
# בדיקת יחס 1:1
df1.join(df2, on='id', how='inner', validate='1:1')

# בדיקת יחס 1:many
df1.join(df2, on='id', how='inner', validate='1:m')

# בדיקת יחס many:1
df1.join(df2, on='id', how='inner', validate='m:1')
```

### ASOF Join (לזמנים)

```python
# Join על בסיס הזמן הקרוב ביותר
df1.set_sorted('time').join_asof(
    df2.set_sorted('time'),
    on='time',
    strategy='backward'  # או 'forward', 'nearest'
)
```

### דוגמאות

```python
# דוגמה 1: Join פשוט
students.join(grades, on='student_id')

# דוגמה 2: Join עם שמות שונים
df1.join(
    df2,
    left_on='emp_id',
    right_on='employee_id'
)

# דוגמה 3: Join עם מספר מפתחות
df1.join(
    df2,
    on=['year', 'month']
)
```

---

<a id="concatenation"></a>
## 📚 Concatenation - שרשור טבלאות

### שרשור אנכי (שורות)

```python
# שיטה 1: concat
pl.concat([df1, df2, df3], how='vertical')

# שיטה 2: vstack
df1.vstack(df2).vstack(df3)

# שיטה 3: extend (משנה במקום!)
df1.extend(df2)
```

### שרשור אופקי (עמודות)

```python
# שיטה 1: concat
pl.concat([df1, df2], how='horizontal')

# שיטה 2: hstack
df1.hstack(df2)
```

### טיפול באורכים שונים

```python
# concat ממלא null אוטומטית
pl.concat([df1, df2, df3], how='horizontal')

# hstack דורש אורכים זהים!
df1.hstack(df2)  # ייכשל אם אורכים שונים
```

---

<a id="additional"></a>
## 🛠️ טכניקות נוספות

### Partition - חלוקה לקבוצות

```python
# חלוקה לפי עמודה
partitions = df.partition_by('category')

# מחזיר רשימה של DataFrames
for partition in partitions:
    print(partition)
```

### Transpose - היפוך

```python
# היפוך שורות ועמודות
df.transpose(include_header=True)
```

### Reshape - שינוי צורה

```python
# שינוי לצורת array
df.select(
    pl.col('column').reshape((rows, cols))
)
```

### Unstack - פריסה

```python
# פריסת עמודה למספר עמודות
df.unstack(
    step=5,
    columns='values',
    how='vertical'
)
```

---

<a id="selectors"></a>
## 🎯 Selectors - בחירה חכמה

### Selectors נפוצים

```python
from polars import selectors as cs

# בחירת טיפוסים
cs.numeric()          # כל המספרים
cs.string()           # כל המחרוזות
cs.float()            # רק Float
cs.integer()          # רק Integer
cs.boolean()          # רק Boolean
cs.temporal()         # תאריכים/זמנים

# בחירה לפי שם
cs.starts_with('sales_')   # מתחיל ב...
cs.ends_with('_2024')      # מסתיים ב...
cs.contains('total')       # מכיל...
cs.matches(r'col_\d+')     # Regex

# שילובים
cs.numeric() & cs.contains('price')  # AND
cs.string() | cs.temporal()          # OR
~cs.numeric()                        # NOT
```

### דוגמאות שימוש

```python
# המרת כל המספרים ל-Int64
df.select(cs.numeric().cast(pl.Int64))

# Unpivot של כל עמודות המכירות
df.unpivot(
    index='date',
    on=cs.starts_with('sales_')
)

# מילוי null בכל העמודות המספריות
df.with_columns(
    cs.numeric().fill_null(0)
)
```

---

<a id="tips"></a>
## 💡 טיפים ודיבאג

### טיפים לביצועים

```python
# 1. השתמש ב-LazyFrame
df.lazy()...collect()

# 2. סנן מוקדם
df.filter(...).unpivot(...)  # ✓ טוב
df.unpivot(...).filter(...)  # ✗ פחות טוב

# 3. השתמש ב-Selectors
df.select(cs.numeric())      # ✓ טוב
df.select(['col1', 'col2'])  # ✓ גם טוב, אבל פחות גמיש
```

### בדיקות נפוצות

```python
# בדיקת גודל
print(f"צורה: {df.shape}")
print(f"עמודות: {df.columns}")

# בדיקת טיפוסים
print(df.dtypes)

# בדיקת null values
print(df.null_count())

# בדיקת unique values
print(df['column'].n_unique())

# סטטיסטיקות
print(df.describe())
```

### שגיאות נפוצות ופתרונות

#### שגיאה 1: "found multiple elements"

```python
# ❌ בעיה
df.pivot(index='id', values='score', on='category')

# ✓ פתרון
df.pivot(
    index='id',
    values='score',
    on='category',
    aggregate_function='sum'  # הוסף פונקציית אגרגציה!
)
```

#### שגיאה 2: "did not fulfil validation"

```python
# ❌ בעיה
df1.join(df2, on='id', validate='1:1')

# ✓ פתרון
# שנה את הוולידציה או תקן את הנתונים
df1.join(df2, on='id', validate='1:m')
```

#### שגיאה 3: "could not create DataFrame"

```python
# ❌ בעיה - אורכים שונים ב-hstack
df1.hstack(df2)

# ✓ פתרון - השתמש ב-concat במקום
pl.concat([df1, df2], how='horizontal')
```

---

## 📊 טבלת השוואה: Polars vs Pandas

| פעולה | Pandas | Polars |
|-------|--------|--------|
| Unpivot | `melt()` | `unpivot()` |
| Pivot | `pivot()` | `pivot()` |
| Join | `merge()` | `join()` |
| Concat אנכי | `concat(axis=0)` | `concat(how='vertical')` |
| Concat אופקי | `concat(axis=1)` | `concat(how='horizontal')` |
| Group By | `groupby()` | `group_by()` |
| Filter | `df[df['col'] > 5]` | `df.filter(pl.col('col') > 5)` |

---

## 🔍 דפוסים נפוצים

### דפוס 1: Wide → Long → Analysis

```python
# 1. Wide to Long
long_df = df.unpivot(
    index='id',
    on=cs.numeric()
)

# 2. ניתוח
result = (
    long_df
    .group_by('variable')
    .agg(pl.col('value').mean())
)
```

### דפוס 2: Join → Unpivot → Aggregate

```python
# 1. חיבור טבלאות
joined = df1.join(df2, on='key')

# 2. Unpivot
long = joined.unpivot(index='key', on=cs.numeric())

# 3. אגרגציה
result = long.group_by('variable').agg(
    pl.col('value').sum()
)
```

### דפוס 3: Partition → Process → Concat

```python
# 1. חלוקה
partitions = df.partition_by('category')

# 2. עיבוד כל חלק
processed = [process(p) for p in partitions]

# 3. שרשור חזרה
result = pl.concat(processed)
```

---

## 🎓 לימוד מתקדם

### נושאים למיקוד הבא

1. **Window Functions** - פונקציות חלון
2. **Lazy API** - אופטימיזציות
3. **Expressions** - ביטויים מתקדמים
4. **Streaming** - נתונים גדולים
5. **UDF** - פונקציות מותאמות

### משאבים מומלצים

- 📖 [תיעוד רשמי](https://pola-rs.github.io/polars/)
- 💬 [Discord קהילה](https://discord.gg/4UfP5cfBE7)
- 📺 [סרטונים](https://www.youtube.com/@polarsofficial)
- 🔧 [GitHub](https://github.com/pola-rs/polars)

---

## ⚡ Quick Commands

```bash
# התקנה
pip install polars

# התקנה עם כל התוספים
pip install 'polars[all]'

# עדכון
pip install --upgrade polars
```

---

**מעודכן:** 2024 | **גרסה:** 1.0 | **שפה:** עברית + English

**רישיון:** ניתן לשימוש חופשי

---

## 📝 הערות סיום

מדריך זה מכסה את 90% מהשימושים היומיומיים ב-Polars. 

**זכרו:**
- 🎯 תרגול הוא המפתח
- 📚 קראו את התיעוד הרשמי
- 💬 הצטרפו לקהילה
- 🚀 התחילו עם דוגמאות פשוטות

**בהצלחה!** 🎉
