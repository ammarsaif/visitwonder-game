import connect_database
from queries.insert import connection


def update_location(new_location, user_email):


    try:
        connection = connect_database.connect_database()


        if connection.is_connected():
            cursor = connection.cursor()

            update_query = "UPDATE user SET location = %s WHERE email = %s"

            cursor.execute(update_query, (new_location, user_email))
            connection.commit()

            cursor.close()

    except :
        print(f"Error in update location")

    finally:
        if connection.is_connected():
            connection.close()


def update(table, field_and_value, where, values=None):
    sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

    cursor = connection.cursor()

    # Using parameterized queries to prevent SQL injection
    if values:
        cursor.execute(sql, values)
    else:
        cursor.execute(sql)

    connection.commit()
    cursor.close()

def update_difficulty(difficulty, player_email):
    table = 'user'
    field_and_value = f"co2_budget = {difficulty}"
    where = f"email = '{player_email}'"

    sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

    cursor = connection.cursor()

    # Using parameterized queries to prevent SQL injection
    cursor.execute(sql)

    connection.commit()
    cursor.close()


"""
def update(table, field_and_value, where):
    sql = f"UPDATE {table} SET {field_and_value} WHERE {where}"

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()

"""