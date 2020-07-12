import re
from Complexity import Checker
from Complexity import CompStr


class SpaceChecker(Checker):

    def cal_method_complexity(self, method, method_begin, method_end):
        """
        计算代码空间复杂度的方法，该方法的计算思路如下：
        1. 任意无循环添加列表的变量均被视为O(1)，包括递归
        2. 含有任意循环添加的空间复杂度被视为O(n^x)
        3. 忽略任何可能出现的条件筛选/二分法导致的添加并视为O(1)
        4. 对出现的递归调用，将该方法的复杂度增加O(n)
        :param method: 方法名
        :param method_begin: 方法起始位置
        :param method_end: 方法结束位置
        :return:
        """
        if method in self.methods_complexity:
            return self.methods_complexity[method]
        deal_recursion = False
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
                    self.deal_loop(i, j, self.codes, self.complexity_tag)
            # 扫描是否是自递归方法
            is_recursion = re.search(method, method_line)
            if is_recursion:
                deal_recursion = True
        res = self.integrate_complexity(method_begin, method_end, self.indentation_structure, self.complexity_tag)
        if deal_recursion:
            return res * CompStr("n")
        else:
            return res

    def cal_main_complexity(self, main_codes):
        """
        计算代码main函数空间复杂度的方法，该方法的计算思路如下：
        1. 以input()函数为基准，将输入的数据作为列表项储存/作为列表长度声明的时候复杂度为O(n)
        2. 输入数据不做储存仅做声明时，将复杂度视为O(1)
        3. 最终的空间复杂度为所有的列表项、字典项储存的最大数据量
        TODO 该方法复用了与time_complexity完全相同的逻辑处理，有待重构
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
                is_match = re.match(word, line) is not None or re.search(" " + word + " ", line) is not None
                if is_match:
                    j = i + 1
                    while j < len(main_indentation) and main_indentation[i] < main_indentation[j]:
                        j += 1
                    self.deal_loop(i, j, main_codes, main_comp_tag)
        return self.integrate_complexity(-1, len(main_codes), main_indentation, main_comp_tag)

    def deal_loop(self, loop_begin: int, loop_end: int, codes: list, complexity_tag: list):
        """
        处理循环结构对空间复杂度的影响，该方法思路如下：
        1. 出现循环关键字时，扫描该循环下的所有行并调用param_comp，直到缩进树上浮/终止
        2. 扫描的所有行中，param_comp返回True，即包含列表/字典的添加动作，标记为O(n)
        3. 不含有2中所描述的操作时，标记为O(1)
        :param loop_begin: 循环开始的位置
        :param loop_end: 循环结束的位置
        :param codes: 要检查的代码样本
        :param complexity_tag: 代码的复杂度标签
        :return:
        """
        loop_loc = loop_begin
        while loop_loc < loop_end:
            if self.param_comp(codes[loop_loc]):
                complexity_tag[loop_begin] = CompStr("n")
                return 1
            loop_loc += 1
        complexity_tag[loop_begin] = CompStr("1")
        return 0

    def integrate_complexity(self, begin: int, end: int, indentation_structure: list, complexity_tag: list) -> CompStr:
        """
        整合complexity_tag上的复杂度标签
        :param begin:
        :param end:
        :param indentation_structure:
        :param complexity_tag:
        :return:
        """
        return CompStr("1")

    def param_comp(self, code_line: str):
        """
        检查一行声明中是否匹配列表或字典的添加模式
        列表/字典的匹配模式有以下两种：
        1. [^\\\\.]*[\\\\.]append
        2. [^[]*[[][^=]*=
        :param code_line: 一行代码
        :return:
        """
        return re.match("[^\\\\.]*[\\\\.]append" or "[^[]*[[][^=]*=", code_line) is not None


if __name__ == '__main__':
    t = SpaceChecker("space_comp_test.py")
    print(t.deal_with_file())
