import re
from collections import defaultdict


class Checker:
    def __init__(self, file_path: str):
        # 方法只能检测.py文件
        if file_path[-2:] != "py":
            print("File is not a python file.")
            return
        self.codes = open(file_path, 'r', encoding="utf-8").readlines()
        for i in range(len(self.codes) - 1, -1, -1):
            if re.match('#', self.codes[i].lstrip()):
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
            if tag == 1 and self.codes[i] != "\n":
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

    def cal_method_complexity(self, method, method_begin, method_end):
        pass

    def cal_main_complexity(self, main_codes):
        pass

    def integrate_complexity(self, begin: int, end: int, indentation_structure: list, complexity_tag: list):
        pass


class CompStr:
    patterns = ['n\\^[0-9]*', 'log[0-9]*_n', 'log[0-9]*_m']
    # 常见复杂度表单，顺序依次为n指数、n幂函数、n、n对数、m、m对数
    to_compare = [
        "[0-9]*\\^n", "n\\^[0-9]*", "n", "log[0-9]*_n", "m", "log[0-9]*_m"
    ]

    def __init__(self, comp: str):
        self.value = comp

    def __mul__(self, other):
        """
        两个复杂度相乘;复杂度具有以下几种格式：
        1. [n|m]
        2. n^[0-9]*
        3. log_[n|m]
        4. [0-9]*^n
        :return:
        """
        # TODO
        c1 = self.value
        c2 = other.value
        matches = [
            re.match(self.patterns[0], c2), re.match('n', c2) and c2.count('^') == 0,
            re.search(self.patterns[1], c2), re.search(self.patterns[2], c2)
        ]
        if c1 == '1':
            return CompStr(c2)
        if c2 == '1':
            return CompStr(c1)
        if c1 == 'n':
            if matches[0]:
                c = c2.split('^')
                return CompStr(c[0] + '^' + str(int(c[1]) + 1))
            elif matches[1]:
                return CompStr("n^2" + c2[1:])
            else:
                return CompStr(c1 + '*' + c2)
        if re.match(self.patterns[0], c1):
            if matches[0]:
                c = c2.split('^')
                return CompStr(c[0] + str(int(c[1]) + int(c1.split('^')[1])))
            elif matches[1]:
                return CompStr("n^" + str(int(c1.split('^')[1]) + 1) + c2[1:])
            else:
                return CompStr(c1 + '*' + c2)
        if re.match(self.patterns[1], c1):
            if matches[2]:
                a1 = int(re.search('log[0-9]*', c1).group()[3:])
                a2 = int(re.search('log[0-9]*', c2).group()[3:])
                return CompStr("log" + str(a1 + a2) + "_n")
            else:
                return CompStr(c2 + '*' + c1)
        if re.match(self.patterns[2], c1):
            if matches[3]:
                a1 = int(re.search('log[0-9]*', c1).group()[3:])
                a2 = int(re.search('log[0-9]*', c2).group()[3:])
                return CompStr("log" + str(a1 + a2) + "_m")
            else:
                return CompStr(c2 + '*' + c1)
        return CompStr(c1 + '*' + c2)

    def __cmp__(self, other):
        """
        查找字典中代表复杂度最高的字符串:比较两个复杂度的大小
        依次比照以下大小
        1. n指数    [0-9]*^n
        2. n幂函数  n^[0-9]*
        3. n        n
        4. n对数    log[0-9]*_n
        5. m        m
        6. m对数    log[0-9]*_m
        :return:
        """
        res = ''
        a = self.value
        b = other.value
        # 预处理 将n变成n^1
        for i in range(len(a)):
            if a[i] == 'n':
                if i != len(a) - 1:
                    if a[i + 1] == '^':
                        continue
                if i != 0:
                    if a[i - 1] == '^' or a[i - 1] == '_':
                        continue
                a_temp = list(a)
                a_temp.insert(i + 1, '^1')
                a = ''.join(a_temp)
        for i in range(len(b)):
            if b[i] == 'n':
                if i != len(b) - 1:
                    if b[i + 1] == '^':
                        continue
                if i != 0:
                    if b[i - 1] == '^' or b[i - 1] == '_':
                        continue
                b_temp = list(b)
                b_temp.insert(i + 1, '^1')
                b = ''.join(b_temp)
        # 比较指数
        index_a = 0
        for i in range(len(a)):
            # 此处为依赖处
            if a[i] == '^':
                if a[i + 1] == 'n':
                    index_a = int(a[i - 1])
        index_b = 0
        for i in range(len(b)):
            # 此处为依赖处
            if b[i] == '^':
                if b[i + 1] == 'n':
                    index_b = int(b[i - 1])
        if index_a > index_b:
            return -1
        elif index_a < index_b:
            return 1
        # 比较幂函数
        power_a = 0
        for i in range(len(a)):
            if a[i] == '^':
                if a[i - 1] == 'n':
                    power_a = int(a[i + 1])
        power_b = 0
        for i in range(len(b)):
            if b[i] == '^':
                if b[i - 1] == 'n':
                    power_b = int(b[i + 1])
        if power_a > power_b:
            return -1
        elif power_a < power_b:
            return 1
        if 'log_n' not in b:
            return -1
        if 'log_n' not in a:
            return 1
