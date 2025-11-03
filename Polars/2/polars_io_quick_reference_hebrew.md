# 📚 מדריך מהיר: Polars I/O

## תוכן עניינים מהיר
- [CSV](#csv)
- [Parquet](#parquet)
- [Delta Lake](#delta-lake)
- [JSON](#json)
- [Excel](#excel)
- [פורמטים נוספים](#פורמטים-נוספים)
- [קבצים מרובים](#קבצים-מרובים)
- [בסיסי נתונים](#בסיסי-נתונים)
- [טיפים חשובים](#טיפים-חשובים)

---

## CSV

### קריאה (Read)

```python
import polars as pl

# בסיסי
df = pl.read_csv('file.csv')

# מתקדם
df = pl.read_csv(
    'file.csv',
    has_header=False,              # אין כותרות
    new_columns=['col1', 'col2'],  # שמות עמודות
    try_parse_dates=True,          # המרת תאריכים
    schema_overrides={             # טיפוסי נתונים
        'age': pl.Int8,
        'quantity': pl.Int32
    },
    separator='|',                 # מפריד אחר
    encoding='utf8'                # קידוד
)

# Lazy (יעיל!)
lf = pl.scan_csv('file.csv')
result = lf.filter(...).collect()
```

### כתיבה (Write)

```python
# בסיסי
df.write_csv('output.csv')

# מתקדם
df.write_csv(
    'output.csv',
    include_header=False,          # ללא כותרות
    separator='|',                 # מפריד אחר
    datetime_format='%Y-%m-%d'     # פורמט תאריכים
)

# Streaming (לקבצים ענקיים)
lf.sink_csv('output.csv')
```

---

## Parquet

### קריאה

```python
# בסיסי
df = pl.read_parquet('file.parquet')

# עמודות ספציפיות
df = pl.read_parquet(
    'file.parquet',
    columns=['col1', 'col2']      # רק אלה!
)

# רק הסכמה
schema = pl.read_parquet_schema('file.parquet')

# Lazy
lf = pl.scan_parquet('file.parquet')

# Partitioned
df = pl.read_parquet(
    'data_partitioned/',
    use_pyarrow=True,
    pyarrow_options={'partitioning': 'hive'}
)
```

### כתיבה

```python
# בסיסי
df.write_parquet('output.parquet')

# עם דחיסה
df.write_parquet(
    'output.parquet',
    compression='zstd',           # או: snappy, lz4, gzip
    compression_level=10          # 1-22
)

# Partitioned
df.write_parquet(
    'output_partitioned/',
    use_pyarrow=True,
    pyarrow_options={
        'partition_cols': ['year', 'category'],
        'existing_data_behavior': 'overwrite_or_ignore'
    }
)

# Streaming
lf.sink_parquet('output.parquet')
```

---

## Delta Lake

### קריאה

```python
# בסיסי
df = pl.read_delta('delta_table/')

# Lazy
lf = pl.scan_delta('delta_table/')

# Partitioned - חלק ספציפי
df = pl.read_delta(
    'delta_partitioned/',
    pyarrow_options={
        'partitions': [('year', '=', '2023')]
    }
)

# מענן (S3)
df = pl.read_delta(
    's3://bucket/delta_table',
    storage_options={
        'aws_access_key_id': 'KEY',
        'aws_secret_access_key': 'SECRET',
        'aws_region': 'us-east-1'
    }
)
```

### כתיבה

```python
# יצירה / החלפה
df.write_delta(
    'delta_table/',
    mode='overwrite'              # או: append, error
)

# הוספה
df.write_delta('delta_table/', mode='append')

# עם Partitioning
df.write_delta(
    'delta_partitioned/',
    mode='overwrite',
    delta_write_options={
        'partition_by': 'category'
    }
)
```

---

## JSON

### קריאה

```python
# JSON רגיל
df = pl.read_json('file.json')

# NDJSON (שורה אחר שורה)
df = pl.read_ndjson('file.jsonl')

# Lazy (רק NDJSON!)
lf = pl.scan_ndjson('file.jsonl')
```

### כתיבה

```python
# JSON
df.write_json('output.json')

# NDJSON (מומלץ לקבצים גדולים!)
df.write_ndjson('output.jsonl')
```

### עבודה עם JSON מקונן

```python
# פירוק struct
df_unnested = df.unnest('nested_column')

# פירוק list
df_exploded = df.explode('list_column')
```

---

## Excel

### התקנה
```bash
pip install xlsx2csv xlsxwriter openpyxl
```

### קריאה

```python
# גיליון אחד
df = pl.read_excel(
    'file.xlsx',
    sheet_name='Sheet1',          # שם הגיליון
    engine='xlsx2csv',            # מהיר!
    read_options={'try_parse_dates': True}
)

# כל הגיליונות
import openpyxl
wb = openpyxl.load_workbook('file.xlsx')
for sheet in wb.sheetnames:
    df = pl.read_excel('file.xlsx', sheet_name=sheet)
```

### כתיבה

```python
# גיליון אחד
df.write_excel(
    'output.xlsx',
    worksheet='Data',
    header_format={'bold': True}
)

# מספר גיליונות
with pl.ExcelWriter('output.xlsx') as writer:
    df1.write_excel(workbook=writer, worksheet='Sheet1')
    df2.write_excel(workbook=writer, worksheet='Sheet2')

# עם עיצוב
df.write_excel(
    'styled.xlsx',
    worksheet='Report',
    header_format={
        'bold': True,
        'font_color': 'white',
        'bg_color': '#4472C4'
    },
    column_formats={
        'price': '₪#,##0.00'
    },
    autofit=True
)
```

---

## פורמטים נוספים

### IPC (Arrow)

```python
# קריאה/כתיבה
df = pl.read_ipc('file.arrow')
df.write_ipc('output.arrow')

# Lazy
lf = pl.scan_ipc('file.arrow')
lf.collect().write_ipc('output.arrow')  # sink_ipc לא נתמך
```

### Avro

```python
# קריאה/כתיבה
df = pl.read_avro('file.avro')
df.write_avro('output.avro')
```

### Iceberg

```python
# סריקה בלבד
lf = pl.scan_iceberg('catalog/db/table/metadata/file.metadata.json')
```

---

## קבצים מרובים

### כתיבה

```python
# חלוקה לקבצים נפרדים
for name, group_df in df.group_by('category'):
    group_df.write_csv(f'output_{name[0]}.csv')
```

### קריאה

```python
# עם wildcard
df = pl.read_csv('data_*.csv')
lf = pl.scan_csv('data_*.csv')

# קריאת מספר קבצים ספציפיים
import glob
files = glob.glob('data/*.parquet')
lf = pl.scan_parquet(files)

# טעינה מקבילה של כל הקבצים
lfs = [pl.scan_csv(f) for f in glob.glob('*.csv')]
dfs = pl.collect_all(lfs)
```

---

## בסיסי נתונים

### התקנה

```bash
# ConnectorX (מהיר!)
pip install connectorx

# ADBC (מומלץ!)
pip install adbc-driver-postgresql pyarrow

# SQLAlchemy
pip install sqlalchemy psycopg2  # או pg8000
```

### קריאה

```python
# ConnectorX
uri = 'postgresql://user:pass@localhost:5432/db'
df = pl.read_database_uri('SELECT * FROM table', uri)

# ADBC (מומלץ!)
df = pl.read_database_uri(
    'SELECT * FROM table',
    uri,
    engine='adbc'
)

# SQLAlchemy
from sqlalchemy import create_engine
con_string = 'postgresql+pg8000://user:pass@localhost:5432/db'
engine = create_engine(con_string)
df = pl.read_database('SELECT * FROM table', connection=engine)
```

### כתיבה

```python
# ADBC
df.write_database(
    table_name='schema.table',
    connection=uri,
    engine='adbc',
    if_table_exists='append'      # או: replace, fail
)

# SQLAlchemy
df.write_database(
    table_name='schema.table',
    connection=con_string,
    engine='sqlalchemy',
    if_table_exists='replace'
)
```

---

## טיפים חשובים

### 🎯 טבלת בחירת פורמט

| מצב | פורמט מומלץ | למה? |
|-----|-------------|------|
| שיתוף עם אנשים | CSV | פשוט ונפוץ |
| אחסון ארוך טווח | Parquet | דחוס ומהיר |
| Data Lake | Delta Lake | ACID + versioning |
| API / Web | JSON/NDJSON | תקן אינטרנט |
| קבצים ענקיים | Parquet + Lazy | אופטימלי |
| נתונים זמניים | IPC/Arrow | מהיר ביותר |
| דוחות עסקיים | Excel | מוכר |

### ⚡ אופטימיזציה

```python
# ❌ לא יעיל
df = pl.read_csv('huge.csv')
df = df.filter(pl.col('age') > 30)

# ✅ יעיל!
df = (
    pl.scan_csv('huge.csv')
    .filter(pl.col('age') > 30)
    .collect()
)
```

### 💾 חיסכון בזיכרון

```python
# בחירת טיפוסים קטנים
schema_overrides = {
    'age': pl.Int8,        # -128 עד 127
    'quantity': pl.Int16,  # -32K עד 32K
    'price': pl.Float32    # במקום Float64
}

df = pl.read_csv('data.csv', schema_overrides=schema_overrides)
```

### 🗜️ השוואת דחיסות (Parquet)

| דחיסה | מהירות | גודל | מומלץ ל... |
|-------|---------|------|-----------|
| `uncompressed` | ⚡⚡⚡ | ❌ | בדיקות |
| `snappy` | ⚡⚡ | ✅ | שימוש יומיומי |
| `lz4` | ⚡⚡ | ✅ | מהירות |
| `zstd` | ⚡ | ✅✅ | **מומלץ!** |
| `gzip` | ⚡ | ✅✅ | אחסון |

### 🐛 פתרון בעיות

#### Out of Memory
```python
# במקום read_*, השתמש ב-scan_*
lf = pl.scan_parquet('huge.parquet')
result = lf.filter(...).select(...).collect()
```

#### תאריכים לא נכונים
```python
df = pl.read_csv('data.csv', try_parse_dates=True)

# או ידנית:
df = df.with_columns(
    pl.col('date').str.strptime(pl.Date, '%d/%m/%Y')
)
```

#### בעיות encoding
```python
df = pl.read_csv('data.csv', encoding='utf8-lossy')
# או: encoding='latin1'
```

#### קובץ CSV משובש
```python
df = pl.read_csv(
    'data.csv',
    ignore_errors=True,           # דלג על שורות בעייתיות
    truncate_ragged_lines=True    # חתוך שורות ארוכות מדי
)
```

---

## 🔥 טיפים מתקדמים

### Streaming עם סינון

```python
# קורא + מסנן + כותב בזרם אחד
(
    pl.scan_csv('input.csv')
    .filter(pl.col('price') > 1000)
    .select(['customer_id', 'price', 'date'])
    .sink_parquet('expensive_items.parquet')
)
```

### עיבוד באצווה (Batch Processing)

```python
# עיבוד 10,000 שורות בכל פעם
for batch in pl.read_csv_batched('huge.csv', batch_size=10_000):
    process_batch(batch)
    batch.write_csv('output.csv', include_header=False)
```

### קריאה מ-URL

```python
# ישירות מהאינטרנט
url = 'https://example.com/data.csv'
df = pl.read_csv(url)

# או parquet
df = pl.read_parquet('https://example.com/data.parquet')
```

### עבודה עם S3

```python
# AWS S3
storage_options = {
    'aws_access_key_id': 'KEY',
    'aws_secret_access_key': 'SECRET',
    'aws_region': 'us-east-1'
}

df = pl.read_parquet(
    's3://bucket/file.parquet',
    storage_options=storage_options
)

df.write_parquet(
    's3://bucket/output.parquet',
    storage_options=storage_options
)
```

---

## 📐 דוגמאות מהירות

### המרת CSV ל-Parquet

```python
pl.read_csv('data.csv').write_parquet('data.parquet', compression='zstd')
```

### המרת Excel ל-CSV

```python
pl.read_excel('data.xlsx').write_csv('data.csv')
```

### מיזוג קבצים מרובים

```python
df = pl.read_csv('data_*.csv')
df.write_parquet('merged.parquet')
```

### סינון ושמירה

```python
(
    pl.scan_csv('input.csv')
    .filter(pl.col('age') > 18)
    .sink_csv('adults.csv')
)
```

### יצירת דוח Excel מרובה גיליונות

```python
df = pl.read_csv('data.csv')

with pl.ExcelWriter('report.xlsx') as writer:
    df.write_excel(workbook=writer, worksheet='Raw')
    df.group_by('category').agg(pl.col('price').sum()) \
      .write_excel(workbook=writer, worksheet='Summary')
```

---

## 🎓 Cheat Sheet - פקודות חובה

```python
# קריאה
df = pl.read_csv('file.csv')
df = pl.read_parquet('file.parquet')
df = pl.read_json('file.json')
df = pl.read_excel('file.xlsx')

# קריאה Lazy
lf = pl.scan_csv('file.csv')
lf = pl.scan_parquet('file.parquet')
lf = pl.scan_ndjson('file.jsonl')

# כתיבה
df.write_csv('out.csv')
df.write_parquet('out.parquet')
df.write_json('out.json')
df.write_excel('out.xlsx')

# Streaming
lf.sink_csv('out.csv')
lf.sink_parquet('out.parquet')

# בסיס נתונים
df = pl.read_database_uri('SELECT * FROM t', 'postgresql://...')
df.write_database(table_name='t', connection='postgresql://...')

# קבצים מרובים
df = pl.read_csv('data_*.csv')
dfs = pl.collect_all([pl.scan_csv(f) for f in files])
```

---

## 📚 משאבים

- **תיעוד רשמי:** https://docs.pola.rs/
- **GitHub:** https://github.com/pola-rs/polars
- **Discord:** https://discord.gg/4UfP5cfBE7
- **YouTube:** https://www.youtube.com/@polarsDataFrame

---

## 🚀 סיום

**המדריך המהיר הושלם!**

זכור:
- ✅ CSV = פשוט ונפוץ
- ✅ Parquet = מהיר ודחוס
- ✅ Delta = ארגוני ובטוח
- ✅ Lazy = חובה לקבצים גדולים!

**בהצלחה! 🎉**
