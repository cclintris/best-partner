import re
from collections import defaultdict


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

    def cal_method_complexity(self, method: str, method_begin: int, method_end: int) -> str:
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
        :return: 代码时间复杂度
        """
        if method in self.methods_complexity:
            return self.methods_complexity[method]

        # 创建保留字列表，复杂度标记;提取参数名
        params = re.search("[(][^()]*[)]", self.codes[method_begin]).group()[1:-1].split(',')
        for i in range(len(params)):
            params[i] = re.match("[^:]*", params[i]).group()

        def deal_recursion(code: str, rec_index: int):
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
                其中计算复杂度时，递归式中若包含对同文件其他函数的调用，将其视为O(n)
            4. 如果无法计算递归的复杂度，将其视为O(n)
            :param code: 产生递归的代码
            :param rec_index: 递归代码所在的行号
            :return:
            """
            if code.count('='):
                code = code.split('=')[1]
            complexity = ''
            has_rec = re.search(method, code)

            def deal_comp() -> str:
                """
                在代码处理结束后对complexity中的记录进行处理和匹配;默认递归中不会出现减号和除号在统一调用中匹配成功的情况
                可能出现的匹配模式如下所示：
                1. [[0-9]*[*]?n^[0-9]*[ ]]*[n1]
                2. [[0-9]*[*]?n/2[ ]]*[n1]
                :return:
                """
                comp_list = complexity.split(' ')[:-1]
                rec_count = 0
                rec_exp = 1
                for frac in comp_list:
                    if re.match("[0-9]*[*]?n/2", frac):
                        a = frac.split('*')
                        if len(a) > 1:
                            rec_count += int(a[0])
                        else:
                            rec_count += 1
                        rec_exp = -1
                    elif re.match("[0-9]*[*]?n\\^*[0-9]*", frac):
                        a = frac.split('*')
                        if len(a) > 1:
                            rec_count += int(a[0])
                        else:
                            rec_count += 1
                        rec_exp = max(rec_exp, int(frac.split('^')[1]))
                rec_tail = comp_list[-1]
                res = self.complexity_list[(rec_exp, rec_count, rec_tail)]
                if res:
                    return res
                else:
                    if rec_exp > 1:
                        return str(rec_exp) + "^n"
                    else:
                        return "n"

            while has_rec:
                # 代码中仍存在自递归调用时
                rec_start = has_rec.start()
                rec_params = re.search("[^()]*", code[has_rec.end() + 1:])
                rec_end = has_rec.end() + rec_params.end() + 1
                rec_params = rec_params.group().split(',')
                for rec_param in rec_params:
                    if not rec_param.lstrip('-').isdigit():
                        # 作为非数字的参数，检查减号、除号以及乘号进行匹配
                        comp_2add = ''
                        rec_m = rec_param.count('-')
                        if rec_m:
                            comp_2add += ("n^" + str(rec_m) + ' ')
                        else:
                            rec_d = rec_param.count('/')
                            if rec_d:
                                comp_2add = "n/2 "
                        rec_mul = re.search('[0-9]*[*]', code[rec_start: rec_end])
                        if rec_mul:
                            comp_2add = rec_mul.group() + comp_2add
                        complexity += comp_2add
                code = code[:rec_start] + code[rec_end + 1:]
                has_rec = re.search(method, code)
            # 代码中无自递归调用时
            is_call = False
            for name in self.methods:
                is_call = is_call | (re.search(name, code) is not None)
                if is_call:
                    break
            if is_call:
                complexity += 'n '
            else:
                complexity += '1 '
            # 认定任何递归调用函数行数大于一行，将递归复杂度标记在递归调用的上一行
            self.complexity_tag[rec_index - 1] = deal_comp()
            return

        for i in range(method_begin + 1, method_end):
            method_line = self.codes[i].lstrip()
            # 扫描行首是否有循环保留字
            for word in self.reserved_words:
                is_match = re.match(word, method_line)
                if is_match:
                    self.deal_loop(word, i, params, self.codes, self.complexity_tag)
            # 扫描是否是自递归方法
            is_recursion = re.search(method, method_line)
            if is_recursion:
                deal_recursion(method_line, i)
        return self.integrate_complexity(method_begin, method_end, self.indentation_structure, self.complexity_tag)

    def cal_main_complexity(self, main_codes: list) -> str:
        """
        计算main函数时间复杂度的方法，该方法通过单文件持有的方法列表计算main函数的方法调用
        :param main_codes: main函数的代码
        :return: main的复杂度
        """
        main_indentation = []
        for i in range(len(main_codes)):
            main_indentation.append((len(main_codes[i]) - len(main_codes[i].lstrip())) // 4)
        main_comp_tag = ['' for i in range(len(main_codes))]
        methods_call_index = self.cal_method_call_index(main_codes)
        for k, v in methods_call_index.items():
            for q in v:
                main_comp_tag[q] = self.methods_complexity[k]
        for i in range(len(main_codes)):
            line = main_codes[i].lstrip()
            # 扫描行首是否有循环保留字
            for word in self.reserved_words:
                is_match = re.match(word, line)
                if is_match:
                    # 把循环本身的条件作为参数
                    self.deal_loop(word, i, re.search("[(][^()]*[)]", line).group()[1:-1].split(','), main_codes,
                                   main_comp_tag)
        return self.integrate_complexity(-1, len(main_codes), main_indentation, main_comp_tag)

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
                # method_define = methods[method]
                # if i == method_define:
                #     continue
                call_pattern = method + "[(][^()]*[)]"
                method_call = re.search(call_pattern, code_line)
                if method_call:
                    method_call_index[method].append(i)
        return method_call_index

    def deal_loop(self, loop_type: str, loop_index: int, params: list, codes: list, complexity_tag: list):
        """
        根据缩进树在缩进层级上标记出独立复杂度
        :param loop_type: 循环关键字的种类
        :param loop_index: 循环关键字的所在行号
        :param params: 循环关键字所持有的参数列表
        :param codes:代码样本
        :param complexity_tag:复杂度标签
        :return:
        """
        if loop_type == "for":
            for param in params:
                if re.search(param, codes[loop_index]):
                    complexity_tag[loop_index] = 'n'
            if complexity_tag[loop_index] == '':
                complexity_tag[loop_index] = 'm'
            return
        elif loop_type == "while":
            for param in params:
                if re.search(param, self.codes[loop_index]):
                    if codes[loop_index].count('/'):
                        complexity_tag[loop_index] = 'log_n'
                    else:
                        complexity_tag[loop_index] = 'n'
            if complexity_tag[loop_index] == '':
                if codes[loop_index].count('/'):
                    complexity_tag[loop_index] = 'log_m'
                else:
                    complexity_tag[loop_index] = 'm'
            return
        return

    def integrate_complexity(self, begin: int, end: int, indentation_structure: list, complexity_tag: list) -> str:
        """
        整合complexity_tag上所记录的单行产生的复杂度，并返回整体复杂度
        :return: 方法的时间复杂度
        """
        if len(complexity_tag) == 1:
            return complexity_tag[0]
        indentation_level = indentation_structure[begin + 1]
        comp_record = [complexity_tag[begin + 1]]
        record2comp = defaultdict(int)

        def integrate(c1: str, c2: str) -> str:
            """
            两个复杂度相乘;复杂度具有以下几种格式：
            1. [n|m]
            2. n^[0-9]*
            3. log_[n|m]
            4. [0-9]*^n
            :param c1: 复杂度1，添加项
            :param c2: 复杂度2，基项
            :return:
            """
            patterns = ['n\\^[0-9]*', 'log[0-9]*_n', 'log[0-9]*_m']
            matches = [
                re.match(patterns[0], c2), re.match('n', c2) and c2.count('^') == 0,
                re.search(patterns[1], c2), re.search(patterns[2], c2)
            ]
            if c1 == '':
                return c2
            if c2 == '':
                return c1
            if c1 == 'n':
                if matches[0]:
                    c = c2.split('^')
                    return c[0] + '^' + str(int(c[1]) + 1)
                elif matches[1]:
                    return "n^2" + c2[1:]
                else:
                    return c1 + '*' + c2
            if re.match(patterns[0], c1):
                if matches[0]:
                    c = c2.split('^')
                    return c[0] + str(int(c[1]) + int(c1.split('^')[1]))
                elif matches[1]:
                    return "n^" + str(int(c1.split('^')[1]) + 1) + c2[1:]
                else:
                    return c1 + '*' + c2
            if re.match(patterns[1], c1):
                if matches[2]:
                    a1 = int(re.search('log[0-9]*', c1).group()[3:])
                    a2 = int(re.search('log[0-9]*', c2).group()[3:])
                    return "log" + str(a1 + a2) + "_n"
                else:
                    return c2 + '*' + c1
            if re.match(patterns[2], c1):
                if matches[3]:
                    a1 = int(re.search('log[0-9]*', c1).group()[3:])
                    a2 = int(re.search('log[0-9]*', c2).group()[3:])
                    return "log" + str(a1 + a2) + "_m"
                else:
                    return c2 + '*' + c1
            return c1 + '*' + c2

        def max_comp() -> str:
            """
            查找字典中代表复杂度最高的字符串:只需要查找与该复杂度所有深度相等的行中复杂度最大的一个即可
            依次比照以下大小
            1. n指数    [0-9]*^n
            2. n幂函数  n^[0-9]*
            3. n        n
            4. n对数    log[0-9]*_n
            5. m        m
            6. m对数    log[0-9]*_m
            :return:
            """
            comp = list(record2comp.keys())
            if len(comp) == 1:
                return str(comp[0])
            for j in range(len(comp)):
                comp[j] = str(comp[j]).split('*')
            for p in self.to_compare:
                if len(comp) == 1:
                    return '*'.join(comp[0])
                flag = False
                candi = []
                for c in comp:
                    for w in c:
                        if re.match(p, w):
                            flag = True
                            candi.append(True)
                        else:
                            candi.append(False)
                if flag:
                    for j in range(len(candi) - 1, -1, -1):
                        if not candi[j]:
                            comp.pop(j)
            return 'n'

        record2comp[complexity_tag[begin + 1]] = indentation_structure[begin + 1]
        for i in range(begin + 1, end):
            temp_level = indentation_structure[i]
            # 缩进层下落则增加复杂度，缩进层上浮则弹出复杂度
            if temp_level > indentation_level:
                comp_record.append(integrate(complexity_tag[i - 1], comp_record[-1]))
                record2comp[comp_record[-1]] = temp_level
            elif temp_level < indentation_level:
                temp_record = comp_record.pop(-1)
                max_level = max(record2comp.values())
                # 当前深度与最大深度相同则添加复杂度串，更深则清空后添加复杂度串，较浅则不添加
                record2comp = {k: v for k, v in record2comp.items() if v == max_level}
                record2comp[temp_record] = temp_level
            else:
                record2comp[comp_record[-1]] = temp_level
            indentation_level = temp_level
        return max_comp()

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


if __name__ == '__main__':
    t = TimeChecker("time_comp_test.py")
    print(t.deal_with_file())
    # print(deal_with_file("time_complexity.py"))
