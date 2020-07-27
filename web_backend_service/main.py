import fetch_Data
import time
import os
import re
import pycode_similarity
import check_is_py
import time_complexity
import space_complexity
import code_style
import comp_str
from decimal import Decimal


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
        if temp[0] not in user_id_list:
            user_id_list.append(temp[0])
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
                    # if origin_file[i] != "16304_2573_306670" or file != "8318_2573_318712":
                    #     if x == 0:
                    #         continue
                    # else:
                    #     x = 1
                    if temp_comparison[0] == user:
                        continue
                    if not check_is_py.is_python("../code/res/" + origin_file[i] + "/properties"):
                        res[user][cases[i]][temp_comparison[0]] = "one of them is not python file"
                        continue
                    if not check_is_py.is_python("../code/res/"+file+"/properties"):
                        res[user][cases[i]][temp_comparison[0]] = "one of them is not python file"
                        continue
                    if temp_comparison[0] in res:
                        res[user][cases[i]][temp_comparison[0]] = res[temp_comparison[0]][cases[i]][user]
                    else:
                        code_similarity = pycode_similarity.inspect("../code/res/"+origin_file[i]+"/main.py",
                                                                    "../code/res/"+file+"/main.py")
                        res[user][cases[i]][temp_comparison[0]] = code_similarity
        os.remove('../code_similarity.txt')
        result = str(res)
        similarity_file = open('../code_similarity.txt', 'w')
        similarity_file.writelines(result)
        similarity_file.close()


def create_complexity_dict():
    # 数据格式{file_name0: [time, space], file_name1: [time, space].... ,}
    res = {}
    code_path = "../code/res"
    # 储存文件名的list
    file_name_list = os.listdir(code_path)
    # print(file_name_list)
    for file in file_name_list:
        print(file)
        res[file] = []
        time_str = time_complexity.TimeChecker("../code/res/" + file + "/main.py").deal_with_file()
        space_str = space_complexity.SpaceChecker("../code/res/" + file + "/main.py").deal_with_file()
        res[file].append(time_str)
        res[file].append(space_str)
    result = str(res)
    complexity_file = open('../code_complexity.txt', 'w')
    complexity_file.writelines(result)
    complexity_file.close()


def create_style_dict():
    code_path = "../code/res"
    res = {}
    file_name_list = os.listdir(code_path)
    for file in file_name_list:
        print(file)
        style = code_style.Checker("../code/res/" + file + "/main.py")
        user_id = file.split("_")[0]
        if user_id not in res:
            res[user_id] = {}
        case_id = file.split("_")[1]
        if not check_is_py.is_python("../code/res/" + file + "/properties"):
            res[user_id][case_id] = "It's not a python file."
        res[user_id][case_id] = {}
        res[user_id][case_id]["is_indent_using_one"] = style.is_indent_using_one
        res[user_id][case_id]["is_space_nums_multiple_of_four"] = style.is_space_nums_multiple_of_four
        res[user_id][case_id]["is_within_len_range"] = style.is_within_len_range
        res[user_id][case_id]["is_not_trailing_space"] = style.is_not_trailing_space
        res[user_id][case_id]["is_space_around_operator"] = style.is_space_around_operator
        res[user_id][case_id]["is_not_space_around_operator_in_def"] = style.is_not_space_around_operator_in_def
        res[user_id][case_id]["is_using_one_quotation"] = style.is_using_one_quotation
        res[user_id][case_id]["is_not_blank_line_beginning"] = style.is_not_blank_line_beginning
        res[user_id][case_id]["is_not_inline_comments"] = style.is_not_inline_comments
        res[user_id][case_id]["is_space_after_pound"] = style.is_space_after_pound
        res[user_id][case_id]["is_blank_line_after_import"] = style.is_blank_line_after_import
        res[user_id][case_id]["is_blank_line_before_class"] = style.is_blank_line_before_class
        res[user_id][case_id]["is_blank_line_before_def"] = style.is_blank_line_before_def
        res[user_id][case_id]["is_not_diff_package_in_the_same_line"] = style.is_not_diff_package_in_the_same_line
        res[user_id][case_id]["is_import_before_from"] = style.is_import_before_from
        res[user_id][case_id]["is_not_blank_between_import"] = style.is_not_blank_between_import
        res[user_id][case_id]["is_using_meaningful_name"] = style.is_using_meaningful_name
    result = str(res)
    style_file = open('../code_style.txt', 'w')
    style_file.writelines(result)
    style_file.close()


def create_total_dict():
    res = []
    file = open("../code_similarity.txt", 'r')
    data = eval(file.read())
    file.close()
    file_name_list = os.listdir("../code/res")
    user_score = {}
    current_user_score = 0
    current_user = ""
    current_case_num = 0
    # 相似度
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        if temp[0] != current_user:
            if current_user != "":
                user_score[current_user] = round(current_user_score/current_case_num, 2)
            current_user_score = 0
            current_case_num = 0
            current_user = temp[0]
        similarity = list(data[temp[0]][temp[1]].values())
        doubt = 0
        for index in range(len(similarity)):
            if similarity[index] == "one of them is not python file" or similarity[index] == "E":
                continue
            else:
                if int(similarity[index]) >= 70:
                    doubt = doubt + 1
        code_similarity = round(doubt / len(similarity) * 100, 2)
        current_user_score = current_user_score + code_similarity
        current_case_num = current_case_num + 1
        if i == len(file_name_list) - 1:
            user_score[current_user] = round(current_user_score / current_case_num, 2)
    for user in list(user_score.keys()):
        user_score[user] = round((100 - user_score[user] * 100 / max(list(user_score.values()))), 2)
    temp = list(user_score.values())
    total = 0
    for i in range(len(temp)):
        total = total + temp[i]
    user_score["total"] = round(total/268, 2)
    res.append(user_score)
    # 风格
    file = open("../code_style.txt", 'r')
    data = eval(file.read())
    file.close()
    user_score = {}
    current_case_num = 0
    current_user_score = 0
    current_user = ""
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        if temp[0] != current_user:
            if current_user != "":
                user_score[current_user] = round(current_user_score / current_case_num, 2)
            current_user_score = 0
            current_case_num = 0
            current_user = temp[0]
        style_num = 0
        student_id = current_user
        ques_id = temp[1]
        if not data[student_id][ques_id]["is_indent_using_one"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_space_nums_multiple_of_four"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_within_len_range"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_trailing_space"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_space_around_operator"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_space_around_operator_in_def"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_using_one_quotation"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_blank_line_beginning"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_inline_comments"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_space_after_pound"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_blank_line_after_import"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_blank_line_before_class"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_blank_line_before_def"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_diff_package_in_the_same_line"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_import_before_from"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_not_blank_between_import"]:
            style_num = style_num + 1
        if not data[student_id][ques_id]["is_using_meaningful_name"]:
            style_num = style_num + 1
        code_style_score = round((17 - style_num) / 17 * 100, 2)
        current_user_score = current_user_score + code_style_score
        current_case_num = current_case_num + 1
        if i == len(file_name_list) - 1:
            user_score[current_user] = round(current_user_score / current_case_num, 2)
    temp = list(user_score.values())
    total = 0
    for i in range(len(temp)):
        total = total + temp[i]
    user_score["total"] = round(total / 268, 2)
    res.append(user_score)
    # 分数
    file_name_list = os.listdir("../code/res")
    file = open("../test_data.json", 'r', encoding="utf-8")
    data = eval(file.read())
    file.close()
    case_score_temp = {}
    for file in file_name_list:
        student_id = file.split("_")[0]
        ques_id = file.split("_")[1]
        if ques_id not in case_score_temp:
            case_score_temp[ques_id] = []
        score = 0
        for case in range(len(data[student_id]["cases"])):
            if data[student_id]["cases"][case]["case_id"] == ques_id:
                score = data[student_id]["cases"][case]["final_score"]
        case_score_temp[ques_id].append(score)
    case_score = {}
    for case in list(case_score_temp.keys()):
        case_score[case] = sum(case_score_temp[case])/len(case_score_temp[case])
    user_score = {}
    current_case_num = 0
    current_user_score = 0
    current_user = ""
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        if temp[0] != current_user:
            if current_user != "":
                user_score[current_user] = round(current_user_score / current_case_num, 2)
            current_user_score = 0
            current_case_num = 0
            current_user = temp[0]
        student_id = current_user
        ques_id = temp[1]
        score = 0
        for case in range(len(data[student_id]["cases"])):
            if data[student_id]["cases"][case]["case_id"] == ques_id:
                score = data[student_id]["cases"][case]["final_score"]
        code_score = score * case_score[ques_id] / 100
        current_user_score = current_user_score + code_score
        current_case_num = current_case_num + 1
        if i == len(file_name_list) - 1:
            user_score[current_user] = round(current_user_score / current_case_num, 2)
    temp = list(user_score.values())
    total = 0
    for i in range(len(temp)):
        total = total + temp[i]
    user_score["total"] = round(total / 268, 2)
    res.append(user_score)
    # 时间复杂
    file = open("../code_complexity.txt", 'r', encoding="utf-8")
    data = eval(file.read())
    file.close()
    case_score_temp = {}
    for file in list(data.keys()):
        ques_id = file.split("_")[1]
        if ques_id not in case_score_temp:
            case_score_temp[ques_id] = []
        if data[file][0] not in case_score_temp[ques_id]:
            case_score_temp[ques_id].append((data[file][0]))
    for case in list(case_score_temp.keys()):
        temp1 = list()
        for value in case_score_temp[case]:
            temp1.append(comp_str.CompStr(value))
        temp1.sort(reverse=True)
        temp = list()
        for obj in temp1:
            temp.append(obj.value)
        case_score_temp[case] = temp
    user_score = {}
    current_case_num = 0
    current_user_score = 0
    current_user = ""
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        if temp[0] != current_user:
            if current_user != "":
                user_score[current_user] = round(current_user_score / current_case_num, 2)
            current_user_score = 0
            current_case_num = 0
            current_user = temp[0]
        ques_id = temp[1]
        score = 100 / len(case_score_temp[ques_id]) * (case_score_temp[ques_id].index(data[file_name_list[i]][0]) + 1)
        current_user_score = current_user_score + score
        current_case_num = current_case_num + 1
        if i == len(file_name_list) - 1:
            user_score[current_user] = round(current_user_score / current_case_num, 2)
    temp = list(user_score.values())
    total = 0
    for i in range(len(temp)):
        total = total + temp[i]
    user_score["total"] = round(total / 268, 2)
    res.append(user_score)
    # 空间复杂
    file = open("../code_complexity.txt", 'r', encoding="utf-8")
    data = eval(file.read())
    file.close()
    case_score_temp = {}
    for file in list(data.keys()):
        ques_id = file.split("_")[1]
        if ques_id not in case_score_temp:
            case_score_temp[ques_id] = []
        if data[file][1] not in case_score_temp[ques_id]:
            case_score_temp[ques_id].append((data[file][1]))
    for case in list(case_score_temp.keys()):
        temp1 = list()
        for value in case_score_temp[case]:
            temp1.append(comp_str.CompStr(value))
        temp1.sort(reverse=True)
        temp = list()
        for obj in temp1:
            temp.append(obj.value)
        case_score_temp[case] = temp
    user_score = {}
    current_case_num = 0
    current_user_score = 0
    current_user = ""
    for i in range(len(file_name_list)):
        temp = file_name_list[i].split("_")
        if temp[0] != current_user:
            if current_user != "":
                user_score[current_user] = round(current_user_score / current_case_num, 2)
            current_user_score = 0
            current_case_num = 0
            current_user = temp[0]
        ques_id = temp[1]
        score = 100 / len(case_score_temp[ques_id]) * (case_score_temp[ques_id].index(data[file_name_list[i]][1]) + 1)
        current_user_score = current_user_score + score
        current_case_num = current_case_num + 1
        if i == len(file_name_list) - 1:
            user_score[current_user] = round(current_user_score / current_case_num, 2)
    temp = list(user_score.values())
    total = 0
    for i in range(len(temp)):
        total = total + temp[i]
    user_score["total"] = round(total / 268, 2)
    res.append(user_score)
    # 写入
    result = str(res)
    complexity_file = open('../code_total.txt', 'w')
    complexity_file.writelines(result)
    complexity_file.close()


if __name__ == "__main__":
    download_zip()
    create_similarity_dict()
    create_complexity_dict()
    create_style_dict()
    create_total_dict()
