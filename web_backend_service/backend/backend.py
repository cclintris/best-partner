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
    if student_id == "student_id=":
        error = {
            'message' : 'Invalid Input'
        }
        return jsonify(error)
    else:
        Echartreport = {
            'message' : 'Valid Input',
            'overall_student_value' : [220, 410, 398, 400],
            'specific_student_value' : [120, 290, 287, 320],
        }
        return jsonify(Echartreport)


if __name__ == "__main__":
    app.run(debug=True)

