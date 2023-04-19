# # 获取merid对应merkey
# import eel
# from flask import  request, jsonify, render_template
#
# f
# from app.model.models import MerInfo
#
#


# def getMerkey(id=None):
#     page_data = MerInfo.query.filter_by(id=id).first_or_404()
#     merkey = page_data.mer_key
#     return merkey
#
#
# @admin.route('/test')
# def test():
#     return render_template("test.html")
#
#
# @admin.route("/progress", methods=['GET'])
# def get_progress():
#     if request.method == "GET":
#
#         memberid = request.args.get("memberid")
#         env = request.args.get("env")
#
#         if memberid == "":
#             password = "Error! Please input memberid"
#
#         else:
#             password = env
#         return jsonify({"password": password})
from flask import render_template
from app.admin import admin


@admin.route('/utils/utilMD5', methods=['GET'])
def MD5sign():
    return render_template("admin/utils/util_MD5sign.html")


# @admin.route('/utils/getMD5signAjax', methods=['POST'])
# def getMD5signAjax():
#     print("走到了这里")
#     input_data = request.get_json()
#     input_text = input_data['input']
#     # 这里进行后台处理，比如将文本转为大写
#     output_text = input_text.upper()
#     print(output_text)
#     return jsonify({'output': output_text})

# MD5加密的方法
def MD5encode(source):
    hexs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
            'b', 'c', 'd', 'e', 'f']
    try:
        # 获得MD5摘要算法的 hashlib 对象
        digester = hashlib.md5()
        sbs = source.encode("UTF8")
        # 使用指定的字节更新摘要
        digester.update(sbs)
        rbs = digester.digest()
        # 把密文转换成十六进制的字符串形式
        j = len(rbs)
        result = []
        for i in range(j):
            b = rbs[i]
            result.append(hexs[b >> 4 & 0xf])
            result.append(hexs[b & 0xf])
        return ''.join(result)
    except Exception as e:
        return None