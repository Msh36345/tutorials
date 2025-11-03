# 🗺️ מפת ניווט מהירה - חבילת לימוד Polars I/O

## 📖 קבצי המדריך

### 1. [README.md](computer:///mnt/user-data/outputs/README.md)
**מה זה:** מבוא מפורט לחבילה, הסבר על המבנה והתוכן
**קרא אותי אם:** אתה חדש בחבילה ורוצה להבין מה יש כאן

### 2. [polars_io_comprehensive_hebrew.ipynb](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb)
**מה זה:** המדריך המקיף - מחברת Jupyter אינטראקטיבית מלאה
**קרא אותי אם:** אתה רוצה ללמוד לעומק עם דוגמאות מפורטות

### 3. [polars_io_quick_reference_hebrew.md](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md)
**מה זה:** מדריך מהיר - Cheat Sheet עם כל הפקודות
**קרא אותי אם:** אתה צריך תזכורת מהירה או דוגמת קוד

---

## 🎯 לפי רמת ניסיון

### 👶 מתחיל ב-Polars?
**מסלול מומלץ:**
1. קרא [README.md](computer:///mnt/user-data/outputs/README.md) - הבן מה כלול
2. פתח [המדריך המקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - למד שלב אחר שלב
3. התחל עם חלק CSV (החלק הראשון)
4. תרגל עם התרגילים
5. עבור למדריך המהיר כאשר אתה מרגיש בטוח

### 👨‍💻 מכיר Pandas/NumPy?
**מסלול מומלץ:**
1. דלג על ההקדמה
2. קפוץ ל[מדריך המקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - חלק Lazy Loading
3. השתמש ב[מדריך המהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) כ-reference

### 🏢 אתה Data Engineer?
**מסלול מומלץ:**
1. התמקד בחלקי Parquet ו-Delta Lake ב[מדריך המקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb)
2. קרא על Partitioning ו-Streaming
3. השתמש ב[מדריך המהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) לעבודה יומיומית

---

## 🔍 לפי נושא

### אני צריך לעבוד עם...

#### 📄 קבצי CSV
- **מדריך מקיף:** חלק 1 - CSV
- **מדריך מהיר:** סעיף CSV
- **נושאים:** קריאה, כתיבה, lazy loading, encoding

#### 📦 קבצי Parquet
- **מדריך מקיף:** חלק 2 - Parquet
- **מדריך מהיר:** סעיף Parquet
- **נושאים:** דחיסה, partitioning, אופטימיזציה

#### 🔄 Delta Lake
- **מדריך מקיף:** חלק 3 - Delta Lake
- **מדריך מהיר:** סעיף Delta Lake
- **נושאים:** ACID, versioning, cloud storage

#### 🌐 JSON
- **מדריך מקיף:** חלק 4 - JSON
- **מדריך מהיר:** סעיף JSON
- **נושאים:** JSON vs NDJSON, nested data

#### 📊 Excel
- **מדריך מקיף:** חלק 5 - Excel
- **מדריך מהיר:** סעיף Excel
- **נושאים:** גיליונות מרובים, עיצוב, הגבלות

#### 🗄️ בסיסי נתונים
- **מדריך מקיף:** חלק 8 - בסיסי נתונים
- **מדריך מהיר:** סעיף בסיסי נתונים
- **נושאים:** PostgreSQL, MySQL, SQLite

#### 📁 קבצים מרובים
- **מדריך מקיף:** חלק 7 - קבצים מרובים
- **מדריך מהיר:** סעיף קבצים מרובים
- **נושאים:** wildcards, glob, parallel loading

---

## 🚀 תרחישי שימוש נפוצים

### "יש לי קובץ CSV ענק ואני רוצה לסנן אותו"
1. קפוץ ל[מדריך מקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - חלק CSV
2. חפש "Lazy Loading"
3. או השתמש בקוד מ[מדריך מהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) - "אופטימיזציה"

### "אני רוצה להמיר CSV ל-Parquet"
1. [מדריך מהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) - "דוגמאות מהירות"
2. קוד מוכן: `pl.read_csv('file.csv').write_parquet('file.parquet')`

### "אני צריך ליצור דוח Excel עם מספר גיליונות"
1. [מדריך מקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - חלק Excel
2. חפש "מספר גיליונות"
3. תרגיל 5 מכסה את זה!

### "איך אני עובד עם Delta Lake?"
1. [מדריך מקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - חלק Delta Lake
2. למד על append vs overwrite
3. ראה דוגמה ל-partitioning

### "הקובץ שלי לא נטען - יש שגיאת encoding"
1. [מדריך מהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) - "פתרון בעיות"
2. חפש "encoding"
3. נסה: `encoding='utf8-lossy'`

---

## 📊 טבלת השוואה מהירה

| מה אני רוצה לעשות? | איפה למצוא? | זמן קריאה |
|---------------------|--------------|-----------|
| ללמוד מאפס | [מדריך מקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) | 2-3 שעות |
| תזכורת מהירה | [מדריך מהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) | 5 דקות |
| להבין את החבילה | [README](computer:///mnt/user-data/outputs/README.md) | 10 דקות |
| לפתור בעיה | [מדריך מהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) - פתרון בעיות | 2 דקות |
| לתרגל | [מדריך מקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - תרגילים | 30 דקות |

---

## 💡 טיפ מקצועי

**השיטה המומלצת ללמידה:**

1. **יום 1:** קרא את ה-README, עבור על חלק CSV במדריך המקיף
2. **יום 2:** למד Parquet ו-Delta Lake
3. **יום 3:** JSON, Excel, פורמטים נוספים
4. **יום 4:** קבצים מרובים ובסיסי נתונים
5. **יום 5+:** השתמש במדריך המהיר לעבודה יומיומית

**זכור:** אל תנסה לבלוע הכל בבת אחת! למד בקצב שלך.

---

## 🎯 Quick Links

### מדריכים
- [📖 המדריך המקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb)
- [⚡ המדריך המהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md)
- [📚 README](computer:///mnt/user-data/outputs/README.md)

### משאבים חיצוניים
- [Polars Documentation](https://docs.pola.rs/)
- [Polars GitHub](https://github.com/pola-rs/polars)
- [Polars Discord](https://discord.gg/4UfP5cfBE7)

---

## 📞 עזרה

**תקוע? יש שאלות?**

1. חפש ב[מדריך המהיר](computer:///mnt/user-data/outputs/polars_io_quick_reference_hebrew.md) - סעיף "פתרון בעיות"
2. עיין ב[מדריך המקיף](computer:///mnt/user-data/outputs/polars_io_comprehensive_hebrew.ipynb) - כל נושא יש לו סיכום
3. בדוק את ה[README](computer:///mnt/user-data/outputs/README.md) - יש רשימת משאבים
4. הצטרף ל-Discord של Polars

---

**בהצלחה בלמידה! 🚀**

*עודכן: נובמבר 2025*
