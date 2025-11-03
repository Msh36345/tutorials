#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מדריך מקיף לעבודה עם מבני נתונים מקוננים ב-Polars
=====================================================

מחבר: נוצר אוטומטית
תאריך: 2025
תיאור: קוד Python מוכן להרצה לעבודה עם Lists, Structs ו-JSON ב-Polars

דרישות:
    pip install polars

שימוש:
    python polars_nested_structures.py
"""

import polars as pl
import warnings
warnings.filterwarnings('ignore')


def print_section(title):
    """הדפסת כותרת מדור"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def load_data(csv_path='../data/us_videos.csv'):
    """
    טעינת נתוני YouTube
    
    Args:
        csv_path (str): נתיב לקובץ CSV
        
    Returns:
        pl.DataFrame: DataFrame עם הנתונים
    """
    print_section("📊 טעינת הנתונים")
    
    # טעינת הנתונים
    df = pl.read_csv(csv_path, try_parse_dates=True)
    
    # המרת עמודת התאריכים
    df = df.with_columns(
        pl.col("trending_date").str.to_date(format="%y.%d.%m")
    )
    
    print(f"✅ נטענו {df.height:,} שורות ו-{df.width} עמודות")
    print(f"\n🔍 5 השורות הראשונות:")
    print(df.head())
    
    return df


def demo_creating_lists(df):
    """הדגמת יצירת רשימות"""
    print_section("📝 1. יצירת רשימות (Creating Lists)")
    
    # דרך 1: פיצול מחרוזות
    print("🔹 דרך 1: פיצול מחרוזות")
    print("-" * 50)
    result = df.select(
        'tags',
        pl.col('tags').str.split('|').alias('tags_list')
    ).head()
    print(result)
    
    # דרך 2: צבירת ערכים
    print("\n🔹 דרך 2: צבירת ערכים")
    print("-" * 50)
    videos_by_date = (
        df
        .group_by('trending_date')
        .agg(pl.col('video_id'))
        .sort('trending_date', descending=True)
    ).head()
    print(videos_by_date)
    
    # דרך 3: איחוד עמודות
    print("\n🔹 דרך 3: איחוד עמודות")
    print("-" * 50)
    engagement = df.select(
        pl.concat_list(
            pl.col('views'),
            pl.col('likes'),
            pl.col('dislikes'),
            pl.col('comment_count')
        ).alias('engagement_metrics')
    ).head()
    print(engagement)


def demo_aggregating_lists(df):
    """הדגמת צבירת אלמנטים ברשימות"""
    print_section("🧮 2. צבירת אלמנטים ברשימות")
    
    # צבירת נתונים
    agg_df = (
        df
        .group_by('trending_date')
        .agg('views', 'likes', 'dislikes', 'comment_count')
        .sort('trending_date', descending=True)
    )
    
    # פעולות צבירה
    print("🔹 סטטיסטיקות על הצפיות")
    print("-" * 50)
    stats = agg_df.select(
        'trending_date',
        pl.col('views').list.min().alias('min_views'),
        pl.col('views').list.max().alias('max_views'),
        pl.col('views').list.mean().alias('avg_views'),
        pl.col('likes').list.max().alias('max_likes'),
        pl.col('dislikes').list.mean().alias('avg_dislikes'),
        pl.col('comment_count').list.sum().alias('total_comments')
    ).head()
    print(stats)
    
    # איחוד למחרוזת
    print("\n🔹 איחוד שמות ערוצים")
    print("-" * 50)
    channels = (
        df
        .group_by('trending_date')
        .agg(pl.col('channel_title'))
        .with_columns(
            pl.col('channel_title').list.join(', ').alias('all_channels')
        )
        .select('trending_date', 'all_channels')
        .sort('trending_date', descending=True)
    ).head(3)
    print(channels)
    
    # ספירת אלמנטים
    print("\n🔹 מספר סרטונים טרנדיים ליום")
    print("-" * 50)
    counts = agg_df.select(
        'trending_date',
        pl.col('views').list.len().alias('num_trending_videos')
    ).head()
    print(counts)


def demo_accessing_elements(df):
    """הדגמת גישה ובחירת אלמנטים"""
    print_section("🎯 3. גישה ובחירת אלמנטים")
    
    # הכנת נתונים
    trending_dates_by_channel = (
        df
        .group_by('channel_title')
        .agg('trending_date')
        .with_columns(
            pl.col('trending_date').list.sort()
        )
    )
    
    # אלמנטים ראשונים ואחרונים
    print("🔹 תאריכים ראשונים ואחרונים")
    print("-" * 50)
    first_last = trending_dates_by_channel.with_columns(
        pl.col('trending_date').list.first().alias('first_trending_date'),
        pl.col('trending_date').list.last().alias('last_trending_date')
    ).head()
    print(first_last)
    
    # גישה לאלמנט ספציפי
    print("\n🔹 האלמנט השמיני")
    print("-" * 50)
    eighth = trending_dates_by_channel.with_columns(
        pl.col('trending_date').list.get(7, null_on_oob=True).alias('8th_element')
    ).head()
    print(eighth)
    
    # חיתוך
    print("\n🔹 דוגמאות חיתוך")
    print("-" * 50)
    sliced = trending_dates_by_channel.select(
        'trending_date',
        pl.col('trending_date').list.slice(0, 2).alias('first_2'),
        pl.col('trending_date').list.slice(-3, 1).alias('3rd_from_end'),
        pl.col('trending_date').list.slice(7).alias('from_8th_onward')
    ).head()
    print(sliced)
    
    # gather
    print("\n🔹 בחירה מותאמת (Gather)")
    print("-" * 50)
    gathered = trending_dates_by_channel.select(
        'trending_date',
        pl.col('trending_date').list.gather([0, -1]).alias('first_and_last'),
        pl.col('trending_date').list.gather([0, 10], null_on_oob=True).alias('first_and_11th')
    ).head()
    print(gathered)


def demo_applying_logic(df):
    """הדגמת החלת לוגיקה על אלמנטים"""
    print_section("⚙️ 4. החלת לוגיקה על אלמנטים")
    
    # הכנת נתונים
    agg_df = (
        df
        .group_by('trending_date')
        .agg('views', 'channel_title')
    )
    
    # המרה לאותיות גדולות
    print("🔹 המרה לאותיות גדולות")
    print("-" * 50)
    uppercase = (
        agg_df
        .select(
            pl.col('channel_title').list.head(2),
            pl.col('channel_title')
            .list.eval(pl.element().str.to_uppercase())
            .list.head(2)
            .alias('channel_uppercase')
        )
    ).head()
    print(uppercase)
    
    # דירוג
    print("\n🔹 דירוג צפיות")
    print("-" * 50)
    ranked = agg_df.select(
        'trending_date',
        'views',
        pl.col('views')
        .list.eval(pl.element().rank('dense', descending=True))
        .alias('views_rank')
    ).head()
    print(ranked)
    
    # חישובים מורכבים
    print("\n🔹 פער מהמקסימום")
    print("-" * 50)
    diff = ranked.select(
        'views',
        pl.col('views')
        .list.eval(pl.element().max() - pl.element())
        .alias('gap_to_max')
    ).head()
    print(diff)
    
    # פעולות קבוצות
    print("\n🔹 פעולות קבוצות")
    print("-" * 50)
    set_ops = ranked.with_columns(
        pl.col('views_rank').list.slice(0, 2).alias('top_2_ranks'),
        pl.col('views_rank').list.slice(-2, 2).alias('bottom_2_ranks')
    ).select(
        'top_2_ranks',
        'bottom_2_ranks',
        pl.col('top_2_ranks').list.set_intersection('bottom_2_ranks').alias('intersection'),
        pl.col('top_2_ranks').list.set_union('bottom_2_ranks').alias('union'),
        pl.col('top_2_ranks').list.set_difference('bottom_2_ranks').alias('difference')
    ).head()
    print(set_ops)


def demo_structs_and_json():
    """הדגמת עבודה עם Structs ו-JSON"""
    print_section("🏗️ 5. עבודה עם Structs ו-JSON")
    
    # טעינת נתוני JSON
    print("🔹 טעינת נתוני JSON")
    print("-" * 50)
    try:
        ga_df = pl.read_json('../data/ga_20170801.json')
        cols = ['visitId', 'date', 'totals', 'trafficSource', 'customDimensions', 'channelGrouping']
        ga_df = ga_df.select(cols)
        
        print(f"✅ נטענו {ga_df.height:,} ביקורים")
        print(ga_df.head(3))
        
        # יצירת struct
        print("\n🔹 יצירת Struct")
        print("-" * 50)
        with_struct = ga_df.with_columns(
            pl.struct('visitId', 'date', 'channelGrouping').alias('visit_info')
        )
        print(with_struct.select('visitId', 'date', 'channelGrouping', 'visit_info').head(3))
        
        # פתיחת struct
        print("\n🔹 פתיחת Struct (Unnesting)")
        print("-" * 50)
        unnested = (
            with_struct
            .select('visit_info')
            .unnest('visit_info')
        ).head(3)
        print(unnested)
        
        # גישה לשדה
        print("\n🔹 גישה לשדה ב-Struct")
        print("-" * 50)
        field_access = with_struct.select(
            'visit_info',
            pl.col('visit_info').struct.field('channelGrouping').alias('channel')
        ).head(3)
        print(field_access)
        
        # המרה ל-JSON
        print("\n🔹 המרה ל-JSON וחזרה")
        print("-" * 50)
        json_conv = (
            ga_df
            .select(
                pl.col('totals').struct.json_encode().alias('totals_json'),
                pl.col('totals').struct.json_encode().str.json_decode().alias('totals_decoded')
            )
        ).head(3)
        print(json_conv)
        
    except Exception as e:
        print(f"⚠️ לא ניתן לטעון את קובץ ה-JSON: {e}")
        print("   אנא ודא שהקובץ '../data/ga_20170801.json' קיים")


def run_all_demos():
    """הרצת כל ההדגמות"""
    print("\n" + "="*70)
    print("  🐻 מדריך מקיף: עבודה עם מבני נתונים מקוננים ב-Polars")
    print("="*70)
    print(f"\n📦 גרסת Polars: {pl.__version__}")
    
    try:
        # טעינת נתונים
        df = load_data()
        
        # הדגמות
        demo_creating_lists(df)
        demo_aggregating_lists(df)
        demo_accessing_elements(df)
        demo_applying_logic(df)
        demo_structs_and_json()
        
        # סיכום
        print_section("🎉 סיכום")
        print("✅ כל ההדגמות הושלמו בהצלחה!")
        print("\n💡 טיפים:")
        print("  - השתמש ב-null_on_oob=True למניעת שגיאות")
        print("  - העדף פעולה אחת על פני פעולות מרובות")
        print("  - השתמש ב-glimpse() לבדיקת טיפוסים")
        print("\n📚 משאבים נוספים:")
        print("  - https://pola-rs.github.io/polars/")
        print("  - https://github.com/pola-rs/polars")
        
    except FileNotFoundError:
        print("\n❌ שגיאה: לא נמצא קובץ הנתונים!")
        print("   אנא ודא שהקובץ '../data/us_videos.csv' קיים")
    except Exception as e:
        print(f"\n❌ שגיאה לא צפויה: {e}")


if __name__ == "__main__":
    run_all_demos()
