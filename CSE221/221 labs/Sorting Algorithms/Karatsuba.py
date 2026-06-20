def karatsuba(x, y):
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y
    else:
        n = max(len(str(x)), len(str(y)))
        m = n // 2
        p = 10 ** m
        xh = x // 10 ** m
        xl = x % 10 ** m
        yh = y // 10 ** m
        yl = y % 10 ** m
        a = karatsuba(xh, yh)
        b = karatsuba(xl, yl)
        c = karatsuba(xh + xl, yh + yl)
        output = a * 10 ** (2 * m) + (c - a - b) * 10 ** m + b
        return output

x = karatsuba(1234, 5678)
print(x)
