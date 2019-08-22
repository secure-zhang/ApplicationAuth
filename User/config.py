import pypyodbc


class Sybase:
    def __init__(self):
        self.con = pypyodbc.connect("DSN=sybase;UID=kstrader;PWD=kstrader")

    def cust_whole(self,cust_no,cust_full_name):
        # 查询用户主表判断用户是否存在,并获取手机号
        cur = self.con.cursor()
        cur.execute("select mobile from cust_whole where cust_no='%s' and cust_full_name='%s'" % (cust_no,cust_full_name))
        result = cur.fetchone()
        cur.close()
        if result:
            if result[0]:
                return result[0].strip()
    def cust_name(self,cust_no):
        # 查询用户主表判断用户是否存在,并获取手机号
        cur = self.con.cursor()
        cur.execute("select cust_full_name from cust_whole where cust_no='%s' " % (cust_no))
        result = cur.fetchone()
        cur.close()
        if result:
            if result[0]:
                return result[0].strip()

    def cust_basic(self,cust_no):
        # 查询用户并获取客户类
        cur = self.con.cursor()
        cur.execute("select cust_class from cust_basic where cust_no='%s'"%(cust_no))
        result = cur.fetchone()
        cur.close()
        if result:
            if result[0]:
                return result[0].strip()[:2]

    def cust_appropriate_assessment(self,cust_no):
        # 查询用户并获取评级
        cur = self.con.cursor()
        cur.execute("select assessment_risk_level from cust_appropriate_assessment where cust_no='%s'"%(cust_no))
        result = cur.fetchone()
        cur.close()
        if result:
            if result[0]:
                return result[0].strip()

if __name__ == '__main__':
    s = Sybase()
    name = s.cust_name('11013156')
    phone = s.cust_whole('11013156',name)
    userClass = s.cust_basic('11013156')
    userGrade = s.cust_appropriate_assessment('11013156')
    print(name,phone, userClass, userGrade)

