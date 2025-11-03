#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מדריך Python Polars - קובץ Python מוכן להרצה
==============================================

קובץ זה מכיל את כל דוגמאות הקוד מהמדריך המקיף ל-Polars.
כל קטע מתועד והסבר מפורט בעברית.

מחבר: מדריך Polars בעברית
תאריך: 2025
גרסת Polars: 0.20+

הוראות הרצה:
-----------
1. וודאו ש-Polars מותקן: pip install polars
2. הריצו את הסקריפט: python polars_guide.py
3. או ייבאו פונקציות ספציפיות למחברת שלכם

דרישות:
-------
- Python 3.8+
- polars
- קובץ הנתונים: ../data/titanic_dataset.csv

"""

import polars as pl
from typing import Optional
import sys


# =============================================================================
# חלק 1: יסודות Polars
# =============================================================================

def section_intro():
    """
    הצגת מבוא ל-Polars ובדיקת גרסה
    """
    print("="*70)
    print("  מדריך Python Polars - קובץ Python מקיף")
    print("="*70)
    print(f"\n✓ Polars מותקן!")
    print(f"✓ גרסה: {pl.__version__}")
    print(f"✓ Python: {sys.version.split()[0]}\n")


def create_simple_dataframe():
    """
    יצירת DataFrame פשוט מתוך Dictionary
    
    Returns:
        pl.DataFrame: DataFrame עם עמודות nums ו-letters
    
    דוגמה:
        >>> df = create_simple_dataframe()
        >>> print(df)
    """
    print("\n" + "="*70)
    print("1️⃣  יצירת DataFrame פשוט")
    print("="*70)
    
    df = pl.DataFrame({
        'nums': [1, 2, 3, 4, 5],
        'letters': ['a', 'b', 'c', 'd', 'e']
    })
    
    print("\n📊 DataFrame שנוצר:")
    print(df)
    
    print("\n📖 הסבר:")
    print("  • יצרנו DataFrame מ-Dictionary")
    print("  • המפתחות הפכו לשמות עמודות")
    print("  • הערכים הפכו לתוכן העמודות")
    print(f"  • Polars זיהה אוטומטית: nums={df['nums'].dtype}, letters={df['letters'].dtype}")
    
    return df


def load_titanic_data(filepath: str = '../data/titanic_dataset.csv'):
    """
    טעינת מערך נתוני Titanic מקובץ CSV
    
    Args:
        filepath: נתיב לקובץ CSV (ברירת מחדל: ../data/titanic_dataset.csv)
    
    Returns:
        pl.DataFrame: מערך נתוני Titanic
    
    Raises:
        FileNotFoundError: אם הקובץ לא נמצא
    """
    print("\n" + "="*70)
    print("2️⃣  קריאת DataFrame מקובץ CSV")
    print("="*70)
    
    try:
        df = pl.read_csv(filepath)
        print(f"\n✓ נטען בהצלחה! ({df.height} שורות, {df.width} עמודות)")
        print("\n📊 5 שורות ראשונות:")
        print(df.head())
        return df
    except FileNotFoundError:
        print(f"\n❌ שגיאה: הקובץ {filepath} לא נמצא")
        print("💡 טיפ: וודאו שהנתיב נכון ושהקובץ קיים")
        return None


def show_dataframe_properties(df: pl.DataFrame):
    """
    הצגת מאפייני DataFrame חשובים
    
    Args:
        df: DataFrame לבדיקה
    """
    print("\n" + "="*70)
    print("3️⃣  מאפייני DataFrame")
    print("="*70)
    
    print("\n🔹 Schema (מבנה הטבלה):")
    print(df.schema)
    
    print("\n🔹 Columns (שמות עמודות):")
    print(df.columns)
    
    print("\n🔹 Dtypes (טיפוסי נתונים):")
    print(df.dtypes)
    
    print(f"\n🔹 Shape (צורה): {df.shape}")
    print(f"   • שורות (height): {df.height}")
    print(f"   • עמודות (width): {df.width}")
    
    print("\n🔹 Describe (סטטיסטיקות):")
    print(df.describe())


# =============================================================================
# חלק 2: Series - עמודה בודדת
# =============================================================================

def work_with_series(df: pl.DataFrame):
    """
    דוגמאות לעבודה עם Series (עמודה בודדת)
    
    Args:
        df: DataFrame עם עמודת Age
    """
    print("\n" + "="*70)
    print("4️⃣  עבודה עם Series")
    print("="*70)
    
    # חילוץ Series
    age_series = df['Age']
    
    print("\n📈 עמודת Age:")
    print(f"  • שם: {age_series.name}")
    print(f"  • טיפוס: {age_series.dtype}")
    print(f"  • אורך: {len(age_series)}")
    
    # סטטיסטיקות
    print("\n📊 סטטיסטיקות:")
    print(f"  • ממוצע: {age_series.mean():.2f}")
    print(f"  • חציון: {age_series.median():.2f}")
    print(f"  • סטיית תקן: {age_series.std():.2f}")
    print(f"  • מינימום: {age_series.min():.2f}")
    print(f"  • מקסימום: {age_series.max():.2f}")
    print(f"  • ערכים ייחודיים: {age_series.n_unique()}")
    print(f"  • ערכים חסרים: {age_series.null_count()}")


# =============================================================================
# חלק 3: LazyFrame - עיבוד עצל
# =============================================================================

def demonstrate_lazyframe(df: pl.DataFrame):
    """
    הדגמת שימוש ב-LazyFrame ועיבוד עצל
    
    Args:
        df: DataFrame להמרה ל-LazyFrame
    """
    print("\n" + "="*70)
    print("5️⃣  LazyFrame - עיבוד עצל")
    print("="*70)
    
    print("\n⚡ יצירת LazyFrame ושרשרת פעולות:")
    
    result_lazy = (
        df.lazy()
        .filter(pl.col('Age') > 30)
        .select(['Name', 'Age', 'Fare'])
        .sort('Fare', descending=True)
        .head(10)
    )
    
    print("\n📋 תוכנית ביצוע (אחרי אופטימיזציה):")
    print(result_lazy.explain(optimized=True))
    
    print("\n✨ ביצוע החישוב:")
    result = result_lazy.collect()
    print(result)


# =============================================================================
# חלק 4: בחירה וסינון
# =============================================================================

def select_and_filter_examples(df: pl.DataFrame):
    """
    דוגמאות מקיפות לבחירה וסינון נתונים
    
    Args:
        df: DataFrame לדוגמאות
    """
    print("\n" + "="*70)
    print("6️⃣  בחירה וסינון נתונים")
    print("="*70)
    
    # בחירת עמודות
    print("\n🔹 בחירת עמודות ספציפיות:")
    selected = df.select(['Name', 'Age', 'Fare']).head(3)
    print(selected)
    
    # סינון פשוט
    print("\n🔹 סינון: גיל מעל 30")
    filtered = df.filter(pl.col('Age') > 30)
    print(f"נמצאו {filtered.height} נוסעים")
    print(filtered.select(['Name', 'Age']).head(3))
    
    # תנאים מורכבים
    print("\n🔹 תנאים מורכבים: נשים מעל גיל 30")
    complex_filter = df.filter(
        (pl.col('Age') > 30) & (pl.col('Sex') == 'female')
    )
    print(f"נמצאו {complex_filter.height} נוסעות")
    print(complex_filter.select(['Name', 'Age', 'Sex']).head(3))
    
    # is_in
    print("\n🔹 שימוש ב-is_in:")
    embarked_filter = df.filter(
        pl.col('Embarked').is_in(['C', 'Q'])
    )
    print(f"נוסעים שעלו בנמלים C או Q: {embarked_filter.height}")
    
    # null values
    print("\n🔹 בדיקת ערכי null:")
    null_cabin = df.filter(pl.col('Cabin').is_null())
    print(f"נוסעים ללא מידע על Cabin: {null_cabin.height}")


# =============================================================================
# חלק 5: שינוי עמודות
# =============================================================================

def modify_columns_examples(df: pl.DataFrame):
    """
    דוגמאות ליצירה, שינוי ומחיקה של עמודות
    
    Args:
        df: DataFrame לשינוי
    """
    print("\n" + "="*70)
    print("7️⃣  שינוי עמודות")
    print("="*70)
    
    # הוספת עמודה
    print("\n🔹 הוספת עמודה 'is_adult':")
    df_with_adult = df.with_columns([
        (pl.col('Age') >= 18).alias('is_adult')
    ])
    print(df_with_adult.select(['Name', 'Age', 'is_adult']).head(3))
    
    # הוספת מספר עמודות
    print("\n🔹 הוספת מספר עמודות:")
    df_extended = df.with_columns([
        (pl.col('Age') >= 18).alias('is_adult'),
        (pl.col('Fare') > 50).alias('expensive_ticket')
    ])
    print(df_extended.select([
        'Name', 'Age', 'is_adult', 'Fare', 'expensive_ticket'
    ]).head(3))
    
    # מחיקת עמודות
    print("\n🔹 מחיקת עמודות:")
    df_dropped = df.drop(['Ticket', 'Cabin'])
    print(f"לפני: {df.width} עמודות")
    print(f"אחרי: {df_dropped.width} עמודות")
    
    # שינוי שם
    print("\n🔹 שינוי שמות עמודות:")
    df_renamed = df.rename({'Pclass': 'Class', 'SibSp': 'Siblings'})
    print(f"עמודות חדשות: {df_renamed.columns[:5]}")


# =============================================================================
# חלק 6: Method Chaining
# =============================================================================

def method_chaining_example(df: pl.DataFrame):
    """
    דוגמה מקיפה לשרשור פעולות
    
    Args:
        df: DataFrame לעיבוד
    
    Returns:
        pl.DataFrame: תוצאה אחרי שרשרת פעולות
    """
    print("\n" + "="*70)
    print("8️⃣  Method Chaining - שרשור פעולות")
    print("="*70)
    
    print("\n⛓️  שרשרת פעולות מורכבת:")
    
    result = (
        df
        # סינון: רק גילאים ידועים
        .filter(pl.col('Age').is_not_null())
        
        # הוספת עמודות חדשות
        .with_columns([
            (pl.col('Age') >= 18).alias('is_adult'),
            (pl.col('Fare') / pl.col('Age')).alias('fare_per_year')
        ])
        
        # סינון: רק מבוגרים
        .filter(pl.col('is_adult'))
        
        # בחירת עמודות
        .select(['Name', 'Age', 'Fare', 'fare_per_year', 'Survived'])
        
        # מיון
        .sort('fare_per_year', descending=True)
        
        # 10 ראשונים
        .head(10)
    )
    
    print("\n✨ תוצאה - 10 המבוגרים עם המחיר הגבוה ביותר לשנת חיים:")
    print(result)
    
    return result


# =============================================================================
# חלק 7: קבצים גדולים
# =============================================================================

def large_files_techniques(filepath: str = '../data/titanic_dataset.csv'):
    """
    טכניקות לעבודה עם קבצים גדולים
    
    Args:
        filepath: נתיב לקובץ
    """
    print("\n" + "="*70)
    print("9️⃣  עיבוד קבצים גדולים")
    print("="*70)
    
    # scan_csv
    print("\n🔹 שימוש ב-scan_csv (קריאה עצלה):")
    result = (
        pl.scan_csv(filepath)
        .filter(pl.col('Age') > 30)
        .select(['Name', 'Age', 'Fare'])
        .collect()
    )
    print(f"נטענו {result.height} שורות (רק מה שצריך!)")
    print(result.head(3))
    
    # streaming
    print("\n🔹 Streaming mode:")
    result_stream = (
        pl.scan_csv(filepath)
        .filter(pl.col('Survived') == 1)
        .group_by('Sex').agg([
            pl.count().alias('count'),
            pl.col('Age').mean().alias('avg_age')
        ])
        .collect(streaming=True)
    )
    print(result_stream)
    
    # קריאת עמודות ספציפיות
    print("\n🔹 קריאת עמודות ספציפיות:")
    df_small = pl.read_csv(filepath, columns=['Name', 'Age', 'Survived'])
    print(f"נקראו רק {df_small.width} עמודות (במקום 12)")


# =============================================================================
# פונקציית Main - הרצת כל הדוגמאות
# =============================================================================

def main():
    """
    פונקציה ראשית המריצה את כל הדוגמאות
    """
    # מבוא
    section_intro()
    
    # DataFrame פשוט
    simple_df = create_simple_dataframe()
    
    # טעינת Titanic
    df = load_titanic_data()
    
    if df is not None:
        # מאפייני DataFrame
        show_dataframe_properties(df)
        
        # Series
        work_with_series(df)
        
        # LazyFrame
        demonstrate_lazyframe(df)
        
        # בחירה וסינון
        select_and_filter_examples(df)
        
        # שינוי עמודות
        modify_columns_examples(df)
        
        # Method Chaining
        method_chaining_example(df)
        
        # קבצים גדולים
        large_files_techniques()
    
    # סיום
    print("\n" + "="*70)
    print("  ✅ כל הדוגמאות הושלמו בהצלחה!")
    print("="*70)
    print("\n💡 טיפ: ייבאו פונקציות ספציפיות למחברת שלכם:")
    print("   from polars_guide import load_titanic_data, method_chaining_example")
    print("\n🚀 בהצלחה עם Polars!\n")


# =============================================================================
# הרצה כסקריפט עצמאי
# =============================================================================

if __name__ == "__main__":
    main()
