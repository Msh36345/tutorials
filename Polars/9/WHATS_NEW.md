# 🎉 עדכון חבילה - נוסף פרק חיזוי סדרות זמן!

## ✨ מה חדש?

### 🔮 פרק 6: חיזוי סדרות זמן עם Functime

החבילה עודכנה והורחבה! נוסף פרק חדש ומקיף על **חיזוי סדרות זמן** (Time Series Forecasting) 
באמצעות ספריית **Functime** המתקדמת.

---

## 📦 הקבצים המעודכנים

כל 6 הקבצים עודכנו עם התוכן החדש:

### ✅ 1. Jupyter Notebook (48KB)
**polars_time_series_guide.ipynb**
- ✨ נוסף פרק 6 מקיף על חיזוי
- ✨ הסברים שלב אחר שלב
- ✨ דוגמאות קוד מוכנות להרצה
- ✨ תרגיל חיזוי מתקדם

### ✅ 2. קובץ Python (22KB ← הוגדל!)
**polars_time_series_code.py**
- ✨ נוספה פונקציה `forecast_temperatures()`
- ✨ קוד מלא לאימון וחיזוי
- ✨ דוגמאות Feature Engineering
- ✨ מוכן להרצה עם try/except

### ✅ 3. Quick Reference (12KB ← הוגדל!)
**polars_time_series_quick_reference.md**
- ✨ נוסף סעיף חיזוי מהיר
- ✨ טבלת מודלים זמינים
- ✨ דוגמאות קוד קצרות
- ✨ טיפים לחיזוי

### ✅ 4. PDF (13KB ← עודכן!)
**polars_time_series_guide.pdf**
- ✨ נוסף פרק 5 על חיזוי
- ✨ טבלאות מעוצבות
- ✨ דוגמאות קוד
- ✨ מוכן להדפסה

### ✅ 5. README (11KB ← עודכן!)
**README.md**
- ✨ מידע על functime
- ✨ הוראות התקנה
- ✨ תרגיל חיזוי חדש
- ✨ פרויקטים מומלצים מעודכנים

### ✅ 6. START_HERE (7KB ← עודכן!)
**START_HERE.md**
- ✨ סטטיסטיקות מעודכנות
- ✨ דרישות חדשות
- ✨ מידע על החומר החדש

---

## 🎯 מה למדים בפרק החדש?

### 🔮 פרק 6: חיזוי סדרות זמן

#### 1. **מבוא לחיזוי**
- מהו Time Series Forecasting
- למה זה חשוב
- מה זה Functime

#### 2. **הכנת נתונים**
- טעינת נתוני טמפרטורות היסטוריות
- צבירה חודשית
- המרת נתונים

#### 3. **פיצול Train/Test**
- פיצול כרונולוגי (לא אקראי!)
- הבנת ההבדל
- שמירת סדר זמן

#### 4. **אימון מודל**
- מודל Linear עם Lags
- הבנת Lags
- אימון וחיזוי

#### 5. **הערכת דיוק**
- מדד MASE
- פרשנות תוצאות
- השוואה בין ערים

#### 6. **ויזואליזציה**
- גרפים של נתונים אמיתיים
- גרפים של חיזויים
- השוואה ויזואלית

#### 7. **Feature Engineering**
- Binned Entropy
- Lempel-Ziv Complexity
- Longest Streak
- Calendar Effects

---

## 🚀 איך להתחיל עם החיזוי?

### צעד 1: התקן functime
```bash
pip install functime
```

### צעד 2: הכן נתונים
צריך קובץ `historical_temperatures.csv` עם עמודות:
- datetime (תאריך ושעה)
- city (שם עיר)
- temperature (טמפרטורה בקלווין)

### צעד 3: הרץ את הקוד
```python
# אופציה 1: Python Script
python polars_time_series_code.py

# אופציה 2: Jupyter Notebook
# פתח את polars_time_series_guide.ipynb
# גלול לפרק 6
# הרץ את התאים
```

---

## 📊 סטטיסטיקות מעודכנות

### לפני העדכון:
- **קבצים:** 6
- **גודל כולל:** ~96KB
- **שורות קוד:** 691
- **דוגמאות:** 30+
- **תרגילים:** 5
- **שעות למידה:** 4-6

### אחרי העדכון: ⭐
- **קבצים:** 6 (כולם עודכנו!)
- **גודל כולל:** ~113KB (+18%)
- **שורות קוד:** 800+ (+16%)
- **דוגמאות:** 40+ (+33%)
- **תרגילים:** 6 (+1 חיזוי!)
- **שעות למידה:** 5-8 (+2 שעות)

---

## 🎓 מודלים זמינים ב-Functime

```python
from functime.forecasting import (
    linear_model,      # רגרסיה לינארית - התחלה טובה
    knn,              # K-Nearest Neighbors - דפוסים פשוטים
    lightgbm,         # LightGBM - מומלץ מאוד! ⭐
    xgboost,          # XGBoost - דיוק גבוה
    catboost,         # CatBoost - טוב לקטגוריות
    auto_lightgbm,    # AutoML - אופטימיזציה אוטומטית
)
```

---

## 💡 טיפים חשובים לחיזוי

### ✅ עשה:
1. **פצל כרונולוגית** - לא אקראי!
2. **השתמש ב-cross-validation** לסדרות זמן
3. **בדוק stationarity** של הנתונים
4. **נרמל נתונים** לפני אימון
5. **טפל ב-outliers** בזהירות
6. **נסה מודלים שונים** והשווה
7. **הוסף תכונות** (feature engineering)
8. **תעד את הניסויים** שלך

### ❌ אל תעשה:
1. **לא לפצל אקראית** - זה data leakage!
2. **לא להשתמש ב-test** באימון
3. **לא להתעלם מעונתיות** - חשוב מאוד
4. **לא לשכוח validation** set
5. **לא להניח stationarity** בלי בדיקה
6. **לא לאמן על נתונים raw** - עבד עליהם קודם

---

## 📈 מדדי הערכה

| מדד | שם מלא | מתי להשתמש | טוב/רע |
|-----|--------|-----------|--------|
| **MASE** | Mean Absolute Scaled Error | כללי (מומלץ!) | <1 טוב |
| **SMAPE** | Symmetric MAPE | נתונים עם 0 | <20% מצוין |
| **MAE** | Mean Absolute Error | פשוט | קטן יותר = טוב |
| **RMSE** | Root Mean Squared Error | קלאסי | קטן יותר = טוב |

---

## 🎯 תרגיל חדש: חיזוי טמפרטורות ⭐⭐⭐⭐

**משימה מאתגרת:**
1. טען את נתוני הטמפרטורות ההיסטוריות
2. צבור לנתונים חודשיים
3. פצל ל-train/test (3 חודשים לבדיקה)
4. אמן מודל LightGBM (במקום Linear)
5. חזה 6 חודשים קדימה
6. חשב MASE והשווה בין ערים
7. צור ויזואליזציה משווה
8. הוסף תכונות מותאמות אישית

**רמז:** נסה `lightgbm(lags=36, freq='1mo')`

---

## 📚 משאבים נוספים

### Functime:
- **Docs:** https://docs.functime.ai/
- **GitHub:** https://github.com/functime-org/functime
- **Examples:** https://github.com/functime-org/functime/tree/main/examples

### Polars:
- **Docs:** https://pola-rs.github.io/polars/
- **Time Series:** https://pola-rs.github.io/polars-book/user-guide/transformations/time-series/

### למידה נוספת:
- Forecasting: Principles and Practice (ספר מומלץ)
- Time Series Analysis in Python (Course)
- Kaggle Time Series Competitions

---

## 🎉 סיכום העדכון

### מה קיבלת:
✅ פרק חדש ומקיף על חיזוי  
✅ 6 קבצים מעודכנים  
✅ 100+ שורות קוד חדשות  
✅ 10+ דוגמאות חדשות  
✅ תרגיל מתקדם נוסף  
✅ כל החומר בעברית  

### מה הלאה:
🚀 תרגל על נתוני חיזוי אמיתיים  
🚀 נסה מודלים שונים  
🚀 בנה פרויקט חיזוי משלך  
🚀 שתף את מה שלמדת  

---

## 💪 בהצלחה עם החיזוי!

עכשיו יש לך את כל הכלים לא רק לנתח סדרות זמן, אלא גם **לחזות את העתיד**! 🔮

**זכור:** חיזוי טוב דורש:
- 📊 נתונים איכותיים
- 🔧 Feature Engineering חכם
- 🎯 בחירת מודל נכונה
- 📈 אימות קפדני
- 🔄 שיפור מתמיד

**תהנה מהלימוד! 🎓**

---

נוצר בתאריך: 02/11/2025  
גרסה: 2.0 (עם חיזוי!)  
שפה: עברית 🇮🇱  
נוסף: Time Series Forecasting with Functime 🔮
