import re
from Complexity import Checker
from Complexity import CompStr
from collections import defaultdict


class SpaceChecker(Checker):
    def __init__(self, filepath):
        Checker.__init__(self, filepath)
        self.param_list = defaultdict(CompStr)

    def cal_method_complexity(self, method, method_begin, method_end):
        """
        计算代码空间复杂度的方法，该方法的计算思路如下：
        1. 任意无循环添加列表的变量均被视为O(1)，包括递归
        2. 含有任意循环添加的空间复杂度被视为O(n^x)
        3. 忽略任何可能出现的条件筛选/二分法导致的添加并视为O(1)
        :param method:
        :param method_begin:
        :param method_end:
        :return:
        """
        return 0

    def cal_main_complexity(self, main_codes):
        """
        计算代码main函数空间复杂度的方法，该方法的计算思路如下：
        1. 以input()函数为基准，将输入的数据作为列表项储存/作为列表长度声明的时候复杂度为O(n)
        2. 输入数据不做储存仅做声明时，将复杂度视为O(1)
        3. 最终的空间复杂度为所有的列表项、字典项储存的最大数据量
        :param main_codes:
        :return:
        """
        return 0

    def deal_loop(self, loop_index: int, codes: list, indentation_structure: list, complexity_tag: list):
        """
        处理循环结构对空间复杂度的影响，该方法思路如下：
        1. 出现循环关键字时，扫描该循环下的所有行并调用param_comp，直到缩进树上浮/终止
        2. 扫描的所有行中，param_comp返回True，即包含列表/字典的添加动作，标记为O(n)
        3. 不含有2中所描述的操作时，标记为O(1)
        :param loop_index: 循环开始的位置
        :param codes: 要检查的代码样本
        :param indentation_structure: 代码的缩进树
        :param complexity_tag: 代码的复杂度标签
        :return:
        """
        loop_loc = loop_index
        while True:
            if self.param_comp(codes[loop_loc]):
                complexity_tag[loop_index] = CompStr("n")
                return 1
            loop_loc += 1
            if loop_loc >= len(codes) or indentation_structure[loop_loc] <= indentation_structure[loop_index]:
                complexity_tag[loop_index] = CompStr("1")
                return 0

    def integrate_complexity(self, begin: int, end: int, indentation_structure: list, complexity_tag: list):
        """
        整合complexity_tag上的复杂度标签
        :param begin:
        :param end:
        :param indentation_structure:
        :param complexity_tag:
        :return:
        """
        return 0

    def param_comp(self, code_line: str):
        """
        检查一行声明中是否匹配列表或字典的添加模式
        列表/字典的匹配模式有以下两种：
        1. [^\\\\.]*[\\\\.]append
        2. [^[]*[[][^=]*=
        :param code_line: 一行代码
        :return:
        """
        return re.match("[^\\\\.]*[\\\\.]append", code_line) or re.match("[^[]*[[][^=]*=", code_line)


if __name__ == '__main__':
    t = SpaceChecker("space_comp_test.py")
    print(t.deal_with_file())
