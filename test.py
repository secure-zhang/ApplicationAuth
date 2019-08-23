
# 文件名称随机
# import uuid
#
# uuid_str = uuid.uuid4()
# tmp_file_name = 'img-%s.png' % uuid_str
# print(tmp_file_name)

# # 发送验证码
# import requests,random
#
# code = random.randint(0, 999999)
#
# code_msg = ('手机验证码:%s,1分钟内有效' % code)
# url = 'http://www.139000.com/send/gsend.asp?name=%b9%da%cd%a8%c6%da%bb%f5&pwd=gtqh0037&dst={dst}&msg={msg}'.format(dst='17635035787',msg=code_msg)
#
# print(url)
# res = requests.get(url)
# print(res.status_code)
# print(res.headers)
# print(res.content.decode('gbk'))

# 验证手机号
#
# phone = '+861117635000000'
#
# import re
#
# re_phone = re.compile('(^1(3[\d])|(47|45)|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}$')  # 创建一个正则表达
# # r是转义，手机号都是1开头^1，后面排列的是第二位和第三位，
# # 后面还有8位0-9的任意整数\d{8}，并且以此结尾$，
# s = re_phone.search(phone)
# ret = re.match(r"^1[35678]\d{9}$", phone)
# if s:
#     print(s.group())
#     print(s)
# else:
#     print('不是正确手机号，请重新输入')


# 操作redis
# import redis,time
#
# class RedisHelper(object):
#     def __init__(self):
#         self.con = redis.Redis(host='127.0.0.1',port=6379)#连接Redis
#
#     def add_code(self,userid,code):#定义发布方法
#         a = self.con.set(userid, code, 10)
#         print(a)
#         return True
#
#     def delete_code(self,userid):#定义订阅方法
#         a = self.con.delete(userid)
#         print(a)
#         return True
#     def get_code(self,userid):
#         ret = self.con.get(userid)
#         print(ret)
#         if ret:
#             return ret.decode('utf-8')
#
#
# if __name__ == '__main__':
#     r = RedisHelper()
#     r.add_code('11111','123456')
#     r.get_code('11111')
#     time.sleep(10)
#     r.get_code('11111')
#     r.delete_code('11111')

from _datetime import datetime
print(datetime.now().strftime('%Y-%m-%d %H:%I:%S'))
print(type(datetime.now().strftime('%Y-%m-%d %H:%I:%S')))






