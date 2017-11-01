a, b, c = map(int, input().split())
D = b ** 2 - 4 * a * c
print((-b + D ** 0.5) / (2 * a))
print((-b - D ** 0.5) / (2 * a))
