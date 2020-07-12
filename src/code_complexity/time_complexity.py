import re
from Complexity import Checker
from Complexity import CompStr
from collections import defaultdict


# TODO 本时间复杂度处理器没有实现关于O(1)复杂度的处理并将O(1)置为了空字符''，详情见__init__对complexity_tag的初始化
class TimeChecker(Checker):

    def cal_method_complexity(self, method: str, method_begin: int, method_end: int):
        """
        计算代码方法时间复杂度的方法，该方法有以下限制：
        1. 允许检查嵌套循环的复杂度;
        2. 允许检查自递归调用的复杂度;
        3. 方法的复杂度由自身的复杂度和同一文件中其他方法调用产生的复杂度结合得出;
        该方法最终会将self的缩进树和复杂度便签列表交由integrate_complexity方法进行处理
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
                is_call = is_call or (re.search(name, code) is not None)
                if is_call:
                    break
            if is_call:
                complexity += 'n '
            else:
                complexity += '1 '
            # 认定任何递归调用函数行数大于一行，将递归复杂度标记在递归调用的上一行
            self.complexity_tag[rec_index - 1] = CompStr(deal_comp())
            return

        for i in range(method_begin + 1, method_end):
            method_line = self.codes[i].lstrip()
            # 扫描行首是否有循环保留字
            for word in self.reserved_words:
                is_match = re.match(word, method_line)
                if is_match:
                    j = i + 1
                    while j < method_end and self.indentation_structure[i] < \
                            self.indentation_structure[j]:
                        j += 1
                    self.deal_loop(word, i, j, params, self.codes, self.complexity_tag)
            # 扫描是否是自递归方法
            is_recursion = re.search(method, method_line)
            if is_recursion:
                deal_recursion(method_line, i)
        return self.integrate_complexity(method_begin, method_end, self.indentation_structure, self.complexity_tag)

    def cal_main_complexity(self, main_codes: list):
        """
        计算main函数时间复杂度的方法，该方法通过单文件持有的方法列表计算main函数的方法调用：
        该方法最终会生成一个main函数缩进树和复杂度便签列表，并交由integrate_complexity方法进行处理
        :param main_codes: main函数的代码
        :return: main的复杂度
        """
        # TODO 对主函数逻辑的处理进行修改和优化 该方法已移交给薛人玮
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
                is_match = re.match(word, line)
                if is_match:
                    j = i + 1
                    while j < len(main_indentation) and main_indentation[i] < main_indentation[j]:
                        j += 1
                    # 把循环本身的条件作为参数
                    self.deal_loop(word, i, j, re.search("[(][^()]*[)]", line).group()[1:-1].split(','), main_codes,
                                   main_comp_tag)
        return self.integrate_complexity(-1, len(main_codes), main_indentation, main_comp_tag)

    def deal_loop(self, loop_type: str, loop_begin: int, loop_end: int, params: list, codes: list,
                  complexity_tag: list):
        """
        根据缩进树在缩进层级上标记出独立复杂度
        该方法有以下简化流程的思路：
        1. 该方法将忽略任何引自其他文件的方法复杂度，将其视为O(1);
        2. 该方法将传入参数产生的for循环均视为O(n)复杂度，非参数产生的for循环均视为O(m)复杂度，原则上m<<n;
        3. 该方法将传入参数产生且不含有整除条件的while循环均视为O(n)复杂度，非参数产生的while循环均视为O(m)复杂度，
           带有二分条件的分别视为O(log_n)和O(log_m)复杂度
        :param loop_type: 循环关键字的种类
        :param loop_begin: 循环关键字的所在行号
        :param loop_end: 循环结束的位置
        :param params: 循环关键字所持有的参数列表
        :param codes:代码样本
        :param complexity_tag:复杂度标签
        :return:
        """
        if loop_type == "for":
            for param in params:
                if re.search(param, codes[loop_begin]):
                    complexity_tag[loop_begin] = CompStr('n')
        elif loop_type == "while":
            # 出现除号表示具有二分性质
            loop_loc = loop_begin
            while loop_loc < loop_end:
                if codes[loop_loc].count('/'):
                    complexity_tag[loop_begin] = CompStr('log_n')
                    return
                loop_loc += 1
            complexity_tag[loop_begin] = CompStr('n')
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

        # TODO max_comp方法将被重构为Complexity.CompStr中的cmp方法
        def max_comp():
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
            comp = list(record2comp.keys())
            to_compare = [
                "[0-9]*\\^n", "n\\^[0-9]*", "n", "log[0-9]*_n", "m", "log[0-9]*_m"
            ]
            if len(comp) == 1:
                return comp[0]
            for j in range(len(comp)):
                comp[j] = comp[j].value.split('*')
            for p in to_compare:
                if len(comp) == 1:
                    return CompStr('*'.join(comp[0]))
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
            return CompStr('n')

        # TODO 对进入integrate和max_comp函数的预处理逻辑有待优化,初步设想如下
        """
        针对缩进树的结构，有：
        1. 不同深度的情况下，单一代码的复杂度一定大于它的上一层循环结构(可以忽略任意代码的上层项)
        2. 不同深度的情况下，单一代码的复杂度可能小于与上一层循环同层的其他代码/调用(不能忽略上层同级项项)
        3. 相同深度的情况下，单一代码的复杂度可能小于与自身同层的其他代码(不能忽略同层同级项)
        """
        record2comp[complexity_tag[begin + 1]] = indentation_structure[begin + 1]
        for i in range(begin + 1, end):
            temp_level = indentation_structure[i]
            # 缩进层下落则增加复杂度，缩进层上浮则弹出复杂度
            if temp_level > indentation_level:
                comp_record.append(complexity_tag[i - 1] * comp_record[-1])
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
        # return max(record2comp)


if __name__ == '__main__':
    t = TimeChecker("../../test/time_comp_test.py")
    print(t.deal_with_file())
    # print(deal_with_file("time_complexity.py"))
