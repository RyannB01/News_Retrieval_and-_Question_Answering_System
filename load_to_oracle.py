import pandas as pd
import oracledb

# ===== LOAD EXCEL =====
file_path = r"C:\Users\ryann\.cache\kagglehub\datasets\hgultekin\bbcnewsarchive\versions\1\bbc-news-data.csv"
df = pd.read_csv(file_path, sep="\t")

df = df.head(2000)

print("Loaded:", len(df))


# ===== CONNECT ORACLE =====
conn = oracledb.connect(
    user="system",
    password="root",
    dsn="localhost:1521/XE"
)

cursor = conn.cursor()


# ===== INSERT CATEGORIES =====
categories = df["category"].unique()
cat_map = {}

for i, cat in enumerate(categories, start=1):
    cursor.execute(
        "INSERT INTO categories (id, name) VALUES (:1, :2)",
        (i, cat)
    )
    cat_map[cat] = i


# ===== INSERT ARTICLES =====
for i, row in df.iterrows():
    cursor.execute(
        """INSERT INTO news_articles 
        (id, title, content, category_id, publish_date)
        VALUES (:1, :2, :3, :4, SYSDATE)""",
        (
            i,
            row["title"],
            row["content"],
            cat_map[row["category"]]
        )
    )

conn.commit()

cursor.close()
conn.close()

import os
print(os.path.exists(file_path))

print("✅ Data inserted into Oracle!")
