import pycode_Similarity

file1path = "D:\數據科學基礎\\best-partner\\test\original_case.py"
file2path = "D:\數據科學基礎\\best-partner\\test\plagiarize_case.py"

if __name__ == '__main__':
    code_Similarity = pycode_Similarity.inspect(file1path, file2path)
    print("code_similarity:" + str(code_Similarity))
