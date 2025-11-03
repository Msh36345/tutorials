# 🚀 מדריך מהיר - Polars עם מקורות Cloud

> **Quick Reference Guide** לעבודה עם Polars ופלטפורמות ענן  
> גרסה: 2024 | תואם ל-Polars 0.20+

---

## 📋 תוכן עניינים

- [התקנה מהירה](#התקנה)
- [Amazon S3](#s3)
- [Azure Blob Storage](#azure)
- [Google Cloud Storage](#gcs)
- [BigQuery](#bigquery)
- [Snowflake](#snowflake)
- [טיפים ודיבאג](#tips)
- [טבלת השוואה](#comparison)

---

## ⚡ התקנה מהירה {#התקנה}

```bash
# חבילות בסיס
pip install polars pyarrow

# עבור S3
pip install s3fs

# עבור Azure
pip install adlfs

# עבור GCS
pip install gcsfs google-cloud-bigquery

# עבור Snowflake
pip install snowflake-connector-python adbc-driver-snowflake

# עבור קריאה ממסדי נתונים
pip install connectorx
```

---

## 🪣 Amazon S3 {#s3}

### קריאה (קובץ פומבי)
```python
import polars as pl

# CSV
df = pl.read_csv('s3://bucket-name/file.csv')

# Parquet
df = pl.read_parquet('s3://bucket-name/file.parquet')

# Lazy (מומלץ לקבצים גדולים)
lf = pl.scan_parquet('s3://bucket-name/file.parquet')
```

### קריאה עם אימות
```python
storage_options = {
    'aws_access_key_id': 'YOUR_KEY',
    'aws_secret_access_key': 'YOUR_SECRET',
    'aws_region': 'us-east-1'
}

df = pl.read_csv('s3://bucket/file.csv', 
                 storage_options=storage_options)
```

### כתיבה
```python
import s3fs

fs = s3fs.S3FileSystem(
    key='YOUR_KEY',
    secret='YOUR_SECRET'
)

with fs.open('s3://bucket/output.parquet', 'wb') as f:
    df.write_parquet(f)
```

### קריאה עם סינון (PyArrow)
```python
import pyarrow.dataset as ds

dataset = ds.dataset('s3://bucket/file.parquet', 
                     format='parquet', filesystem=fs)

df = (
    pl.scan_pyarrow_dataset(dataset)
    .filter(pl.col('age') > 30)
    .collect()
)
```

**📌 פורמט נתיב:** `s3://bucket-name/path/to/file.ext`

---

## ☁️ Azure Blob Storage {#azure}

### קריאה
```python
storage_options = {
    'account_name': 'YOUR_ACCOUNT',
    'access_key': 'YOUR_KEY'
}

df = pl.read_csv('az://container/file.csv', 
                 storage_options=storage_options)
```

### כתיבה
```python
import adlfs

fs = adlfs.AzureBlobFileSystem(
    account_name='YOUR_ACCOUNT',
    account_key='YOUR_KEY'
)

with fs.open('az://container/output.parquet', 'wb') as f:
    df.write_parquet(f)
```

### משתני סביבה
```python
import os

os.environ['AZURE_STORAGE_ACCOUNT_NAME'] = 'YOUR_ACCOUNT'
os.environ['AZURE_STORAGE_ACCOUNT_KEY'] = 'YOUR_KEY'

# עכשיו יעבוד בלי storage_options
df = pl.read_csv('az://container/file.csv')
```

### Azure Data Lake (ADLS)
```python
# אותו API - רק שנה את account_name
storage_options['account_name'] = 'YOUR_ADLS_ACCOUNT'
```

**📌 פורמט נתיב:** `az://container-name/path/to/file.ext`

---

## 🌐 Google Cloud Storage (GCS) {#gcs}

### קריאה (פומבי)
```python
df = pl.read_csv('gs://bucket-name/file.csv')
```

### קריאה עם אימות
```python
# שיטה 1: נתיב לקובץ JSON
storage_options = {'token': 'path/to/credentials.json'}

df = pl.read_csv('gs://bucket/file.csv', 
                 storage_options=storage_options)

# שיטה 2: טעינת JSON
import json

with open('credentials.json') as f:
    storage_options = json.load(f)

df = pl.read_csv('gs://bucket/file.csv', 
                 storage_options=storage_options)
```

### כתיבה
```python
import gcsfs

fs = gcsfs.GCSFileSystem(token='credentials.json')

with fs.open('gs://bucket/output.parquet', 'wb') as f:
    df.write_parquet(f)
```

**📌 פורמט נתיב:** `gs://bucket-name/path/to/file.ext`

---

## 📊 BigQuery {#bigquery}

### קריאה - ConnectorX (מהיר)
```python
project = 'my-project'
dataset = 'my_dataset'
table = 'my_table'

query = f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT 1000"
uri = f'bigquery://path/to/credentials.json'

df = pl.read_database_uri(query, uri, engine='connectorx')
```

### קריאה - BigQuery Client
```python
from google.cloud import bigquery

client = bigquery.Client.from_service_account_json('creds.json')
query_job = client.query(query)
rows = query_job.result()

df = pl.from_arrow(rows.to_arrow())
```

### קריאה - read_database
```python
df = pl.read_database(query, connection=client)
```

### כתיבה
```python
import io

with io.BytesIO() as stream:
    df.write_csv(stream)
    stream.seek(0)
    
    job = client.load_table_from_file(
        stream,
        destination=f'{project}.{dataset}.new_table',
        project=project,
        job_config=bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV
        )
    )
    job.result()
```

### 💡 טיפים לחיסכון
```python
# ✅ טוב - בחר עמודות ספציפיות
query = "SELECT name, age FROM table LIMIT 1000"

# ❌ רע - שולף הכל
query = "SELECT * FROM huge_table"

# ✅ טוב - סנן בשאילתה
query = "SELECT * FROM table WHERE date >= '2024-01-01'"
```

---

## ❄️ Snowflake {#snowflake}

### הגדרת פרמטרים
```python
config = {
    'username': 'YOUR_USER',
    'password': 'YOUR_PASS',
    'account': 'abc12345.region',
    'database': 'MY_DB',
    'schema': 'PUBLIC',
    'warehouse': 'COMPUTE_WH',
    'role': 'ACCOUNTADMIN'
}
```

### קריאה - ADBC (מומלץ - הכי מהיר)
```python
uri = (
    f"snowflake://{config['username']}:{config['password']}"
    f"@{config['account']}/{config['database']}/{config['schema']}"
    f"?warehouse={config['warehouse']}&role={config['role']}"
)

query = "SELECT * FROM my_table"
df = pl.read_database_uri(query, uri, engine='adbc')
```

### קריאה - Snowflake Connector
```python
import snowflake.connector

conn = snowflake.connector.connect(
    user=config['username'],
    password=config['password'],
    account=config['account'],
    warehouse=config['warehouse'],
    database=config['database'],
    schema=config['schema']
)

# דרך Arrow (מהיר)
df = pl.from_arrow(
    conn.cursor().execute(query).fetch_arrow_all()
)

# או
df = pl.read_database(query, connection=conn)
```

### 💡 טיפים
```python
# השהה warehouse אחרי שימוש
conn.cursor().execute("ALTER WAREHOUSE my_wh SUSPEND")

# שנה גודל לפי צורך
conn.cursor().execute(
    "ALTER WAREHOUSE my_wh SET WAREHOUSE_SIZE = 'LARGE'"
)
```

---

## 🔧 טיפים כלליים ודיבאג {#tips}

### 1. בחירת פורמט קובץ

| פורמט | קריאה | כתיבה | גודל | מהירות | מתי להשתמש |
|-------|-------|-------|------|--------|------------|
| CSV | ✅ | ✅ | 😐 | 😐 | קבצים קטנים, שיתוף אנושי |
| Parquet | ✅ | ✅ | ✅ | ✅ | **מומלץ לכל דבר!** |
| JSON | ✅ | ✅ | ❌ | ❌ | APIs, הגדרות |

```python
# ✅ מומלץ - Parquet
df.write_parquet('output.parquet')

# 😐 לשיתוף - CSV
df.write_csv('output.csv')
```

### 2. Lazy vs Eager

```python
# Eager - טוען מיד (קבצים קטנים)
df = pl.read_csv('file.csv')

# Lazy - מחשב רק כשצריך (קבצים גדולים)
lf = pl.scan_csv('file.csv')
result = (
    lf
    .filter(pl.col('age') > 30)
    .select(['name', 'age'])
    .collect()  # רק כאן זה רץ באמת!
)
```

### 3. אבטחת Credentials

```python
# ❌ לעולם לא!
api_key = "my-secret-key-123"

# ✅ משתני סביבה
import os
api_key = os.environ.get('API_KEY')

# ✅ קבצי config מחוץ ל-git
with open('../secrets/config.json') as f:
    config = json.load(f)

# ✅ .gitignore
"""
secrets/
*.json
credentials*
"""
```

### 4. דיבאג שגיאות נפוצות

#### שגיאה: "No module named 's3fs'"
```bash
pip install s3fs
```

#### שגיאה: "Access Denied" ב-S3
```python
# בדוק credentials
import boto3
s3 = boto3.client('s3')
s3.list_buckets()  # אמור לעבוד
```

#### שגיאה: "File not found" ב-GCS
```python
# וודא שהנתיב נכון
import gcsfs
fs = gcsfs.GCSFileSystem()
fs.ls('gs://bucket-name/')  # רשימת קבצים
```

#### שגיאה: חיבור ל-Snowflake נכשל
```python
# בדוק את כל הפרמטרים
import snowflake.connector
try:
    conn = snowflake.connector.connect(
        user='USER',
        password='PASS',
        account='ACCOUNT'  # ללא .snowflakecomputing.com
    )
    print("✅ חיבור הצליח!")
except Exception as e:
    print(f"❌ שגיאה: {e}")
```

### 5. אופטימיזציה

```python
# ✅ סנן מוקדם
df = (
    pl.scan_parquet('huge_file.parquet')
    .filter(pl.col('year') == 2024)  # סינון לפני טעינה
    .select(['id', 'name'])           # רק עמודות נדרשות
    .collect()
)

# ❌ לא יעיל
df = pl.read_parquet('huge_file.parquet')  # טוען הכל
df = df.filter(pl.col('year') == 2024)     # מסנן אחרי

# ✅ השתמש ב-predicate pushdown
import pyarrow.dataset as ds
dataset = ds.dataset('s3://bucket/data.parquet', filesystem=fs)
df = pl.scan_pyarrow_dataset(dataset).filter(...).collect()
```

### 6. ניהול זיכרון

```python
# בדיקת גודל DataFrame
df.estimated_size('mb')  # מגה-בייטים

# streaming לקבצים ענקיים
for batch in pl.read_csv_batched('huge.csv', batch_size=10000):
    process(batch)

# שחרור זיכרון
del df
import gc
gc.collect()
```

---

## 📊 טבלת השוואה - פלטפורמות {#comparison}

### אחסון (Storage)

| תכונה | S3 | Azure Blob | GCS |
|-------|----|-----------|----|
| **מחיר** (לTB/חודש) | ~$23 | ~$18 | ~$20 |
| **מהירות קריאה** | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ |
| **זמינות** | 99.99% | 99.9% | 99.95% |
| **אינטגרציה AWS** | ✅✅✅ | ❌ | ❌ |
| **אינטגרציה Azure** | ❌ | ✅✅✅ | ❌ |
| **אינטגרציה GCP** | ❌ | ❌ | ✅✅✅ |
| **פשטות API** | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ |
| **גמישות אזורים** | ✅✅✅ | ✅✅ | ✅✅ |

### מסדי נתונים (Databases)

| תכונה | BigQuery | Snowflake |
|-------|----------|-----------|
| **מחיר לTB סרוק** | $5 | $40 (compute) |
| **מהירות שאילתות** | ⚡⚡⚡ | ⚡⚡⚡ |
| **Serverless** | ✅ | ✅ |
| **SQL Standard** | ✅ | ✅ |
| **למידה** | קל | בינוני |
| **Data Sharing** | ❌ | ✅✅✅ |
| **Multi-cloud** | ❌ | ✅ |
| **אידיאלי ל** | GCP users | Enterprise |

### מתי להשתמש במה?

#### S3 - השתמש כאשר:
- ✅ אתה כבר ב-AWS
- ✅ צריך אינטגרציה עם EC2/Lambda
- ✅ צריך versioning מתקדם
- ✅ יש לך צוות DevOps חזק

#### Azure Blob - השתמש כאשר:
- ✅ אתה ב-Microsoft ecosystem
- ✅ יש לך Active Directory
- ✅ צריך tier pricing (Hot/Cool/Archive)
- ✅ צוות מוכר עם Azure

#### GCS - השתמש כאשר:
- ✅ אתה ב-GCP
- ✅ משתמש ב-BigQuery/Dataflow
- ✅ רוצה API פשוט
- ✅ צריך ביצועים גבוהים

#### BigQuery - השתמש כאשר:
- ✅ ניתוח נתונים גדולים (TB+)
- ✅ שאילתות ad-hoc תכופות
- ✅ לא רוצה לנהל תשתית
- ✅ צריך auto-scaling

#### Snowflake - השתמש כאשר:
- ✅ צריך multi-cloud
- ✅ Data sharing חשוב
- ✅ צריך גמישות compute/storage
- ✅ יש תקציב גדול

---

## 🎯 דוגמאות קוד מהירות

### Example 1: קריאה מ-S3 ← עיבוד ← שמירה ל-GCS
```python
import polars as pl
import s3fs
import gcsfs

# קריאה מ-S3
s3_fs = s3fs.S3FileSystem()
df = pl.read_parquet('s3://my-bucket/input.parquet')

# עיבוד
df_processed = (
    df
    .filter(pl.col('status') == 'active')
    .select(['id', 'name', 'value'])
    .with_columns(pl.col('value') * 2)
)

# שמירה ל-GCS
gcs_fs = gcsfs.GCSFileSystem(token='creds.json')
with gcs_fs.open('gs://my-bucket/output.parquet', 'wb') as f:
    df_processed.write_parquet(f)
```

### Example 2: שאילתה ב-BigQuery ← שמירה ל-S3
```python
from google.cloud import bigquery
import s3fs

# קריאה מ-BigQuery
client = bigquery.Client.from_service_account_json('creds.json')
query = "SELECT * FROM `project.dataset.table` WHERE date >= '2024-01-01'"
df = pl.from_arrow(client.query(query).result().to_arrow())

# שמירה ל-S3
s3_fs = s3fs.S3FileSystem(key='KEY', secret='SECRET')
with s3_fs.open('s3://bucket/output.parquet', 'wb') as f:
    df.write_parquet(f)
```

### Example 3: Snowflake ← עיבוד ← Azure
```python
import snowflake.connector
import adlfs

# קריאה מ-Snowflake
conn = snowflake.connector.connect(
    user='USER', password='PASS', account='ACCOUNT',
    database='DB', schema='SCHEMA', warehouse='WH'
)
df = pl.from_arrow(
    conn.cursor().execute("SELECT * FROM table").fetch_arrow_all()
)

# עיבוד
df_agg = df.group_by('category').agg(pl.col('amount').sum())

# שמירה ל-Azure
azure_fs = adlfs.AzureBlobFileSystem(
    account_name='ACCOUNT', account_key='KEY'
)
with azure_fs.open('az://container/output.parquet', 'wb') as f:
    df_agg.write_parquet(f)
```

---

## 🆘 פתרון בעיות נפוצות

### בעיה: "ImportError: cannot import name 'polars'"
```bash
# פתרון
pip install --upgrade polars
```

### בעיה: "PermissionDenied" ב-S3
```python
# בדוק הרשאות IAM
import boto3
sts = boto3.client('sts')
print(sts.get_caller_identity())  # מי אתה?

# בדוק bucket permissions
s3 = boto3.client('s3')
s3.get_bucket_policy(Bucket='my-bucket')
```

### בעיה: "AuthenticationFailed" ב-Azure
```python
# בדוק connection string
from azure.storage.blob import BlobServiceClient
try:
    blob_service = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )
    blob_service.list_containers()
    print("✅ אימות הצליח!")
except Exception as e:
    print(f"❌ {e}")
```

### בעיה: "Quota exceeded" ב-BigQuery
```python
# הקטן את השאילתה
query = """
SELECT * FROM table
WHERE date >= CURRENT_DATE() - 7  -- רק שבוע אחרון
LIMIT 10000                        -- הגבל שורות
"""

# או השתמש ב-sampling
query = """
SELECT * FROM table
TABLESAMPLE SYSTEM (10 PERCENT)  -- 10% מהנתונים
"""
```

### בעיה: DataFrame גדול מדי לזיכרון
```python
# פתרון 1: Lazy evaluation
lf = pl.scan_parquet('huge.parquet')
result = (
    lf
    .filter(pl.col('year') == 2024)
    .select(['id', 'value'])
    .collect()
)

# פתרון 2: Streaming
for batch in pl.read_parquet_batched('huge.parquet', batch_size=10000):
    process_batch(batch)

# פתרון 3: השתמש בCloud compute
# העבר את העיבוד ל-BigQuery/Snowflake
```

---

## 📌 סיכום - הכי חשוב לזכור

### ✅ DO (תעשה)
1. **השתמש ב-Parquet** - תמיד עדיף על CSV
2. **Lazy evaluation** - לקבצים גדולים
3. **סנן מוקדם** - לפני קריאת הנתונים
4. **משתני סביבה** - לsensitive data
5. **Context managers** - `with` לניהול קבצים
6. **טיפוסי נתונים** - שמור על consistency

### ❌ DON'T (אל תעשה)
1. **אל תשמור credentials בקוד** - NEVER!
2. **אל תקרא SELECT \*** - בחר עמודות
3. **אל תשכח LIMIT** - בשאילתות מבחן
4. **אל תטען הכל לזיכרון** - streaming!
5. **אל תשכח לסגור connections** - memory leaks
6. **אל תעבוד ישירות על production** - backup!

### 🔥 One-liners שימושיים

```python
# קריאה מהירה מS3
df = pl.read_parquet('s3://bucket/file.parquet')

# קריאה עם סינון
df = pl.scan_parquet('s3://bucket/huge.parquet').filter(pl.col('year')==2024).collect()

# שמירה מהירה
import s3fs; fs = s3fs.S3FileSystem()
with fs.open('s3://bucket/out.parquet','wb') as f: df.write_parquet(f)

# BigQuery בשורה אחת
df = pl.from_arrow(bigquery.Client().query("SELECT * FROM table LIMIT 100").result().to_arrow())

# בדיקת גודל
print(f"{df.estimated_size('mb'):.2f} MB")
```

---

## 📚 משאבים מהירים

### לינקים מהירים
- [Polars Docs](https://pola-rs.github.io/polars/)
- [AWS CLI Config](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [Azure Storage Explorer](https://azure.microsoft.com/features/storage-explorer/)
- [GCS Console](https://console.cloud.google.com/storage)
- [BigQuery Sandbox](https://console.cloud.google.com/bigquery) (חינם!)

### Cheat Sheets
- [Polars Cheat Sheet](https://franzdiebold.github.io/polars-cheat-sheet/Polars_cheat_sheet.pdf)
- [AWS S3 CLI](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [SQL for BigQuery](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)

---

<div style="background: #f0f0f0; padding: 20px; border-radius: 10px; text-align: center;">
<h2>🎉 זהו! אתם מוכנים לכבוש את הענן! ☁️</h2>
<p><strong>שמרו את המדריך הזה - תצטרכו אותו! 📌</strong></p>
<p>נוצר עם ❤️ עבור קהילת Polars בישראל 🇮🇱</p>
</div>

---

**גרסה:** 1.0 | **עודכן לאחרונה:** 2024 | **רישיון:** MIT
