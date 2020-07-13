import sys
sys.path.insert(0, '../../src/code_similarity')
import pycode_similarity

from flask import Flask, jsonify
app = Flask(__name__)

# solve CORS problem
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

@app.route("/report")
def report():
    # file1path = "D:\數據科學基礎\\best-partner\\test\original_case.py"
    # file2path = "D:\數據科學基礎\\best-partner\\test\plagiarize_case.py"
    # code_similarity = pycode_similarity.inspect(file1path, file2path)
    # return jsonify({"code_similarity": code_similarity})
    report = {
        'student_name' : '林希澄',
        'student_id' : '181250083',
        'code_similarity' : 80,
        'code_complexity' : 'O(n)',
        'overall_access' : '菜鸡一个'
    }
    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)

