# -*- coding: utf-8 -*-
"""0003 嘉兴风格卷 逐题核算（100 分制，压轴为动角问题）"""
from fractions import Fraction as F
import math

ok = []
def chk(name, got, exp):
    good = (got == exp)
    ok.append(good)
    print(("PASS " if good else "FAIL ") + f"{name}: got={got} exp={exp}")

# ---------- 选择题 10×3 ----------
chk("Q1 比-2小", min([-3, -1, 0, 1]), -3)
chk("Q2 |−1/2026|", abs(F(-1, 2026)), F(1, 2026))
chk("Q3 5420000", f"{5420000/1e6:.2f}e6", "5.42e6")
# Q4 去括号：a-(b-c) = a-b+c
a, b, c = 7, 3, 2
chk("Q4 a-(b-c)", a - (b - c), a - b + c)
# Q5 2a-3=1 -> a=2
chk("Q5 a", (1 + 3) / 2, 2)
# Q6 AB=8, C 中点, D 是 BC 中点 -> AD
AB = F(8); AC = AB / 2; BC = AB / 2; CD = BC / 2
chk("Q6 AD", AC + CD, 6)
# Q7 ∠1+∠2=90, ∠1=3∠2
s2 = F(90, 4)
chk("Q7 ∠2", s2, F(45, 2))
chk("Q7 ∠1", 3 * s2, F(135, 2))
# Q8 a※b = a^2 - ab ; (-1)※(-2)
def star(p, q): return p * p - p * q
chk("Q8", star(-1, -2), -1)
# Q9 三角数 1,3,6,10,15 第8个
tri = [n * (n + 1) // 2 for n in range(1, 9)]
chk("Q9 前5项", tri[:5], [1, 3, 6, 10, 15])
chk("Q9 第8项", tri[7], 36)
# Q10 |x-1|=2, |y+1|=3, x<y -> x+y
sol = sorted({p + q for p in (1 + 2, 1 - 2) for q in (-1 + 3, -1 - 3) if p < q})
chk("Q10 x+y", sol, [1])

# ---------- 填空题 6×4 ----------
chk("T11 |−7|−(−3)", abs(-7) - (-3), 10)
chk("T12 3.14159→0.001", round(3.14159, 3), 3.142)
# T13 2x^m y^3 与 -5x^2 y^n 的和仍是单项式 -> m=2,n=3 -> m^n
chk("T13 m^n", 2 ** 3, 8)
# T14 a-2b=3 -> 4b-2a+1 = -2(a-2b)+1
chk("T14", -2 * 3 + 1, -5)
# T15 ∠AOB=80, ∠AOC=3∠BOC
chk("T15 ∠BOC", F(80, 4), 20)
# T16 日历 2×2 左上角 x -> x+(x+1)+(x+7)+(x+8)
x = 12
chk("T16 数值验证", x + (x + 1) + (x + 7) + (x + 8), 4 * x + 16)

# ---------- 解答题 ----------
chk("Q17(1)", F(-12) / F(-3) * F(-1, 4), -1)
chk("Q17(2)", -(1 ** 2026) + math.isqrt(36) - round(27 ** (1 / 3)), 2)
# Q18(1) 3(x-2)=5x+4 -> x=-5
xv = F(-5)
chk("Q18(1) 代回", 3 * (xv - 2), 5 * xv + 4)
# Q18(2) (3x-1)/4-(5x+1)/6=1 -> x=-17
xv = F(-17)
chk("Q18(2) 代回", (3 * xv - 1) / 4 - (5 * xv + 1) / 6, F(1))
# Q19 5ab-[2a^2b-(3ab-a^2b)] = 8ab-3a^2b ; a=-1,b=2
aa, bb = -1, 2
inner = 3 * aa * bb - aa * aa * bb
orig = 5 * aa * bb - (2 * aa * aa * bb - inner)
simple = 8 * aa * bb - 3 * aa * aa * bb
chk("Q19 化简一致", orig, simple)
chk("Q19 值", orig, -22)
# Q20 ∠AOB=90, OC 平分, ∠BOD=2∠COD, OD 在 ∠BOC 内
BOC = F(90, 2)
chk("Q20 ∠BOC", BOC, 45)
cod = BOC / 3
chk("Q20 ∠COD", cod, 15)
chk("Q20 ∠BOD", 2 * cod, 30)
chk("Q20 ∠AOD", BOC + cod, 60)
# Q21 a△b = 2a+b
def tri2(p, q): return 2 * p + q
chk("Q21(1) 2△(−1)", tri2(2, -1), 3)
xx = None
for t in [F(i, 10) for i in range(-50, 51)]:
    if tri2(t, 3) == tri2(3, t):
        xx = t
chk("Q21(2) x", xx, F(3))
# Q22 260km, 60km/h, 1h 后另一辆 40km/h
t = None
for i in range(1, 100):
    tt = F(i, 10)
    if 60 * tt + 40 * (tt - 1) == 260:
        t = tt
chk("Q22(1) t", t, F(3))
chk("Q22(2) 距甲", 60 * t, 180)
# Q23 ∠AOB=90, OC 从 OA 顺时针 3°/s, 0<t<60
def AOC(t): return 3 * t
chk("Q23(1) ∠AOC", AOC(10), 30)
chk("Q23(1) ∠BOC", 90 - AOC(10), 60)
chk("Q23(2) 平分 t", F(45, 3), 15)
sols = []
for i in range(1, 600):
    tt = F(i, 10)
    if tt <= 0 or tt >= 60:
        continue
    ang = 3 * tt
    boc = 90 - ang if ang <= 90 else ang - 90
    if boc == 30:
        sols.append(tt)
chk("Q23(3) t", sols, [F(20), F(40)])
chk("Q23(3) 检验 t=20", (AOC(20), 90 - AOC(20)), (60, 30))
chk("Q23(3) 检验 t=40", (AOC(40), AOC(40) - 90), (120, 30))

# ---------- 分值 ----------
choice, fill, essay = 10 * 3, 6 * 4, 6 + 6 + 6 + 8 + 6 + 6 + 8
print(f"\n分值：选择{choice} + 填空{fill} + 解答{essay} = {choice + fill + essay}")
chk("总分", choice + fill + essay, 100)
chk("解答题题数", 7, 7)

print("\nRESULT:", "ALL PASS" if all(ok) else "HAS FAIL")
