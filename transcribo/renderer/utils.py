
'''number conversion for enumerated_list'''


from roman import toRoman


def to_arabic(n):
    return unicode(n)


def to_loweralpha(n):
    digits = []
    while n:
        digits.append(chr((n % 26) + 96))
        n = n // 26
    digits.reverse()
    return unicode(''.join(digits))


def to_upperalpha(n):
    return to_loweralpha(n).upper()

def to_lowerroman(n):
    return toRoman(n).lower()

def to_upperroman(n):
    return toRoman(n)
