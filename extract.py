import sqlite3
import csv
import sys

def export_table_to_csv(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    with open(f"{table_name}.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # Write column headers
        csv_writer.writerows(cursor)

def main(database_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # Export each table to a CSV file
    for table in tables:
        table_name = table[0]
        export_table_to_csv(cursor, table_name)
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py database_file.db")
        sys.exit(1)

    database_file = sys.argv[1]
    main(database_file)