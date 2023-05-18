import openai
import os

# # 设置您的API密钥
# # openai.api_key = os.environ["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"]
# openai.api_key = "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"
#
#
# # 设置API端点
# endpoint = "https://api.openai.com"
#
# # 调用API
# prompt = "python实现一个http请求的例子"
# # model = "text-davinci-002"
# model = "gpt-3.5-turbo"
# response = openai.Completion.create(
#     engine=model,
#     prompt=prompt,
#     max_tokens=50
# )
#
# # 输出结果
# print(response.choices[0].text)
# # print(response)
from app.model.admin import Admin


def test():
    data = dict()
    data["account"] = '77'
    admin7 = Admin.query.filter_by(name=data["account"]).first()
    print(admin7)
    flag = admin7.check_pwd(Admin, '77')
    print(flag)


if __name__ == '__main__':
    test()
