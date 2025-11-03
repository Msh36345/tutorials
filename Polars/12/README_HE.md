# 📦 חבילת לימוד: Testing & Debugging ב-Polars

## 🎯 מה כלול בחבילה?

חבילת לימוד מקיפה ומאורגנת בעברית ללימוד בדיקות וניפוי שגיאות ב-Polars.

### קבצים בחבילה:

1. **📓 `polars_testing_debugging_guide.ipynb`** - מדריך מקיף + מחברת אינטראקטיבית
2. **📄 `polars_quick_reference.md`** - מדריך מהיר (Cheat Sheet)
3. **📖 `README_HE.md`** - הקובץ הזה (הוראות שימוש)

---

## 📓 1. המדריך המקיף (Jupyter Notebook)

### מה כלול?
- ✅ תוכן עניינים מפורט עם קישורים פנימיים
- ✅ הסברים מפורטים בעברית לכל נושא
- ✅ כל דוגמאות הקוד עם הסברים שלב אחר שלב
- ✅ תאי קוד מוכנים להרצה
- ✅ דוגמאות נוספות להמחשה
- ✅ תרגילים אינטראקטיביים
- ✅ טיפים וטריקים בתיבות מודגשות
- ✅ סיכומים בסוף כל חלק
- ✅ משאבים נוספים

### נושאים מכוסים:
1. **ניפוי שגיאות בפעולות משורשרות**
   - שלוש שיטות: commenting, eager mode, pipe()
   - דוגמאות עובדות ולא עובדות
   - פתרונות מומלצים

2. **בדיקה ואופטימיזציה של Query Plan**
   - show_graph() - הצגה גרפית
   - explain() - הצגה טקסטואלית
   - הבנת אופטימיזציות אוטומטיות
   - Streaming mode

3. **בדיקת איכות נתונים עם cuallee**
   - בדיקות שלמות (Completeness)
   - בדיקות ייחודיות (Uniqueness)
   - בדיקות ערכים מקובלים
   - בדיקות סטטיסטיות
   - שימוש ב-assertions

4. **תרגילים מעשיים**
   - 5 תרגילים מדורגים בקושי
   - מתאים למתחילים ומתקדמים

### איך להשתמש?

#### התקנת תלויות:
```bash
pip install polars cuallee jupyter
```

#### הרצת המחברת:
```bash
jupyter notebook polars_testing_debugging_guide.ipynb
```

#### או ב-JupyterLab:
```bash
jupyter lab polars_testing_debugging_guide.ipynb
```

#### או ב-VS Code:
1. פתחו את הקובץ ב-VS Code
2. וודאו שיש לכם את התוסף "Jupyter" מותקן
3. לחצו על "Run All" או הריצו תא אחר תא

### 💡 טיפים לשימוש:
- **התחילו מהתחלה** - המדריך בנוי בצורה הדרגתית
- **הריצו כל תא** - כל הקוד ניתן להרצה
- **פתרו את התרגילים** - התרגילים בסוף מחזקים את הלמידה
- **שנו וניסו** - שנו את הקוד ונסו דברים חדשים
- **השתמשו בתוכן עניינים** - לניווט מהיר

---

## 📄 2. המדריך המהיר (Quick Reference)

### מה כלול?
- ✅ סיכום תמציתי של כל הפקודות והמושגים
- ✅ טבלאות עזר מאורגנות
- ✅ דוגמאות קוד קצרות עם הסברים
- ✅ טיפים לדיבאג ופתרון בעיות נפוצות
- ✅ Cheat Sheet ויזואלי
- ✅ Checklist לפני Production

### מבנה המדריך:
1. **ניפוי שגיאות** - שלוש שיטות מהירות
2. **אופטימיזציה** - טבלת פקודות ועקרונות
3. **בדיקות איכות** - טבלת פקודות cuallee
4. **פקודות מהירות** - Template וחיפוש מהיר
5. **טיפים לדיבאג** - 5 טכניקות שימושיות
6. **שגיאות נפוצות** - טבלת שגיאות ופתרונות

### איך להשתמש?

#### קריאה ב-VS Code / עורך טקסט:
```bash
code polars_quick_reference.md
```

#### קריאה ב-GitHub או GitLab:
המדריך מעוצב ב-Markdown ונראה מצוין בממשקי Git.

#### המרה ל-PDF (אופציונלי):
```bash
# באמצעות pandoc
pandoc polars_quick_reference.md -o polars_quick_reference.pdf

# או באמצעות markdown-pdf
markdown-pdf polars_quick_reference.md
```

### 💡 טיפים לשימוש:
- **הדפיסו אותו** - מצוין כ-cheat sheet ליד המחשב
- **שמרו אותו פתוח** - בזמן עבודה עם Polars
- **חפשו במהירות** - Ctrl+F לחיפוש מונח ספציפי
- **שלבו אותו בדוקומנטציה** - הוסיפו אותו לפרויקט שלכם

---

## 🎓 מסלול למידה מומלץ

### שלב 1: למידה בסיסית (2-3 שעות)
1. קראו את המדריך המקיף מתחילה לסוף
2. הריצו כל דוגמה
3. עצרו אחרי כל נושא והבינו אותו

### שלב 2: תרגול (1-2 שעות)
1. פתרו את 5 התרגילים במדריך
2. נסו לפתור בלי לראות את הפתרון
3. השוו את הפתרון שלכם

### שלב 3: יישום (בפרויקט שלכם)
1. יישמו את pipe() בקוד שלכם
2. הוסיפו בדיקות cuallee
3. השתמשו ב-explain() להבנת הביצועים

### שלב 4: התמקצעות
1. השתמשו במדריך המהיר כעזר יומיומי
2. קראו את המאמרים המומלצים
3. הצטרפו לקהילת Polars

---

## 📊 טבלת השוואה: מתי להשתמש בכל קובץ?

| מצב | קובץ מומלץ | סיבה |
|-----|-----------|------|
| **לומד לראשונה** | המדריך המקיף (.ipynb) | הסברים מפורטים ודוגמאות |
| **צריך תזכורת מהירה** | המדריך המהיר (.md) | מידע תמציתי ומאורגן |
| **עובד על פרויקט** | המדריך המהיר (.md) | חיפוש מהיר של פקודות |
| **מתרגל** | המדריך המקיף (.ipynb) | תרגילים אינטראקטיביים |
| **מכין מצגת** | שניהם | תוכן מקיף ונקודות תמציתיות |

---

## 🔧 פתרון בעיות נפוצות

### הקובץ .ipynb לא נפתח
**פתרון:**
```bash
# התקנת Jupyter אם לא מותקן
pip install jupyter

# הרצת Jupyter
jupyter notebook
```

### הקוד לא רץ - שגיאת "Module not found"
**פתרון:**
```bash
# התקנת כל התלויות
pip install polars cuallee pandas numpy
```

### הקובץ .md נראה לא טוב
**פתרון:**
- השתמשו בעורך שתומך ב-Markdown (VS Code, Typora, Obsidian)
- או פתחו אותו ב-GitHub/GitLab

### אין לי נתוני Pokemon
**פתרון:**
```python
# יצירת נתונים לדוגמה
import polars as pl

df = pl.DataFrame({
    'Name': ['Bulbasaur', 'Charmander', 'Squirtle'],
    'Type 1': ['Grass', 'Fire', 'Water'],
    'HP': [45, 39, 44],
    'Attack': [49, 52, 48]
})

df.write_csv('pokemon.csv')
```

---

## 📚 משאבים נוספים

### תיעוד רשמי
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [cuallee Documentation](https://canimus.github.io/cuallee/)
- [Pytest Documentation](https://docs.pytest.org/)

### קורסים מומלצים
- [Data Engineering with Polars - DataCamp](https://www.datacamp.com/)
- [Polars Course - Mode Analytics](https://mode.com/)

### קהילה
- [Polars Discord](https://discord.gg/4UfP5cfBE7) - קהילה פעילה ועזרה בזמן אמת
- [Polars GitHub Discussions](https://github.com/pola-rs/polars/discussions)
- [Stack Overflow - python-polars](https://stackoverflow.com/questions/tagged/python-polars)

### ערוצי YouTube
- [Rob Mulla - Polars Tutorials](https://www.youtube.com/@robmulla)
- [Polars Official Channel](https://www.youtube.com/@polars-tech)

---

## 🤝 תרומה ומשוב

### מצאתם טעות?
- פתחו Issue ב-GitHub
- או תקנו ישירות ושלחו Pull Request

### רוצים להוסיף תוכן?
- נשמח לקבל הצעות לשיפור
- דוגמאות נוספות תמיד מתקבלות בברכה

### שאלות?
- פנו דרך Discord של Polars
- או שאלו ב-Stack Overflow עם התג `python-polars`

---

## 📝 רישיון

חבילת לימוד זו נוצרה למטרות חינוכיות.

- ✅ מותר לשתף
- ✅ מותר לשנות
- ✅ מותר לשימוש מסחרי
- ✅ מותר להוסיף לקורסים

**בבקשה ציינו את המקור כאשר משתמשים בחומר.**

---

## 🎉 בהצלחה בלמידה!

זכרו: **התרגול הוא המפתח להצלחה!**

אל תפחדו לנסות, לשנות את הקוד, ולעשות טעויות - כך לומדים!

**Happy Coding! 🚀**

---

*חבילה זו נוצרה ב-2025 | עודכן לאחרונה: נובמבר 2025*
