# 📚 חבילת לימוד מקיפה: טיפול בערכים חסרים ב-Polars

## 🎯 מה זה?

זוהי חבילת לימוד שלמה ומסודרת שנוצרה מ-Jupyter Notebook על טיפול בערכים חסרים (Missing Values) ב-Polars.
החבילה כוללת **5 קבצים משלימים** שמתאימים לסגנונות למידה שונים!

---

## 📦 הקבצים שנכללים בחבילה

### 1️⃣ **מדריך מקיף (polars_missing_values_guide.md)** 📖
**פורמט:** Markdown | **גודל:** ~28KB | **למי:** לכולם!

**מה כלול:**
- ✅ תוכן עניינים מפורט עם קישורים
- ✅ הסברים מפורטים בעברית
- ✅ דוגמאות קוד עם הסברים שלב אחר שלב
- ✅ פלטים צפויים לכל דוגמה
- ✅ טיפים וטריקים מתקדמים
- ✅ תרגילים עם פתרונות
- ✅ משאבים נוספים

---

### 2️⃣ **קובץ Python מוכן להרצה (polars_missing_values_executable.py)** 🐍
**פורמט:** Python | **גודל:** ~11KB | **למי:** מי שרוצה לראות את הקוד בפעולה

**איך להריץ:**
```bash
pip install polars numpy
python polars_missing_values_executable.py
```

---

### 3️⃣ **Jupyter Notebook אינטראקטיבי (polars_missing_values_interactive.ipynb)** 📓
**פורמט:** Jupyter | **גודל:** ~14KB | **למי:** לומדים אינטראקטיביים

**איך להשתמש:**
```bash
jupyter notebook polars_missing_values_interactive.ipynb
```

---

### 4️⃣ **מדריך מהיר (polars_quick_reference.md)** ⚡
**פורמט:** Markdown | **גודל:** ~11KB | **למי:** צריכים תשובה מהירה

**מה כלול:**
- ✅ Cheat sheet מהיר
- ✅ טבלאות השוואה
- ✅ דפוסים נפוצים
- ✅ בעיות ופתרונות

---

### 5️⃣ **PDF לסיכום (polars_missing_values_summary.pdf)** 📄
**פורמט:** PDF | **גודל:** ~6KB | **למי:** הדפסה או שמירה offline

---

## 🚀 איך להתחיל?

### חדשים ב-Polars? 🌱
1. 📖 קראו את **המדריך המקיף**
2. 🐍 הריצו את **הקובץ Python**
3. 📓 תרגלו עם ה**-Notebook**
4. ⚡ שמרו את **המדריך המהיר** לשימוש יומיומי

### כבר מכירים? 💪
1. ⚡ **Quick Reference** למציאה מהירה
2. 📓 **Notebook** לתרגילים מתקדמים
3. 📄 **PDF** לעזר מהיר

---

## 📋 דרישות

```bash
pip install polars numpy jupyter
```

**גרסאות מומלצות:**
- Python 3.8+
- Polars 0.18.0+

---

## 🎓 נושאים מכוסים

### ✅ זיהוי ערכים חסרים
- `null_count()`, `is_null()`, `is_nan()`
- סינון והצגת שורות

### ✅ מחיקת ערכים חסרים
- `drop_nulls()`, `drop()`
- טיפול ב-NaN + null

### ✅ מילוי ערכים חסרים
- `fill_null()` - קבוע/סטטיסטי
- `interpolate()` - אינטרפולציה
- `forward_fill()` / `backward_fill()`

---

## 💡 טיפים חשובים

### 🔴 להימנע:
```python
# ❌ NaN ≠ null
df.drop_nulls()  # לא עובד על NaN

# ✅ נכון
df.with_columns(pl.all().fill_nan(None)).drop_nulls()
```

### 🟢 Best Practices:
1. ✅ בדקו את הנתונים: `df.null_count()`
2. ✅ תעדו החלטות
3. ✅ בדקו השפעה

---

## 📚 משאבים נוספים

- [Polars Documentation](https://pola-rs.github.io/polars/)
- [API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/)
- [Polars Discord](https://discord.gg/4UfP5cfBE7)

---

## ❓ FAQ

**Q: מה ההבדל בין Polars ל-Pandas?**  
A: Polars מהיר יותר (פי 5-10) ויש לו תחביר יותר ברור.

**Q: מה עדיף - למחוק או למלא?**  
A: תלוי בהקשר! מחקו אם יש הרבה נתונים, מלאו אם הם יקרים.

**Q: איזו שיטת מילוי הכי טובה?**  
A: תלוי בסוג הנתונים והקשר העסקי.

---

## 🎉 סיכום

📚 5 קבצים משלימים  
🎯 מתאים לכל רמה  
💡 דוגמאות מעשיות  
✅ מוכן להרצה מיידית  
🇮🇱 הכל בעברית  

**בהצלחה! 🐻‍❄️**
