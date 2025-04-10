# convert_xml_to_db_votes_only.py

import os
import sqlite3
import xml.etree.ElementTree as ET
import time

# === File paths ===
xml_files = {
    "votes": "datasets/Votes.xml"
}
db_file = "stackoverflow.db"

# === Schema for votes table ===
table_schemas = {
    "votes": {
        "columns": [
            ("Id", "INTEGER PRIMARY KEY"),
            ("PostId", "INTEGER"),
            ("VoteTypeId", "INTEGER"),
            ("CreationDate", "TEXT")
        ]
    }
}

# === Connect to SQLite ===
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# === Create table and insert data ===
def create_and_insert_table(table_name, schema, xml_file):
    columns = [col for col, _ in schema]
    col_defs = ", ".join([f"{col} {dtype}" for col, dtype in schema])

    # Create table with proper types (if not exists)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})")
    conn.commit()

    batch_size = 50000
    batch = []
    processed = 0
    inserted = 0
    start_time = time.time()

    # Parse XML
    for event, elem in ET.iterparse(xml_file, events=("start",)):
        if elem.tag == "row":
            row_data = tuple(elem.attrib.get(col, None) for col in columns)
            batch.append(row_data)
            processed += 1

            if len(batch) >= batch_size:
                cursor.executemany(
                    f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})",
                    batch
                )
                conn.commit()
                inserted += len(batch)
                print(f"🧾 Processed: {processed:,} | Inserted: {inserted:,} | Time: {int(time.time() - start_time)}s")
                batch = []

            elem.clear()

    # Insert remaining rows
    if batch:
        cursor.executemany(
            f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})",
            batch
        )
        conn.commit()
        inserted += len(batch)

    print(f"✅ Finished {table_name} | Total processed: {processed:,} | Inserted: {inserted:,}")
    print(f"⏱️ Total time: {int(time.time() - start_time)} seconds.")

# === Turn off FK checks temporarily (optional speed boost) ===
cursor.execute("PRAGMA foreign_keys = OFF;")

# === Process table ===
for table, schema_info in table_schemas.items():
    print(f"📥 Processing {table}...")
    create_and_insert_table(table, schema_info["columns"], xml_files[table])
    print(f"✅ {table} done.")

# === Close connection ===
conn.close()
print("🎉 All done.")
