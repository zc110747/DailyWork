# -*- coding: utf-8 -*-
"""角弧审计：SVG 里所有 `M x y A r r ... x2 y2` 弧线，
两端点必须落在以某个"顶点"为圆心、半径 r 的圆上。
顶点取自：line 端点、circle 圆心、polygon 顶点。
半径偏差 > 1.5px 视为绘制错误（端点写错 -> 弧被 SVG 自动缩放而漂移）。
"""
import io, re, glob, math

ARC = re.compile(r'M\s*([\d.]+)\s+([\d.]+)\s+A\s*([\d.]+)\s+([\d.]+)\s+\d\s+\d\s+\d\s+([\d.]+)\s+([\d.]+)')
LINE = re.compile(r'<line\s+x1="([\d.]+)"\s+y1="([\d.]+)"\s+x2="([\d.]+)"\s+y2="([\d.]+)"')
CIRC = re.compile(r'<circle\s+cx="([\d.]+)"\s+cy="([\d.]+)"')
POLY = re.compile(r'<polygon\s+points="([^"]+)"')

def vertices(svg):
    pts = []
    for m in LINE.finditer(svg):
        x1, y1, x2, y2 = map(float, m.groups())
        pts += [(x1, y1), (x2, y2)]
    for m in CIRC.finditer(svg):
        pts.append((float(m.group(1)), float(m.group(2))))
    for m in POLY.finditer(svg):
        nums = list(map(float, re.split(r'[ ,]+', m.group(1).strip())))
        pts += list(zip(nums[0::2], nums[1::2]))
    return pts

bad = 0
for path in sorted(glob.glob('七年级/*.html')) + sorted(glob.glob('七年级(下)/*.html')):
    s = io.open(path, encoding='utf-8').read()
    for m in ARC.finditer(s):
        x1, y1, r, r2, x2, y2 = map(float, m.groups())
        # 找到所在 svg 的顶点集合
        sv_start = s.rfind('<svg', 0, m.start())
        sv_end = s.find('</svg>', m.start())
        svg = s[sv_start:sv_end]
        vs = vertices(svg)
        best = None
        for (cx, cy) in vs:
            d1 = abs(math.hypot(x1 - cx, y1 - cy) - r)
            d2 = abs(math.hypot(x2 - cx, y2 - cy) - r)
            if best is None or d1 + d2 < best[0]:
                best = (d1 + d2, cx, cy, d1, d2)
        tag = ''
        if best is None:
            tag = 'NO VERTEX'
        elif max(best[3], best[4]) > 1.5:
            tag = 'BAD d1=%.1f d2=%.1f' % (best[3], best[4])
        if tag:
            bad += 1
            ctx = re.sub(r'<[^>]+>', '', s[max(0, m.start() - 400):sv_start])[-40:]
            print('%-30s %-22s %s' % (path.split('/')[-1], tag, m.group(0)[:60]))
            print('      近旁文字: ...%s' % ctx.strip().replace('\n', ' ')[-30:])
print('RESULT:', 'ALL ARCS OK' if bad == 0 else '%d 处弧线端点异常' % bad)
