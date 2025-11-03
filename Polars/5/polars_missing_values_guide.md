# 📚 מדריך מקיף: טיפול בערכים חסרים (Missing Values) ב-Polars

<div dir="rtl">

## 📑 תוכן עניינים

1. [מבוא](#מבוא)
2. [זיהוי ערכים חסרים](#זיהוי-ערכים-חסרים)
   - [null_count() - ספירת ערכים חסרים](#null_count---ספירת-ערכים-חסרים)
   - [is_null() - זיהוי שורות עם ערכים חסרים](#is_null---זיהוי-שורות-עם-ערכים-חסרים)
   - [is_nan() - זיהוי ערכי NaN](#is_nan---זיהוי-ערכי-nan)
3. [מחיקת ערכים חסרים](#מחיקת-ערכים-חסרים)
   - [drop_nulls() - מחיקת שורות](#drop_nulls---מחיקת-שורות)
   - [drop() - מחיקת עמודות](#drop---מחיקת-עמודות)
4. [מילוי ערכים חסרים](#מילוי-ערכים-חסרים)
   - [fill_null() - מילוי בערכים קבועים](#fill_null---מילוי-בערכים-קבועים)
   - [אסטרטגיות מילוי סטטיסטיות](#אסטרטגיות-מילוי-סטטיסטיות)
   - [interpolate() - אינטרפולציה](#interpolate---אינטרפולציה)
   - [forward_fill() ו-backward_fill()](#forward_fill-ו-backward_fill)
5. [טיפים וטריקים](#טיפים-וטריקים)
6. [תרגילים מומלצים](#תרגילים-מומלצים)
7. [משאבים נוספים](#משאבים-נוספים)

---

## 🎯 מבוא

### מה זה Polars?

**Polars** היא ספריית Python מודרנית ומהירה במיוחד לעיבוד נתונים. היא מהווה אלטרנטיבה מצוינת ל-Pandas, עם ביצועים משופרים משמעותית ותחביר ברור יותר.

### למה ערכים חסרים חשובים?

בעולם האמיתי, נתונים לעולם אינם מושלמים. ערכים חסרים (Missing Values) הם בעיה נפוצה שנובעת מ:
- **שגיאות באיסוף נתונים** - חיישנים שנכשלו, טפסים שלא מולאו
- **מידע שלא קיים** - למשל, תאריך פטירה עבור אדם חי
- **שגיאות בעיבוד** - בעיות בהמרת פורמטים

### ההבדל בין `null` ל-`NaN` ב-Polars

🔍 **null (None)**: ערך חסר "אמיתי" - מייצג היעדר מידע
- מוגדר כ-`None` ב-Python
- נוצר כאשר יש פער במידע

🔢 **NaN (Not a Number)**: תוצאה של פעולה מתמטית לא חוקית
- מוגדר כ-`np.nan` (מספריית NumPy)
- נוצר מפעולות כמו `0/0` או `inf - inf`

---

## 🔍 זיהוי ערכים חסרים

### הכנת הנתונים לדוגמה

ראשית, נייבא את Polars וניצור DataFrame לדוגמה עם ערכים חסרים:

```python
import polars as pl
from datetime import date
import numpy as np

# יצירת טווח תאריכים
date_col = pl.date_range(date(2023, 1, 1), date(2023, 1, 15), '1d', eager=True)

# רשימת טמפרטורות עם ערכים חסרים
avg_temp_c_list = [-3, None, 6, -1, np.nan, 6, 4, None, 1, 2, np.nan, 7, 9, -2, None]

# יצירת DataFrame
df = pl.DataFrame({
    'date': date_col,
    'avg_temp_celsius': avg_temp_c_list
}, strict=False)

print(df.head())
```

**פלט צפוי:**
```
shape: (5, 2)
┌────────────┬──────────────────┐
│ date       ┆ avg_temp_celsius │
│ ---        ┆ ---              │
│ date       ┆ f64              │
╞════════════╪══════════════════╡
│ 2023-01-01 ┆ -3.0             │
│ 2023-01-02 ┆ null             │
│ 2023-01-03 ┆ 6.0              │
│ 2023-01-04 ┆ -1.0             │
│ 2023-01-05 ┆ NaN              │
└────────────┴──────────────────┘
```

**💡 הסבר:**
- `strict=False` מאפשר ערבוב של `None` ו-`np.nan` באותה עמודה
- `eager=True` ב-`date_range` מבצע את הפעולה מיידית (לא lazy)

---

### `null_count()` - ספירת ערכים חסרים

הפונקציה `null_count()` מחזירה את מספר הערכים החסרים (`null` בלבד, לא `NaN`) בכל עמודה.

#### דוגמה 1: ספירה על כל ה-DataFrame

```python
df.null_count()
```

**פלט:**
```
shape: (1, 2)
┌──────┬──────────────────┐
│ date ┆ avg_temp_celsius │
│ ---  ┆ ---              │
│ u32  ┆ u32              │
╞══════╪══════════════════╡
│ 0    ┆ 3                │
└──────┴──────────────────┘
```

**הסבר:** יש 3 ערכי `null` בעמודת הטמפרטורה, ו-0 בעמודת התאריכים.

#### דוגמה 2: ספירה על עמודה אחת

```python
df.select('avg_temp_celsius').null_count()
```

**פלט:**
```
shape: (1, 1)
┌──────────────────┐
│ avg_temp_celsius │
│ ---              │
│ u32              │
╞══════════════════╡
│ 3                │
└──────────────────┘
```

#### דוגמה 3: שימוש ב-`pl.col()`

```python
df.select(pl.col('avg_temp_celsius').null_count())
```

זוהי הדרך המומלצת כאשר רוצים לעשות פעולות נוספות על התוצאה.

---

### `is_null()` - זיהוי שורות עם ערכים חסרים

הפונקציה `is_null()` מחזירה DataFrame בוליאני (True/False) המציין איפה יש ערכים חסרים.

#### דוגמה 4: ספירה עם is_null()

```python
df.select(
    pl.col('avg_temp_celsius')
    .is_null()
    .sum()
)
```

**פלט:**
```
shape: (1, 1)
┌──────────────────┐
│ avg_temp_celsius │
│ ---              │
│ u32              │
╞══════════════════╡
│ 3                │
└──────────────────┘
```

**💡 טיפ:** `is_null()` משולב עם `sum()` נותן את אותה תוצאה כמו `null_count()`.

#### דוגמה 5: סינון שורות עם ערכים חסרים

```python
df.filter(pl.col('avg_temp_celsius').is_null()).select(pl.len())
```

זה יחזיר את **מספר השורות** שבהן הטמפרטורה היא `null`.

#### דוגמה 6: גישה ל-shape

```python
df.filter(pl.col('avg_temp_celsius').is_null()).shape[0]
```

גישה ישירה למספר השורות בעזרת `shape[0]`.

---

### `is_nan()` - זיהוי ערכי NaN

לזיהוי ערכי `NaN` (שונה מ-`null`):

```python
df.select(
    pl.col('avg_temp_celsius')
    .is_nan()
    .sum()
)
```

**פלט:**
```
shape: (1, 1)
┌──────────────────┐
│ avg_temp_celsius │
│ ---              │
│ u32              │
╞══════════════════╡
│ 2                │
└──────────────────┘
```

**📝 הבדל חשוב:**
- `is_null()` מזהה רק `None` / `null`
- `is_nan()` מזהה רק `np.nan`
- יש 3 `null` ו-2 `NaN` בנתונים שלנו!

#### סינון שורות עם NaN

```python
df.filter(pl.col('avg_temp_celsius').is_nan()).select(pl.len())
```

---

## 🗑️ מחיקת ערכים חסרים

### הכנת הנתונים

נטען קובץ CSV לדוגמה (או נשתמש בנתונים הקודמים):

```python
import polars as pl

# אם יש לכם קובץ:
# df = pl.read_csv('../data/temperatures.csv')

# אחרת, נשתמש בנתונים שיצרנו:
from datetime import date
import numpy as np

date_col = pl.date_range(date(2023, 1, 1), date(2023, 1, 15), '1d', eager=True)
avg_temp_c_list = [-3, None, 6, -1, np.nan, 6, 4, None, 1, 2, np.nan, 7, 9, -2, None]

df = pl.DataFrame({
    'date': date_col,
    'avg_temp_celsius': avg_temp_c_list
}, strict=False)

print(df.head())
```

---

### `drop_nulls()` - מחיקת שורות

הפונקציה `drop_nulls()` מוחקת שורות שבהן יש ערכים חסרים (`null` בלבד).

#### דוגמה 1: מחיקת כל השורות עם null

```python
df.drop_nulls().null_count()
```

**פלט:**
```
shape: (1, 2)
┌──────┬──────────────────┐
│ date ┆ avg_temp_celsius │
│ ---  ┆ ---              │
│ u32  ┆ u32              │
╞══════╪══════════════════╡
│ 0    ┆ 0                │
└──────┴──────────────────┘
```

**⚠️ שימו לב:** `drop_nulls()` לא מוחק שורות עם `NaN`! רק `null`.

#### דוגמה 2: מחיקה לפי עמודה ספציפית

```python
df.drop_nulls(subset=['avg_temp_celsius'])
```

זה ימחק רק שורות שבהן **עמודת הטמפרטורה** מכילה `null`.

**💡 מתי להשתמש:**
- כאשר אין לנו דרך למלא את הערכים החסרים
- כאשר יש לנו מספיק נתונים והשורות החסרות לא קריטיות

---

### הסרת NaN (בנוסף ל-null)

אם רוצים להסיר גם `NaN`, צריך לעשות זאת בשני שלבים:

```python
# שלב 1: להמיר NaN ל-null
df_cleaned = df.with_columns(
    pl.col('avg_temp_celsius').fill_nan(None)
)

# שלב 2: להסיר null
df_cleaned = df_cleaned.drop_nulls()

print(f"מספר שורות לפני: {len(df)}")
print(f"מספר שורות אחרי: {len(df_cleaned)}")
```

**פלט צפוי:**
```
מספר שורות לפני: 15
מספר שורות אחרי: 10
```

---

### מחיקת עמודות עם ערכים חסרים רבים

לפעמים עמודה שלמה מכילה יותר מדי ערכים חסרים ולא שווה לשמור אותה.

```python
# בדיקה: אחוז הערכים החסרים בכל עמודה
null_percentage = (df.null_count() / len(df) * 100)
print(null_percentage)
```

**דוגמה: מחיקת עמודות עם יותר מ-50% ערכים חסרים**

```python
threshold = 0.5  # 50%

for col in df.columns:
    null_ratio = df.select(pl.col(col).null_count()).item() / len(df)
    if null_ratio > threshold:
        df = df.drop(col)
        print(f"נמחקה עמודה: {col} (יחס null: {null_ratio:.2%})")
```

---

## 📝 מילוי ערכים חסרים

לפעמים מחיקת נתונים היא פתרון יקר מדי. במקום זאת, נוכל למלא ערכים חסרים בדרכים חכמות.

### `fill_null()` - מילוי בערכים קבועים

#### דוגמה 1: מילוי בערך קבוע

```python
df.with_columns(
    pl.col('avg_temp_celsius').fill_null(0).alias('filled_with_zero')
)
```

**פלט:**
```
shape: (15, 3)
┌────────────┬──────────────────┬──────────────────┐
│ date       ┆ avg_temp_celsius ┆ filled_with_zero │
│ ---        ┆ ---              ┆ ---              │
│ date       ┆ f64              ┆ f64              │
╞════════════╪══════════════════╪══════════════════╡
│ 2023-01-01 ┆ -3.0             ┆ -3.0             │
│ 2023-01-02 ┆ null             ┆ 0.0              │
│ 2023-01-03 ┆ 6.0              ┆ 6.0              │
...
```

**💡 מתי להשתמש:**
- כאשר אפס הוא ערך הגיוני (למשל, כמות גשמים)
- כאשר רוצים לסמן "לא ידוע" בערך ברירת מחדל

---

### אסטרטגיות מילוי סטטיסטיות

ניתן למלא ערכים חסרים בעזרת מדדים סטטיסטיים מהנתונים הקיימים.

#### דוגמה 2: מילוי בממוצע (mean)

```python
df.with_columns(
    pl.col('avg_temp_celsius').fill_null(strategy='mean').alias('mean_filled')
)
```

**אסטרטגיות זמינות:**
- `'mean'` - ממוצע חשבוני
- `'min'` - ערך מינימלי
- `'max'` - ערך מקסימלי
- `'zero'` - מילוי באפס
- `'one'` - מילוי ב-1

#### דוגמה 3: השוואת אסטרטגיות

```python
df.select(
    pl.col('avg_temp_celsius'),
    mean_filled=pl.col('avg_temp_celsius').fill_null(strategy='mean'),
    min_filled=pl.col('avg_temp_celsius').fill_null(strategy='min'),
    max_filled=pl.col('avg_temp_celsius').fill_null(strategy='max'),
)
```

**פלט:**
```
shape: (15, 4)
┌──────────────────┬─────────────┬────────────┬────────────┐
│ avg_temp_celsius ┆ mean_filled ┆ min_filled ┆ max_filled │
│ ---              ┆ ---         ┆ ---        ┆ ---        │
│ f64              ┆ f64         ┆ f64        ┆ f64        │
╞══════════════════╪═════════════╪════════════╪════════════╡
│ -3.0             ┆ -3.0        ┆ -3.0       ┆ -3.0       │
│ null             ┆ 3.333...    ┆ -3.0       ┆ 9.0        │
│ 6.0              ┆ 6.0         ┆ 6.0        ┆ 6.0        │
...
```

**⚠️ שימו לב:**
- אסטרטגיות אלו לא עובדות עם `NaN`!
- צריך להמיר `NaN` ל-`null` לפני (`fill_nan(None)`)

---

### `interpolate()` - אינטרפולציה

אינטרפולציה ממלאת ערכים חסרים על בסיס הערכים הסמוכים, תוך יצירת מעבר חלק.

#### דוגמה 4: אינטרפולציה לינארית

```python
df.select(
    'avg_temp_celsius',
    interpolated_linear=pl.col('avg_temp_celsius').interpolate(),
    interpolated_nearest=pl.col('avg_temp_celsius').interpolate(method='nearest')
)
```

**פלט:**
```
shape: (15, 3)
┌──────────────────┬─────────────────────┬──────────────────────┐
│ avg_temp_celsius ┆ interpolated_linear ┆ interpolated_nearest │
│ ---              ┆ ---                 ┆ ---                  │
│ f64              ┆ f64                 ┆ f64                  │
╞══════════════════╪═════════════════════╪══════════════════════╡
│ -3.0             ┆ -3.0                ┆ -3.0                 │
│ null             ┆ 1.5                 ┆ 6.0                  │
│ 6.0              ┆ 6.0                 ┆ 6.0                  │
│ -1.0             ┆ -1.0                ┆ -1.0                 │
│ NaN              ┆ NaN                 ┆ NaN                  │
...
```

**הסבר:**
- **אינטרפולציה לינארית** (`method='linear'`, ברירת מחדל): מחשבת ערך ממוצע משוקלל בין הערכים הקודמים והבאים
  - בשורה 2: בין -3 ל-6 → `(−3 + 6) / 2 = 1.5`
- **אינטרפולציה nearest**: בוחרת בערך הקרוב ביותר
  - בשורה 2: 6.0 קרוב יותר מ--3.0

**💡 מתי להשתמש באינטרפולציה:**
- נתוני סדרות זמן (טמפרטורות, מחירי מניות)
- כאשר יש המשכיות טבעית בנתונים
- כאשר רוצים מעבר חלק בין נקודות

---

### מילוי מותאם אישית

ניתן למלא ערכים חסרים בעזרת חישובים מורכבים יותר.

#### דוגמה 5: מילוי בחציון (median)

```python
df.select(
    'avg_temp_celsius',
    avg_temp_median=pl.col('avg_temp_celsius').fill_null(
        pl.col('avg_temp_celsius').median()
    )
)
```

#### דוגמה 6: מילוי בפונקציה מותאמת אישית

```python
df.select(
    'avg_temp_celsius',
    avg_temp_max_minus_min=pl.col('avg_temp_celsius').fill_null(
        pl.col('avg_temp_celsius').max() - pl.col('avg_temp_celsius').min()
    )
)
```

**פלט:**
```
shape: (15, 2)
┌──────────────────┬────────────────────────┐
│ avg_temp_celsius ┆ avg_temp_max_minus_min │
│ ---              ┆ ---                    │
│ f64              ┆ f64                    │
╞══════════════════╪════════════════════════╡
│ -3.0             ┆ -3.0                   │
│ null             ┆ 12.0                   │  ← 9 - (-3) = 12
│ 6.0              ┆ 6.0                    │
...
```

**💡 דוגמאות נוספות למילוי:**
```python
# מילוי בממוצע של 3 הערכים הקרובים
df.select(
    pl.col('avg_temp_celsius').fill_null(
        pl.col('avg_temp_celsius').rolling_mean(window_size=3)
    )
)

# מילוי לפי תנאי
df.with_columns(
    pl.when(pl.col('avg_temp_celsius').is_null())
      .then(pl.col('avg_temp_celsius').mean())
      .otherwise(pl.col('avg_temp_celsius'))
      .alias('conditional_fill')
)
```

---

## 🔄 `forward_fill()` ו-`backward_fill()`

שיטות אלו ממלאות ערכים חסרים על בסיס הערכים הקודמים או הבאים בסדרה.

### הכנת דוגמה חדשה

```python
df = pl.DataFrame({
    'values': [1, 2, None, None, None, 3, 4, None, 5]
})
print(df)
```

**פלט:**
```
shape: (9, 1)
┌────────┐
│ values │
│ ---    │
│ i64    │
╞════════╡
│ 1      │
│ 2      │
│ null   │
│ null   │
│ null   │
│ 3      │
│ 4      │
│ null   │
│ 5      │
└────────┘
```

---

### דוגמה מקיפה

```python
df.select(
    'values',
    forward_fill=pl.col('values').forward_fill(),
    forward_fill_1=pl.col('values').forward_fill(limit=1),
    backward_fill=pl.col('values').backward_fill(),
    backward_fill_2=pl.col('values').backward_fill(limit=2),
)
```

**פלט:**
```
shape: (9, 5)
┌────────┬──────────────┬────────────────┬───────────────┬─────────────────┐
│ values ┆ forward_fill ┆ forward_fill_1 ┆ backward_fill ┆ backward_fill_2 │
│ ---    ┆ ---          ┆ ---            ┆ ---           ┆ ---             │
│ i64    ┆ i64          ┆ i64            ┆ i64           ┆ i64             │
╞════════╪══════════════╪════════════════╪═══════════════╪═════════════════╡
│ 1      ┆ 1            ┆ 1              ┆ 1             ┆ 1               │
│ 2      ┆ 2            ┆ 2              ┆ 2             ┆ 2               │
│ null   ┆ 2            ┆ 2              ┆ 3             ┆ null            │
│ null   ┆ 2            ┆ null           ┆ 3             ┆ 3               │
│ null   ┆ 2            ┆ null           ┆ 3             ┆ 3               │
│ 3      ┆ 3            ┆ 3              ┆ 3             ┆ 3               │
│ 4      ┆ 4            ┆ 4              ┆ 4             ┆ 4               │
│ null   ┆ 4            ┆ 4              ┆ 5             ┆ 5               │
│ 5      ┆ 5            ┆ 5              ┆ 5             ┆ 5               │
└────────┴──────────────┴────────────────┴───────────────┴─────────────────┘
```

### הסבר מפורט:

#### `forward_fill()` - מילוי קדימה
```python
pl.col('values').forward_fill()
```
- ממלא ערכים חסרים בערך הקודם הקרוב ביותר
- **בלי limit**: ממלא את כל הערכים החסרים
- **עם limit=1**: ממלא רק ערך חסר **אחד** אחרי כל ערך לא-חסר

**דוגמה:**
- שורות 3-5 (null): נמלאות ב-2 (הערך הקודם)
- שורה 8 (null): נמלאת ב-4 (הערך הקודם)

#### `backward_fill()` - מילוי אחורה
```python
pl.col('values').backward_fill()
```
- ממלא ערכים חסרים בערך הבא הקרוב ביותר
- **בלי limit**: ממלא את כל הערכים החסרים
- **עם limit=2**: ממלא רק **2 ערכים חסרים** לפני כל ערך לא-חסר

**דוגמה:**
- שורות 3-5 (null): נמלאות ב-3 (הערך הבא)
- שורה 8 (null): נמלאת ב-5 (הערך הבא)

**⚠️ שימו לב:** שורה 3 ב-`backward_fill_2` נשארת null כי היא השלישית מ-3, והגבלנו ל-2 בלבד.

---

### 💡 מתי להשתמש?

| שיטה | מתאים ל... | דוגמאות |
|------|------------|---------|
| **forward_fill** | נתונים שנשארים קבועים עד לשינוי | מלאי מוצר, סטטוס משתמש, מחיר אחרון ידוע |
| **backward_fill** | נתונים שנחזו מראש | תחזיות מזג אויר, לוח זמנים מתוכנן |
| **אינטרפולציה** | נתונים מתמטיים רציפים | טמפרטורות, מדידות מדעיות |
| **ממוצע/חציון** | נתונים סטטיסטיים | סקרים, מדגמים אקראיים |

---

## 💡 טיפים וטריקים

### 1. טיפול ב-NaN לפני עיבוד

תמיד המירו `NaN` ל-`null` לפני שימוש בפונקציות טיפול ב-nulls:

```python
df = df.with_columns(
    pl.col('avg_temp_celsius').fill_nan(None)
)
```

### 2. שימוש ב-`with_columns()` במקום `select()`

כאשר רוצים לשמור את כל העמודות ולהוסיף חדשות:

```python
# ✅ טוב - שומר את כל העמודות
df = df.with_columns(
    pl.col('avg_temp_celsius').fill_null(0).alias('temp_filled')
)

# ❌ פחות טוב - מחזיר רק את העמודות הנבחרות
df = df.select(
    'date',
    pl.col('avg_temp_celsius').fill_null(0).alias('temp_filled')
)
```

### 3. בדיקה לפני מחיקה

תמיד בדקו כמה נתונים תאבדו לפני מחיקה:

```python
print(f"שורות לפני מחיקה: {len(df)}")
print(f"שורות עם null: {df.null_count()}")
print(f"שורות אחרי מחיקה: {len(df.drop_nulls())}")
```

### 4. שרשור פעולות (Method Chaining)

Polars תומך בכתיבה קריאה ונקייה:

```python
result = (
    df
    .with_columns(pl.col('avg_temp_celsius').fill_nan(None))
    .drop_nulls()
    .with_columns(
        pl.col('avg_temp_celsius').fill_null(strategy='mean').alias('temp_filled')
    )
)
```

### 5. שימוש ב-`describe()` לזיהוי בעיות

```python
df.describe()
```

זה יראה לכם סטטיסטיקות בסיסיות ויעזור לזהות עמודות עם הרבה ערכים חסרים.

---

## 🏋️ תרגילים מומלצים

### תרגיל 1: זיהוי ומחיקה בסיסית

```python
# צרו DataFrame עם ערכים חסרים
df = pl.DataFrame({
    'name': ['Alice', 'Bob', None, 'David'],
    'age': [25, None, 30, 35],
    'city': ['Tel Aviv', 'Haifa', 'Jerusalem', None]
})

# 1. מצאו את מספר הערכים החסרים בכל עמודה
# 2. מחקו את השורות שבהן יש ערכים חסרים
# 3. כמה שורות נשארו?
```

<details>
<summary>פתרון</summary>

```python
# 1. ספירת nulls
print(df.null_count())

# 2. מחיקת שורות
df_clean = df.drop_nulls()

# 3. מספר שורות
print(f"שורות שנשארו: {len(df_clean)}")  # תשובה: 1
```
</details>

---

### תרגיל 2: מילוי חכם

```python
# נתוני מכירות חודשיות
df = pl.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'sales': [1000, None, 1200, None, 1300]
})

# 1. מלאו את הערכים החסרים באינטרפולציה
# 2. השוו לתוצאה של מילוי בממוצע
# 3. איזו שיטה נראית יותר הגיונית? למה?
```

<details>
<summary>פתרון</summary>

```python
# 1. אינטרפולציה
interpolated = df.with_columns(
    pl.col('sales').interpolate().alias('sales_interpolated')
)

# 2. ממוצע
mean_filled = df.with_columns(
    pl.col('sales').fill_null(strategy='mean').alias('sales_mean')
)

print(interpolated)
print(mean_filled)

# 3. אינטרפולציה נראית יותר הגיונית כי:
#    - מכירות בדרך כלל עולות באופן הדרגתי
#    - אינטרפולציה שומרת על המגמה
```
</details>

---

### תרגיל 3: forward_fill מתקדם

```python
# מחירי מניה (null = לא היה מסחר)
df = pl.DataFrame({
    'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'price': [100, None, None, 105, None]
})

# 1. השתמשו ב-forward_fill עם limit=2
# 2. הסבירו מדוע זה הגיוני למניות
# 3. מה היה קורה עם backward_fill?
```

<details>
<summary>פתרון</summary>

```python
# 1. forward_fill
result = df.with_columns(
    pl.col('price').forward_fill(limit=2).alias('price_filled')
)
print(result)

# 2. הסבר: במניות, המחיר האחרון ידוע נשאר תקף
#    עד לעסקה חדשה. limit=2 מונע הנחה שהמחיר נשאר
#    קבוע לאינסוף.

# 3. backward_fill היה פחות הגיוני כי:
#    - לא יודעים מחירים עתידיים מראש
#    - זה יוצר "מבט לעתיד" שאינו ריאלי
```
</details>

---

## 📚 משאבים נוספים

### תיעוד רשמי
- [Polars Documentation - Missing Data](https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.null_count.html)
- [Polars User Guide](https://pola-rs.github.io/polars-book/)

### מאמרים ומדריכים
- [Polars vs Pandas: Performance Comparison](https://www.pola.rs/posts/benchmarks/)
- [Best Practices for Handling Missing Data](https://towardsdatascience.com/handling-missing-data-in-polars)

### קורסים מומלצים
- [Data Cleaning with Polars - YouTube Series](https://www.youtube.com/)
- [Advanced Polars Techniques - DataCamp](https://www.datacamp.com/)

### ספרייה וקוד לדוגמה
- [Polars Cookbook - GitHub](https://github.com/pola-rs/polars/tree/master/examples)

---

## 🎓 סיכום

**במדריך זה למדנו:**

✅ איך לזהות ערכים חסרים (`null_count`, `is_null`, `is_nan`)  
✅ איך למחוק שורות ועמודות עם ערכים חסרים (`drop_nulls`, `drop`)  
✅ איך למלא ערכים חסרים בשיטות שונות:
  - ערכים קבועים (`fill_null`)
  - אסטרטגיות סטטיסטיות (`mean`, `min`, `max`)
  - אינטרפולציה (`interpolate`)
  - מילוי קדימה/אחורה (`forward_fill`, `backward_fill`)  
✅ מתי להשתמש בכל שיטה

**הבסיס לעבודה עם Polars:**
- 🚀 **מהירות** - Polars מהיר פי 5-10 מ-Pandas
- 📖 **קריאות** - תחביר ברור ואינטואיטיבי
- 🔧 **גמישות** - כלים רבים לטיפול בנתונים

**זכרו:**
- תמיד המירו `NaN` ל-`null` לפני עיבוד
- בחרו את שיטת המילוי לפי ההקשר העסקי
- בדקו את ההשפעה של מחיקת נתונים לפני שאתם מבצעים אותה

---

## 🙏 תודה!

אם יש שאלות, הערות או הצעות לשיפור, נשמח לשמוע!

**בהצלחה בעבודה עם Polars!** 🐻‍❄️

</div>
