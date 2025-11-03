# 🚀 מדריך מהיר: Testing & Debugging ב-Polars

## 📋 תוכן עניינים
- [ניפוי שגיאות](#debugging)
- [אופטימיזציה](#optimization)
- [בדיקות איכות](#quality)
- [פקודות מהירות](#commands)
- [טיפים לדיבאג](#tips)
- [שגיאות נפוצות](#errors)

---

## 🔍 ניפוי שגיאות {#debugging}

### שלוש שיטות לדיבאג שרשראות

#### 1️⃣ הערת קוד (Commenting)
```python
# הסרת שלבים עד שהקוד עובד
(
    lf
    .with_columns(...)
    # .select(...)  # ← העירו כאן
    .sort(...)
    .collect()
)
```

#### 2️⃣ Eager Mode
```python
# הוספת collect() מוקדם
(
    lf
    .collect()  # ← הופך ל-DataFrame
    .with_columns(...)
    .select(...)
)
```

#### 3️⃣ שימוש ב-pipe() ⭐ מומלץ!
```python
def step1(lf): ...
def step2(lf): ...

(
    lf
    .pipe(step1)  # ניתן לבדוק בנפרד
    .pipe(step2)
    .collect()
)
```

---

## ⚡ אופטימיזציה {#optimization}

### בדיקת Query Plan

| פקודה | מה זה עושה | שימוש |
|-------|------------|-------|
| `.show_graph()` | הצגה גרפית | `lf.show_graph()` |
| `.show_graph(optimized=False)` | ללא אופטימיזציה | לראות את הסדר המקורי |
| `.explain()` | הצגה טקסטואלית | `print(lf.explain())` |
| `.explain(streaming=True)` | עם streaming | לקבצים גדולים |

### טבלת אופטימיזציות

| אופטימיזציה | מה זה | דוגמה |
|-------------|-------|--------|
| **Predicate Pushdown** | העברת סינונים מוקדם | `filter` לפני `with_columns` |
| **Projection Pushdown** | קריאת רק עמודות נחוצות | `select` לפני פעולות כבדות |
| **Query Coalescing** | איחוד פעולות | מספר `filter` → `filter` אחד |

### כללי אצבע לביצועים

✅ **עשו:**
- סננו מוקדם (`filter` בהתחלה)
- בחרו עמודות מוקדם (`select` בהתחלה)
- השתמשו ב-Lazy mode
- השתמשו ב-`pipe()` לארגון

❌ **אל תעשו:**
- אל תעשו `collect()` מוקדם מדי
- אל תשאירו עמודות מיותרות
- אל תשתמשו ב-Eager mode בלי צורך

---

## ✅ בדיקות איכות (cuallee) {#quality}

### התקנה
```bash
pip install cuallee
```

### ייבוא
```python
from cuallee import Check, CheckLevel
df = lf.collect()  # cuallee עובד עם DataFrame
```

### טבלת בדיקות נפוצות

| בדיקה | קוד | משמעות |
|-------|-----|---------|
| **שלמות** | `.is_complete('col')` | אין ערכים null |
| **ייחודיות** | `.is_unique('col')` | כל הערכים שונים |
| **ערכים מקובלים** | `.is_contained_in('col', set)` | רק ערכים מהרשימה |
| **חיובי** | `.is_greater_than('col', 0)` | כל הערכים > 0 |
| **שלילי** | `.is_less_than('col', 0)` | כל הערכים < 0 |
| **טווח** | `.is_between('col', min, max)` | בטווח מסוים |

### דוגמאות מהירות

#### בדיקה בסיסית
```python
check = Check(CheckLevel.WARNING, 'My Check')
(
    check
    .is_complete('Name')
    .is_unique('Name')
    .validate(df)
)
```

#### בדיקת מספר עמודות
```python
check = Check(CheckLevel.WARNING, 'Multi Check')
cols = ['col1', 'col2', 'col3']
(
    check
    .are_complete(cols)  # ← are במקום is
    .are_unique(cols)
    .validate(df)
)
```

#### בדיקה עם assertion
```python
check = Check(CheckLevel.WARNING, 'Test')
result = (
    check
    .is_complete('col')
    .validate(df)
    .select('status')[0,0] == 'PASS'
)
assert result, "הבדיקה נכשלה!"
```

---

## 🎯 פקודות מהירות {#commands}

### Template למבנה מומלץ

```python
import polars as pl
from cuallee import Check, CheckLevel

# 1. טעינה
lf = pl.scan_csv('data.csv')

# 2. פונקציות מודולריות
def clean_data(lf):
    return lf.filter(...)

def transform(lf):
    return lf.with_columns(...)

# 3. Pipeline
result = (
    lf
    .pipe(clean_data)
    .pipe(transform)
    .collect()
)

# 4. בדיקות איכות
check = Check(CheckLevel.WARNING, 'QA')
check.is_complete('col').validate(result)
```

### Cheat Sheet - פעולות נפוצות

| צריך | קוד |
|------|-----|
| **לטעון CSV** | `pl.scan_csv('file.csv')` |
| **לסנן שורות** | `.filter(pl.col('x') > 5)` |
| **לבחור עמודות** | `.select('a', 'b', 'c')` |
| **להוסיף עמודה** | `.with_columns(pl.col('x') * 2)` |
| **למיין** | `.sort('col')` |
| **לקחת N ראשונים** | `.head(n)` |
| **לבצע שאילתה** | `.collect()` |
| **לשמור תוצאה** | `.write_csv('out.csv')` |

### Regex לבחירת עמודות

```python
# כל העמודות המסתיימות ב-"Rank"
pl.col('^.*Rank$')

# כל העמודות המתחילות ב-"Type"
pl.col('^Type.*')

# כל העמודות המכילות "Stat"
pl.col('.*Stat.*')
```

---

## 💡 טיפים לדיבאג {#tips}

### 1. הדפסת ביניים
```python
# הוספת print באמצע pipeline
def debug_print(lf):
    print(lf.head().collect())
    return lf

lf.pipe(step1).pipe(debug_print).pipe(step2)
```

### 2. בדיקת schema
```python
# לראות את סוגי העמודות
lf.schema
# או
lf.collect_schema()
```

### 3. בדיקת count
```python
# כמה שורות יש?
lf.select(pl.count()).collect()
```

### 4. בדיקת nulls
```python
# ספירת nulls בכל עמודה
lf.null_count().collect()
```

### 5. describe לסטטיסטיקות
```python
# סטטיסטיקות בסיסיות
df.describe()
```

---

## ⚠️ שגיאות נפוצות ופתרונות {#errors}

### טבלת שגיאות

| שגיאה | גורם | פתרון |
|-------|------|--------|
| `ColumnNotFoundError` | שם עמודה שגוי | בדקו את `lf.schema` |
| `ComputeError` | פעולה לא חוקית | בדקו סוגי נתונים |
| `SchemaError` | אי התאמת סכימה | בדקו את `lf.dtypes` |
| `ShapeError` | גודל לא מתאים | בדקו עם `lf.shape` |

### דוגמאות לשגיאות נפוצות

#### ❌ שגיאה: שם עמודה שגוי
```python
# שגיאה
.select('Deffense')  # שגיאת הקלדה

# תיקון
.select('Defense')
```

#### ❌ שגיאה: שכחת collect()
```python
# שגיאה
lf.head()  # מחזיר LazyFrame

# תיקון
lf.head().collect()  # מחזיר DataFrame
```

#### ❌ שגיאה: סוג נתונים לא נכון
```python
# שגיאה
.filter(pl.col('age') > '18')  # משווים מספר למחרוזת

# תיקון
.filter(pl.col('age') > 18)
```

---

## 🔧 דיבאג מתקדם

### בדיקת execution plan
```python
# לפני אופטימיזציה
print(lf.explain(optimized=False))

# אחרי אופטימיזציה
print(lf.explain(optimized=True))

# השוואה
```

### מדידת זמן ביצוע
```python
import time

start = time.time()
result = lf.collect()
end = time.time()

print(f"זמן ביצוע: {end - start:.2f} שניות")
```

### profiling
```python
# הפעלת profiling
result = lf.collect(profile=True)

# הצגת תוצאות
print(result[1])  # פרופיל
```

---

## 📊 Streaming Mode

### מתי להשתמש?
- ✅ קבצים גדולים מהזיכרון
- ✅ פעולות פשוטות (filter, select)
- ❌ Join מורכב
- ❌ Window functions מסוימות

### שימוש
```python
# טעינה עם streaming
result = (
    lf
    .filter(...)
    .select(...)
    .collect(streaming=True)
)
```

---

## 🎨 עיצוב קוד מומלץ

### ✅ קוד טוב
```python
def filter_valid(lf: pl.LazyFrame) -> pl.LazyFrame:
    """מסנן שורות תקינות"""
    return lf.filter(pl.col('value') > 0)

def add_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    """מוסיף עמודות חדשות"""
    return lf.with_columns(
        ratio=pl.col('a') / pl.col('b')
    )

# שימוש
result = (
    lf
    .pipe(filter_valid)
    .pipe(add_features)
    .collect()
)
```

### ❌ קוד פחות טוב
```python
# שרשרת ארוכה בלי מבנה
result = (
    lf
    .filter(pl.col('value') > 0)
    .with_columns(pl.col('a') / pl.col('b'))
    .filter(pl.col('x').is_not_null())
    .with_columns(pl.col('y') * 2)
    # ... עוד 20 שורות ...
    .collect()
)
```

---

## 📝 Checklist לפני Production

- [ ] כל הפונקציות מתועדות
- [ ] יש בדיקות cuallee
- [ ] הקוד משתמש ב-pipe()
- [ ] בדקתי את ה-query plan
- [ ] אין collect() מיותר
- [ ] יש טיפול בשגיאות (try/except)
- [ ] הקוד נבדק עם נתונים אמיתיים
- [ ] יש tests אוטומטיים (pytest)

---

## 🔗 קישורים מהירים

- [Polars Docs](https://pola-rs.github.io/polars/)
- [cuallee Docs](https://canimus.github.io/cuallee/)
- [Polars GitHub](https://github.com/pola-rs/polars)
- [Polars Discord](https://discord.gg/4UfP5cfBE7)

---

## 🎯 זכרו!

| עיקרון | מדוע |
|--------|------|
| 🔍 **pipe() תמיד** | קוד מודולרי וברור |
| ⚡ **סננו מוקדם** | ביצועים טובים יותר |
| ✅ **בדקו איכות** | מניעת באגים |
| 📊 **הסתכלו ב-plan** | הבנת האופטימיזציות |
| 🌊 **streaming לגדולים** | חיסכון בזיכרון |

---

**בהצלחה! 🚀**

*מדריך זה נוצר עבור Polars - ספריית DataFrame מהירה וחזקה לעיבוד נתונים*
