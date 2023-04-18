# import requests
#
# response = requests.request('GET', 'http://127.0.0.1:8000/')
# print(response.status_code)  # 响应状态码
# headers = {
#     'content-type': "application/json;charset=UTF-8",
#     'dahai-access-token': 'SQwNSp',
#     'x-trailer-biz-product-line': 'k12'
# }
# # get请求
# url1 = 'https://work/ehr/get?' + 'work_no=' + w_id + '&ts=123'
# re1 = requests.get(url1, headers=headers, verify=False)
#
# result = re1.json()  # 转化
# # 返回值：{"error_code":0,"message":"ok","result":{"mobile":"123","mobile_code":86,"real_name":"杨阳","work_email":"102@tal.com","work_no":"288533"}}
# mobile = result['result']['mobile']  # 或者返回值
# work_email = result['result']['work_email']
# real_name = result['result']['real_name']
# print(mobile, work_email, real_name)
# ————————————————
# 版权声明：本文为CSDN博主「xiangrikui1155」的原创文章，遵循CC
# 4.0
# BY - SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https: // blog.csdn.net / xiangrikui1155 / article / details / 118164182
# if __name__ == '__main__':
#     print('test')