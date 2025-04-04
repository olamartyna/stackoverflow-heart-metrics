# import sqlite3
# import pandas as pd

# users_df = pd.read_xml("datasets/Users.xml")

# conn = sqlite3.connect("stackoverflow.db")
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Users (
#         Id INTEGER PRIMARY KEY,
#         Reputation INTEGER,
#         CreationDate TEXT,
#         DisplayName TEXT,
#         LastAccessDate TEXT,
#         AboutMe TEXT,
#         Views INTEGER,
#         UpVotes INTEGER,
#         DownVotes INTEGER       
#     )
# ''')

# # Insert data into SQLite (batch insert for speed)
# users_df.to_sql('Users', conn, if_exists='replace', index=False, chunksize=10000)

# # Close the connection
# conn.commit()
# conn.close()

# print("Users.xml has been successfully imported into SQLite.")

# import sqlite3
# import xml.etree.ElementTree as ET

# # File paths
# xml_file = "datasets/Users.xml"
# db_file = "stackoverflow.db"

# # Connect to SQLite
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()

# # Create table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Users (
#         Id INTEGER PRIMARY KEY,
#         Reputation INTEGER,
#         CreationDate TEXT,
#         DisplayName TEXT,
#         LastAccessDate TEXT,
#         AboutMe TEXT,
#         Views INTEGER,
#         UpVotes INTEGER,
#         DownVotes INTEGER       
#     )
# ''')

# # Commit table creation
# conn.commit()

# # Parse XML and insert data in chunks
# batch_size = 10000  # Process in chunks of 10,000 rows
# batch = []

# for event, elem in ET.iterparse(xml_file, events=("start",)):
#     if elem.tag == "row":
#         user_data = (
#             int(elem.attrib.get("Id", 0)),
#             int(elem.attrib.get("Reputation", 0)),
#             elem.attrib.get("CreationDate", ""),
#             elem.attrib.get("DisplayName", ""),
#             elem.attrib.get("LastAccessDate", ""),
#             elem.attrib.get("AboutMe", ""),
#             int(elem.attrib.get("Views", 0)),
#             int(elem.attrib.get("UpVotes", 0)),
#             int(elem.attrib.get("DownVotes", 0))
#         )
        
#         batch.append(user_data)

#         # Insert batch into SQLite
#         if len(batch) >= batch_size:
#             cursor.executemany('''
#                 INSERT INTO Users (Id, Reputation, CreationDate, DisplayName, LastAccessDate, AboutMe, Views, UpVotes, DownVotes)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', batch)
#             conn.commit()
#             batch = []  # Clear batch memory
        
#         elem.clear()  # Free up memory

# # Insert remaining batch
# if batch:
#     cursor.executemany('''
#         INSERT INTO Users (Id, Reputation, CreationDate, DisplayName, LastAccessDate, AboutMe, Views, UpVotes, DownVotes)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', batch)
#     conn.commit()

# # Close SQLite connection
# conn.close()

# print("Users.xml has been successfully imported into SQLite.")


# import sqlite3
# import xml.etree.ElementTree as ET

# # File paths
# xml_files = {
#     "Users": "datasets/Users.xml",
#     "Comments": "datasets/Comments.xml",
#     "Posts": "datasets/Posts.xml",
#     "Tags": "datasets/Tags.xml",
#     "Votes": "datasets/Votes.xml"
# }
# db_file = "stackoverflow.db"

# # Connect to SQLite
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()

# # Function to create a table and insert data
# def create_and_insert_table(table_name, columns, xml_file):
#     # Create table
#     cursor.execute(f'''
#         CREATE TABLE IF NOT EXISTS {table_name} ({", ".join([f"{col} TEXT" for col in columns])})
#     ''')
#     conn.commit()

#     # Parse XML and insert data in chunks
#     batch_size = 10000  # Process in chunks of 10,000 rows
#     batch = []

#     for event, elem in ET.iterparse(xml_file, events=("start",)):
#         if elem.tag == "row":
#             row_data = tuple([elem.attrib.get(col, '') for col in columns])
            
#             # Skip rows with duplicate IDs (if primary key constraint fails)
#             try:
#                 batch.append(row_data)
#                 if len(batch) >= batch_size:
#                     cursor.executemany(f'''
#                         INSERT OR IGNORE INTO {table_name} ({", ".join(columns)})
#                         VALUES ({", ".join(["?" for _ in columns])})
#                     ''', batch)
#                     conn.commit()
#                     batch = []  # Clear batch memory
#             except sqlite3.IntegrityError:
#                 continue  # Skip this row if it causes a primary key constraint error
            
#             elem.clear()  # Free up memory

#     # Insert remaining batch
#     if batch:
#         cursor.executemany(f'''
#             INSERT OR IGNORE INTO {table_name} ({", ".join(columns)})
#             VALUES ({", ".join(["?" for _ in columns])})
#         ''', batch)
#         conn.commit()

# # Create and insert Users
# create_and_insert_table("Users", 
#                         ["Id", "Reputation", "CreationDate", "DisplayName", "LastAccessDate", 
#                          "AboutMe", "Views", "UpVotes", "DownVotes"], 
#                         xml_files["Users"])

# # Create and insert Comments
# create_and_insert_table("Comments", 
#                         ["Id", "PostId", "Score", "Text", "CreationDate", "UserId"], 
#                         xml_files["Comments"])

# # Create and insert Posts
# create_and_insert_table("Posts", 
#                         ["Id", "PostTypeId", "AcceptedAnswerId", "CreationDate", "Score", 
#                          "ViewCount", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId", 
#                          "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", 
#                          "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ContentLicense"], 
#                         xml_files["Posts"])

# # Create and insert Tags
# create_and_insert_table("Tags", 
#                         ["Id", "TagName", "Count", "ExcerptPostId", "WikiPostId"], 
#                         xml_files["Tags"])

# # Create and insert Votes
# create_and_insert_table("Votes", 
#                         ["Id", "PostId", "VoteTypeId", "CreationDate"], 
#                         xml_files["Votes"])

# # Close SQLite connection
# conn.close()

# print("✅ All XML files have been successfully imported into SQLite.")

import os
import sqlite3
import xml.etree.ElementTree as ET

# Delete old DB if it exists
if os.path.exists("stackoverflow.db"):
    os.remove("stackoverflow.db")
    print("🗑️ Old database removed.")

# File paths
xml_files = {    
    "comments": "datasets/Comments.xml",
    "posts": "datasets/Posts.xml",
    "tags": "datasets/Tags.xml",
    "users": "datasets/Users.xml",
    "votes": "datasets/Votes.xml"
}
db_file = "stackoverflow.db"

# Table schemas with correct types
table_schemas = {
    "comments": {
        "columns": [
            ("Id", "INTEGER PRIMARY KEY"),
            ("PostId", "INTEGER"),
            ("Score", "INTEGER"),
            ("Text", "TEXT"),
            ("CreationDate", "TEXT"),
            ("UserId", "INTEGER")
        ]
    },
    "posts": {
        "columns": [
            ("Id", "INTEGER PRIMARY KEY"),
            ("PostTypeId", "INTEGER"),
            ("AcceptedAnswerId", "INTEGER"),
            ("CreationDate", "TEXT"),
            ("Score", "INTEGER"),
            ("ViewCount", "INTEGER"),
            ("Body", "TEXT"),
            ("OwnerUserId", "INTEGER"),
            ("OwnerDisplayName", "TEXT"),
            ("LastEditorUserId", "INTEGER"),
            ("LastEditorDisplayName", "TEXT"),
            ("LastEditDate", "TEXT"),
            ("LastActivityDate", "TEXT"),
            ("Title", "TEXT"),
            ("Tags", "TEXT"),
            ("AnswerCount", "INTEGER"),
            ("CommentCount", "INTEGER"),
            ("FavoriteCount", "INTEGER"),
            ("ContentLicense", "TEXT")
        ]
    },
    "tags": {
        "columns": [
            ("Id", "INTEGER PRIMARY KEY"),
            ("TagName", "TEXT"),
            ("Count", "INTEGER"),
            ("ExcerptPostId", "INTEGER"),
            ("WikiPostId", "INTEGER")
        ]
    },    
    "users": {
        "columns": [
            ("Id", "INTEGER PRIMARY KEY"),
            ("Reputation", "INTEGER"),
            ("CreationDate", "TEXT"),
            ("DisplayName", "TEXT"),
            ("LastAccessDate", "TEXT"),
            ("AboutMe", "TEXT"),
            ("Views", "INTEGER"),
            ("UpVotes", "INTEGER"),
            ("DownVotes", "INTEGER")
        ]
    },
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
