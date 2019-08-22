
# 文件名称随机
# import uuid
#
# uuid_str = uuid.uuid4()
# tmp_file_name = 'img-%s.png' % uuid_str
# print(tmp_file_name)

# 发送验证码

import requests
from urllib.parse import urlencode

#
url = 'http://www.139000.com/send/gsend.asp?name=%b9%da%cd%a8%c6%da%bb%f5&pwd=gtqh0037&dst={dst}&msg={msg}'.format(dst='17635035787',msg='hello')
print(url)
res = requests.get(url)
print(res.status_code)
print(res.headers)
print(res.text)