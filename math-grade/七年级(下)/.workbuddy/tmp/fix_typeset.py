# -*- coding: utf-8 -*-
"""一次性排版修复：分式基线、方程组花括号、几何角弧、直方图问号柱高度。
只做字符串级替换，逐项打印计数，任何一项计数不符即中止，不写文件。"""
import io, re, sys

OLD_CSS = '''.frac{display:inline-flex;flex-direction:column;vertical-align:-.42em;text-align:center;font-size:.92em;line-height:1.15;margin:0 3px}
.frac>span:first-child{border-bottom:1.2px solid currentColor;padding:0 4px 1px}
.frac>span:last-child{padding:1px 4px 0}'''

MASK = ("url(\"data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 20 100' preserveAspectRatio='none'%3E%3Cpath "
        "d='M18.5 2.5C10 9 8.6 19 8.6 33 8.6 45 7.4 48.6 2.5 50 7.4 51.4 8.6 55 8.6 67 8.6 81 10 91 18.5 97.5' "
        "fill='none' stroke='%23000' stroke-width='5.5'/%3E%3C/svg%3E\") left center/100% 100% no-repeat")

NEW_CSS = '''.frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.9em;line-height:1.12;margin:0 2px;position:relative;top:-.08em}
.frac>span:first-child{border-bottom:1.2px solid currentColor;padding:0 4px 1px}
.frac>span:last-child{padding:1px 4px 0}
.paren{font-size:1.3em;vertical-align:-.06em;line-height:1}
.sys{display:inline-flex;align-items:center;vertical-align:middle;margin:0 3px;line-height:1.3}
.sys::before{content:"";align-self:stretch;width:.44em;margin-right:2px;background:currentColor;-webkit-mask:__M__;mask:__M__}
.sys .rows{display:inline-flex;flex-direction:column;font-size:.95em;line-height:1.42}
.sys .rows>span{display:block;white-space:nowrap}'''.replace('__M__', MASK)

SYS_PAT = re.compile(r'\{ ([^{}<>]{2,70}?)，([^{}<>]{2,70}?) \}')

def fix_sys(s):
    out, n = [], 0
    pos = 0
    for m in SYS_PAT.finditer(s):
        a, b = m.group(1), m.group(2)
        if ';' in a or ':' in a or ';' in b or ':' in b or 'return' in a:
            continue
        out.append(s[pos:m.start()])
        out.append('<span class="sys"><span class="rows"><span>%s</span><span>%s</span></span></span>' % (a, b))
        pos = m.end(); n += 1
    out.append(s[pos:])
    return ''.join(out), n

def fix_paren(s):
    """把紧贴分式两侧的圆括号换成 .paren 放大版。"""
    n = 0
    while True:
        i = s.find('<span class="frac">')
        done = True
        start = 0
        while True:
            i = s.find('<span class="frac">', start)
            if i < 0:
                break
            # 找匹配的 </span>
            depth, j = 0, i
            while True:
                nxt_o = s.find('<span', j)
                nxt_c = s.find('</span>', j)
                if nxt_o != -1 and nxt_o < nxt_c:
                    depth += 1; j = nxt_o + 5
                else:
                    depth -= 1; j = nxt_c + 7
                    if depth == 0:
                        break
            before = s[:i]
            after = s[j:]
            neg = before.endswith('(−')
            if (neg or before.endswith('(')) and after.startswith(')'):
                lp = i - 1 if not neg else i - 2
                s = s[:lp] + '<span class="paren">' + s[lp:i] + '</span>' + s[i:j] + '<span class="paren">)</span>' + s[j + 1:]
                n += 1
                done = False
                break
            start = j
        if done:
            break
    return s, n

JOBS = {
    '七年级/0001-七年级(上).html': [],
    '七年级/0002-七年级(上).html': [],
    '七年级/0003-七年级(上).html': [],
    '七年级(下)/1001-七年级(下).html': [
        # 角弧：E 处 ∠AEF 60°、F 处 ∠CFE 120°，此前只画了 25°/30° 的一小段
        ('<path d="M 260.3 63.8 A 24 24 0 0 0 268.0 70.8"',
         '<path d="M 256.0 50.0 A 24 24 0 0 0 268.0 70.8"'),
        ('<path d="M 211.0 146.0 A 24 24 0 0 1 223.0 149.2"',
         '<path d="M 187.0 170.0 A 24 24 0 0 1 223.0 149.2"'),
        # 未标出的那一柱原本正好画在 40 的刻度线上（等于把答案画出来）
        ('<rect x="160" y="100" width="54" height="60"/>',
         '<rect x="160" y="112" width="54" height="48"/>'),
        ('<text x="187" y="130" font-size="14" fill="#b0302a" text-anchor="middle">?</text>',
         '<text x="187" y="142" font-size="14" fill="#b0302a" text-anchor="middle">?</text>'),
    ],
    '七年级(下)/1002-七年级(下).html': [],
    '七年级(下)/1003-七年级(下).html': [
        # 同上：4~6 小时这一柱原画在 20 的刻度线上，改成明显不对刻度的 18
        ('<rect x="222" y="40" width="58" height="120"/>',
         '<rect x="222" y="52" width="58" height="108"/>'),
        ('<text x="251" y="66" font-size="15" fill="#b0302a" text-anchor="middle">?</text>',
         '<text x="251" y="80" font-size="15" fill="#b0302a" text-anchor="middle">?</text>'),
    ],
}

ok = True
WRITE = '--write' in sys.argv
for path, pairs in JOBS.items():
    file_ok = True
    s = io.open(path, encoding='utf-8').read()
    orig_len = len(s)
    assert s.count(OLD_CSS) == 1, path + ' CSS 未命中'
    s = s.replace(OLD_CSS, NEW_CSS)
    s, nsys = fix_sys(s)
    s, npar = fix_paren(s)
    for old, new in pairs:
        c = s.count(old)
        if c != 1:
            print('!! %s 目标片段命中 %d 次: %s' % (path, c, old[:50])); file_ok = False; ok = False; continue
        s = s.replace(old, new)
    print('%-34s sys=%d paren=%d  长度 %d -> %d' % (path, nsys, npar, orig_len, len(s)))
    if file_ok and WRITE:
        io.open(path, 'w', encoding='utf-8').write(s)

print('RESULT:', 'OK' if ok else 'ABORT（未写入任何文件）')
sys.exit(0 if ok else 1)
