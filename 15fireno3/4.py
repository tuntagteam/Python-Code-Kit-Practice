import itertools

def solve24(nums):
    ops = ['+', '-', '*', '/']
    # สร้างกรอบวงเล็บ 5 แบบสำหรับ 4 ตัวแปร a,b,c,d
    patterns = [
        '(({a}{op1}{b}){op2}{c}){op3}{d}',
        '({a}{op1}({b}{op2}{c})){op3}{d}',
        '{a}{op1}(({b}{op2}{c}){op3}{d})',
        '{a}{op1}({b}{op2}({c}{op3}{d}))',
        '({a}{op1}{b}){op2}({c}{op3}{d})'
    ]
    # ลองทุก permutation ของตัวเลข และทุก combination ของเครื่องหมาย
    for a, b, c, d in itertools.permutations(nums):
        for op1, op2, op3 in itertools.product(ops, repeat=3):
            for pat in patterns:
                expr = pat.format(a=a, b=b, c=c, d=d, op1=op1, op2=op2, op3=op3)
                try:
                    if abs(eval(expr) - 24) < 1e-6:
                        return expr
                except ZeroDivisionError:
                    continue
    return None

if __name__ == '__main__':
    nums = list(map(float, input().split()))
    result = solve24(nums)
    if result:
        print(result + " = 24")
    else:
        print("ไม่สามารถทำได้")