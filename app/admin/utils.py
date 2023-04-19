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


@admin.route('/util/utilMD5', methods=['GET'])
def MD5sign():
    return render_template("admin/util/util_MD5sign.html")
