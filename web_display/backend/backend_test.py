from flask import Flask, jsonify
app = Flask(__name__)

# solve CORS problem
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

@app.route("/hello")
def hello():
    # file1path = "D:\數據科學基礎\\best-partner\\test\original_case.py"
    # file2path = "D:\數據科學基礎\\best-partner\\test\plagiarize_case.py"
    # code_similarity = pycode_Similarity.inspect(file1path, file2path)
    # return jsonify({"code_similarity": code_similarity})
    return jsonify({"about":"hello world"})

if __name__ == "__main__":
    app.run(debug=True)

