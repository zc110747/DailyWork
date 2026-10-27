# -*- coding: utf-8 -*-
"""把正文（<body> 到 <script> 之间）里包住中文的英文直引号改成中文引号。
只处理标签之外的文字节点，且排除含 {} ; : < > 的内容，避免误伤 CSS/JS。"""
import io, re, glob

PAT = re.compile(r'"([^"]{1,40})"')

def cn(t):
    return re.search(r'[\u4e00-\u9fa5]', t) is not None

def bad(t):
    return re.search(r'[{};:<>"]', t) is not None

for p in sorted(glob.glob('七年级/*.html')) + sorted(glob.glob('七年级(下)/*.html')):
    s = io.open(p, encoding='utf-8').read()
    b = s.index('<body')
    e = s.index('<script>')
    head, body, tail = s[:b], s[b:e], s[e:]
    parts = re.split(r'(<[^>]+>)', body)
    n = 0
    for i in range(0, len(parts), 2):
        def rep(m):
            global n
            t = m.group(1)
            if cn(t) and not bad(t):
                n += 1
                return '“' + t + '”'
            return m.group(0)
        parts[i] = PAT.sub(rep, parts[i])
    out = head + ''.join(parts) + tail
    io.open(p, 'w', encoding='utf-8').write(out)
    css_ok = '"Times New Roman"' in head
    print('%-34s 引号替换 %3d 处 | CSS 直引号完好=%s | “%d ”%d' % (
        p.split('\\')[-1], n, css_ok, out.count('“'), out.count('”')))
