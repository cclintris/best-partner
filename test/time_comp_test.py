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


def binary_search(n, arr, target):
    # O(log_n)
    left = 0
    right = n
    mid = (left + right) // 2
    while left < right:
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid
        else:
            right = mid
        mid = (left + right) // 2


def search_bs_06():
    # O(n)
    def can_ship(w: list, d: int, lim: int) -> bool:
        cur = lim
        for weight in w:
            if weight > lim:
                return False
            if cur < weight:
                cur = lim
                d -= 1
            cur -= weight
        return d > 0

    weights = list(map(int, input()[1:-1].split(",")))
    D = int(input())
    totalWeight = sum(weights)
    limit = 0
    while limit < totalWeight:
        mid = (limit + totalWeight) // 2
        if can_ship(weights, D, mid):
            totalWeight = mid
        else:
            limit = mid + 1
    print(limit)


def arr_dp_31():
    # O(n^2)
    K = int(input())
    N = int(input())
    dp = [[0 for i in range(N + 1)] for j in range(K + 1)]
    m = 0
    while dp[K][m] < N:
        m += 1
        for k in range(K + 1):
            dp[k][m] = dp[k][m - 1] + dp[k - 1][m - 1] + 1
    print(m)


def serial_dp_23():
    # O(n^3)
    def dp(g: list, k: int, n: int, p: int) -> int:
        # O(n)
        if n < len(g):
            if k == 0:
                return 0
            else:
                ans = 0
                for i in range(p, len(g[n])):
                    if grid[n][i] > 0:
                        ans = max(ans, dp(g, k - 1, i + 1, i + 1) + g[n][i])
                return ans
        else:
            return 0

    T = int(input())
    for t in range(T):
        K = int(input())
        N = int(input())
        arr = list(map(int, input().split()))
        grid = [[0 for i in range(N)] for j in range(N - 1)]
        for i in range(N - 1):
            for j in range(i + 1, N):
                grid[i][j] = arr[j] - arr[i]
        print(dp(grid, K, 0, 0))


print(fibonacci(5))
print(loop1(5))
print(loop3(5))
