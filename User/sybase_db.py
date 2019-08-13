import pypyodbc

cnxn = pypyodbc.connect("DSN=sybase;UID=kstrader;PWD=kstrader")
cursor =cnxn.cursor()
print(cursor)
# cursor.execute("select * from cust_appropriate_assessment")
# row = cursor.fetchone()


