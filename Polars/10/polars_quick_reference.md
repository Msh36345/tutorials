# 🚀 מדריך מהיר: Polars Interoperability

> מדריך תמציתי לאינטגרציה של Polars עם pandas, NumPy, PyArrow ו-DuckDB

---

## 📋 תוכן עניינים

1. [Polars ↔ pandas](#polars--pandas)
2. [Polars ↔ NumPy](#polars--numpy)
3. [Polars ↔ PyArrow](#polars--pyarrow)
4. [Polars ↔ DuckDB](#polars--duckdb)
5. [טבלת השוואה מהירה](#טבלת-השוואה-מהירה)
6. [דפוסים נפוצים](#דפוסים-נפוצים)
7. [טיפים ודיבאג](#טיפים-ודיבאג)

---

## 🐼 Polars ↔ pandas

### המרה בסיסית

```python
import polars as pl
import pandas as pd

# Polars → pandas
df_pandas = df_polars.to_pandas()

# pandas → Polars (שתי אפשרויות)
df_polars = pl.from_pandas(df_pandas)
df_polars = pl.DataFrame(df_pandas)

# Series
s_pandas = s_polars.to_pandas()
s_polars = pl.from_pandas(s_pandas)
```

### אופציות מתקדמות

```python
# שימוש ב-PyArrow extension arrays (מומלץ!)
df_pandas = df_polars.to_pandas(use_pyarrow_extension_array=True)

# שמירה על טיפוסי נתונים מדויקים יותר
# מהיר יותר בהמרות הבאות
```

### מתי להשתמש?

| מצב | פתרון |
|-----|--------|
| קוד קיים ב-pandas | `to_pandas()` |
| ספרייה שתומכת רק ב-pandas | `to_pandas()` |
| נתונים קטנים (<1M שורות) | כל אחד בסדר |
| נתונים גדולים (>1M שורות) | **תישארו ב-Polars!** |

---

## 🔢 Polars ↔ NumPy

### DataFrame ↔ Array

```python
import numpy as np

# NumPy → Polars DataFrame
arr = np.array([[1, 2, 3], [4, 5, 6]])

# orient='col': כל עמודה ב-array = עמודה ב-DataFrame
df = pl.from_numpy(arr, schema=['a', 'b', 'c'], orient='col')

# orient='row': כל שורה ב-array = שורה ב-DataFrame  
df = pl.from_numpy(arr, schema=['a', 'b'], orient='row')

# Polars → NumPy
arr = df.to_numpy()                    # array רגיל
arr = df.to_numpy(structured=True)     # structured array (עם שמות עמודות)
```

### Series ↔ Array

```python
# Polars Series → NumPy array
s = pl.Series([1, 2, 3, 4, 5])
arr = s.to_numpy()

# NumPy array → Polars Series
s = pl.Series('name', arr)
```

### שימוש בפונקציות NumPy על Polars

```python
# חישובים מתמטיים
df.with_columns([
    np.sqrt(pl.col('a')).alias('sqrt_a'),
    np.power(pl.col('b'), 2).alias('b_squared'),
    np.log(pl.col('c')).alias('log_c'),
    np.gcd(pl.col('a'), pl.col('b')).alias('gcd')
])

# פונקציות שימושיות
np.mean(arr)      # ממוצע
np.std(arr)       # סטיית תקן
np.median(arr)    # חציון
np.percentile(arr, 75)  # אחוזון
```

### פונקציות NumPy פופולריות

| קטגוריה | פונקציות |
|----------|----------|
| **בסיסי** | `np.sum`, `np.mean`, `np.std`, `np.var` |
| **מינימום/מקסימום** | `np.min`, `np.max`, `np.argmin`, `np.argmax` |
| **מתמטיקה** | `np.sqrt`, `np.exp`, `np.log`, `np.power` |
| **טריגונומטריה** | `np.sin`, `np.cos`, `np.tan` |
| **עיגול** | `np.round`, `np.floor`, `np.ceil` |
| **מספרים שלמים** | `np.gcd`, `np.lcm`, `np.abs` |

---

## 🏹 Polars ↔ PyArrow

### המרות בסיסיות

```python
import pyarrow as pa

# Polars → PyArrow Table
table = df.to_arrow()

# PyArrow Table → Polars
df = pl.from_arrow(table)

# Series → PyArrow Array
arr = s.to_arrow()

# PyArrow Array → Series
s = pl.Series(arr)
```

### עבודה עם PyArrow Datasets

```python
import pyarrow.dataset as ds

# קריאת dataset מחולק (partitioned)
dataset = ds.dataset('path/to/partitioned/data', 
                     partitioning=ds.partitioning(flavor='hive'))

# המרה ל-Polars
df = pl.from_arrow(dataset.to_table())

# או סריקה lazy (מומלץ לנתונים גדולים!)
lf = pl.scan_pyarrow_dataset(dataset)
```

### שמירה וטעינה מהירה

```python
# Parquet (המהיר ביותר!)
df.write_parquet('data.parquet')
df = pl.read_parquet('data.parquet')

# Feather (גם מהיר)
df.write_ipc('data.feather')
df = pl.read_ipc('data.feather')
```

### למה PyArrow?

✅ **מהיר ביותר** לקריאה/כתיבה  
✅ **חיסכון במקום** (דחיסה טובה)  
✅ **תואם** בין שפות (Python, R, Java)  
✅ **יעיל** בזיכרון  

---

## 🦆 Polars ↔ DuckDB

### שימוש בסיסי

```python
import duckdb

# הרצת SQL על Polars DataFrame
# שימו לב: DuckDB "רואה" את df ישירות!
result = duckdb.sql('SELECT * FROM df WHERE age > 25')

# המרה חזרה ל-Polars
df_result = result.pl()

# או הצגה ישירה
result.show()
```

### שאילתות נפוצות

```python
# סינון
duckdb.sql('SELECT * FROM df WHERE city = "תל אביב"')

# קיבוץ
duckdb.sql('''
    SELECT 
        department,
        COUNT(*) as count,
        AVG(salary) as avg_salary
    FROM df
    GROUP BY department
''')

# מיון
duckdb.sql('SELECT * FROM df ORDER BY age DESC LIMIT 10')

# JOIN
duckdb.sql('''
    SELECT *
    FROM df1
    INNER JOIN df2 ON df1.id = df2.user_id
''')
```

### פונקציות SQL שימושיות

```python
# סטטיסטיקות
duckdb.sql('''
    SELECT 
        COUNT(*) as total,
        AVG(value) as mean,
        MEDIAN(value) as median,
        STDDEV(value) as std,
        MIN(value) as min,
        MAX(value) as max
    FROM df
''')

# CASE WHEN (תנאים)
duckdb.sql('''
    SELECT 
        name,
        CASE 
            WHEN score >= 90 THEN 'מצוין'
            WHEN score >= 80 THEN 'טוב'
            ELSE 'לא טוב'
        END as grade
    FROM df
''')

# Window Functions
duckdb.sql('''
    SELECT 
        name,
        salary,
        RANK() OVER (ORDER BY salary DESC) as rank
    FROM df
''')
```

### למה DuckDB?

✅ **תחביר SQL** מוכר ונוח  
✅ **מהיר מאוד** על נתונים גדולים  
✅ **אינטגרציה מושלמת** עם Polars  
✅ **תומך בכל** SQL המודרני (CTEs, Window Functions, וכו')  

---

## 📊 טבלת השוואה מהירה

| ספרייה | שימוש עיקרי | מהירות | נוחות |
|--------|-------------|--------|-------|
| **pandas** | עיבוד נתונים כללי | 🐌 | ⭐⭐⭐⭐⭐ |
| **NumPy** | חישובים מתמטיים | 🚀 | ⭐⭐⭐⭐ |
| **PyArrow** | I/O מהיר, Parquet | 🚀🚀🚀 | ⭐⭐⭐ |
| **DuckDB** | שאילתות SQL מורכבות | 🚀🚀 | ⭐⭐⭐⭐⭐ |
| **Polars** | הכל! | 🚀🚀 | ⭐⭐⭐⭐ |

---

## 💼 דפוסים נפוצים

### דפוס 1: טעינה מהירה + עיבוד

```python
# טעינה מהירה עם PyArrow
df = pl.read_parquet('big_file.parquet')

# עיבוד עם Polars
df = df.filter(pl.col('date') > '2024-01-01')

# ייצוא ל-pandas רק לצורך הצגה
df.head(10).to_pandas()
```

### דפוס 2: שילוב עם קוד pandas קיים

```python
# קוד ישן ב-pandas
def old_pandas_function(df_pandas):
    # עיבוד מורכב...
    return df_pandas

# שימוש עם Polars
df_polars = pl.read_csv('data.csv')
df_pandas = df_polars.to_pandas()
result_pandas = old_pandas_function(df_pandas)
result_polars = pl.from_pandas(result_pandas)
```

### דפוס 3: חישובים מתמטיים מתקדמים

```python
# עיבוד בסיסי ב-Polars
df = pl.read_csv('data.csv')

# המרה ל-NumPy לחישובים מתמטיים
arr = df.select(['x', 'y', 'z']).to_numpy()

# חישובים מתקדמים
from scipy import stats
correlation = np.corrcoef(arr.T)
p_values = stats.pearsonr(arr[:, 0], arr[:, 1])

# חזרה ל-Polars
df = df.with_columns(
    pl.Series('correlation', correlation[0])
)
```

### דפוס 4: SQL על נתונים מרובים

```python
import duckdb

# טעינת מספר DataFrames
df_sales = pl.read_csv('sales.csv')
df_customers = pl.read_csv('customers.csv')
df_products = pl.read_csv('products.csv')

# שאילתת SQL מורכבת
result = duckdb.sql('''
    SELECT 
        c.customer_name,
        p.product_name,
        SUM(s.amount) as total_amount
    FROM df_sales s
    JOIN df_customers c ON s.customer_id = c.id
    JOIN df_products p ON s.product_id = p.id
    GROUP BY c.customer_name, p.product_name
    HAVING total_amount > 1000
    ORDER BY total_amount DESC
''')

# המרה חזרה ל-Polars
final_df = result.pl()
```

### דפוס 5: Pipeline מלא

```python
# 1. טעינה מהירה
df = pl.read_parquet('data.parquet')

# 2. עיבוד ב-Polars
df = (df
    .filter(pl.col('status') == 'active')
    .group_by('category')
    .agg([
        pl.col('amount').sum().alias('total'),
        pl.col('id').count().alias('count')
    ])
)

# 3. חישובים עם NumPy
df = df.with_columns(
    np.log1p(pl.col('total')).alias('log_total')
)

# 4. שאילתת SQL מורכבת
result = duckdb.sql('''
    SELECT *,
        RANK() OVER (ORDER BY total DESC) as rank
    FROM df
''').pl()

# 5. שמירה
result.write_parquet('output.parquet')
```

---

## 🔧 טיפים ודיבאג

### ⚡ טיפים לביצועים

```python
# ✅ טוב: השתמש ב-PyArrow extension arrays
df.to_pandas(use_pyarrow_extension_array=True)

# ❌ לא טוב: המרה רגילה (איטית יותר)
df.to_pandas()

# ✅ טוב: scan_pyarrow_dataset לנתונים גדולים
lf = pl.scan_pyarrow_dataset(dataset)

# ❌ לא טוב: טעינת הכל לזיכרון
df = pl.from_arrow(dataset.to_table())

# ✅ טוב: שמירה ב-Parquet (מהיר ודחוס)
df.write_parquet('data.parquet')

# ❌ לא טוב: שמירה ב-CSV (איטי וגדול)
df.write_csv('data.csv')
```

### 🐛 בעיות נפוצות ופתרונות

#### בעיה 1: טיפוסי נתונים לא מתאימים

```python
# בעיה: לאחר המרה מ-pandas, טיפוסי הנתונים משתנים
df_pandas = pd.DataFrame({'a': [1, 2, 3]})
df_polars = pl.from_pandas(df_pandas)
# 'a' עשוי להיות Int64 במקום UInt32

# פתרון: הגדרת schema מפורשת
df_polars = pl.from_pandas(df_pandas).with_columns([
    pl.col('a').cast(pl.UInt32)
])
```

#### בעיה 2: orient מבלבל ב-from_numpy

```python
# בעיה: לא בטוח איזה orient להשתמש?
arr = np.array([[1, 2], [3, 4], [5, 6]])

# זכרו:
# orient='col' → arr.shape[0] = מספר שורות, arr.shape[1] = מספר עמודות
df = pl.from_numpy(arr, schema=['A', 'B'], orient='col')
# תוצאה: 3 שורות, 2 עמודות (A, B)

# orient='row' → arr.shape[0] = מספר עמודות, arr.shape[1] = מספר שורות  
df = pl.from_numpy(arr, schema=['R1', 'R2', 'R3'], orient='row')
# תוצאה: 2 שורות, 3 עמודות (R1, R2, R3)
```

#### בעיה 3: DuckDB לא רואה את ה-DataFrame

```python
# בעיה: NameError: name 'my_df' is not defined
my_df = pl.DataFrame({'a': [1, 2, 3]})
result = duckdb.sql('SELECT * FROM my_df')  # ❌ שגיאה!

# פתרון: השתמש בשם המשתנה בדיוק כמו שהוא
result = duckdb.sql('SELECT * FROM my_df')  # ✅ עובד!

# או: העבר את ה-DataFrame במפורש
result = duckdb.query('SELECT * FROM df', alias='df', df=my_df)
```

#### בעיה 4: זיכרון גבוה בהמרות

```python
# בעיה: זיכרון כפול כשממירים DataFrame גדול
big_df_polars = pl.read_csv('huge_file.csv')  # 5GB
big_df_pandas = big_df_polars.to_pandas()      # עוד 5GB!

# פתרון 1: המר רק את מה שצריך
small_df = big_df_polars.head(1000).to_pandas()

# פתרון 2: עבוד עם חלקים (chunks)
for chunk_df in big_df_polars.iter_slices(100000):
    chunk_pandas = chunk_df.to_pandas()
    # עיבוד...

# פתרון 3: תישאר ב-Polars!
result = big_df_polars.filter(...)  # לא צריך pandas
```

#### בעיה 5: Index ב-pandas נעלם

```python
# בעיה: pandas DataFrame עם index מיוחד
df_pandas = pd.DataFrame({'a': [1, 2, 3]}, index=['x', 'y', 'z'])
df_polars = pl.from_pandas(df_pandas)
# ה-index נעלם!

# פתרון: איפוס index לפני ההמרה
df_pandas_reset = df_pandas.reset_index()
df_polars = pl.from_pandas(df_pandas_reset)
```

### 📝 Cheat Sheet - פקודות חיוניות

```python
# ייבואים
import polars as pl
import pandas as pd
import numpy as np
import pyarrow as pa
import duckdb

# Polars → pandas
df.to_pandas()
df.to_pandas(use_pyarrow_extension_array=True)  # מומלץ!

# pandas → Polars
pl.from_pandas(df)
pl.DataFrame(df)

# Polars → NumPy
df.to_numpy()
df.to_numpy(structured=True)
s.to_numpy()

# NumPy → Polars
pl.from_numpy(arr, schema=['col1', 'col2'], orient='col')
pl.from_numpy(arr, schema=['col1', 'col2'], orient='row')

# Polars → PyArrow
df.to_arrow()
s.to_arrow()

# PyArrow → Polars
pl.from_arrow(table)
pl.scan_pyarrow_dataset(dataset)  # lazy

# DuckDB
result = duckdb.sql('SELECT * FROM df')
df_result = result.pl()
result.show()
```

---

## 🎯 מתי להשתמש במה?

### תרחישים נפוצים

| מה אתה צריך לעשות? | איזה כלי? | למה? |
|---------------------|-----------|------|
| עיבוד נתונים גדולים | **Polars** | הכי מהיר |
| שאילתות SQL מורכבות | **DuckDB** | תחביר נוח |
| חישובים מתמטיים מתקדמים | **NumPy** | פונקציות רבות |
| קריאת Parquet מהירה | **PyArrow** | המהיר ביותר |
| עבודה עם קוד קיים | **pandas** | תאימות |
| מכונת למידה (sklearn) | המר ל-**NumPy** | תאימות |
| Plotting (matplotlib) | המר ל-**pandas** | תאימות |
| JOINs מרובים | **DuckDB** | SQL נוח |

### המלצה כללית

```
התחל ב-Polars → עבד ב-Polars → המר רק בסוף (אם בכלל!)
```

**סדר עדיפויות:**
1. נסה לעשות הכל ב-Polars
2. אם צריך SQL - השתמש ב-DuckDB
3. אם צריך math - השתמש ב-NumPy
4. אם צריך I/O מהיר - PyArrow
5. pandas רק אם אין ברירה!

---

## 🔗 קישורים שימושיים

- [Polars Documentation](https://docs.pola.rs/)
- [pandas Comparison](https://docs.pola.rs/user-guide/migration/pandas/)
- [PyArrow Guide](https://arrow.apache.org/docs/python/)
- [DuckDB SQL Reference](https://duckdb.org/docs/sql/introduction)
- [NumPy Reference](https://numpy.org/doc/stable/reference/)

---

## 📌 סיכום מהיר

### פקודות חיוניות (חייב לזכור!)

```python
# pandas
df_pandas = df_polars.to_pandas()
df_polars = pl.from_pandas(df_pandas)

# NumPy  
arr = df.to_numpy()
df = pl.from_numpy(arr, schema=['a', 'b'])

# PyArrow
table = df.to_arrow()
df = pl.from_arrow(table)

# DuckDB
result = duckdb.sql('SELECT * FROM df').pl()
```

### זהירות! ⚠️

- ❌ אל תמיר DataFrame גדול ל-pandas אם לא חייב
- ❌ אל תשכח `use_pyarrow_extension_array=True`
- ❌ אל תשכח `orient` ב-`from_numpy`
- ✅ תמיד תתחיל ותסיים ב-Polars
- ✅ תשתמש ב-lazy evaluation כשאפשר

---

**🎉 זהו! עכשיו יש לך מדריך מלא לכל ההמרות!**

זכור: Polars הוא המקום הכי טוב להיות. המר לספריות אחרות רק כשבאמת צריך! 🚀
