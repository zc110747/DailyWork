# -*- coding: utf-8 -*-
"""三卷结构校验：标签配对 / 题号连续 / 分值 / selfscore / SVG 数值 / 关键答案"""
import io, re, sys
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.depth_max = 0
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        self.stack.append((tag, self.getpos()))
        self.depth_max = max(self.depth_max, len(self.stack))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errors.append('多余的 </%s> @%s' % (tag, self.getpos())); return
        top, pos = self.stack.pop()
        if top != tag:
            self.errors.append('标签不配对：期望 </%s>(%s) 实得 </%s> @%s' % (top, pos, tag, self.getpos()))

JOBS = [
    ('1001-七年级(下).html', 24, 30, 24, 66, 120, 8),
    ('1002-七年级(下).html', 22, 30, 24, 46, 100, 6),
    ('1003-七年级(下).html', 23, 30, 24, 46, 100, 7),
]

allfail = 0
for page, nq_total, c_sc, b_sc, e_sc, total, n_essay in JOBS:
    s = io.open(page, encoding='utf-8').read()
    print('=' * 24, page)

    # 1) 标签配对
    ck = Checker(); ck.feed(s)
    if ck.stack:
        ck.errors.append('未闭合：%s' % [t for t, _ in ck.stack])
    print('  标签配对 : %s (最大嵌套 %d)' % ('OK' if not ck.errors else 'FAIL', ck.depth_max))
    for e in ck.errors[:6]:
        print('     -', e); allfail += 1

    # 2) 题号连续
    nums = [int(x) for x in re.findall(r'<span class="q-num">(\d+)\.</span>', s)]
    ok = nums == list(range(1, nq_total + 1))
    print('  题号连续 : %s %s' % ('OK' if ok else 'FAIL', '' if ok else nums))
    if not ok: allfail += 1

    # 3) 分值
    choice = sum(int(x) for x in re.findall(r'data-type="choice" data-score="(\d+)"', s))
    blank  = sum(int(x) for x in re.findall(r'data-type="blank" data-score="(\d+)"', s))
    essay  = sum(int(x) for x in re.findall(r'data-type="essay" data-score="(\d+)"', s))
    ok = (choice, blank, essay) == (c_sc, b_sc, e_sc) and choice + blank + essay == total
    print('  分值     : %s %d + %d + %d = %d (应为 %d)' % ('OK' if ok else 'FAIL', choice, blank, essay, choice+blank+essay, total))
    if not ok: allfail += 1

    # 4) 每道解答题的 selfscore 与 data-score 一致
    foot = s.index('<div class="foot">')
    starts = [(m.start(), int(m.group(1))) for m in re.finditer(r'<div class="q" data-type="essay" data-score="(\d+)">', s)]
    bad = []
    for i, (pos, sc) in enumerate(starts):
        end = starts[i+1][0] if i+1 < len(starts) else foot
        ss = re.search(r'selfscore" min="0" max="(\d+)" data-max="(\d+)"', s[pos:end])
        if not ss or not (sc == int(ss.group(1)) == int(ss.group(2))):
            bad.append((i+1, sc, ss.groups() if ss else None))
    print('  selfscore: %s (%d 道)' % ('OK' if not bad and len(starts) == n_essay else 'FAIL', len(starts)))
    if bad or len(starts) != n_essay:
        print('     -', bad); allfail += 1

    # 5) SVG 数值合法性：不能有 NaN/inf/undefined，viewBox 内坐标
    svgs = re.findall(r'<svg\b[^>]*viewBox="0 0 ([\d.]+) ([\d.]+)"[^>]*>(.*?)</svg>', s, re.S)
    print('  SVG 数量 : %d' % len(svgs))
    for i, (vw, vh, inner) in enumerate(svgs, 1):
        prob = []
        if re.search(r'NaN|Infinity|undefined|null', inner):
            prob.append('含非法值')
        # 提取所有数值属性，检查是否远超出画布
        for attr, vals in re.findall(r'(x|y|x1|y1|x2|y2|cx|cy|r|width|height|points|d)="([^"]*)"', inner):
            nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', vals)]
            if attr == 'points':      # points 同时含 x、y，用两轴的较大者做上界
                lim = max(float(vw), float(vh)) * 1.15
            else:
                lim = (float(vw) if attr in ('x','x1','x2','cx','width') else float(vh)) * 1.15
            for v in nums:
                if abs(v) > lim and attr != 'd':
                    prob.append('%s=%s 超界' % (attr, v))
                    break
        if prob:
            print('     SVG#%d (%sx%s): %s' % (i, vw, vh, '; '.join(prob))); allfail += 1
    if not svgs:
        print('     - 未找到 SVG')

    # 6) 关键文本抽查
    keys = {
        '1001-七年级(下).html': ['无解', 'a + b = 4', '同旁内角', '5700', '490', 'a = 6，b = 4'],
        '1002-七年级(下).html': ['m = 7', 'x = 5，y = −1', '15.3', 'x = 2', '30°', '(a − b)(a − b − 4)'],
        '1003-七年级(下).html': ['x = 2', 'xy(x + 2y)(x − 2y)', 'a = 3', '384', '不能达到'],
    }[page]
    miss = [k for k in keys if k not in s]
    print('  关键内容 : %s %s' % ('OK' if not miss else 'FAIL', '' if not miss else miss))
    if miss: allfail += 1

    # 7) 题干长度体检：解答题题干（q-text）过长会挤行
    for m in re.finditer(r'<div class="q" data-type="essay"[^>]*>\s*<div class="q-head"><span class="q-num">(\d+)\.</span><span class="q-text">(.*?)</span><span class="tag">', s, re.S):
        txt = re.sub(r'<[^>]+>', '', m.group(2))
        if len(txt) > 75:
            print('     题干偏长 Q%s: %d 字' % (m.group(1), len(txt)))

print()
print('FAIL 总数: %d' % allfail)
print('RESULT: ' + ('ALL OK' if allfail == 0 else 'NEED FIX'))
