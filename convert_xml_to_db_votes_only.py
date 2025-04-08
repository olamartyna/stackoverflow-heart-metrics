# When last table - votes - was being converted, I had to interrupt
# So now I am going to add remaining rows for votes:

import os
import sqlite3
import xml.etree.ElementTree as ET


# File paths
xml_files = {    
    "votes": "datasets/Votes.xml"
}
db_file = "stackoverflow.db"

# I am running only votes table
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

# Connect to SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to create a table and insert data
def create_and_insert_table(table_name, schema, xml_file):
    columns = [col for col, _ in schema]
    col_defs = ", ".join([f"{col} {dtype}" for col, dtype in schema])

    # Create table with proper types
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})")
    conn.commit()

    # Parse XML and insert data in chunks
    batch_size = 10000
    batch = []

    for event, elem in ET.iterparse(xml_file, events=("start",)):
        if elem.tag == "row":
            row_data = tuple(elem.attrib.get(col, None) for col in columns)
            batch.append(row_data)

            if len(batch) >= batch_size:
                cursor.executemany(
                    f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})",
                    batch
                )
                conn.commit()
                batch = []

            elem.clear()

    # Insert remaining
    if batch:
        cursor.executemany(
            f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})",
            batch
        )
        conn.commit()

# Clear old DB (optional, or delete manually before running this)
cursor.execute("PRAGMA foreign_keys = OFF;")  # Disable FK for faster insert

# Loop through all tables and run processing
for table, schema_info in table_schemas.items():
    print(f"📥 Processing {table}...")
    create_and_insert_table(table, schema_info["columns"], xml_files[table])
    print(f"✅ {table} done.")

# Close
conn.close()
print("🎉 All XML files successfully imported into SQLite with proper schema.")
