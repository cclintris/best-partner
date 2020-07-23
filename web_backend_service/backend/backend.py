#import pycode_similarity
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
        report = {
            'message' : 'Valid Input',
            'ques_type': '排序',
            'upload_time': 'yyyy-mm-dd',
            'code_similarity': 80,
            'code_time_complexity': 'O(n)',
            'code_space_complexity': 'O(nlog(n))',
            'overall_access': '菜鸡一个',
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
        specific_student_value.append(320)
        Echartreport = {
            'message' : 'Valid Input',
            'overall_student_value' : overall_student_value,
            'specific_student_value' : specific_student_value,
        }
        return jsonify(Echartreport)


if __name__ == "__main__":
    app.run(debug=True)

