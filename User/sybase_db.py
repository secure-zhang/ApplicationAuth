import pypyodbc
Config = {
    'dsn': '10.0.0.4',
}
cnxn = pypyodbc.connect("DSN=10.0.0.4;UID=kstrader;PWD=kstrader")
cursor =cnxn.cursor()
print(cursor)
# cursor.execute("select * from cust_appropriate_assessment")
# row = cursor.fetchone()



