# 📋 מדריך מהיר - עבודה עם מחרוזות ב-Polars

**גרסה:** 1.0 | **שפה:** עברית

---

## 🎯 סינון מחרוזות

### סינון לפי תחילה/סוף

```python
# מתחיל ב...
df.filter(pl.col('text').str.starts_with('Hello'))

# מסתיים ב...
df.filter(pl.col('text').str.ends_with('.com'))
```

### חיפוש טקסט

```python
# חיפוש מדויק
df.filter(pl.col('text').str.contains('word', literal=True))

# חיפוש עם Regex
df.filter(pl.col('text').str.contains(r'pattern'))

# חיפוש מרובה
df.filter(pl.col('text').str.contains_any(['word1', 'word2']))
```

### תנאים מורכבים

```python
# אורך מחרוזת
df.filter(pl.col('text').str.len_chars() > 10)

# ספירת התאמות
df.filter(pl.col('text').str.count_matches(r'pattern') > 2)
```

---

## 📅 המרות תאריך ושעה

```python
# תאריך
pl.col('date_str').str.to_date(format='%Y-%m-%d')

# שעה
pl.col('time_str').str.to_time(format='%H:%M:%S')

# תאריך ושעה
pl.col('datetime_str').str.to_datetime(format='%Y-%m-%d %H:%M:%S')

# גמיש
pl.col('str').str.strptime(pl.Date, '%Y-%m-%d')
```

### פורמטי תאריך נפוצים

| פורמט | תיאור | דוגמה |
|-------|--------|-------|
| `%Y-%m-%d` | ISO 8601 | 2024-01-15 |
| `%d/%m/%Y` | DD/MM/YYYY | 15/01/2024 |
| `%m/%d/%Y` | MM/DD/YYYY | 01/15/2024 |
| `%Y-%m-%d %H:%M:%S` | Datetime מלא | 2024-01-15 14:30:00 |

---

## ✂️ חילוץ וחיתוך

### חיתוך בסיסי

```python
# מתו ה-3 ואילך
pl.col('text').str.slice(3)

# 5 תווים מתו ה-3
pl.col('text').str.slice(3, 5)

# מהסוף
pl.col('text').str.slice(-5)
```

### חילוץ עם Regex

```python
# התאמה ראשונה
pl.col('text').str.extract(r'([A-Za-z]+)')

# כל ההתאמות
pl.col('text').str.extract_all(r'([A-Za-z]+)')

# קבוצות לכידה
pl.col('text').str.extract(r'(\d+)-(\d+)', 1)  # קבוצה 1

# מבנה
pl.col('text').str.extract_groups(r'(\d+)-(\d+)')
```

### דפוסי Regex שימושיים

| דפוס | תיאור | דוגמה |
|------|--------|-------|
| `\d+` | ספרה אחת או יותר | 123 |
| `[A-Za-z]+` | אותיות | Hello |
| `\w+` | מילה | word_123 |
| `\s+` | רווח לבן | ` ` |
| `.+` | כל תו | abc123!@# |
| `[0-9]{3}` | בדיוק 3 ספרות | 456 |
| `^start` | התחלת מחרוזת | start... |
| `end$` | סוף מחרוזת | ...end |

---

## 🧹 ניקוי וטיפול

### הסרת רווחים

```python
# מהתחלה והסוף
pl.col('text').str.strip_chars()

# רק מהתחלה
pl.col('text').str.strip_chars_start()

# רק מהסוף
pl.col('text').str.strip_chars_end()
```

### החלפת טקסט

```python
# ההופעה הראשונה
pl.col('text').str.replace('old', 'new', literal=True, n=1)

# כל ההופעות
pl.col('text').str.replace_all('old', 'new', literal=True)

# עם Regex
pl.col('text').str.replace_all(r'\s+', ' ')
```

### שינוי רישיות

```python
# אותיות קטנות
pl.col('text').str.to_lowercase()

# אותיות גדולות
pl.col('text').str.to_uppercase()

# Title Case
pl.col('text').str.to_titlecase()
```

### ריפוד (Padding)

```python
# ריפוד משמאל
pl.col('text').str.pad_start(10, '0')

# ריפוד מימין
pl.col('text').str.pad_end(10, ' ')
```

---

## ✂️ פיצול מחרוזות

```python
# פיצול פשוט
pl.col('text').str.split(by=' ')

# פיצול מוגבל
pl.col('text').str.splitn(by=' ', n=5)

# פיצול מדויק
pl.col('text').str.split_exact(by=' ', n=5)
```

### גישה לחלקים

```python
# המילה השלישית
pl.col('text').str.split(by=' ').list.get(2)

# מספר מילים
pl.col('text').str.split(by=' ').list.len()
```

---

## ➕ שרשור מחרוזות

```python
# אופרטור +
pl.col('first') + ' ' + pl.col('last')

# concat_str עם מפריד
pl.concat_str(pl.col('a'), pl.col('b'), separator=', ')

# שרשור כל הערכים בעמודה
pl.col('text').str.join(delimiter=', ')

# עם ערך ליטרלי
pl.col('name') + pl.lit(' - 2024')
```

---

## 📊 טבלת פונקציות מהירה

| פעולה | פונקציה | דוגמה |
|-------|---------|--------|
| **סינון** |
| התחלה | `.str.starts_with()` | `'Hello'` |
| סיום | `.str.ends_with()` | `'.com'` |
| מכיל | `.str.contains()` | `'word'` |
| אורך | `.str.len_chars()` | `> 10` |
| **המרות** |
| תאריך | `.str.to_date()` | `'2024-01-15'` |
| שעה | `.str.to_time()` | `'14:30:00'` |
| Datetime | `.str.to_datetime()` | `'2024-01-15 14:30'` |
| **חילוץ** |
| חיתוך | `.str.slice()` | `(0, 5)` |
| Regex | `.str.extract()` | `r'(\d+)'` |
| הכל | `.str.extract_all()` | `r'(\w+)'` |
| **ניקוי** |
| רווחים | `.str.strip_chars()` | `'  text  '` |
| החלפה | `.str.replace_all()` | `'old' → 'new'` |
| קטנות | `.str.to_lowercase()` | `'TEXT'` |
| גדולות | `.str.to_uppercase()` | `'text'` |
| **פיצול** |
| פיצול | `.str.split()` | `by=' '` |
| מוגבל | `.str.splitn()` | `n=5` |
| **שרשור** |
| חיבור | `+` | `col1 + col2` |
| עם מפריד | `pl.concat_str()` | `sep=','` |

---

## 💡 דוגמאות מהירות

### ניקוי מלא של טקסט

```python
df.select(
    pl.col('text')
    .str.strip_chars()                    # הסר רווחים
    .str.to_lowercase()                   # אותיות קטנות
    .str.replace_all(r'\s+', ' ')        # רווח אחד במקום מרובים
    .str.replace_all(r'[^\w\s]', '')     # הסר סימנים מיוחדים
    .alias('clean_text')
)
```

### חילוץ אימייל

```python
df.select(
    pl.col('text')
    .str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
    .alias('email')
)
```

### חילוץ מספר טלפון

```python
df.select(
    pl.col('text')
    .str.extract(r'(\d{3}-\d{3}-\d{4})')
    .alias('phone')
)
```

### פיצול שם מלא

```python
df.select(
    'full_name',
    pl.col('full_name').str.split(by=' ').list.get(0).alias('first_name'),
    pl.col('full_name').str.split(by=' ').list.get(-1).alias('last_name')
)
```

### יצירת ID מתאריך

```python
df.select(
    pl.concat_str(
        pl.col('date').str.slice(0, 4),    # שנה
        pl.col('date').str.slice(5, 2),    # חודש
        pl.col('user_id'),
        separator='-'
    ).alias('transaction_id')
)
```

---

## 🐛 טיפים לדיבאג

### בדיקת NULL values

```python
df.filter(pl.col('text').is_null())
```

### בדיקת אורכים חריגים

```python
df.select(
    pl.col('text').str.len_chars().describe()
)
```

### מציאת תווים מיוחדים

```python
df.filter(
    pl.col('text').str.contains(r'[^\x00-\x7F]')  # תווים לא-ASCII
)
```

### וולידציה של פורמט

```python
# וולידציה של אימייל
df.filter(
    ~pl.col('email').str.contains(r'^[^@]+@[^@]+\.[^@]+$')
)
```

---

## ⚡ טיפים לביצועים

### DO ✅

```python
# השתמש ב-literal=True כשלא צריך Regex
df.filter(pl.col('text').str.contains('word', literal=True))

# השתמש ב-starts_with במקום Regex
df.filter(pl.col('text').str.starts_with('prefix'))

# פילטר לפני עיבוד כבד
df.filter(pl.col('text').is_not_null()).select(...)
```

### DON'T ❌

```python
# אל תשתמש ב-Regex ללא צורך
df.filter(pl.col('text').str.contains('word'))  # יותר איטי

# אל תעבד NULL values
# השתמש ב-fill_null או filter לפני
```

---

## 🔗 קישורים מהירים

- [תיעוד Polars String](https://pola-rs.github.io/polars/py-polars/html/reference/expressions/string.html)
- [Regex Tester](https://regex101.com/)
- [Python strftime](https://strftime.org/)

---

## 📝 הערות

- **Case Sensitivity:** רוב הפונקציות רגישות לרישיות. השתמש ב-`(?i)` ב-Regex לחיפוש לא רגיש.
- **NULL Handling:** רוב הפונקציות מחזירות NULL עבור ערכי NULL קלט.
- **Performance:** `literal=True` מהיר יותר מ-Regex.
- **Unicode:** Polars תומך ב-Unicode מלא.

---

**נוצר עבור:** לומדי Polars בעברית  
**גרסה:** 1.0  
**תאריך עדכון אחרון:** 2024
