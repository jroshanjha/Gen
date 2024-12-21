import pymysql

def create_database(db_name):
  try:
    # Connect to MySQL server
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='jroshan@98'
    )
    cursor = conn.cursor()

    # Create database (if not exists)
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    conn.commit()
    print(f"Database '{db_name}' created successfully")
  except pymysql.Error as err:
    print(f"Error creating database: {err}")
  finally:
    conn.close()
    cursor.close()

# Call the function with your desired database name
create_database('infoDB')