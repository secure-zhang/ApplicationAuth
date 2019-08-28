import pyodbc

# cnxn = pyodbc.connect("DSN=sybase;UID=kstrader;PWD=kstrader")
# cursor =cnxn.cursor()

conn_info = 'DRIVER={Sybase ASE ODBC Driver};DATABASE=ksqhdb;NetworkAddress=10.0.0.3,2048;UID=kstrader;PWD=kstrader'
sybase_conn = pyodbc.connect(conn_info)
cursor =sybase_conn.cursor()
# 查询用户主表判断用户是否存在,并获取手机号
cursor.execute("select mobile from cust_whole where cust_no='%s' and cust_full_name='%s'"%('11001052','李忠龙'))
row = cursor.fetchone()
print(row)

# 查询用户客户类
# cursor.execute("select cust_class from cust_basic where cust_no='%s'"%('11001052'))
# row = cursor.fetchone()
# print(row)

# 查询用户评级
# cursor.execute("select assessment_risk_level from cust_appropriate_assessment where cust_no='%s'"%('11001052'))
# row = cursor.fetchone()
# print(row)




