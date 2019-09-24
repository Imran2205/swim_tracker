import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='lrnDatabase',
                                         user='root',
                                         password='imran1996')
    sql_Query = "select Required_Time_ms from pointTable where Name =%s"
    id = ("imran",)
    cursor = connection.cursor(buffered=True)
    cursor.execute(sql_Query, id)
    record = cursor.fetchall()
    # selecting column value into varible
    #value = float(record[0])
    #print("column value: ", value)
    print(record)
except mysql.connector.Error as error:
    print("Failed to get record from database: {}".format(error))
finally:
    # closing database connection.
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")