import json
import random
import urllib.request
import os
import shutil
import zipfile


def a(c):
    isoc = random.randint(0, 1)
    if isoc == 0:
        return False
    else:
        return True


f = open("../sample.json", 'r', encoding='utf-8')
res = f.read()
data = json.loads(res)
f.close()
if not os.path.exists("../code"):
    os.mkdir("../code")
destination = "../code/"

user_score = {}
case_type = {}
users = list(data)
for user in users:
    s = {}
    for case in range(len(data[user]["cases"])):
        name = []
        for i in range(len(data[user]["cases"][case]["upload_records"])):
            name.append(str(i))
        score = []
        for i in range(len(data[user]["cases"][case]["upload_records"])):
            score.append(data[user]["cases"][case]["upload_records"][i]["score"])
        for upload in range(len(data[user]["cases"][case]["upload_records"])):  # 每一次提交
            url = data[user]["cases"][case]["upload_records"][upload]["code_url"]
            urllib.request.urlretrieve(url, destination + name[upload] + ".zip")
            zFile = zipfile.ZipFile(destination + name[upload] + ".zip")
            for z in zFile.namelist():
                zFile.extract(z, destination + name[upload])
                zz = zipfile.ZipFile(destination + name[upload] + "/" + z)
                for zi in zz.namelist():
                    zz.extract(zi, destination + "res/" + name[upload])
                zz.close()
            zFile.close()
            transferPath = destination + "res/" + name[upload] + "/main.py"  # 传递的路径
            code = open(destination + "res/" + name[upload] + "/main.py", 'r', encoding='utf-8')
            c = code.read()  # 整个代码-字符串类型
            code.close()
            x = a(c)
            # 当x是true时，说明这份代码面向用例了, 此时认为这次提交的分数应为0分
            if x:
                score[upload] = 0.0
            # 清空文件夹
            shutil.rmtree('../code')
            os.mkdir('../code')
        final_score = max(score)
        s[data[user]["cases"][case]["case_id"]] = final_score
        case_type[data[user]["cases"][case]["case_id"]] = data[user]["cases"][case]["case_type"]
    user_score[user] = s
