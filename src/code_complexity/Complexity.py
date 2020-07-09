import re


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
        self.complexity_tag = ['' for i in range(len(self))]
        self.reserved_words = ["for", "while"]
        # 常见递归表单，由指数、系数和尾数构成元组项，对应复杂度
        self.complexity_list = {
            (-1, 1, '1'): "log_n", (-1, 2, '1'): "n", (-1, 2, 'n'): "n*log_n", (1, 1, '1'): "n",
            (1, 1, 'n'): "n^2", (1, 2, '1'): "2^n", (2, 1, '1'): "n^2", (2, 2, '1'): "n^2*log_n"
        }
        # 常见复杂度表单，顺序依次为n指数、n幂函数、n、n对数、m、m对数
        self.to_compare = [
            "[0-9]*\\^n", "n\\^[0-9]*", "n", "log[0-9]*_n", "m", "log[0-9]*_m"
        ]

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
                method_name = re.match("[^():]*", code_line[4:]).group()
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
        return main_complexity

    def cal_method_complexity(self, method, method_begin, method_end):
        pass

    def cal_main_complexity(self, main_codes):
        pass


class Complexity:
    def __init__(self, comp: str):
        self.value = comp

    def __mul__(self, other):
        # TODO
        return 0

    def __cmp__(self, other):
        # TODO
        return 0
