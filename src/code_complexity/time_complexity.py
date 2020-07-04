from collections import defaultdict
import re


def cal_method_complexity(codes: list) -> str:
    """
    计算代码方法时间复杂度的方法，该方法有以下功能：
    1. 允许检查普通的嵌套循环;
    2. 允许检查普通的递归调用;
    :param codes: 代码样本
    :return: 代码时间复杂度
    """
    return ''


def cal_main_complexity(codes: list, methods: dict) -> str:
    """
    计算main函数时间复杂度的方法，该方法通过单文件持有的方法列表计算main函数的方法调用
    :param codes: main函数的代码
    :param methods: 文件的代码列表
    :return: main的复杂度
    """
    return ''


def cal_method_call_index(codes: list, methods: list) -> dict:
    """
    计算方法在代码样本中被调用的位置
    :param codes: 代码样本
    :param methods: 方法列表
    :return:方法在代码样本中被调用的位置
    """
    # 标定所有的方法调用的位置
    method_call_index = defaultdict(list)
    for i in range(len(codes)):
        code_line = codes[i]
        for method in methods:
            # method_define = methods[method]
            # if i == method_define:
            #     continue
            call_pattern = method + "([^]]*)"
            method_call = re.search(call_pattern, code_line)
            if method_call:
                method_call_index[method].append(method_call)
    return method_call_index


def deal_with_file(file_path: str):
    """
    处理python文件的方法，该方法有以下限制：
    1. 方法只能处理.py文件;
    2. 方法处理的文件中没有死循环;
    3. 方法默认处理的文件均以标准形式缩进(每级缩进4格)
    :param file_path: 处理文件的路径
    :return:main函数的复杂度
    """
    # 方法只能检测.py文件
    if file_path[-2:] != "py":
        print("File is not a python file.")
        return
    codes = open(file_path, 'r', encoding="utf-8").readlines()
    codes_len = len(codes)
    # 构建缩进树
    indentation_structure = []
    for i in range(codes_len):
        indentation_structure.append((len(codes[i]) - len(codes[i].lstrip())) // 4)
    indentation_structure.append(0)
    # 获取方法名称
    methods = {}
    for i in range(codes_len):
        code_line = codes[i]
        if code_line.lstrip()[:3] == "def":
            method_name = re.match("[^ ():]*", code_line[4:]).group()
            methods[method_name] = i
    # 扫描所有方法的时间复杂度，标定所有方法的位置
    method_complexity = {}
    main_tag = [1 for i in range(codes_len)]
    for method in methods:
        method_begin = methods[method]
        indentation_level = indentation_structure[method_begin]
        method_end = indentation_structure.index(indentation_level, method_begin + 1, codes_len)
        method_complexity[method] = cal_method_complexity(codes[method_begin:method_end])
        for i in range(method_begin, method_end):
            main_tag[i] = 0
    # 获取主函数副本并检查复杂度
    main_codes = []
    for i in range(codes_len):
        tag = main_tag[i]
        if tag == 1:
            main_codes.append(codes[i])
    main_complexity = cal_main_complexity(main_codes, method_complexity)
    return main_complexity


if __name__ == '__main__':
    print(deal_with_file("../check_similarity/K_gram.py"))
    # print(deal_with_file("time_complexity.py"))
