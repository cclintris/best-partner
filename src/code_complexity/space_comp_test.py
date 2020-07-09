def const1():
    # 常数级别复杂度
    a = 1
    return a


def const2():
    # 多个常数的分配
    a = 1
    b = 2
    c = 3
    d = a + b + c
    return d


def list1(n: int) -> list:
    # 带有列表的循环添加的复杂度: O(n)
    a = []
    for i in range(n):
        a.append(i)
    return a


def list2(s: str) -> list:
    # 带有字符串处理的列表复杂度: O(1)
    s = s.split(' ')
    for i in s:
        s += ' '
    return s


def loop(n):
    # 多重循环带来的复杂度处理：O(n^x)
    a = []
    for i in range(n):
        a.append([' ' for j in range(n)])
    return a


def fibonacci(n):
    # 递归函数循环压栈的复杂度处理：O(1)
    if n < 1:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


print(list1(5))
print(fibonacci(5))
print(loop(5))
