#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מדריך מעשי: עיצוב וארגון נתונים ב-Polars
Reshaping and Tidying Data with Polars

קובץ זה מכיל את כל דוגמאות הקוד מהמדריך המקיף, מוכן להרצה.
כל פונקציה מתועדת היטב בעברית עם docstrings והערות מפורטות.

חבר: Your Name
תאריך: 2024
"""

import polars as pl
from polars import selectors as cs


def print_section(title):
    """
    מדפיסה כותרת מסודרת לקונסול.
    
    Args:
        title (str): הכותרת להדפסה
    """
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def load_and_prepare_data(file_path='../data/academic.csv'):
    """
    טוענת ומכינה את הנתונים לעבודה.
    
    Args:
        file_path (str): נתיב לקובץ CSV
        
    Returns:
        pl.DataFrame: DataFrame מעובד ומוכן
    """
    print_section("טעינה והכנת נתונים")
    
    # טעינת הנתונים
    df = pl.read_csv(file_path)
    print("✓ נתונים נטענו בהצלחה")
    print(f"  גודל: {df.shape[0]} שורות, {df.shape[1]} עמודות")
    
    # עיבוד ראשוני
    df = (
        df
        .select(
            pl.col('year').alias('academic_year'),
            cs.numeric().cast(pl.Int64)
        )
        .filter(
            pl.col('academic_year').str.slice(0, 4).cast(pl.Int32) >= 2018
        )
    )
    
    print("✓ נתונים עובדו בהצלחה")
    print(f"  גודל לאחר סינון: {df.shape[0]} שורות\n")
    
    return df


def demo_unpivot(df):
    """
    מדגימה את פעולת Unpivot - הפיכת עמודות לשורות.
    
    Args:
        df (pl.DataFrame): DataFrame לעבוד עליו
        
    Returns:
        pl.DataFrame: DataFrame בפורמט Long
        
    הסבר:
        Unpivot משמשת להפוך נתונים מפורמט "רחב" (Wide) לפורמט "ארוך" (Long).
        זה שימושי כאשר רוצים לנתח או לוויזואליזציה את הנתונים לפי קטגוריה.
    """
    print_section("דוגמה 1: Unpivot - הפיכת עמודות לשורות")
    
    # הפיכת עמודות לשורות
    long_df = df.unpivot(
        index='academic_year',
        on=[
            'students',
            'us_students',
            'undergraduate',
            'graduate',
            'non_degree',
            'opt'
        ],
        variable_name='student_type',
        value_name='count'
    )
    
    print("נתונים בפורמט Wide (לפני):")
    print(df.head())
    
    print("\nנתונים בפורמט Long (אחרי):")
    print(long_df.head())
    
    # בדיקת סוגי הסטודנטים
    print("\nסוגי סטודנטים ייחודיים:")
    print(long_df.select('student_type').unique())
    
    return long_df


def demo_unpivot_with_selectors(df):
    """
    מדגימה Unpivot עם Selectors - בחירה אוטומטית של עמודות.
    
    Args:
        df (pl.DataFrame): DataFrame לעבוד עליו
        
    Returns:
        pl.DataFrame: DataFrame בפורמט Long
        
    טיפ:
        Selectors מאפשרים לבחור עמודות לפי קריטריונים במקום לרשום כל שם באופן ידני.
    """
    print_section("דוגמה 2: Unpivot עם Selectors")
    
    # שימוש ב-Selector לבחירת עמודות מספריות
    result = df.unpivot(
        index='academic_year',
        on=cs.numeric()  # בוחר אוטומטית כל עמודה מספרית
    )
    
    print("שימוש ב-cs.numeric() לבחירה אוטומטית:")
    print(result.head())
    
    return result


def demo_pivot(long_df):
    """
    מדגימה את פעולת Pivot - הפיכת שורות לעמודות.
    
    Args:
        long_df (pl.DataFrame): DataFrame בפורמט Long
        
    Returns:
        pl.DataFrame: DataFrame בפורמט Wide
        
    הסבר:
        Pivot היא הפעולה ההפוכה ל-Unpivot.
        משמשת להפוך נתונים מפורמט "ארוך" לפורמט "רחב" לתצוגה נוחה.
    """
    print_section("דוגמה 3: Pivot - הפיכת שורות לעמודות")
    
    print("נתונים בפורמט Long (לפני):")
    print(long_df.head())
    
    # הפיכת שורות לעמודות
    wide_df = (
        long_df
        .pivot(
            index='academic_year',
            values='count',
            on='student_type'
        )
    )
    
    print("\nנתונים בפורמט Wide (אחרי):")
    print(wide_df)
    
    return wide_df


def demo_pivot_with_duplicates():
    """
    מדגימה טיפול בכפילויות בעת Pivot.
    
    Returns:
        tuple: (DataFrame עם כפילויות, DataFrame מצליח)
        
    חשוב:
        כאשר יש כפילויות, חובה לציין פונקציית אגרגציה!
    """
    print_section("דוגמה 4: טיפול בכפילויות ב-Pivot")
    
    # יצירת נתונים עם כפילויות לדוגמה
    df = pl.DataFrame({
        'year': ['2020', '2020', '2021', '2021'],
        'category': ['A', 'A', 'B', 'B'],
        'value': [10, 20, 30, 40]
    })
    
    print("נתונים עם כפילויות:")
    print(df)
    
    # ניסיון pivot ללא פונקציית אגרגציה (ייכשל)
    print("\n❌ ניסיון ללא פונקציית אגרגציה:")
    try:
        df.pivot(index='year', values='value', on='category')
    except Exception as e:
        print(f"   שגיאה: {e}")
    
    # pivot מוצלח עם פונקציית אגרגציה
    print("\n✓ עם פונקציית אגרגציה (sum):")
    result = df.pivot(
        index='year',
        values='value',
        on='category',
        aggregate_function='sum'
    )
    print(result)
    
    return df, result


def demo_join():
    """
    מדגימה חיבור (Join) של שתי טבלאות.
    
    Returns:
        pl.DataFrame: טבלה מחוברת
        
    הסבר:
        Join מאפשר לחבר שתי טבלאות על בסיס עמודת מפתח משותפת.
        סוגי Join: inner, left, right, outer
    """
    print_section("דוגמה 5: Join - חיבור טבלאות")
    
    # יצירת שתי טבלאות לדוגמה
    df1 = pl.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'score': [85, 90, 95]
    })
    
    df2 = pl.DataFrame({
        'id': [1, 2, 4],
        'city': ['Tel Aviv', 'Jerusalem', 'Haifa'],
        'age': [25, 30, 28]
    })
    
    print("טבלה 1 (students):")
    print(df1)
    
    print("\nטבלה 2 (details):")
    print(df2)
    
    # Inner Join
    print("\n1. Inner Join (רק שורות משותפות):")
    inner_result = df1.join(df2, on='id', how='inner')
    print(inner_result)
    
    # Left Join
    print("\n2. Left Join (כל השורות מטבלה 1):")
    left_result = df1.join(df2, on='id', how='left')
    print(left_result)
    
    # Outer Join
    print("\n3. Outer Join (כל השורות משתי הטבלאות):")
    outer_result = df1.join(df2, on='id', how='full')
    print(outer_result)
    
    return inner_result


def demo_concat():
    """
    מדגימה שרשור (Concatenation) של טבלאות.
    
    Returns:
        tuple: (concat אנכי, concat אופקי)
        
    הסבר:
        Concatenation מאפשר לחבר מספר טבלאות:
        - vertical: שורות זו מתחת לזו
        - horizontal: עמודות זו ליד זו
    """
    print_section("דוגמה 6: Concatenation - שרשור טבלאות")
    
    # יצירת שלוש טבלאות קטנות
    df1 = pl.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df2 = pl.DataFrame({'a': [5, 6], 'b': [7, 8]})
    df3 = pl.DataFrame({'c': [9, 10], 'd': [11, 12]})
    
    print("טבלה 1:")
    print(df1)
    print("\nטבלה 2:")
    print(df2)
    print("\nטבלה 3:")
    print(df3)
    
    # שרשור אנכי (Vertical)
    print("\n1. Concatenation אנכי (שורות):")
    vertical_result = pl.concat([df1, df2], how='vertical')
    print(vertical_result)
    
    # שרשור אופקי (Horizontal)
    print("\n2. Concatenation אופקי (עמודות):")
    horizontal_result = pl.concat([df1, df3], how='horizontal')
    print(horizontal_result)
    
    return vertical_result, horizontal_result


def demo_partition(df):
    """
    מדגימה חלוקת DataFrame לחלקים (Partition).
    
    Args:
        df (pl.DataFrame): DataFrame לחלק
        
    Returns:
        list: רשימה של DataFrames
        
    שימוש:
        Partition שימושי כאשר רוצים לעבד כל קבוצה בנפרד.
    """
    print_section("דוגמה 7: Partition - חלוקה לקבוצות")
    
    # חלוקה לפי שנה אקדמית
    partitions = df.partition_by('academic_year')
    
    print(f"מספר קבוצות שנוצרו: {len(partitions)}")
    
    # הצגת הקבוצה הראשונה
    print("\nקבוצה ראשונה:")
    print(partitions[0])
    
    return partitions


def demo_transpose(df):
    """
    מדגימה היפוך שורות ועמודות (Transpose).
    
    Args:
        df (pl.DataFrame): DataFrame להיפוך
        
    Returns:
        pl.DataFrame: DataFrame מהופך
        
    הערה:
        Transpose הופך את השורות לעמודות והעמודות לשורות.
    """
    print_section("דוגמה 8: Transpose - היפוך שורות ועמודות")
    
    print("DataFrame מקורי:")
    print(df.head(3))
    
    # ביצוע Transpose
    transposed = df.head(3).transpose(include_header=True)
    
    print("\nDataFrame לאחר Transpose:")
    print(transposed)
    
    return transposed


def main():
    """
    פונקציה ראשית שמריצה את כל הדוגמאות.
    
    מריצה את כל הפונקציות בסדר לוגי ומדפיסה את התוצאות.
    """
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  מדריך מעשי: עיצוב וארגון נתונים ב-Polars".center(78) + "█")
    print("█" + "  Reshaping and Tidying Data with Polars".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    try:
        # 1. טעינת נתונים
        df = load_and_prepare_data()
        
        # 2. Unpivot - דוגמאות שונות
        long_df = demo_unpivot(df)
        demo_unpivot_with_selectors(df)
        
        # 3. Pivot
        wide_df = demo_pivot(long_df)
        demo_pivot_with_duplicates()
        
        # 4. Join
        demo_join()
        
        # 5. Concatenation
        demo_concat()
        
        # 6. טכניקות נוספות
        demo_partition(df)
        demo_transpose(df)
        
        # סיום מוצלח
        print_section("✓ כל הדוגמאות רצו בהצלחה!")
        print("הקובץ מוכן לשימוש. אפשר להריץ פונקציות בנפרד או את כולן ביחד.")
        print("\nלהרצת דוגמה ספציפית:")
        print("  from polars_reshaping import demo_unpivot")
        print("  df = load_and_prepare_data()")
        print("  result = demo_unpivot(df)")
        
    except FileNotFoundError:
        print("\n❌ שגיאה: קובץ הנתונים לא נמצא!")
        print("   וודאו שקובץ 'academic.csv' נמצא בתיקייה '../data/'")
        print("   או שנו את הנתיב בפונקציה load_and_prepare_data()")
        
    except Exception as e:
        print(f"\n❌ שגיאה בלתי צפויה: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # הרצת הקובץ ישירות
    main()
