import re
from complexity import Checker
from comp_str import CompStr


class SpaceChecker(Checker):

    def cal_method_complexity(self, method, method_begin, method_end):
        """
        计算代码空间复杂度的方法，该方法的计算思路如下：
        1. 任意无循环添加列表的变量均被视为O(1)，包括递归
        2. 含有任意循环添加的空间复杂度被视为O(n^x)
        3. 忽略任何可能出现的条件筛选/二分法导致的添加并视为O(1)
        4. 对出现的递归调用，将该方法的复杂度增加O(n):n次压栈
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
                is_match = self.param_match(word, method_line)
                if is_match:
                    j = i + 1
                    while j < method_end and self.indentation_structure[i] < \
                            self.indentation_structure[j]:
                        j += 1
                    self.deal_loop(word, i, j, self.codes, self.complexity_tag)
            # 扫描是否是自递归方法
            is_recursion = re.search(method, method_line)
            if is_recursion:
                deal_recursion = True
        res = self.integrate_complexity(method_begin, method_end, self.indentation_structure, self.complexity_tag)
        if deal_recursion:
            return res * CompStr("n")
        else:
            return res

    def deal_loop(self, loop_type: str, loop_begin: int, loop_end: int, codes: list, complexity_tag: list):
        """
        处理循环结构对空间复杂度的影响，该方法思路如下：
        1. 出现循环关键字时，扫描该循环下的所有行并调用param_comp，直到缩进树上浮/终止
        2. 扫描的所有行中，param_comp返回True，即包含列表/字典的添加动作，标记为O(n)
        3. 不含有2中所描述的操作时，标记为O(1)
        :param loop_type: 循环的种类
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

    @staticmethod
    def param_comp(code_line: str):
        """
        检查一行声明中是否匹配列表或字典的添加模式
        列表/字典的匹配模式有以下两种：
        1. [^\\\\.]*[\\\\.]append
        2. [^[]*[[][^=]*=
        :param code_line: 一行代码
        :return:
        """
        return re.match("[^\\\\.]*[\\\\.]append", code_line) is not None or re.match("[^\\[]*\\[[^=]*=",
                                                                                     code_line) is not None

    @staticmethod
    def param_match(loop_type: str, code_line: str) -> bool:
        return re.match(loop_type, code_line) is not None or re.search(" " + loop_type + " ", code_line) is not None


if __name__ == '__main__':
    # t = SpaceChecker("../../test/space_comp_test.py")
    t = SpaceChecker("mini_test.py")
    print(t.deal_with_file())
