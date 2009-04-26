'''number conversion for enumerated_list'''


from roman import toRoman


def to_arabic(n):
    return str(n)

def to_loweralpha(n):
    digits = []
    while n:
        digits.append(n % 26)
        n = n // 26
    result = ''
    digits.reverse()
    for d in digits:
        result += chr(d+96)
    return result

def to_upperalpha(n):
    return to_loweralpha(n).upper()

def to_lowerroman(n):
    return toRoman(n).lower()

def to_upperroman(n):
    return toRoman(n)


