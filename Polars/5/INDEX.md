# 🎓 חבילת לימוד שלמה: טיפול בערכים חסרים ב-Polars

<div dir="rtl" style="text-align: right;">

## 🎉 החבילה מוכנה!

יצרתי עבורך **חבילת לימוד מקיפה ומסודרת** על טיפול בערכים חסרים (Missing Values) ב-Polars, הכוללת **6 קבצים משלימים**!

---

## 📦 הקבצים שלך

### 📖 1. המדריך המקיף (28KB)
**[polars_missing_values_guide.md](polars_missing_values_guide.md)**

**הכי מומלץ להתחלה!** 🌟

- ✅ תוכן עניינים מלא עם קישורים
- ✅ הסברים מפורטים בעברית
- ✅ כל דוגמאות הקוד מה-Notebook המקורי
- ✅ הסברים שלב אחר שלב
- ✅ פלטים צפויים לכל דוגמה
- ✅ ההבדל בין `null` ל-`NaN`
- ✅ דוגמאות נוספות להמחשה
- ✅ 3 תרגילים עם פתרונות מלאים
- ✅ טיפים וטריקים מתקדמים
- ✅ טבלאות השוואה
- ✅ משאבים נוספים

**קרא את זה קודם!**

---

### 🐍 2. קובץ Python מוכן להרצה (11KB)
**[polars_missing_values_executable.py](polars_missing_values_executable.py)**

**מושלם כדי לראות הכל בפעולה!**

כל דוגמאות הקוד מהמחברת, מוכנות להרצה מיידית:
- ✅ מחולק ל-4 חלקים לוגיים
- ✅ הדפסות ברורות לכל שלב
- ✅ תיעוד מפורט בעברית
- ✅ סיכום בסוף

**איך להריץ:**
```bash
pip install polars numpy
python polars_missing_values_executable.py
```

---

### 📓 3. Jupyter Notebook אינטראקטיבי (14KB)
**[polars_missing_values_interactive.ipynb](polars_missing_values_interactive.ipynb)**

**ללמידה אינטראקטיבית!**

- ✅ תאי קוד ו-Markdown מעורבים
- ✅ תרגילים פתוחים עם רמזים
- ✅ דוגמאות להתנסות
- ✅ הסברים בעברית בתאי Markdown
- ✅ אפשר לשנות ולהריץ מחדש

**איך להשתמש:**
```bash
jupyter notebook polars_missing_values_interactive.ipynb
```

---

### ⚡ 4. מדריך מהיר - Quick Reference (11KB)
**[polars_quick_reference.md](polars_quick_reference.md)**

**למציאה מהירה של פקודות!**

- ✅ Cheat Sheet מקוצר
- ✅ טבלאות השוואה מהירות
- ✅ דפוסים נפוצים (patterns)
- ✅ בעיות ופתרונות (troubleshooting)
- ✅ טיפים לביצועים
- ✅ דוגמאות קצרות לכל פקודה

**שמור את זה פתוח בזמן עבודה!**

---

### 📄 5. PDF לסיכום (6KB)
**[polars_missing_values_summary.pdf](polars_missing_values_summary.pdf)**

**מסודר להדפסה או לשמירה offline!**

- ✅ סיכום כל הנושאים
- ✅ טבלאות מעוצבות
- ✅ מתאים להדפסה
- ✅ פורמט מקצועי

---

### 🚀 6. דוגמה מהירה להדגמה (1.4KB)
**[demo_example.py](demo_example.py)**

**הדגמה מהירה של 4 שלבים!**

```bash
python demo_example.py
```

---

## 🎯 איך להתחיל?

### 🌱 אם אתה חדש ב-Polars:

1. **קרא** את [המדריך המקיף](polars_missing_values_guide.md) 📖
2. **הרץ** את [הקובץ Python](polars_missing_values_executable.py) 🐍
3. **התנסה** עם ה-[Notebook](polars_missing_values_interactive.ipynb) 📓
4. **שמור** את ה-[Quick Reference](polars_quick_reference.md) ⚡

### 💪 אם אתה כבר מכיר Polars:

1. **צלול** ישר ל-[Quick Reference](polars_quick_reference.md) ⚡
2. **נסה** את התרגילים ב-[Notebook](polars_missing_values_interactive.ipynb) 📓
3. **שמור** את ה-[PDF](polars_missing_values_summary.pdf) לעזר מהיר 📄

---

## 📚 מה למדת?

### ✅ זיהוי ערכים חסרים
- `null_count()` - ספירת nulls
- `is_null()` - זיהוי שורות
- `is_nan()` - ההבדל מ-null
- סינון והצגת שורות

### ✅ מחיקת ערכים חסרים
- `drop_nulls()` - מחיקת שורות
- `drop()` - מחיקת עמודות
- טיפול ב-NaN + null ביחד
- מתי כדאי למחוק

### ✅ מילוי ערכים חסרים
- `fill_null()` - ערך קבוע
- אסטרטגיות: `mean`, `min`, `max`
- `interpolate()` - אינטרפולציה
- `forward_fill()` / `backward_fill()`
- מילוי מותאם אישית

---

## 🔥 נקודות חשובות לזכור!

### ⚠️ הבדל קריטי: null vs NaN

```python
# ❌ שגיאה נפוצה
df.drop_nulls()  # לא מוחק NaN!

# ✅ נכון
df.with_columns(pl.all().fill_nan(None)).drop_nulls()
```

### 💡 Best Practices

1. **תמיד בדקו** לפני מחיקה: `df.null_count()`
2. **המירו NaN** לפני עיבוד: `fill_nan(None)`
3. **בחרו נכון** - אסטרטגיית מילוי תלויה בהקשר
4. **תעדו החלטות** - למה בחרתם בשיטה מסוימת
5. **השתמשו ב-with_columns()** לשמירת עמודות

---

## 📊 טבלת מתי להשתמש במה

| שיטה | מתאים ל... | דוגמה |
|------|------------|--------|
| **drop_nulls** | מעט ערכים חסרים | בדיקת תקינות נתונים |
| **fill_null(0)** | ערך ברירת מחדל | כמות גשמים, ספירות |
| **mean/median** | נתונים סטטיסטיים | סקרים, מדידות |
| **interpolate** | סדרות זמן | טמפרטורות, מחירים |
| **forward_fill** | קבוע עד שינוי | מלאי, סטטוס |

---

## 🛠️ התקנה

```bash
# דרישות בסיסיות
pip install polars numpy

# אופציונלי - לעבודה עם Jupyter
pip install jupyter

# אופציונלי - ליצירת PDFs
pip install reportlab
```

---

## 📖 משאבים נוספים

### תיעוד רשמי
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/)
- [User Guide](https://pola-rs.github.io/polars-book/)

### קהילה
- [Polars Discord](https://discord.gg/4UfP5cfBE7)
- [GitHub](https://github.com/pola-rs/polars)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python-polars)

---

## ❓ שאלות נפוצות (FAQ)

**Q: מה ההבדל בין Polars ל-Pandas?**  
A: Polars מהיר יותר (פי 5-10), תחביר יותר ברור, וזיכרון יעיל יותר.

**Q: מה עדיף - למחוק או למלא ערכים חסרים?**  
A: תלוי! אם יש הרבה נתונים - מחקו. אם הם יקרים - מלאו בחוכמה.

**Q: איזו שיטת מילוי הכי טובה?**  
A: תלוי בסוג הנתונים:
- סדרות זמן → `interpolate()`
- נתונים סטטיסטיים → `mean`/`median`
- ערכים קבועים → `forward_fill()`

**Q: למה יש גם null וגם NaN?**  
A: `null` = מידע חסר, `NaN` = פעולה מתמטית לא חוקית. הם שונים!

**Q: איך אני יודע איזה קובץ לפתוח?**  
A: 
- רוצה ללמוד מאפס? → **המדריך המקיף**
- רוצה לראות בפעולה? → **הקובץ Python**
- רוצה להתנסות? → **הNotebook**
- צריך משהו מהיר? → **Quick Reference**

---

## ✨ סיכום

נוצרה עבורך חבילת לימוד מקיפה הכוללת:

✅ **6 קבצים משלימים**  
✅ **הכל בעברית**  
✅ **דוגמאות מעשיות**  
✅ **תרגילים עם פתרונות**  
✅ **מוכן להרצה מיידית**  

---

## 🙏 תודה!

אני מקווה שחבילת הלימוד הזו תעזור לך להבין ולהשתמש ב-Polars בצורה מקצועית!

**יש שאלות? הערות? רעיונות לשיפור?**  
תרגיש חופשי לפנות! 😊

---

**בהצלחה בעבודה עם Polars! 🐻‍❄️**

</div>
