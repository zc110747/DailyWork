# -*- coding: utf-8 -*-
"""六个文件的通用结构校验：标签配对、题号连续、分值分桶、selfscore 与 data-score 一致。"""
import io, re, glob

VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'path', 'line', 'circle', 'rect',
        'polygon', 'polyline', 'use', 'stop', 'ellipse', 'source', 'col'}

def check(p):
    s = io.open(p, encoding='utf-8').read()
    body = s[s.index('<body'):]
    stack, bad = [], []
    for m in re.finditer(r'<(/?)([a-zA-Z][\w]*)([^>]*?)(/?)>', body):
        close, tag, _, selfc = m.groups()
        tag = tag.lower()
        if tag in VOID or selfc or tag in ('html', 'body'):
            continue
        if not close:
            stack.append(tag)
        else:
            if stack and stack[-1] == tag:
                stack.pop()
            else:
                bad.append(tag)

    nums = [int(x) for x in re.findall(r'<span class="q-num">(\d+)\.</span>', body)]
    seq_ok = nums == list(range(1, len(nums) + 1))

    buckets = {}
    for tag in re.findall(r'<div class="q"[^>]*>', body):
        t = re.search(r'data-type="(\w+)"', tag)
        v = re.search(r'data-score="(\d+)"', tag)
        if t and v:
            buckets[t.group(1)] = buckets.get(t.group(1), 0) + int(v.group(1))
    total = sum(buckets.values())

    starts = [(m.start(), int(m.group(1))) for m in
              re.finditer(r'<div class="q" data-type="essay" data-score="(\d+)">', body)]
    ss_bad = 0
    for i, (pos, sc) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(body)
        m = re.search(r'class="selfscore" min="0" max="(\d+)" data-max="(\d+)"', body[pos:end])
        if not m or int(m.group(1)) != sc or int(m.group(2)) != sc:
            ss_bad += 1

    n_opt = body.count('class="opt"')
    n_bi = body.count('class="bi"')
    n_ans = body.count('<div class="ans">')
    score_str = '+'.join(str(buckets[k]) for k in ('choice', 'blank', 'essay') if k in buckets)
    residue = len(stack) + len(bad)
    ok = residue == 0 and seq_ok and ss_bad == 0
    extra = '' if residue == 0 else (' 未闭合:' + ','.join(stack) + ' 多余闭合:' + ','.join(bad))
    print('%-22s 残留=%d%s 题号=%s(%d) 分值=%s=%d self异常=%d 选项=%d 填空=%d 解析=%d  %s'
          % (p.split('\\')[-1], residue, extra, 'OK' if seq_ok else 'BAD', len(nums),
             score_str, total, ss_bad, n_opt, n_bi, n_ans, 'OK' if ok else 'FAIL'))
    return ok

ok = True
for p in sorted(glob.glob('七年级/*.html')) + sorted(glob.glob('七年级(下)/*.html')):
    ok = check(p) and ok
print('RESULT:', 'ALL OK' if ok else 'HAS FAIL')
