import json
import urllib.request
import os
import shutil
import zipfile


class Data:

    def __init__(self, filepath: str):
        f = open(filepath, 'r', encoding='utf-8')
        res = f.read()
        data = json.loads(res)
        f.close()
        # 如果不存在，创建code
        if not os.path.exists("../code"):
            os.mkdir("../code")
        # 如果不存在，创建zip，用以存放zip文件
        if not os.path.exists("../code/zip"):
            os.mkdir("../code/zip")
        # 如果不存在，创建temp
        if not os.path.exists("../code/temp"):
            os.mkdir("../code/temp")
        destination = "../code/"
        users = list(data)
        # users = ["3544"]
        for user in users:
            for case in range(len(data[user]["cases"])):
                index = len(data[user]["cases"][case]["upload_records"]) - 1
                if index == -1:
                    continue
                name = (user + "_"
                        + data[user]["cases"][case]["case_id"] + "_"
                        + str(data[user]["cases"][case]["upload_records"][index]["upload_id"]))
                print(name)
                # 数据集似乎此处有错
                if name == "60765_2528_284171":
                    case = case + 1
                    continue
                url = data[user]["cases"][case]["upload_records"][index]["code_url"]
                urllib.request.urlretrieve(url, destination + "zip/" + name + ".zip")
                z_file = zipfile.ZipFile(destination + "zip/" + name + ".zip")
                for z in z_file.namelist():
                    z_file.extract(z, destination + "temp/" + name)
                    zz = zipfile.ZipFile(destination + "temp/" + name + "/" + z)
                    for zi in zz.namelist():
                        zz.extract(zi, destination + "res/" + name)
                    zz.close()
                z_file.close()
        shutil.rmtree('../code/temp')

