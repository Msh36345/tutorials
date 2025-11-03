"""
========================================
עבודה עם מחרוזות ב-Polars - קובץ Python מוכן להרצה
========================================

קובץ זה מכיל את כל הדוגמאות מהמחברת המקורית עם תיעוד מפורט בעברית.
ניתן להריץ כל קטע בנפרד או את כל הקובץ ביחד.

מחבר: חבילת למידה Polars
תאריך: 2024
"""

import polars as pl
import os

# =====================================
# הגדרות בסיסיות
# =====================================

# הגדרת אורך תצוגה של מחרוזות (50 תווים)
os.environ['POLARS_FMT_STR_LEN'] = str(50)

print("=" * 70)
print("📚 עבודה עם מחרוזות ב-Polars")
print("=" * 70)
print()


# =====================================
# חלק 1: סינון שורות לפי תנאים
# =====================================

print("\n" + "=" * 70)
print("🔍 חלק 1: סינון שורות לפי תנאים")
print("=" * 70)

# טעינת הנתונים
print("\n📁 טוען נתונים...")
df = pl.read_csv('../data/google_store_reviews.csv')
print(f"✅ נטענו {df.height} שורות בהצלחה!")
print("\n🔍 5 השורות הראשונות:")
print(df.head())

# 1.1 סינון לפי תחילת מחרוזת
print("\n" + "-" * 70)
print("1.1 סינון ביקורות שמתחילות במילה 'Very'")
print("-" * 70)
result = (
    df
    .filter(pl.col('content').str.starts_with('Very'))
    .select('content')
    .head()
)
print(result)

# 1.2 סינון לפי סיומת מחרוזת
print("\n" + "-" * 70)
print("1.2 סינון משתמשים ששם המשפחה שלהם 'Smith'")
print("-" * 70)
result = (
    df
    .filter(pl.col('userName').str.ends_with('Smith'))
    .select('userName')
    .head()
)
print(result)

# 1.3 סינון עם contains - מחרוזת מדויקת
print("\n" + "-" * 70)
print("1.3 חיפוש המילה 'happy' בביקורות (מחרוזת מדויקת)")
print("-" * 70)
result = (
    df
    .filter(pl.col('content').str.contains('happy', literal=True))
    .select('content')
    .head()
)
print(result)

# 1.4 סינון עם ביטויים רגולריים
print("\n" + "-" * 70)
print("1.4 חיפוש עם Regex: 'very happy' OR 'best app' OR 'I love'")
print("-" * 70)
result = (
    df
    .filter(pl.col('content').str.contains(r'very happy|best app|I love'))
    .select('content')
    .head()
)
print(result)

# 1.5 סינון עם מספר מילות מפתח
print("\n" + "-" * 70)
print("1.5 ספירת ביקורות המכילות: happy / love / best")
print("-" * 70)
count = (
    df
    .filter(pl.col('content').str.contains_any(['happy', 'love', 'best']))
    .height
)
print(f"✅ נמצאו {count} ביקורות")

# 1.6 ספירת התאמות
print("\n" + "-" * 70)
print("1.6 מציאת ביקורות עם יותר מ-2 התאמות")
print("-" * 70)
result = (
    df
    .filter(pl.col('content').str.count_matches(r'very happy|best app|I love') > 2)
    .select('content')
)
print(f"✅ נמצאו {result.height} ביקורות")
print("\nדוגמאות:")
print(result)

# 1.7 סינון לפי אורך
print("\n" + "-" * 70)
print("1.7 מציאת שמות משתמשים עם יותר מ-10 תווים")
print("-" * 70)
result = (
    df
    .filter(pl.col('userName').str.len_chars() > 10)
    .select('userName')
    .head()
)
print(result)


# =====================================
# חלק 2: המרת מחרוזות לתאריכים ושעות
# =====================================

print("\n" + "=" * 70)
print("📅 חלק 2: המרת מחרוזות לתאריכים ושעות")
print("=" * 70)

# טעינה מחדש של הנתונים
df = pl.read_csv('../data/google_store_reviews.csv')

# 2.1 המרה לתאריך
print("\n" + "-" * 70)
print("2.1 המרה לתאריך (Date)")
print("-" * 70)
result = df.select(
    'at',
    pl.col('at').str.to_date(format='%Y-%m-%d %H:%M:%S').alias('at(date)')
).head()
print(result)

# 2.2 המרה לשעה
print("\n" + "-" * 70)
print("2.2 המרה לשעה (Time)")
print("-" * 70)
result = df.select(
    'at',
    pl.col('at').str.to_time(format='%Y-%m-%d %H:%M:%S').alias('at(time)')
).head()
print(result)

# 2.3 המרה לתאריך ושעה
print("\n" + "-" * 70)
print("2.3 המרה לתאריך ושעה (Datetime)")
print("-" * 70)
result = df.select(
    'at',
    pl.col('at').str.to_datetime(format='%Y-%m-%d %H:%M:%S').alias('at(datetime)')
).head()
print(result)

# 2.4 שימוש ב-strptime
print("\n" + "-" * 70)
print("2.4 שימוש ב-strptime (גמיש יותר)")
print("-" * 70)
result = df.select(
    'at',
    pl.col('at').str.strptime(pl.Date, '%Y-%m-%d %H:%M:%S').alias('at(date)'),
    pl.col('at').str.strptime(pl.Time, '%Y-%m-%d %H:%M:%S').alias('at(time)'),
    pl.col('at').str.strptime(pl.Datetime, '%Y-%m-%d %H:%M:%S').alias('at(datetime)')
).head()
print(result)


# =====================================
# חלק 3: חילוץ חלקי מחרוזת
# =====================================

print("\n" + "=" * 70)
print("✂️ חלק 3: חילוץ חלקי מחרוזת")
print("=" * 70)

# טעינה מחדש
df = pl.read_csv('../data/google_store_reviews.csv')

# 3.1 חיתוך בסיסי
print("\n" + "-" * 70)
print("3.1 חילוץ מהתו הרביעי ואילך")
print("-" * 70)
result = df.select(
    'userName',
    pl.col('userName').str.slice(3).alias('4thCharAndAfter')
).head()
print(result)

# 3.2 חיתוך עם אורך
print("\n" + "-" * 70)
print("3.2 חילוץ 5 תווים החל מהתו הרביעי")
print("-" * 70)
result = df.select(
    'userName',
    pl.col('userName').str.slice(3, 5).alias('5CharsAfter4thChar')
).head()
print(result)

# 3.3 חיתוך מהסוף
print("\n" + "-" * 70)
print("3.3 חילוץ התו השני מהסוף")
print("-" * 70)
result = df.select(
    'userName',
    pl.col('userName').str.slice(-2, 1).alias('TheLastToSecondChar')
).head()
print(result)

# 3.4 חילוץ עם Regex - התאמה ראשונה
print("\n" + "-" * 70)
print("3.4 חילוץ המילה הראשונה עם Regex")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content')
    .str.extract(r'([A-Za-z]+)')
    .alias('extract')
).head(5)
print(result)

# 3.5 חילוץ עם קבוצות לכידה
print("\n" + "-" * 70)
print("3.5 חילוץ עם קבוצות לכידה (3 אותיות + מספר)")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content')
    .str.extract(r'([A-Za-z]{3}) ([0-9]+)', 0)
    .alias('extract whole matches'),
    pl.col('content')
    .str.extract(r'([A-Za-z]{3}) ([0-9]+)', 1)
    .alias('extract group 1'),
    pl.col('content')
    .str.extract(r'([A-Za-z]{3}) ([0-9]+)', 2)
    .alias('extract group 2')
).head(5)
print(result)

# 3.6 חילוץ כל ההתאמות
print("\n" + "-" * 70)
print("3.6 חילוץ כל המילים מהטקסט")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content')
    .str.extract(r'([A-Za-z]+)')
    .alias('extract'),
    pl.col('content')
    .str.extract_all(r'([A-Za-z]+)')
    .alias('extract_all')
).head(5)
print(result)

# 3.7 חילוץ עם extract_groups
print("\n" + "-" * 70)
print("3.7 חילוץ מספר קבוצות למבנה")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content')
    .str.extract(r'([A-Za-z]{3}) ([0-9]+)', 0)
    .alias('extract'),
    pl.col('content')
    .str.extract_groups(r'([A-Za-z]{3}) ([0-9]+)')
    .alias('extract_groups')
).head()
print(result)

# 3.8 Regex עם דגלים
print("\n" + "-" * 70)
print("3.8 חיפוש לא תלוי רישיות (case-insensitive)")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content')
    .str.extract_all(r'(?i)([A-Z]+)')
    .alias('extract_all')
).head()
print(result)


# =====================================
# חלק 4: ניקוי וטיפול במחרוזות
# =====================================

print("\n" + "=" * 70)
print("🧹 חלק 4: ניקוי וטיפול במחרוזות")
print("=" * 70)

# יצירת DataFrame לדוגמה
df = pl.DataFrame({
    'text': [
        '  I aM a HUmAn.  ',
        'it is NOT   easy!  ',
        ' WHY are You cool'
    ]
})

print("\n📊 DataFrame לדוגמה:")
print(df)

# 4.1 הסרת רווחים
print("\n" + "-" * 70)
print("4.1 הסרת רווחים מהתחלה והסוף")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.strip_chars().alias('stripped_text')
)
print(result)

# 4.2 החלפת טקסט - התאמה ראשונה
print("\n" + "-" * 70)
print("4.2 החלפת ההופעה הראשונה של 'a'")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text')
    .str.replace('a', 'new_a', literal=True, n=1)
    .alias('replaced_text')
)
print(result)

# 4.3 החלפת כל ההופעות
print("\n" + "-" * 70)
print("4.3 החלפת כל ההופעות של 'a'")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text')
    .str.replace_all('a', 'new_a', literal=True)
    .alias('replaced_all_text')
)
print(result)

# 4.4 Title Case
print("\n" + "-" * 70)
print("4.4 המרה ל-Title Case")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.to_titlecase().alias('title_case')
)
print(result)

# 4.5 Lowercase
print("\n" + "-" * 70)
print("4.5 המרה לאותיות קטנות")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.to_lowercase().alias('lower_case')
)
print(result)

# 4.6 Uppercase
print("\n" + "-" * 70)
print("4.6 המרה לאותיות גדולות")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.to_uppercase().alias('upper_case')
)
print(result)

# 4.7 ריפוד (Padding)
print("\n" + "-" * 70)
print("4.7 ריפוד משמאל ומימין")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.pad_start(20, '~').alias('pad_start'),
    pl.col('text').str.pad_end(20, '~').alias('pad_end')
)
print(result)

# 4.8 Zero Padding
print("\n" + "-" * 70)
print("4.8 ריפוד עם אפסים")
print("-" * 70)
result = df.select(
    'text',
    pl.col('text').str.pad_start(20, '0').alias('pad_start')
)
print(result)


# =====================================
# חלק 5: פיצול מחרוזות
# =====================================

print("\n" + "=" * 70)
print("✂️ חלק 5: פיצול מחרוזות לרשימות")
print("=" * 70)

# טעינה מחדש של הנתונים
df = pl.read_csv('../data/google_store_reviews.csv')

# 5.1 פיצול בסיסי
print("\n" + "-" * 70)
print("5.1 פיצול לפי רווח")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content').str.split(by=' ').alias('split')
).head()
print(result)

# 5.2 פיצול עם הגבלת מספר חלקים
print("\n" + "-" * 70)
print("5.2 פיצול למקסימום 10 חלקים")
print("-" * 70)
result = df.select(
    'content',
    pl.col('content').str.splitn(by=' ', n=10).alias('splitn'),
    pl.col('content').str.split_exact(by=' ', n=10).alias('split_exact')
).head()
print(result)


# =====================================
# חלק 6: שרשור מחרוזות
# =====================================

print("\n" + "=" * 70)
print("➕ חלק 6: שרשור מחרוזות")
print("=" * 70)

# יצירת DataFrame לדוגמה
df = pl.DataFrame({
    'colA': ['a', 'b', 'c', 'd'],
    'colB': ['aa', 'bb', 'cc', 'dd']
})

print("\n📊 DataFrame לדוגמה:")
print(df)

# 6.1 שרשור פשוט
print("\n" + "-" * 70)
print("6.1 שרשור עם טקסט קבוע")
print("-" * 70)
result = df.select(
    pl.all(),
    (pl.col('colB') + ' new').alias('newColB')
)
print(result)

# 6.2 שרשור בין עמודות
print("\n" + "-" * 70)
print("6.2 שרשור שתי עמודות")
print("-" * 70)
result = df.select(
    pl.all(),
    (pl.col('colA') + pl.col('colB')).alias('colC')
)
print(result)

# 6.3 concat_str מתקדם
print("\n" + "-" * 70)
print("6.3 שרשור מתקדם עם מפריד")
print("-" * 70)
result = df.select(
    pl.all(),
    pl.concat_str(
        pl.lit(100) + 3,
        pl.lit(' '),
        pl.col('colA'),
        pl.col('colB'),
        separator='::'
    ).alias('newCol')
)
print(result)

# 6.4 שרשור כל הערכים בעמודה
print("\n" + "-" * 70)
print("6.4 שרשור כל הערכים בעמודה לטקסט אחד")
print("-" * 70)
result = df.select(
    pl.all(),
    pl.col('colA').str.join(delimiter=', ').alias('concatenatedColA')
)
print(result)


# =====================================
# סיכום
# =====================================

print("\n" + "=" * 70)
print("✅ הרצת הקוד הושלמה בהצלחה!")
print("=" * 70)
print("""
📚 למדת:
  ✓ סינון שורות לפי תנאים
  ✓ המרת מחרוזות לתאריכים ושעות
  ✓ חילוץ חלקי מחרוזת
  ✓ ניקוי וטיפול במחרוזות
  ✓ פיצול מחרוזות לרשימות
  ✓ שרשור מחרוזות

💡 המשך לתרגל ולהתנסות!
""")
