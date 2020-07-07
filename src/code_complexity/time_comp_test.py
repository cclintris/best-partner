def loop1(n):
    # 普通的一层循环
    ans = 0
    for i in range(n):
        ans += 1
    return ans


def loop_1ex(n: int) -> int:
    # python3限定类型的一层循环
    ans = 0
    for i in range(n):
        ans -= 1
    return ans


def loop2(n):
    # 普通的单参数二层循环
    ans = 0
    for i in range(n):
        for j in range(n):
            ans += 1
    return ans


def loop_2ex(n, m):
    # 普通的双参数二层循环
    ans = 0
    for i in range(n):
        for j in range(m):
            ans += 1
    return ans


def loop3(n):
    # 普通的三层循环
    ans = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ans += 1
    return ans


def loop_3ex(n, m, p):
    # 普通的三参数三层循环
    ans = 0
    for i in range(n):
        for j in range(m):
            for k in range(p):
                ans += 1
    return ans


def fibonacci(n):
    # 斐波那契数列
    if n < 1:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(5))
