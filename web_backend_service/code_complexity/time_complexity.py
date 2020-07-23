import re
from complexity import Checker
from comp_str import CompStr


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
                    self.deal_loop(word, i, j, self.codes, self.complexity_tag)
            # 扫描是否是自递归方法
            self.deal_recursion(method, method_line, i)
        return self.integrate_complexity(method_begin, method_end, self.indentation_structure, self.complexity_tag)

    @staticmethod
    def deal_loop(loop_type: str, loop_begin: int, loop_end: int, codes: list,
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
        :param codes:代码样本
        :param complexity_tag:复杂度标签
        :return:
        """
        if loop_type == "for":
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

    def deal_recursion(self, method: str, code: str, rec_index: int):
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
        :param method: 递归方法的名称
        :param code: 产生递归的代码
        :param rec_index: 递归代码所在的行号
        :return:
        """
        is_recursion = re.search(method, code)
        if not is_recursion:
            return

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
                if re.match("[0-9]*\\*?n/2", frac):
                    # log_n幂函数
                    a = frac.split('*')
                    if len(a) > 1:
                        rec_count += int(a[0])
                    else:
                        rec_count += 1
                    rec_exp = -1
                elif re.match("[0-9]*\\*?n\\^*[0-9]*", frac):
                    # n幂函数
                    a = frac.split('*')
                    if len(a) > 1:
                        rec_count += int(a[0])
                    else:
                        rec_count += 1
                    temp_exp = frac.split('^')
                    rec_exp = max(rec_exp, int(temp_exp[1]) if len(temp_exp) > 1 else 1)
            rec_tail = comp_list[-1]
            try:
                res = self.complexity_list[(rec_exp, rec_count, rec_tail)]
                return res
            except KeyError:
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
                    rec_mul = re.search('[0-9]+\\*]', code[rec_start: rec_end])
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
        self.complexity_tag[rec_index] = CompStr(deal_comp())
        return

    @staticmethod
    def param_match(loop_type: str, code_line: str):
        return re.match(loop_type, code_line)


if __name__ == '__main__':
    # t = TimeChecker("../../test/time_comp_test.py")
    # t = TimeChecker("mini_test.py")
    t = TimeChecker("../../code/res/" + "58547_2746_271261" + "/main.py")
    print(t.deal_with_file())
