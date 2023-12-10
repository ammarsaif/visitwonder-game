import connect_database


connection = connect_database.connect_database()


def insert(table, field, value):
    sql = f"INSERT INTO {table} ({field}) VALUES ({value})"

    cursor = connection.cursor()
    cursor.execute(sql)