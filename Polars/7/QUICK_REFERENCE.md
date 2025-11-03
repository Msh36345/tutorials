# 📋 מדריך מהיר: מבני נתונים מקוננים ב-Polars

> **Cheat Sheet** מהיר לעבודה עם Lists, Structs ו-JSON ב-Polars

---

## 📦 התקנה וייבוא

```python
# התקנה
pip install polars

# ייבוא
import polars as pl
```

---

## 📝 1. יצירת רשימות (Creating Lists)

### 🔹 פיצול מחרוזות

```python
# פיצול לפי תו מפריד
df.select(
    pl.col('tags').str.split('|').alias('tags_list')
)
```

**דוגמה:**
```
"a|b|c" → ["a", "b", "c"]
```

### 🔹 צבירת ערכים

```python
# איסוף כל הערכים לרשימה
df.group_by('category').agg('values')
```

**דוגמה:**
```
date       | video_id
-----------|---------
2024-01-01 | [v1, v2, v3]
2024-01-02 | [v4, v5]
```

### 🔹 איחוד עמודות

```python
# איחוד מספר עמודות לרשימה אחת
pl.concat_list('col1', 'col2', 'col3')
```

**דוגמה:**
```
views | likes | dislikes → engagement
------|-------|----------|-------------
1000  | 50    | 5        | [1000, 50, 5]
```

---

## 🧮 2. צבירת אלמנטים (Aggregation)

### פעולות בסיסיות

| פעולה | תיאור | דוגמה |
|-------|--------|-------|
| `list.min()` | מינימום | `[3,1,4] → 1` |
| `list.max()` | מקסימום | `[3,1,4] → 4` |
| `list.mean()` | ממוצע | `[3,1,4] → 2.67` |
| `list.sum()` | סכום | `[3,1,4] → 8` |
| `list.len()` | אורך | `[3,1,4] → 3` |

### דוגמאות קוד

```python
# סטטיסטיקות על רשימה
df.select(
    pl.col('views').list.min().alias('min_views'),
    pl.col('views').list.max().alias('max_views'),
    pl.col('views').list.mean().alias('avg_views'),
    pl.col('views').list.sum().alias('total_views')
)
```

### איחוד למחרוזת

```python
# איחוד עם מפריד
pl.col('items').list.join(', ')
```

**דוגמה:**
```
["a", "b", "c"] → "a, b, c"
```

---

## 🎯 3. גישה ובחירת אלמנטים

### גישה בסיסית

| פעולה | תיאור | דוגמה |
|-------|--------|-------|
| `list.first()` | ראשון | `[1,2,3] → 1` |
| `list.last()` | אחרון | `[1,2,3] → 3` |
| `list.get(n)` | אלמנט n | `[1,2,3].get(1) → 2` |

### בחירת מספר אלמנטים

| פעולה | תיאור | דוגמה |
|-------|--------|-------|
| `list.head(n)` | n ראשונים | `[1,2,3,4].head(2) → [1,2]` |
| `list.tail(n)` | n אחרונים | `[1,2,3,4].tail(2) → [3,4]` |

### חיתוך (Slicing)

```python
# תחביר: list.slice(offset, length)

# 2 ראשונים
pl.col('items').list.slice(0, 2)

# מהאלמנט ה-3 עד ה-5
pl.col('items').list.slice(2, 3)

# מהאלמנט ה-5 עד הסוף
pl.col('items').list.slice(4)

# 2 אחרונים
pl.col('items').list.slice(-2)
```

### בחירה מותאמת (Gather)

```python
# בחירת אלמנטים במיקומים ספציפיים
pl.col('items').list.gather([0, 2, -1])
# מיקומים: ראשון, שלישי, אחרון

# עם טיפול ב-null
pl.col('items').list.gather([0, 100], null_on_oob=True)
```

---

## ⚙️ 4. החלת לוגיקה על אלמנטים

### תחביר `list.eval()`

```python
# החלת פעולה על כל אלמנט
pl.col('my_list').list.eval(
    פעולה_על_pl.element()
)
```

### הקשרים מיוחדים

- `pl.element()` - האלמנט הנוכחי
- `pl.first()` - האלמנט הראשון
- `pl.last()` - האלמנט האחרון
- `pl.col('')` - כל העמודה

### דוגמאות

```python
# המרה לאותיות גדולות
pl.col('names').list.eval(
    pl.element().str.to_uppercase()
)

# כפל ב-2
pl.col('numbers').list.eval(
    pl.element() * 2
)

# סינון
pl.col('items').list.eval(
    pl.element().filter(pl.element() > 10)
)

# דירוג
pl.col('scores').list.eval(
    pl.element().rank('dense', descending=True)
)

# הפרש מהמקסימום
pl.col('values').list.eval(
    pl.element().max() - pl.element()
)
```

### פעולות קבוצות

```python
list1 = pl.col('list1')
list2 = pl.col('list2')

# חיתוך (משותפים)
list1.list.set_intersection(list2)

# איחוד (כל הייחודיים)
list1.list.set_union(list2)

# הפרש (ב-A אבל לא ב-B)
list1.list.set_difference(list2)

# הפרש סימטרי (ב-A או ב-B אבל לא בשניהם)
list1.list.set_symmetric_difference(list2)
```

---

## 🏗️ 5. עבודה עם Structs

### יצירת Struct

```python
# מעמודות קיימות
pl.struct('col1', 'col2', 'col3')

# עם שם מותאם
pl.struct('col1', 'col2').alias('my_struct')
```

### פתיחת Struct (Unnesting)

```python
# פריסת struct לעמודות
df.unnest('struct_column')
```

### גישה לשדה

```python
# גישה לשדה ספציפי
pl.col('my_struct').struct.field('field_name')
```

### שינוי שמות שדות

```python
# שינוי שמות
pl.col('my_struct').struct.rename_fields(['new1', 'new2', 'new3'])
```

### המרת רשימה ל-Struct

```python
# כל אלמנט הופך לשדה
pl.col('my_list').list.to_struct()
```

---

## 🔄 6. עבודה עם JSON

### קריאה וכתיבה

```python
# קריאת JSON
df = pl.read_json('data.json')

# המרת struct ל-JSON string
pl.col('my_struct').struct.json_encode()

# המרת JSON string ל-struct
pl.col('json_str').str.json_decode()
```

### דוגמה מלאה

```python
# struct → JSON → struct
df.select(
    pl.col('data').struct.json_encode().alias('json_string'),
    pl.col('data').struct.json_encode().str.json_decode().alias('back_to_struct')
)
```

---

## 💥 7. פיצול רשימות (Explode)

```python
# הפיכת כל אלמנט ברשימה לשורה נפרדת
df.explode('list_column')

# פיצול מספר עמודות בו-זמנית
df.explode('list_col1', 'list_col2')
```

**דוגמה:**

```python
# לפני
date       | videos
-----------|----------------
2024-01-01 | ['v1', 'v2']

# אחרי explode
date       | videos
-----------|--------
2024-01-01 | 'v1'
2024-01-01 | 'v2'
```

---

## 🔍 8. פעולות נוספות

### מיון רשימה

```python
# מיון עולה
pl.col('items').list.sort()

# מיון יורד
pl.col('items').list.sort(descending=True)
```

### ערכים ייחודיים

```python
# הסרת כפילויות
pl.col('items').list.unique()
```

### בדיקות

```python
# האם הרשימה מכילה ערך
pl.col('items').list.contains(value)

# האם כל האלמנטים מקיימים תנאי
pl.col('items').list.eval(pl.element() > 0).list.all()

# האם לפחות אחד מקיים תנאי
pl.col('items').list.eval(pl.element() > 0).list.any()
```

---

## ⚠️ 9. מלכודות נפוצות ופתרונות

### ❌ שגיאת Out of Bounds

```python
# רע - יזרוק שגיאה אם הרשימה קצרה
pl.col('items').list.get(100)

# טוב - יחזיר null אם הרשימה קצרה
pl.col('items').list.get(100, null_on_oob=True)
```

### ❌ שימוש מיותר ב-eval

```python
# רע - מורכב מדי
pl.col('items').list.eval(pl.element().sum())

# טוב - פשוט יותר
pl.col('items').list.sum()
```

### ❌ ערבוב explode עם agg

```python
# רע - לא יעבוד כמצופה
df.explode('tags').group_by('date').agg('tags')

# טוב
df.group_by('date').agg('tags')
```

---

## 💡 10. טיפים לביצועים

### ✅ פעולה אחת על פני מספר

```python
# רע - שתי פעולות
df.with_columns(
    pl.col('tags').str.split('|')
).with_columns(
    pl.col('tags').list.len()
)

# טוב - פעולה אחת
df.with_columns(
    pl.col('tags').str.split('|').list.len().alias('num_tags')
)
```

### ✅ שימוש נכון ב-eval

```python
# השתמש ב-eval רק כשצריך להחיל לוגיקה מותאמת
# לא להחזרת הרשימה כמות שהיא
```

### ✅ קריאות קוד

```python
# טוב - שלבים ברורים
(
    df
    .group_by('category')
    .agg('values')
    .with_columns(
        pl.col('values').list.mean().alias('avg_value')
    )
)
```

---

## 📊 11. טבלת השוואה מהירה

| משימה | קוד | תוצאה |
|-------|-----|-------|
| פיצול | `str.split('│')` | `"a│b" → ["a","b"]` |
| איחוד | `concat_list('a','b')` | `1,2 → [1,2]` |
| ראשון | `list.first()` | `[1,2,3] → 1` |
| אחרון | `list.last()` | `[1,2,3] → 3` |
| n ראשונים | `list.head(n)` | `[1,2,3].head(2) → [1,2]` |
| ממוצע | `list.mean()` | `[1,2,3] → 2` |
| סכום | `list.sum()` | `[1,2,3] → 6` |
| אורך | `list.len()` | `[1,2,3] → 3` |
| מיון | `list.sort()` | `[3,1,2] → [1,2,3]` |
| ייחודיים | `list.unique()` | `[1,1,2] → [1,2]` |

---

## 🎯 12. דוגמאות מהירות לפי תרחיש

### תרחיש 1: ניתוח תגיות

```python
# פיצול, ספירה ומציאת הפופולריות
(
    df
    .select(pl.col('tags').str.split('|'))
    .explode('tags')
    .group_by('tags')
    .agg(pl.count().alias('count'))
    .sort('count', descending=True)
    .head(10)
)
```

### תרחיש 2: חישוב סטטיסטיקות יומיות

```python
# צבירה וחישוב מדדים
(
    df
    .group_by('date')
    .agg('views', 'likes')
    .with_columns(
        pl.col('views').list.mean().alias('avg_views'),
        pl.col('likes').list.max().alias('max_likes'),
        pl.col('views').list.len().alias('num_videos')
    )
)
```

### תרחיש 3: מציאת Top N

```python
# דירוג ובחירת הטובים ביותר
(
    df
    .group_by('category')
    .agg('views')
    .with_columns(
        pl.col('views')
        .list.eval(pl.element().rank('dense', descending=True))
        .alias('rank')
    )
    .explode('views', 'rank')
    .filter(pl.col('rank') <= 3)
)
```

### תרחיש 4: עבודה עם JSON

```python
# טעינה, פירוק והמרה
(
    pl.read_json('data.json')
    .unnest('nested_field')
    .with_columns(
        pl.col('struct_field').struct.field('value')
    )
)
```

---

## 📚 13. משאבים נוספים

### תיעוד רשמי
- **User Guide**: https://pola-rs.github.io/polars/user-guide/
- **API Reference**: https://pola-rs.github.io/polars/py-polars/html/reference/

### דוגמאות ומדריכים
- **GitHub Examples**: https://github.com/pola-rs/polars/tree/main/examples
- **Modern Polars**: https://github.com/pola-rs/polars-book

### קהילה
- **Discord**: https://discord.gg/4UfP5cfBE7
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/polars

---

## 🔧 14. פתרון בעיות נפוצות

### בעיה: "Index out of bounds"

```python
# פתרון: השתמש ב-null_on_oob
pl.col('items').list.get(10, null_on_oob=True)
```

### בעיה: "Type mismatch in list"

```python
# פתרון: המר לטיפוס אחיד
pl.col('mixed').cast(pl.List(pl.Utf8))
```

### בעיה: "Cannot explode non-list column"

```python
# פתרון: ודא שהעמודה היא list
df.select(pl.col('column').dtype)  # בדיקה
df.with_columns(pl.col('column').str.split(','))  # המרה
```

---

## 🎓 15. תבניות קוד לשימוש חוזר

### תבנית 1: טעינה וניקוי

```python
df = (
    pl.read_csv('data.csv')
    .with_columns(
        pl.col('tags').str.split('|'),
        pl.col('date').str.to_date()
    )
    .drop_nulls()
)
```

### תבנית 2: צבירה וחישוב

```python
result = (
    df
    .group_by('category')
    .agg('metric')
    .with_columns(
        pl.col('metric').list.mean().alias('avg'),
        pl.col('metric').list.max().alias('max'),
        pl.col('metric').list.len().alias('count')
    )
    .sort('avg', descending=True)
)
```

### תבנית 3: פיצול וניתוח

```python
exploded = (
    df
    .select(pl.col('items').str.split(','))
    .explode('items')
    .with_columns(pl.col('items').str.strip())
    .group_by('items')
    .agg(pl.count().alias('frequency'))
)
```

---

**🐻 סיימתם את המדריך המהיר!**

> **Pro Tip**: שמרו את המדריך הזה בקובץ נפרד ופתחו אותו כשאתם עובדים עם Polars.

**בהצלחה!** 🚀
