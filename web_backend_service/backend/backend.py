#import pycode_similarity
import time
from decimal import Decimal
from flask import Flask, jsonify
app = Flask(__name__)

# solve CORS problem
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

@app.route("/report/<student_id>/<ques_id>")
def report(student_id, ques_id):
    # print(student_id)
    # print(ques_id)
    if student_id == "student_id=" or ques_id == "ques_id=":
        error = {
            'message' : 'Invalid Input'
        }
        return jsonify(error)
    else:
        student_id = student_id.split("=")[1]
        ques_id = ques_id.split("=")[1]
        file = open("../test_data.json", 'r', encoding="utf-8")
        data = eval(file.read())
        file.close()
        ques_type = ''
        otherStyleTime = ''
        flag = False
        if student_id not in data:
            report = {
                'message' : 'Invalid Input'
            }
            return jsonify(report)
        for case in range(len(data[student_id]["cases"])):
            if data[student_id]["cases"][case]["case_id"] == ques_id:
                flag = True
                ques_type = data[student_id]["cases"][case]["case_type"]
                if len(data[student_id]["cases"][case]["upload_records"]) != 0:
                    upload_time = data[student_id]["cases"][case]["upload_records"][len(data[student_id]["cases"][case]["upload_records"])-1]["upload_time"]
                    timeStamp = float(upload_time / 1000)
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
                else:
                    report = {
                        'message': 'Valid Input',
                        'ques_type': ques_type,
                        'upload_time': "Null",
                        'code_similarity': 0,
                        'code_time_complexity': 'Null',
                        'code_space_complexity': 'Null',
                        'is_indent_using_one': 'Null',
                        'is_space_nums_multiple_of_four': 'Null',
                        'is_within_len_range': 'Null',
                        'is_not_trailing_space': 'Null',
                        'is_space_around_operator': 'Null',
                        'is_not_space_around_operator_in_def': 'Null',
                        'is_using_one_quotation': 'Null',
                        'is_not_blank_line_beginning': 'Null',
                        'is_not_inline_comments': 'Null',
                        'is_space_after_pound': 'Null',
                        'is_blank_line_after_import': 'Null',
                        'is_blank_line_before_class': 'Null',
                        'is_blank_line_before_def': 'Null',
                        'is_not_diff_package_in_the_same_line': 'Null',
                        'is_import_before_from': 'Null',
                        'is_not_blank_between_import': 'Null',
                        'is_using_meaningful_name': 'Null',
                        'code_style_score': 'Null',
                    }
                    return jsonify(report)
        if not flag:
            report = {
                'message': 'Invalid Input'
            }
            return jsonify(report)
        file = open("../code_similarity.txt", 'r')
        data = eval(file.read())
        file.close()
        similarity = list(data[student_id][ques_id].values())
        doubt = 0
        for index in range(len(similarity)):
            if similarity[index] == "one of them is not python file" or index == "E":
                continue
            else:
                if int(similarity[index]) >= 70:
                    doubt = doubt + 1
        code_similarity = round(doubt/len(similarity)*100, 2)
        file = open("../code_complexity.txt", 'r')
        data = eval(file.read())
        file.close()
        file_name_list = list(data.keys())
        key = ''
        for file in file_name_list:
            if student_id in file and ques_id in file:
                key = file
                break
        code_time_complexity = "O(" + data[key][0] + ")"
        code_space_complexity = "O(" + data[key][1] + ")"
        file = open("../code_style.txt", 'r')
        data = eval(file.read())
        file.close()
        style_num = 0
        if data[student_id][ques_id]["is_indent_using_one"]:
            data[student_id][ques_id]["is_indent_using_one"] = "是"
        else:
            data[student_id][ques_id]["is_indent_using_one"] = "否"
            style_num = style_num + 1
        is_indent_using_one = data[student_id][ques_id]["is_indent_using_one"]
        if data[student_id][ques_id]["is_space_nums_multiple_of_four"]:
            data[student_id][ques_id]["is_space_nums_multiple_of_four"] = "是"
        else:
            data[student_id][ques_id]["is_space_nums_multiple_of_four"] = "否"
            style_num = style_num + 1
        is_space_nums_multiple_of_four = data[student_id][ques_id]["is_space_nums_multiple_of_four"]
        if data[student_id][ques_id]["is_within_len_range"]:
            data[student_id][ques_id]["is_within_len_range"] = "是"
        else:
            data[student_id][ques_id]["is_within_len_range"] = "否"
            style_num = style_num + 1
        is_within_len_range = data[student_id][ques_id]["is_within_len_range"]
        if data[student_id][ques_id]["is_not_trailing_space"]:
            data[student_id][ques_id]["is_not_trailing_space"] = "是"
        else:
            data[student_id][ques_id]["is_not_trailing_space"] = "否"
            style_num = style_num + 1
        is_not_trailing_space = data[student_id][ques_id]["is_not_trailing_space"]
        if data[student_id][ques_id]["is_space_around_operator"]:
            data[student_id][ques_id]["is_space_around_operator"] = "是"
        else:
            data[student_id][ques_id]["is_space_around_operator"] = "否"
            style_num = style_num + 1
        is_space_around_operator = data[student_id][ques_id]["is_space_around_operator"]
        if data[student_id][ques_id]["is_not_space_around_operator_in_def"]:
            data[student_id][ques_id]["is_not_space_around_operator_in_def"] = "是"
        else:
            data[student_id][ques_id]["is_not_space_around_operator_in_def"] = "否"
            style_num = style_num + 1
        is_not_space_around_operator_in_def = data[student_id][ques_id]["is_not_space_around_operator_in_def"]
        if data[student_id][ques_id]["is_using_one_quotation"]:
            data[student_id][ques_id]["is_using_one_quotation"] = "是"
        else:
            data[student_id][ques_id]["is_using_one_quotation"] = "否"
            style_num = style_num + 1
        is_using_one_quotation = data[student_id][ques_id]["is_using_one_quotation"]
        if data[student_id][ques_id]["is_not_blank_line_beginning"]:
            data[student_id][ques_id]["is_not_blank_line_beginning"] = "是"
        else:
            data[student_id][ques_id]["is_not_blank_line_beginning"] = "否"
            style_num = style_num + 1
        is_not_blank_line_beginning = data[student_id][ques_id]["is_not_blank_line_beginning"]
        if data[student_id][ques_id]["is_not_inline_comments"]:
            data[student_id][ques_id]["is_not_inline_comments"] = "是"
        else:
            data[student_id][ques_id]["is_not_inline_comments"] = "否"
            style_num = style_num + 1
        is_not_inline_comments = data[student_id][ques_id]["is_not_inline_comments"]
        if data[student_id][ques_id]["is_space_after_pound"]:
            data[student_id][ques_id]["is_space_after_pound"] = "是"
        else:
            data[student_id][ques_id]["is_space_after_pound"] = "否"
            style_num = style_num + 1
        is_space_after_pound = data[student_id][ques_id]["is_space_after_pound"]
        if data[student_id][ques_id]["is_blank_line_after_import"]:
            data[student_id][ques_id]["is_blank_line_after_import"] = "是"
        else:
            data[student_id][ques_id]["is_blank_line_after_import"] = "否"
            style_num = style_num + 1
        is_blank_line_after_import = data[student_id][ques_id]["is_blank_line_after_import"]
        if data[student_id][ques_id]["is_blank_line_before_class"]:
            data[student_id][ques_id]["is_blank_line_before_class"] = "是"
        else:
            data[student_id][ques_id]["is_blank_line_before_class"] = "否"
            style_num = style_num + 1
        is_blank_line_before_class = data[student_id][ques_id]["is_blank_line_before_class"]
        if data[student_id][ques_id]["is_blank_line_before_def"]:
            data[student_id][ques_id]["is_blank_line_before_def"] = "是"
        else:
            data[student_id][ques_id]["is_blank_line_before_def"] = "否"
            style_num = style_num + 1
        is_blank_line_before_def = data[student_id][ques_id]["is_blank_line_before_def"]
        if data[student_id][ques_id]["is_not_diff_package_in_the_same_line"]:
            data[student_id][ques_id]["is_not_diff_package_in_the_same_line"] = "是"
        else:
            data[student_id][ques_id]["is_not_diff_package_in_the_same_line"] = "否"
            style_num = style_num + 1
        is_not_diff_package_in_the_same_line = data[student_id][ques_id]["is_not_diff_package_in_the_same_line"]
        if data[student_id][ques_id]["is_import_before_from"]:
            data[student_id][ques_id]["is_import_before_from"] = "是"
        else:
            data[student_id][ques_id]["is_import_before_from"] = "否"
            style_num = style_num + 1
        is_import_before_from = data[student_id][ques_id]["is_import_before_from"]
        if data[student_id][ques_id]["is_not_blank_between_import"]:
            data[student_id][ques_id]["is_not_blank_between_import"] = "是"
        else:
            data[student_id][ques_id]["is_not_blank_between_import"] = "否"
            style_num = style_num + 1
        is_not_blank_between_import = data[student_id][ques_id]["is_not_blank_between_import"]
        if data[student_id][ques_id]["is_using_meaningful_name"]:
            data[student_id][ques_id]["is_using_meaningful_name"] = "是"
        else:
            data[student_id][ques_id]["is_using_meaningful_name"] = "否"
            style_num = style_num + 1
        is_using_meaningful_name = data[student_id][ques_id]["is_using_meaningful_name"]
        code_style_score = round((17 - style_num)/17 * 100, 2)
        report = {
            'message' : 'Valid Input',
            'ques_type': ques_type,
            'upload_time': otherStyleTime,
            'code_similarity': code_similarity,
            'code_time_complexity': code_time_complexity,
            'code_space_complexity': code_space_complexity,
            'is_indent_using_one': is_indent_using_one,
            'is_space_nums_multiple_of_four': is_space_nums_multiple_of_four,
            'is_within_len_range': is_within_len_range,
            'is_not_trailing_space': is_not_trailing_space,
            'is_space_around_operator': is_space_around_operator,
            'is_not_space_around_operator_in_def': is_not_space_around_operator_in_def,
            'is_using_one_quotation': is_using_one_quotation,
            'is_not_blank_line_beginning': is_not_blank_line_beginning,
            'is_not_inline_comments': is_not_inline_comments,
            'is_space_after_pound': is_space_after_pound,
            'is_blank_line_after_import': is_blank_line_after_import,
            'is_blank_line_before_class': is_blank_line_before_class,
            'is_blank_line_before_def': is_blank_line_before_def,
            'is_not_diff_package_in_the_same_line': is_not_diff_package_in_the_same_line,
            'is_import_before_from': is_import_before_from,
            'is_not_blank_between_import': is_not_blank_between_import,
            'is_using_meaningful_name': is_using_meaningful_name,
            'code_style_score': code_style_score,
        }
        return jsonify(report)

@app.route("/Echartreport/<student_id>")
def Echartreport(student_id):
    # print(student_id)
    overall_student_value = []
    specific_student_value = []

    if student_id == "student_id=":
        error = {
            'message' : 'Invalid Input'
        }
        return jsonify(error)
    else:
        '''
        顺序如下：
        1. 代码估计相似度
        2. 代码时间复杂度
        3. 代码风格水平
        4. 代码空间复杂度
        '''
        overall_student_value.append(220)
        overall_student_value.append(410)
        overall_student_value.append(398)
        overall_student_value.append(400)

        specific_student_value.append(120)
        specific_student_value.append(290)
        specific_student_value.append(287)
        specific_student_value.append(300)
        Echartreport = {
            'message' : 'Valid Input',
            'overall_student_value' : overall_student_value,
            'specific_student_value' : specific_student_value,
        }
        return jsonify(Echartreport)


if __name__ == "__main__":
    app.run(debug=True)

