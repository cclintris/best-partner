import fetch_Data
import time
import os
import re
import pycode_similarity
import check_is_py
import shutil


def download_zip():
    start = time.time()
    filepath = "../test_data.json"
    Data = fetch_Data.Data(filepath)
    end = time.time()
    print(end - start)


def create_similarity_dict():
    # d = {'a': 'aaa', 'b': 'bbb'}
    # s = str(d)
    # f = open('../code_similarity.txt', 'w')
    # f.writelines(s)
    # f.close()
    res = {}
    result = str(res)
    similarity_file = open('../code_similarity.txt', 'w')
    similarity_file.writelines(result)
    similarity_file.close()
    code_path = "C:/Python/BigCode/code/res"
    # 储存文件名的list
    file_name_list = os.listdir(code_path)
    # 所有题目号的list
    case_id_list = []
    # 所有用户号的list
    user_id_list = []
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        case_id_list.append(temp[1])
        if temp[0] not in user_id_list:
            user_id_list.append(temp[0])
    print(user_id_list)
#     for user in user_id_list:
#         res[user] = {}
#         cases = []
#         origin_file = []
#         # 找到做了那些题目
#         for file in file_name_list:
#             if re.match(user, file):
#                 origin_file.append(file)
#                 temp_origin = file.split("_")
#                 cases.append(temp_origin[1])
#                 res[user][temp_origin[1]] = {}
#         for i in range(len(cases)):
#             for file in file_name_list:
#                 # 找到需要比较的file
#                 if re.match("\\d+_"+cases[i]+"_\\d+", file):
#                     temp_comparison = file.split("_")
#                     # if origin_file[i] != "16304_2573_306670" or file != "8318_2573_318712":
#                     #     if x == 0:
#                     #         continue
#                     # else:
#                     #     x = 1
#                     if temp_comparison[0] == user:
#                         continue
#                     if not check_is_py.is_python("C:/Python/BigCode/code/res/" + origin_file[i] + "/main.py"):
#                         res[user][cases[i]][temp_comparison[0]] = "one of them is not python file"
#                         continue
#                     if not check_is_py.is_python("C:/Python/BigCode/code/res/"+file+"/main.py"):
#                         res[user][cases[i]][temp_comparison[0]] = "one of them is not python file"
#                         continue
#                     if temp_comparison[0] in res:
#                         res[user][cases[i]][temp_comparison[0]] = res[temp_comparison[0]][cases[i]][user]
#                     else:
#                         code_similarity = pycode_similarity.inspect("C:/Python/BigCode/code/res/"+origin_file[i]+"/main.py",
#                                                                     "C:/Python/BigCode/code/res/"+file+"/main.py")
#                         res[user][cases[i]][temp_comparison[0]] = code_similarity
#         os.remove('../code_similarity.txt')
#         result = str(res)
#         similarity_file = open('../code_similarity.txt', 'w')
#         similarity_file.writelines(result)
#         similarity_file.close()
#
#
# def create_complexity_dict():
#     # 数据格式{file_name0: [time, space], file_name1: [time, space].... ,}
#     res = {}
#     code_path = "C:\\Python\\BigCode\\code\\res"
#     # 储存文件名的list
#     file_name_list = os.listdir(code_path)
#     # print(file_name_list)
#     for file in file_name_list:
#         print(file)
#         res[file] = []
#         time_str = time_complexity.TimeChecker("C:/Python/BigCode/code/res/" + file + "/main.py").deal_with_file()
#         space_str = space_complexity.SpaceChecker("C:/Python/BigCode/code/res/" + file + "/main.py").deal_with_file()
#         res[file].append(time_str)
#         res[file].append(space_str)
#         print(res)
#     print(res)
#     result = str(res)
#     complexity_file = open('../code_complexity.txt', 'w')
#     complexity_file.writelines(result)
#     complexity_file.close()


if __name__ == "__main__":
    # test = "../../test/space_comp_test.py"
    # print(space_complexity.SpaceChecker("../test/space_comp_test.py").deal_with_file())
    # print(time_complexity.TimeChecker("../test/time_comp_test.py").deal_with_file())
    # create_complexity_dict()
    create_similarity_dict()
