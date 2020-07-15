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
        :return:
        """
        # 按乘法连接分离不同特征项
        a = self.value.split("*")
        b = other.value.split("*")

        # 定义字符串分析规则函数
        def analyze(p: str) -> tuple:
            has_A = False
            has_B = False
            A = ''
            B = ''
            for i in a:
                if re.match(p, i):
                    has_A = True
                    A = i
                    break
            for i in b:
                if re.match(p, i):
                    has_B = True
                    B = i
                    break
            return has_A, has_B, A, B

        # 查找n指数
        has_expA, has_expB, expA, expB = analyze("[0-9]*\\^n")
        if has_expA and has_expB:
            if int(expA[0]) > int(expB[0]):
                return 1
            else:
                return 0
        elif has_expA:
            return 1
        elif has_expB:
            return 0
        # 查找n幂函数
        has_powerA, has_powerB, powerA, powerB = analyze("n\\^[0-9]*")
        if has_powerA and has_powerB:
            if int(powerA[-1]) > int(powerB[-1]):
                return 1
            else:
                return 0
        elif has_powerA:
            return 1
        elif has_powerB:
            return 0
        # 查找n字符
        has_nA, has_nB, nA, nB = analyze("n")
        if has_nA and not has_nB:
            return 1
        elif has_nB and not has_nA:
            return 0
        # 查找n对数
        has_logA, has_logB, logA, logB = analyze("log_n")
        if has_logA and not has_logB:
            return 1
        elif has_logB and not has_logA:
            return 0
        # 所有匹配规则都失效
        return 0
