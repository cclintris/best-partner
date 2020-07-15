import fetch_Data
import time
import os
import re
import pycode_similarity


def download_zip():
    start = time.time()
    filepath = "../test_data.json"
    Data = fetch_Data.Data(filepath)
    end = time.time()
    print(end - start)


def creat_similarity_dict():
    # d = {'a': 'aaa', 'b': 'bbb'}
    # s = str(d)
    # f = open('../code_similarity.txt', 'w')
    # f.writelines(s)
    # f.close()
    res = {}
    code_path = "../code/res"
    # 储存文件名的list
    file_name_list = os.listdir(code_path)
    # 所有题目号的list
    case_id_list = []
    # 所有用户号的list
    user_id_list = []
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        case_id_list.append(temp[1])
        user_id_list.append(temp[0])
    temp = set(case_id_list)
    case_id_list = list(temp)
    temp = set(user_id_list)
    user_id_list = list(temp)
    for user in user_id_list:
        res[user] = {}
        cases = []
        origin_file = []
        # 找到做了那些题目
        for file in file_name_list:
            if re.match(user, file):
                origin_file.append(file)
                temp_origin = file.split("_")
                cases.append(temp_origin[1])
                res[user][temp_origin[1]] = {}
        for i in range(len(cases)):
            for file in file_name_list:
                # 找到需要比较的file
                if re.match("\\d+_"+cases[i]+"_\\d+", file):
                    temp_comparison = file.split("_")
                    if temp_comparison[0] in res:
                        res[user][cases[i]][temp_comparison[0]] = res[temp_comparison[0]][cases[i]][user]
                    else:
                        code_similarity = pycode_similarity.inspect("../code/res/"+origin_file[i]+"/main.py",
                                                                    "../code/res/"+file+"/main.py")
                        res[user][cases[i]][temp_comparison[0]] = code_similarity
    result = str(res)
    similarity_file = open('../code_similarity.txt', 'w')
    similarity_file.writelines(result)
    similarity_file.close()


def creat_complexity_dict():
    # 数据格式{file_name0: [time, space], file_name1: [time, space].... ,}
    res = {}


if __name__ == "__main__":
    creat_similarity_dict()


