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
        1. 以input()函数为基准，将输入的数据作为列表项储存的时候复杂度为O(n)
        2. 输入数据不做储存仅做声明时，将复杂度视为O(1)
        3. 最终的空间复杂度为所有的列表项、字典项储存的最大数据量
        :param main_codes:
        :return:
        """
        return 0

    def integrate_complexity(self, begin: int, end: int, indentation_structure: list, complexity_tag: list):
        return 0

    def get_param_type(self, code_line: str):
        """
        在一行声明当中获取所声明变量类型的复杂度级别：常数或n级数
        1. 声明项不在参数列表中时，如为常量，标记为O(1),如为列表项或字典项，标记为O(n)
        2. 声明项已经存在于参数列表中时，不做任何变动
        :param code_line: 一行代码
        :return:
        """
        if not code_line.count('='):
            return 0
        code_line = code_line.split('=')

        return 0
