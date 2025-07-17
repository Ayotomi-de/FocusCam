import mysql.connector

try:
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
       host='localhost',
       user='root',
       password='', 
       database='focuscam',
       charset='utf8mb4'
    )
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("Connection successful!")
    print("Available tables:")
    for table in tables:
       print(f"- {table[0]}")
    
except mysql.connector.Error as err:
    print(f"Database Error: {err}")
    
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

