import re
from comp_str import CompStr
from collections import defaultdict


class Checker:
    def __init__(self, file_path: str):
        # 方法只能检测.py文件
        if file_path[-2:] != "py":
            print("File is not a python file.")
            return
        self.codes = open(file_path, 'r', encoding="utf-8").readlines()
        for i in range(len(self.codes) - 1, -1, -1):
            if re.match('#', self.codes[i].lstrip()) or self.codes[i] == "\n":
                self.codes.pop(i)
        # 构建缩进树
        self.indentation_structure = []
        for i in range(len(self)):
            self.indentation_structure.append((len(self.codes[i]) - len(self.codes[i].lstrip())) // 4)
        self.indentation_structure.append(0)
        self.methods = {}
        self.methods_complexity = {}
        self.complexity_tag = [CompStr('1') for i in range(len(self))]
        self.reserved_words = ["for", "while"]
        # 常见递归表单，由指数、系数和尾数构成元组项，对应复杂度
        self.complexity_list = {
            (-1, 1, '1'): "log_n", (-1, 2, '1'): "n", (-1, 2, 'n'): "n*log_n", (1, 1, '1'): "n",
            (1, 1, 'n'): "n^2", (1, 2, '1'): "2^n", (2, 1, '1'): "n^2", (2, 2, '1'): "n^2*log_n"
        }

    def __len__(self):
        return len(self.codes)

    def deal_with_file(self):
        """
        处理python文件的方法，该方法有以下限制：
        1. 方法只能处理.py文件;
        2. 方法处理的文件中没有死循环;
        3. 方法默认处理的文件均以标准形式缩进(每级缩进4格)
        :return:main函数的复杂度
        """
        codes_len = len(self)
        # 获取方法名称
        methods = {}
        for i in range(codes_len):
            code_line = self.codes[i]
            if code_line.lstrip()[:3] == "def":
                method_name = re.match("[^():]*", code_line.lstrip()[4:]).group()
                methods[method_name] = i
        self.methods = methods
        # 扫描所有方法的时间复杂度，标定所有方法的位置
        method_complexity = {}
        main_tag = [1 for i in range(codes_len)]
        for method in methods:
            method_begin = methods[method]
            method_end = self.indentation_structure.index(self.indentation_structure[method_begin], method_begin + 1,
                                                          codes_len + 1)
            method_complexity[method] = self.cal_method_complexity(method, method_begin, method_end)
            for i in range(method_begin, method_end):
                main_tag[i] = 0
        self.methods_complexity = method_complexity
        # 获取主函数副本并检查复杂度
        main_codes = []
        for i in range(codes_len):
            tag = main_tag[i]
            if tag == 1:
                main_codes.append(self.codes[i])
        main_complexity = self.cal_main_complexity(main_codes)
        return main_complexity.value

    def cal_method_call_index(self, main_codes: list) -> dict:
        """
        计算方法在代码样本中被调用的位置
        :param main_codes: main函数的代码
        :return:方法在代码样本中被调用的位置
        """
        # 标定所有的方法调用的位置
        method_call_index = defaultdict(list)
        for i in range(len(main_codes)):
            code_line = main_codes[i]
            for method in self.methods_complexity:
                call_pattern = method + "[(][^()]*[)]"
                method_call = re.search(call_pattern, code_line)
                if method_call:
                    method_call_index[method].append(i)
        return method_call_index

    def cal_method_complexity(self, method: str, method_begin: int, method_end: int) -> CompStr:
        pass

    def cal_main_complexity(self, main_codes: list) -> CompStr:
        """
        计算代码main函数空间复杂度的方法，该方法的计算思路如下：
        1. 以input()函数为基准，将输入的数据作为列表项储存/作为列表长度声明的时候复杂度为O(n)
        2. 输入数据不做储存仅做声明时，将复杂度视为O(1)
        3. 最终的空间复杂度为所有的列表项、字典项储存的最大数据量
        :param main_codes:
        :return:
        """
        main_indentation = []
        for i in range(len(main_codes)):
            main_indentation.append((len(main_codes[i]) - len(main_codes[i].lstrip())) // 4)
        main_comp_tag = [CompStr('1') for i in range(len(main_codes))]
        methods_call_index = self.cal_method_call_index(main_codes)
        for k, v in methods_call_index.items():
            for q in v:
                main_comp_tag[q] = self.methods_complexity[k]
        for i in range(len(main_codes)):
            line = main_codes[i].lstrip()
            # 扫描行首是否有循环保留字
            for word in self.reserved_words:
                is_match = self.param_match(word, line)
                if is_match:
                    j = i + 1
                    while j < len(main_indentation) and main_indentation[i] < main_indentation[j]:
                        j += 1
                    self.deal_loop(word, i, j, main_codes, main_comp_tag)
        return self.integrate_complexity(-1, len(main_codes), main_indentation, main_comp_tag)

    @staticmethod
    def deal_loop(loop_type: str, loop_begin: int, loop_end: int, codes: list,
                  complexity_tag: list):
        pass

    def deal_recursion(self, method: str, code: str, rec_index: int):
        pass

    @staticmethod
    def param_match(loop_type: str, code_line: str):
        pass

    @staticmethod
    def integrate_complexity(begin: int, end: int, indentation_structure: list, complexity_tag: list) -> CompStr:
        """
        整合complexity_tag上所记录的单行产生的复杂度，并返回整体复杂度
        针对缩进树的结构，有：
        1. 不同深度的情况下，单一代码的复杂度一定大于它的上一层循环结构(可以忽略任意代码的上层项)
        2. 不同深度的情况下，单一代码的复杂度可能小于与上一层循环同层的其他代码/调用(不能忽略上层同级项项)
        3. 相同深度的情况下，单一代码的复杂度可能小于与自身同层的其他代码(不能忽略同层同级项)
        :param begin: 起始计算位置
        :param end: 终止计算位置
        :param indentation_structure: 缩进树
        :param complexity_tag: complexity_tag 复杂度列表
        :return: 复杂度
        """
        if len(complexity_tag) == 1:
            return complexity_tag[0]
        indentation_level = indentation_structure[begin + 1]
        comp_record = [complexity_tag[begin + 1]]
        record2comp = defaultdict(int)
        record2comp[complexity_tag[begin + 1]] = indentation_structure[begin + 1]
        for i in range(begin + 1, end):
            temp_level = indentation_structure[i]
            # 缩进层下落则增加复杂度，缩进层上浮则弹出复杂度
            if temp_level > indentation_level:
                comp_record.append(complexity_tag[i - 1] * comp_record[-1])
                record2comp[comp_record[-1]] = temp_level
            elif temp_level < indentation_level:
                temp_record = comp_record.pop(-1)
                # max_level = max(record2comp.values())
                # 当前深度与最大深度相同则添加复杂度串，更深则清空后添加复杂度串，较浅则不添加
                # record2comp = {k: v for k, v in record2comp.items() if v == max_level}
                record2comp[temp_record] = temp_level
            else:
                comp_record.append(complexity_tag[i])
                record2comp[comp_record[-1]] = temp_level
            indentation_level = temp_level
        return max(record2comp)
