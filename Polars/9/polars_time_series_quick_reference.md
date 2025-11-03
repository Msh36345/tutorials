# ⚡ מדריך מהיר - ניתוח סדרות זמן ב-Polars

## 📚 תוכן עניינים מהיר
- [עבודה עם תאריכים](#dates)
- [חלונות מתגלגלים](#rolling)
- [דגימה מחדש](#resampling)
- [טיפים ודיבאג](#tips)
- [פקודות נפוצות](#commands)

---

<a id="dates"></a>
## 📅 עבודה עם תאריכים

### טעינה וניתוח

```python
# טעינה אוטומטית
lf = pl.scan_csv('file.csv', try_parse_dates=True)

# המרה ידנית
lf = lf.with_columns(pl.col('datetime').str.to_datetime())
```

### פירוק תאריכים

| פונקציה | תיאור | דוגמה |
|---------|-------|--------|
| `.dt.year()` | שנה | `2024` |
| `.dt.month()` | חודש | `1-12` |
| `.dt.day()` | יום | `1-31` |
| `.dt.hour()` | שעה | `0-23` |
| `.dt.minute()` | דקה | `0-59` |
| `.dt.weekday()` | יום בשבוע | `0-6` |
| `.dt.date()` | תאריך בלבד | `2024-01-15` |
| `.dt.time()` | זמן בלבד | `14:30:00` |

### סינון לפי תאריך

```python
# טווח תאריכים
from datetime import datetime

lf.filter(
    pl.col('datetime').dt.date().is_between(
        datetime(2020, 1, 1),
        datetime(2020, 12, 31)
    )
)

# שעות בוקר
lf.filter(pl.col('datetime').dt.hour() < 12)

# סוף שבוע
lf.filter(pl.col('datetime').dt.weekday().is_in([5, 6]))
```

### אזורי זמן

```python
# החלפת אזור זמן (לא משנה את הזמן)
pl.col('datetime').dt.replace_time_zone('America/New_York')

# המרה לאזור זמן אחר (משנה את הזמן)
pl.col('datetime').dt.convert_time_zone('America/Toronto')
```

### חשבון עם זמנים

```python
# הוספה/הפחתה
pl.col('datetime') + pl.duration(days=7)
pl.col('datetime') - pl.duration(hours=3)

# יחידות זמן
pl.duration(
    weeks=...,
    days=...,
    hours=...,
    minutes=...,
    seconds=...,
    milliseconds=...
)
```

---

<a id="rolling"></a>
## 📈 חלונות מתגלגלים (Rolling Windows)

### פונקציות בסיסיות

```python
# ממוצע נע
pl.col('value').rolling_mean(window_size=7)

# מינימום/מקסימום נע
pl.col('value').rolling_min(7)
pl.col('value').rolling_max(7)

# סכום נע
pl.col('value').rolling_sum(7)

# סטיית תקן נעה
pl.col('value').rolling_std(7)
```

### פרמטרים חשובים

```python
# עם min_periods (למניעת nulls)
pl.col('value').rolling_mean(
    window_size=7,
    min_periods=1  # מחשב גם עם פחות נקודות
)

# חלון מבוסס זמן
pl.col('value').mean().rolling(
    index_column='date',
    period='7d',      # 7 ימים
    closed='right'    # 'left', 'right', 'both', 'none'
)
```

### Rolling Context

```python
# חישוב מרובה בבת אחת
lf.set_sorted('date').rolling(
    'date',
    period='7d'
).agg(
    pl.col('value').mean().alias('avg'),
    pl.col('value').std().alias('std'),
    pl.col('value').min().alias('min')
)
```

### פונקציה מותאמת

```python
def my_function(values):
    return max(values) - min(values)

pl.col('value').rolling_map(my_function, window_size=7)
```

**⚠️ אזהרה:** `rolling_map` איטי - השתמשו בפונקציות מובנות כשאפשר!

---

<a id="resampling"></a>
## ⏱️ דגימה מחדש (Resampling)

### תת-דגימה (Downsampling)

```python
# קיבוץ דינמי
lf.set_sorted('datetime').group_by_dynamic(
    'datetime',
    every='1w'  # תדירות חדשה
).agg(
    pl.col('value').mean()  # אגרגציה
)
```

**תדירויות נפוצות:**
- `'1h'` - שעה
- `'1d'` - יום  
- `'1w'` - שבוע
- `'1mo'` - חודש
- `'1q'` - רבעון
- `'1y'` - שנה

### דגימת יתר (Upsampling)

```python
# ⚠️ דורש DataFrame (לא LazyFrame)
df.upsample(
    time_column='datetime',
    every='15m',
    maintain_order=True
)
```

### אינטרפולציה

```python
# מילוי ערכים חסרים
pl.col('value').interpolate()

# שיטות שונות
pl.col('value').interpolate(method='linear')  # ברירת מחדל
```

### מילוי פערים

```python
# שיטה 1: עם datetime_range
datetime_range = pl.datetime_range(
    start=start_date,
    end=end_date,
    interval='1h',
    eager=True
)

pl.LazyFrame({'datetime': datetime_range}).join(
    lf, on='datetime', how='left'
)

# שיטה 2: forward fill
pl.col('value').fill_null(strategy='forward')

# שיטה 3: backward fill
pl.col('value').fill_null(strategy='backward')
```

---

<a id="tips"></a>
## 💡 טיפים ודיבאג

### בעיות נפוצות ופתרונות

| בעיה | פתרון |
|------|--------|
| `datetime is not sorted` | הוסף `.set_sorted('datetime')` |
| `upsample requires DataFrame` | השתמש ב-`.collect()` קודם |
| יותר מדי nulls בחלון | הוסף `min_periods=1` |
| `rolling_map` איטי | השתמש בפונקציות מובנות |
| אזור זמן שגוי | בדוק `replace` vs `convert` |
| תאריך לא מזוהה | המר עם `str.to_datetime()` |

### בדיקת סוגי נתונים

```python
# בדיקה מהירה
lf.collect_schema()
lf.collect_schema().dtypes()

# האם עמודה ממוינת?
lf.select(pl.col('date').is_sorted())
```

### אופטימיזציה

```python
# ✅ טוב - LazyFrame
lf = pl.scan_csv('file.csv')
result = lf.filter(...).select(...).collect()

# ❌ פחות טוב - DataFrame מיד
df = pl.read_csv('file.csv')
result = df.filter(...).select(...)

# ✅ טוב - פעולות מובנות
pl.col('value').rolling_mean(7)

# ❌ איטי - rolling_map
pl.col('value').rolling_map(lambda x: sum(x)/len(x), 7)
```

### דיבאג

```python
# הצגת שלבים ביניים
lf.head().collect()  # תמיד בדקו עם head קודם

# ספירת nulls
lf.select(pl.col('value').is_null().sum())

# סטטיסטיקה מהירה
lf.select(pl.col('value').describe())
```

---

<a id="commands"></a>
## 🎯 פקודות נפוצות - Cheat Sheet

### ייבוא בסיסי

```python
import polars as pl
from datetime import datetime
```

### זרימת עבודה טיפוסית

```python
# 1. טעינה
lf = pl.scan_csv('data.csv', try_parse_dates=True)

# 2. המרת תאריכים (אם נדרש)
lf = lf.with_columns(pl.col('datetime').str.to_datetime())

# 3. סימון ממוין (חשוב!)
lf = lf.set_sorted('datetime')

# 4. עיבוד
result = lf.filter(...).select(...).collect()
```

### דפוסים נפוצים

#### ממוצע נע יומי

```python
lf.select(
    pl.col('datetime').dt.date().alias('date'),
    'value'
).group_by('date', maintain_order=True).agg(
    pl.col('value').mean()
).with_columns(
    pl.col('value').rolling_mean(7).alias('7day_avg')
)
```

#### השוואת שנים

```python
lf.select(
    pl.col('datetime').dt.year().alias('year'),
    pl.col('datetime').dt.month().alias('month'),
    'value'
).group_by(['year', 'month']).agg(
    pl.col('value').mean()
).pivot(
    index='month',
    columns='year',
    values='value'
)
```

#### זיהוי חריגות (outliers)

```python
lf.with_columns(
    pl.col('value').rolling_mean(7).alias('avg'),
    pl.col('value').rolling_std(7).alias('std')
).with_columns(
    ((pl.col('value') - pl.col('avg')).abs() > 
     2 * pl.col('std')).alias('is_outlier')
)
```

---

## 📊 טבלת השוואה - Pandas vs Polars

| פעולה | Pandas | Polars |
|-------|--------|--------|
| ממוצע נע | `df['col'].rolling(7).mean()` | `pl.col('col').rolling_mean(7)` |
| Resample | `df.resample('1W').mean()` | `df.group_by_dynamic('date', every='1w').agg(...)` |
| Upsample | `df.resample('1H').asfreq()` | `df.upsample('date', every='1h')` |
| Interpolate | `df.interpolate()` | `pl.col('col').interpolate()` |
| Date parts | `df['date'].dt.year` | `pl.col('date').dt.year()` |

---

## 🔥 דפוסים מתקדמים

### Bollinger Bands

```python
lf.with_columns(
    pl.col('price').rolling_mean(20).alias('sma'),
    pl.col('price').rolling_std(20).alias('std')
).with_columns(
    (pl.col('sma') + 2 * pl.col('std')).alias('upper_band'),
    (pl.col('sma') - 2 * pl.col('std')).alias('lower_band')
)
```

### Exponential Moving Average (EMA)

```python
# דורש חישוב ידני או שימוש ב-ewm
pl.col('value').ewm_mean(span=12)
```

### מדד עונתיות

```python
lf.select(
    pl.col('datetime').dt.month().alias('month'),
    'value'
).group_by('month').agg(
    pl.col('value').mean().alias('monthly_avg')
)
```

---

## ⚠️ טעויות נפוצות

```python
# ❌ שכחת set_sorted
lf.rolling('date', period='7d')  # יכול להיכשל

# ✅ נכון
lf.set_sorted('date').rolling('date', period='7d')

# ❌ upsample על LazyFrame
lf.upsample('date', every='1h')  # שגיאה!

# ✅ נכון
lf.collect().upsample('date', every='1h')

# ❌ rolling על תאריך כ-String
pl.col('date').rolling_mean(7)  # לא יעבוד

# ✅ נכון
pl.col('date').str.to_datetime().rolling_mean(7)
```

---

## 🔮 חיזוי סדרות זמן (Forecasting)

### התקנה

```bash
pip install functime
```

### זרימת עבודה בסיסית

```python
from functime.cross_validation import train_test_split
from functime.forecasting import linear_model
from functime.metrics import mase

# 1. הכנת נתונים - צבירה חודשית
y = lf.group_by_dynamic(
    'datetime',
    every='1mo',
    group_by='city'
).agg(
    pl.col('temperature').mean()
)

# 2. פיצול train/test (כרונולוגי!)
test_size = 3
y_train, y_test = y.pipe(train_test_split(test_size))

# 3. אימון מודל
forecaster = linear_model(lags=24, freq='1mo')
forecaster.fit(y=y_train)

# 4. חיזוי
y_pred = forecaster.predict(fh=test_size)

# 5. הערכת דיוק
scores = mase(y_true=y_test, y_pred=y_pred, y_train=y_train)
```

### מודלים זמינים

```python
from functime.forecasting import (
    linear_model,    # רגרסיה לינארית
    knn,            # K-Nearest Neighbors
    lightgbm,       # LightGBM (מומלץ!)
    xgboost,        # XGBoost
    catboost,       # CatBoost
    auto_lightgbm,  # AutoML
)
```

### Feature Engineering

```python
from functime.seasonality import add_calendar_effects

# הוספת תכונות זמן
y_features = y.pipe(
    add_calendar_effects(['month', 'quarter', 'year'])
)

# תכונות סדרה זמנית
y_features = y.with_columns(
    pl.col('value').ts.binned_entropy(bin_count=10),
    pl.col('value').ts.lempel_ziv_complexity(),
    pl.col('value').ts.longest_streak_above_mean()
)
```

### מדדי הערכה

| מדד | תיאור | מתי להשתמש |
|-----|-------|-----------|
| `mase` | Mean Absolute Scaled Error | כללי, מומלץ |
| `smape` | Symmetric MAPE | לנתונים עם 0 |
| `mae` | Mean Absolute Error | פשוט |
| `rmse` | Root Mean Squared Error | קלאסי |

```python
from functime.metrics import mase, smape, mae, rmse

# חישוב מדדים
mase_score = mase(y_true, y_pred, y_train)
smape_score = smape(y_true, y_pred)
```

### טיפים לחיזוי

**✅ עשה:**
- פצל כרונולוגית (לא אקראי!)
- השתמש ב-cross-validation לסדרות זמן
- בדוק stationarity
- נרמל את הנתונים
- טפל ב-outliers

**❌ אל תעשה:**
- לא לפצל אקראית
- לא להשתמש בנתוני test באימון
- לא להתעלם מעונתיות
- לא לשכוח validation set

---

## 📚 משאבים מהירים

- **תיעוד רשמי:** https://pola-rs.github.io/polars/
- **API Reference:** https://pola-rs.github.io/polars/py-polars/html/reference/
- **Discord קהילה:** https://discord.gg/4UfP5cfBE7

---

## 🎓 זכור!

1. ✅ **תמיד** `set_sorted()` לפני פעולות זמן
2. ✅ **בדוק** עם `head()` לפני `collect()`
3. ✅ **השתמש** ב-LazyFrame כשאפשר
4. ✅ **העדף** פונקציות מובנות על `rolling_map`
5. ✅ **תעד** את הקוד שלך

---

**🚀 בהצלחה בניתוח סדרות הזמן שלכם!**
