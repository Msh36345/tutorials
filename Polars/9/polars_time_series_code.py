#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מדריך מקיף לניתוח סדרות זמן עם Polars
==========================================

פרק 9: Time Series Analysis

קובץ זה מכיל את כל דוגמאות הקוד מהמדריך המקיף.
הקוד מאורגן בפונקציות ומוכן להרצה.

מחבר: Generated from Jupyter Notebook
תאריך: 2025
"""

import polars as pl
from datetime import datetime
import statistics


def print_section(title):
    """מדפיס כותרת מעוצבת לקטע"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def load_data(file_path='../data/toronto_weather.csv'):
    """
    טוען את קובץ נתוני מזג האוויר
    
    Parameters:
    -----------
    file_path : str
        נתיב לקובץ CSV
        
    Returns:
    --------
    lf : pl.LazyFrame
        LazyFrame עם הנתונים
    """
    print_section("1. טעינת נתונים")
    
    print("📥 טוען נתוני מזג אוויר מטורונטו...")
    lf = pl.scan_csv(file_path)
    
    print("✅ הנתונים נטענו בהצלחה!")
    print("\n🔍 5 שורות ראשונות:")
    print(lf.head().collect())
    
    return lf


def convert_temperature(lf):
    """
    ממיר טמפרטורה מקלווין לצלזיוס
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת temperature
        
    Returns:
    --------
    lf : pl.LazyFrame
        LazyFrame עם טמפרטורה בצלזיוס
    """
    print_section("2. המרת טמפרטורה לצלזיוס")
    
    print("🌡️  ממיר מקלווין לצלזיוס (°C = K - 273.15)...")
    lf = lf.with_columns(
        (pl.col('temperature') - 273.15).alias('temperature')
    )
    
    print("✅ ההמרה הושלמה!")
    print("\n🔍 דוגמת נתונים:")
    print(lf.head().collect())
    
    return lf


def parse_dates_automatically(file_path='../data/toronto_weather.csv'):
    """
    מדגים ניתוח תאריכים אוטומטי
    
    Parameters:
    -----------
    file_path : str
        נתיב לקובץ CSV
        
    Returns:
    --------
    lf : pl.LazyFrame
        LazyFrame עם תאריכים מנותחים
    """
    print_section("3. ניתוח תאריכים אוטומטי")
    
    print("📅 טוען עם ניתוח תאריכים אוטומטי...")
    lf_date_parsed = pl.scan_csv(file_path, try_parse_dates=True)
    
    print("\n✅ תאריכים נותחו!")
    print("🔍 סכמה וסוגי נתונים:")
    schema = lf_date_parsed.collect_schema()
    print(schema)
    
    return lf_date_parsed


def parse_dates_manually(lf):
    """
    ממיר עמודת datetime מטקסט לתאריך
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת datetime כטקסט
        
    Returns:
    --------
    lf : pl.LazyFrame
        LazyFrame עם datetime כתאריך
    """
    print_section("4. המרת תאריכים ידנית")
    
    print("🔧 ממיר datetime מטקסט לתאריך...")
    lf = lf.with_columns(
        pl.col('datetime').str.to_datetime()
    )
    
    print("✅ ההמרה הושלמה!")
    print("\n🔍 דוגמה:")
    print(lf.head().collect())
    
    return lf


def extract_date_components(lf):
    """
    מפרק תאריך לרכיביו השונים
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת datetime
        
    Returns:
    --------
    df : pl.DataFrame
        DataFrame עם רכיבי התאריך
    """
    print_section("5. פירוק תאריכים לרכיבים")
    
    print("🔍 מפרק את התאריך לשנה, חודש, יום וזמן...")
    
    date_components = (
        lf
        .select(
            'datetime',
            pl.col('datetime').dt.year().alias('year'),
            pl.col('datetime').dt.month().alias('month'),
            pl.col('datetime').dt.day().alias('day'),
            pl.col('datetime').dt.time().alias('time')
        )
        .head()
        .collect()
    )
    
    print("✅ פירוק הושלם!")
    print("\n📊 תוצאה:")
    print(date_components)
    
    return date_components


def filter_by_date(lf):
    """
    מסנן נתונים לפי תאריך ושעה
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת datetime
        
    Returns:
    --------
    filtered_lf : pl.LazyFrame
        נתונים מסוננים
    """
    print_section("6. סינון לפי תאריך ושעה")
    
    print("🔍 מסנן לשנת 2017, רק שעות בוקר (עד 12:00)...")
    
    filtered_lf = (
        lf
        .filter(
            pl.col('datetime').dt.date().is_between(
                datetime(2017, 1, 1),
                datetime(2017, 12, 31)
            ),
            pl.col('datetime').dt.hour() < 12
        )
    )
    
    print("✅ סינון הושלם!")
    print("\n📊 דוגמת נתונים מסוננים:")
    print(filtered_lf.head().collect())
    
    # אימות
    print("\n🔬 אימות הסינון:")
    validation = (
        filtered_lf
        .select(
            pl.col('datetime').dt.year().unique()
            .implode()
            .list.len()
            .alias('year_cnt'),
            pl.col('datetime').dt.hour().unique()
            .implode()
            .list.len()
            .alias('hour_cnt')
        )
        .head()
        .collect()
    )
    print(validation)
    
    return filtered_lf


def demonstrate_timezones(lf):
    """
    מדגים עבודה עם אזורי זמן
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת datetime
    """
    print_section("7. עבודה עם אזורי זמן")
    
    print("🌍 מדגים replace_time_zone vs convert_time_zone...")
    
    time_zones_lf = (
        lf
        .select(
            'datetime',
            pl.col('datetime').dt.replace_time_zone('America/Toronto')
            .alias('replaced_time_zone_toronto'),
            pl.col('datetime').dt.convert_time_zone('America/Toronto')
            .alias('converted_time_zone_toronto')
        )
    )
    
    print("✅ פעולות אזור זמן הושלמו!")
    print("\n📊 תוצאה:")
    print(time_zones_lf.head().collect())


def demonstrate_duration(lf):
    """
    מדגים חשבון עם תקופות זמן
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת datetime
    """
    print_section("8. חשבון עם תקופות זמן (Duration)")
    
    print("⏱️  מדגים חיבור וחיסור של תקופות זמן...")
    
    duration_example = (
        lf
        .select(
            'datetime',
            (pl.col('datetime') - pl.duration(weeks=5)).alias('minus_5weeks'),
            (pl.col('datetime') + pl.duration(milliseconds=5)).alias('plus_5ms'),
        )
        .head()
        .collect()
    )
    
    print("✅ חישובים הושלמו!")
    print("\n📊 תוצאה:")
    print(duration_example)


def rolling_mean_simple(lf):
    """
    מחשב ממוצע נע פשוט
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם עמודת temperature
        
    Returns:
    --------
    df : pl.DataFrame
        DataFrame עם ממוצע נע
    """
    print_section("9. ממוצע נע פשוט (3 שעות)")
    
    print("📈 מחשב ממוצע נע של 3 שעות על הטמפרטורה...")
    
    rolling_temp = (
        lf
        .select(
            'datetime',
            'temperature',
            pl.col('temperature').rolling_mean(3).alias('3hr_rolling_avg')
        )
        .head()
        .collect()
    )
    
    print("✅ חישוב הושלם!")
    print("\n📊 תוצאה:")
    print(rolling_temp)
    
    return rolling_temp


def calculate_daily_averages(lf):
    """
    מחשב ממוצעים יומיים
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם נתוני טמפרטורה
        
    Returns:
    --------
    daily_lf : pl.LazyFrame
        LazyFrame עם ממוצעים יומיים
    """
    print_section("10. חישוב ממוצעים יומיים")
    
    print("📅 מחשב ממוצע טמפרטורה יומי...")
    
    daily_avg_temperature_lf = (
        lf
        .select(
            pl.col('datetime').dt.date().alias('date'),
            'temperature'
        )
        .group_by('date', maintain_order=True)
        .agg(
            pl.col('temperature').mean().alias('daily_avg_temp')
        )
    )
    
    print("✅ חישוב הושלם!")
    print("\n📊 דוגמה:")
    print(daily_avg_temperature_lf.head().collect())
    
    return daily_avg_temperature_lf


def rolling_statistics(daily_lf):
    """
    מחשב סטטיסטיקות מתגלגלות
    
    Parameters:
    -----------
    daily_lf : pl.LazyFrame
        LazyFrame עם ממוצעים יומיים
    """
    print_section("11. סטטיסטיקות מתגלגלות (3 ימים)")
    
    print("📊 מחשב ממוצע, מינימום ומקסימום נעים...")
    
    rolling_stats = (
        daily_lf
        .select(
            'date',
            'daily_avg_temp',
            pl.col('daily_avg_temp').rolling_mean(3).alias('3day_rolling_avg'),
            pl.col('daily_avg_temp').rolling_min(3).alias('3day_rolling_min'),
            pl.col('daily_avg_temp').rolling_max(3).alias('3day_rolling_max')
        )
        .head()
        .collect()
    )
    
    print("✅ חישובים הושלמו!")
    print("\n📊 תוצאה:")
    print(rolling_stats)


def rolling_methods_comparison(daily_lf):
    """
    משווה שיטות שונות לחישוב חלונות מתגלגלים
    
    Parameters:
    -----------
    daily_lf : pl.LazyFrame
        LazyFrame עם ממוצעים יומיים
    """
    print_section("12. השוואת שיטות חישוב חלונות")
    
    print("🔍 משווה 3 שיטות שונות...")
    
    rolling_methods = (
        daily_lf
        .set_sorted('date')
        .select(
            'date',
            'daily_avg_temp',
            pl.col('daily_avg_temp').rolling_mean(3).alias('3day_rolling_avg'),
            pl.col('daily_avg_temp').rolling_mean(
                window_size=3,
                min_periods=1
            ).alias('3day_rolling_avg2'),
            pl.col('daily_avg_temp').mean().rolling(
                index_column='date',
                period='3d',
                closed='right'
            ).alias('3day_rolling_avg3')
        )
        .head(10)
        .collect()
    )
    
    print("✅ השוואה הושלמה!")
    print("\n📊 תוצאה:")
    print(rolling_methods)


def rolling_context_example(daily_lf):
    """
    מדגים שימוש ב-rolling context
    
    Parameters:
    -----------
    daily_lf : pl.LazyFrame
        LazyFrame עם ממוצעים יומיים
    """
    print_section("13. שימוש ב-Rolling Context")
    
    print("🎯 משתמש ב-rolling context לאגרגציות מרובות...")
    
    rolling_context = (
        daily_lf
        .set_sorted('date')
        .rolling(
            'date',
            period='3d'
        )
        .agg(
            pl.col('daily_avg_temp'),
            pl.col('daily_avg_temp').mean().alias('3day_rolling_avg'),
            pl.col('daily_avg_temp').min().alias('3day_rolling_min'),
            pl.col('daily_avg_temp').max().alias('3day_rolling_max'),
        )
        .head(10)
        .collect()
    )
    
    print("✅ הושלם!")
    print("\n📊 תוצאה:")
    print(rolling_context)


def custom_rolling_function(daily_lf):
    """
    מדגים שימוש בפונקציה מותאמת אישית
    
    Parameters:
    -----------
    daily_lf : pl.LazyFrame
        LazyFrame עם ממוצעים יומיים
    """
    print_section("14. פונקציה מותאמת אישית - חישוב טווח")
    
    def get_range(nums):
        """מחשב את ההפרש בין המקסימום למינימום"""
        return max(nums) - min(nums)
    
    print("🔧 מחשב טווח (range) מתגלגל...")
    
    custom_rolling = (
        daily_lf
        .with_columns(
            pl.col('daily_avg_temp')
            .rolling_map(get_range, window_size=3)
            .alias('3day_rolling_range')
        )
        .head()
        .collect()
    )
    
    print("✅ חישוב הושלם!")
    print("\n📊 תוצאה:")
    print(custom_rolling)


def downsampling_example(lf):
    """
    מדגים תת-דגימה (downsampling)
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם נתונים שעתיים
    """
    print_section("15. תת-דגימה - מעבר לנתונים שבועיים")
    
    print("📉 מדגם מחדש לנתונים שבועיים...")
    
    weekly_humidity = (
        lf
        .set_sorted('datetime')
        .group_by_dynamic(
            'datetime',
            every='1w'
        )
        .agg(
            pl.col('humidity').mean().round(1)
        )
        .head(10)
        .collect()
    )
    
    print("✅ דגימה מחדש הושלמה!")
    print("\n📊 תוצאה:")
    print(weekly_humidity)


def upsampling_example(lf):
    """
    מדגים דגימת יתר (upsampling)
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם נתונים שעתיים
        
    Returns:
    --------
    df : pl.DataFrame
        DataFrame עם נתונים כל 30 דקות
    """
    print_section("16. דגימת יתר - נתונים כל 30 דקות")
    
    print("📈 מדגם מחדש לכל 30 דקות...")
    
    upsampled_df = (
        lf
        .set_sorted('datetime')
        .collect()
        .upsample(
            time_column='datetime',
            every='30m',
            maintain_order=True
        )
        .select(
            'datetime',
            pl.col('humidity')
        )
    )
    
    print("✅ דגימת יתר הושלמה!")
    print("\n📊 דוגמה (שימו לב ל-nulls):")
    print(upsampled_df.head(10))
    
    return upsampled_df


def interpolation_example(upsampled_df):
    """
    מדגים אינטרפולציה למילוי ערכים חסרים
    
    Parameters:
    -----------
    upsampled_df : pl.DataFrame
        DataFrame עם ערכים חסרים
        
    Returns:
    --------
    df : pl.DataFrame
        DataFrame עם ערכים ממולאים
    """
    print_section("17. אינטרפולציה - מילוי ערכים חסרים")
    
    print("🔧 ממלא ערכים חסרים עם אינטרפולציה לינארית...")
    
    interpolated_df = (
        upsampled_df
        .with_columns(
            pl.col('humidity').interpolate()
        )
    )
    
    print("✅ אינטרפולציה הושלמה!")
    print("\n📊 תוצאה (כעת ללא nulls):")
    print(interpolated_df.head(10))
    
    return interpolated_df


def fill_gaps_example(lf):
    """
    מדגים מילוי פערים עם datetime_range
    
    Parameters:
    -----------
    lf : pl.LazyFrame
        LazyFrame עם נתונים
    """
    print_section("18. מילוי פערים עם datetime_range")
    
    print("🔧 יוצר טווח תאריכים רציף...")
    
    # יצירת טווח רציף
    datetime_range_lf = pl.LazyFrame({
        'datetime': pl.datetime_range(
            start=lf.select(pl.col('datetime').min()).collect()[0, 0],
            end=lf.select(pl.col('datetime').max()).collect()[0, 0],
            interval='30m',
            eager=True
        )
    })
    
    # חיבור עם הנתונים המקוריים
    filled_with_join = (
        datetime_range_lf
        .join(lf, on='datetime', how='left')
        .select(
            'datetime',
            pl.col('humidity')
        )
        .collect()
    )
    
    print("✅ פערים מולאו!")
    print("\n📊 דוגמה:")
    print(filled_with_join.head(10))


def forecast_temperatures(file_path='../data/historical_temperatures.csv'):
    """
    מדגים חיזוי סדרות זמן עם functime
    
    Parameters:
    -----------
    file_path : str
        נתיב לקובץ נתוני טמפרטורות היסטוריות
    """
    print_section("19. חיזוי סדרות זמן עם Functime")
    
    try:
        from functime.cross_validation import train_test_split
        from functime.forecasting import linear_model
        from functime.metrics import mase
        from functime.seasonality import add_calendar_effects
    except ImportError:
        print("⚠️  ספריית functime לא מותקנת!")
        print("💡 התקן עם: pip install functime")
        return
    
    print("🔮 טוען נתוני טמפרטורות היסטוריות...")
    
    lf = pl.scan_csv(file_path, try_parse_dates=True)
    
    # קבלת שמות עמודות
    time_col, entity_col, value_col = lf.collect_schema().names()
    
    print(f"✅ נטען! עמודות: {time_col}, {entity_col}, {value_col}")
    
    # צבירה חודשית
    print("\n📊 מצבר לנתונים חודשיים...")
    y = (
        lf
        .group_by_dynamic(
            time_col,
            every='1mo',
            group_by=entity_col,
        )
        .agg(
            (pl.col('temperature').mean() - 273.15).round(1),
        )
    )
    
    print("✅ צבירה הושלמה!")
    print("\n🔍 דוגמה:")
    print(y.group_by('city').head(3).collect())
    
    # פיצול train/test
    print("\n🎯 מפצל לנתוני אימון ובדיקה...")
    test_size = 3
    
    X = y.select(entity_col, time_col)
    y_train, y_test = (
        y
        .select(entity_col, time_col, value_col)
        .pipe(train_test_split(test_size))
    )
    X_train, X_test = X.pipe(train_test_split(test_size))
    
    print(f"✅ פיצול הושלם! Train: {y_train.collect().shape[0]} שורות")
    
    # אימון וחיזוי
    print("\n🤖 מאמן מודל לינארי...")
    forecaster = linear_model(lags=24, freq='1mo')
    forecaster.fit(y=y_train)
    
    print("🎯 מבצע חיזוי...")
    y_pred = forecaster.predict(fh=test_size)
    
    print("✅ חיזוי הושלם!")
    
    # הערכת דיוק
    print("\n📊 מעריך דיוק עם MASE...")
    scores = mase(y_true=y_test, y_pred=y_pred, y_train=y_train)
    
    print("\n🎯 תוצאות:")
    print("\nחיזויים:")
    print(y_pred.collect())
    print("\nציוני MASE:")
    print(scores.collect())
    
    # Feature Engineering
    print("\n✨ יוצר תכונות מתקדמות...")
    y_features = (
        lf
        .group_by_dynamic(
            time_col,
            every='1mo',
            group_by=entity_col,
        )
        .agg(
            (pl.col('temperature').mean() - 273.15).round(1),
            pl.col(value_col).ts.binned_entropy(bin_count=10)
            .alias('binned_entropy'),
            pl.col(value_col).ts.lempel_ziv_complexity(threshold=3)
            .alias('lempel_ziv_complexity'),
            pl.col(value_col).ts.longest_streak_above_mean()
            .alias('longest_streak_above_mean')
        )
        .pipe(add_calendar_effects(['month']))
    )
    
    print("✅ תכונות נוצרו!")
    print("\n📊 דוגמה עם תכונות:")
    print(y_features.head().collect())


def main():
    """
    פונקציה ראשית שמריצה את כל הדוגמאות
    """
    print("\n" + "=" * 80)
    print("  🚀 מדריך מקיף לניתוח סדרות זמן עם Polars")
    print("  📚 פרק 9: Time Series Analysis + Forecasting")
    print("=" * 80)
    
    try:
        # חלק 1: טעינה והכנת נתונים
        lf = load_data()
        lf = convert_temperature(lf)
        
        # חלק 2: עבודה עם תאריכים
        lf_parsed = parse_dates_automatically()
        lf = parse_dates_manually(lf)
        extract_date_components(lf)
        filtered_lf = filter_by_date(lf)
        demonstrate_timezones(lf)
        demonstrate_duration(lf)
        
        # חלק 3: חלונות מתגלגלים
        rolling_mean_simple(lf)
        daily_lf = calculate_daily_averages(lf)
        rolling_statistics(daily_lf)
        rolling_methods_comparison(daily_lf)
        rolling_context_example(daily_lf)
        custom_rolling_function(daily_lf)
        
        # חלק 4: Resampling
        downsampling_example(lf)
        upsampled_df = upsampling_example(lf)
        interpolated_df = interpolation_example(upsampled_df)
        fill_gaps_example(lf)
        
        # חלק 5: חיזוי סדרות זמן (אופציונלי)
        print("\n" + "=" * 80)
        print("  🔮 חלק נוסף: חיזוי סדרות זמן")
        print("=" * 80)
        forecast_temperatures()
        
        print("\n" + "=" * 80)
        print("  ✅ כל הדוגמאות הורצו בהצלחה!")
        print("=" * 80 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ שגיאה: קובץ נתונים לא נמצא - {e}")
        print("💡 ודא שקבצי הנתונים קיימים:")
        print("   - '../data/toronto_weather.csv'")
        print("   - '../data/historical_temperatures.csv'")
        print("   או שנה את הנתיבים בקוד.\n")
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")


if __name__ == "__main__":
    main()
