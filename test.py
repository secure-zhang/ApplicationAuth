
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
data = {'name':'冠通期货','pwd':'GTQH0037'}
url = 'http://www.139000.com/send/getfee.asp?'+urlencode(data)
url1 = 'http://www.139000.com/send/gsend.asp?name=冠通期货&pwd=GTQH0037&dst=17635035787&msg=测试'
res = requests.get(url1)
print(res.status_code)
print(res.headers)
print(res.text)