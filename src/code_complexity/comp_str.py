import re


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

    def __gt__(self, other):
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
