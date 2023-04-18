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


def test():
    nums = [3, 6, 7, 7, 0]
    n = len(nums)
    flag = 0
    for i in range(1, n + 1):
        for v in nums:
            if v >= i:
                flag += 1
        if flag == i:
            return i
        else:
            flag = 0
            continue
    if flag == 0:
        return -1


if __name__ == '__main__':
    print(test())
