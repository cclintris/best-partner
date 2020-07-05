from collections import defaultdict
import re


class TimeChecker:
    def __init__(self, file_path: str):
        # 方法只能检测.py文件
        if file_path[-2:] != "py":
            print("File is not a python file.")
            return
        self.codes = open(file_path, 'r', encoding="utf-8").readlines()
        # 构建缩进树
        self.indentation_structure = []
        for i in range(len(self)):
            self.indentation_structure.append((len(self.codes[i]) - len(self.codes[i].lstrip())) // 4)
        self.indentation_structure.append(0)
        self.methods = {}
        self.methods_complexity = {}

    def __len__(self):
        return len(self.codes)

    def cal_method_complexity(self, method: str, method_begin: int, method_end: int, methods: dict) -> str:
        """
        计算代码方法时间复杂度的方法，该方法有以下限制：
        1. 允许检查嵌套循环的复杂度;
        2. 允许检查自递归调用的复杂度;
        3. 方法的复杂度由自身的复杂度和同一文件中其他方法调用产生的复杂度结合得出;
        该方法有以下简化流程的思路：
        1. 该方法将忽略任何引自其他文件的方法复杂度，将其视为O(1);
        2. 该方法将传入参数产生的for循环均视为O(n)复杂度，非参数产生的for循环均视为O(m)复杂度，原则上m<<n;
        3. 该方法将传入参数产生且不含有整除条件的while循环均视为O(n)复杂度，非参数产生的while循环均视为O(m)复杂度，
           带有二分条件的分别视为O(log_n)和O(log_m)复杂度
        :param method: 检查方法的名字
        :param method_begin: 方法的起始位置
        :param method_end: 方法的结束位置
        :param methods: 同文件方法的起始位置字典
        :return: 代码时间复杂度
        """
        if method in self.methods_complexity:
            return self.methods_complexity[method]

        # 创建保留字列表，复杂度标记;提取参数名
        reserved_words = ["for", "while"]
        complexity_tag = ['' for i in range(len(self))]
        params = re.search("[(][^()]*[)]", self.codes[method_begin]).group()[1:-1].split(',')
        for i in range(len(params)):
            params[i] = re.match("[^:]*", params[i]).group()

        def deal_loop(loop_type: str, loop_index: int):
            """
            根据缩进树在缩进层级上标记出独立复杂度
            :param loop_type: 循环关键字的种类
            :param loop_index: 循环关键字的所在行号
            :return:
            """
            if loop_type == "for":
                for param in params:
                    if re.search(param, self.codes[loop_index]):
                        complexity_tag[loop_index] = 'n'
                if complexity_tag[loop_index] == '':
                    complexity_tag[loop_index] = 'm'
                return
            elif loop_type == "while":
                for param in params:
                    if re.search(param, self.codes[loop_index]):
                        if self.codes[loop_index].count('/'):
                            complexity_tag[loop_index] = 'log_n'
                        else:
                            complexity_tag[loop_index] = 'n'
                if complexity_tag[loop_index] == '':
                    if self.codes[loop_index].count('/'):
                        complexity_tag[loop_index] = 'log_m'
                    else:
                        complexity_tag[loop_index] = 'm'
                return
            return

        def deal_recursion(code: str):
            """
            根据递归代码计算递归复杂度，该方法有以下限制：
            1. 仅仅以常见的递归复杂度为模板估算复杂度，而不进行详尽的变量扫描和计算得出结论;
            2. 任意自递归调用的参数均被视为n级别;
            3. 常见的自递归函数复杂度由下列出：
                T(n)=T(n/2)+O(1)         T(n)=O(log_n)
                T(n)=T(n-1)+O(1)         T(n)=O(n)
                T(n)=2*T(n/2)+O(1)       T(n)=O(n)
                T(n)=2*T(n/2)+O(n)       T(n)=O(n*log_n)
                T(n)=2*T(n/2)+O(n*log_n) T(n)=O(n*log^2_n)
                T(n)=T(n-1)+O(n)         T(n)=O(n^2)
                T(n)=2*T(n-1)+O(1)       T(n)=O(2^n)
                T(n)=T(n-1)+T(n-2)+O(1)  T(n)=O(2^n)
            :param code: 产生递归的代码
            :return:
            """
            if code.count('='):
                code = code.split('=')[1]
            has_rec = re.search(method, code)
            while has_rec:
                # 代码中仍存在自递归调用时
                rec_start = has_rec.start()
                rec_params = re.search("[^()]*", code[has_rec.end() + 1:])
                rec_end = rec_params.end() + 1
                rec_params = rec_params.group().split(',')
                for rec_param in rec_params:
                    if not rec_param.lstrip('-').isdigit():
                        # 作为非数字的参数，检查减号和除号进行匹配
                        return

        def integration_complexity() -> str:
            """
            整合complexity_tag上所记录的单行产生的复杂度，并返回整体复杂度
            :return: 方法的时间复杂度
            """
            return ''

        for i in range(method_begin + 1, method_end):
            method_line = self.codes[i].lstrip()
            # 扫描行首是否有循环保留字
            for word in reserved_words:
                is_match = re.match(word, method_line)
                if is_match:
                    deal_loop(word, i)
            # 扫描是否是自递归方法
            is_recursion = re.search(method, method_line)
            if is_recursion:
                deal_recursion(method_line)
        return integration_complexity()

    def cal_main_complexity(self, codes: list, methods: dict) -> str:
        """
        计算main函数时间复杂度的方法，该方法通过单文件持有的方法列表计算main函数的方法调用
        :param codes: main函数的代码
        :param methods: 文件的代码列表
        :return: main的复杂度
        """
        return ''

    def cal_method_call_index(self, codes: list, methods: list) -> dict:
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
            indentation_level = self.indentation_structure[method_begin]
            method_end = self.indentation_structure.index(indentation_level, method_begin + 1, codes_len)
            method_complexity[method] = self.cal_method_complexity(method, method_begin, method_end, methods)
            for i in range(method_begin, method_end):
                main_tag[i] = 0
        # 获取主函数副本并检查复杂度
        main_codes = []
        for i in range(codes_len):
            tag = main_tag[i]
            if tag == 1:
                main_codes.append(self.codes[i])
        main_complexity = self.cal_main_complexity(main_codes, method_complexity)
        return main_complexity


if __name__ == '__main__':
    t = TimeChecker("../check_similarity/K_gram.py")
    print(t.deal_with_file())
    # print(deal_with_file("time_complexity.py"))
