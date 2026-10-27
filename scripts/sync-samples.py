#!/usr/bin/env python3
"""从 Org 书稿同步明确选择的试读篇章，不发布完整版。"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

SITE = Path(__file__).resolve().parents[1]
PUBLIC_SAMPLES = {'kongjing', 'breath_gap', 'piquan_quanjia'}
SAMPLES = [
    ('kongjing', '空空静静', '从整体受力与心神觉察，进入作者对“空”和“静”的讨论。', 10),
    ('zhonghe', '中和之道', '从“无过无不及”与“临界态”的体会，理解书中的中和之道。', 20),
    ('yiqi', '先天真一之炁', '从伸懒腰、顺伸逆缩与日用体会，理解作者所说的中和之气。', 30),
    ('breath_gap', '呼吸互含气住脉停', '从内外呼吸与“气口”，理解作者对“呼吸互含，气住脉停”的解释。', 40),
    ('piquan_quanjia', '要做神仙需练劈拳', '从起钻落翻与以外带内，理解作者对孙氏劈拳拳架与练法的讨论。', 50),
]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--book-root', type=Path, default=SITE.parent / 'martial_art')
parser.add_argument('--only', nargs='+', choices=[item[0] for item in SAMPLES], help='仅同步指定试读，避免覆盖其它网页内容')
args = parser.parse_args()
pandoc = os.environ.get('PANDOC') or shutil.which('pandoc')
if not pandoc:
    raise SystemExit('需要 Pandoc；请安装后重试，或设置 PANDOC=/path/to/pandoc。')
book = args.book_root.resolve()
for slug, title, summary, weight in SAMPLES:
    if args.only and slug not in args.only:
        continue
    source = book / 'content' / (slug + '.org')
    original = source.read_text()
    # 网页不携带印刷指令；正文、脚注、图注通过 Pandoc 转换。
    original = re.sub(r'^#\+ATTR_LATEX:.*\n?', '', original, flags=re.M | re.I)
    original = re.sub(r'^#\+LATEX:.*\n?', '', original, flags=re.M | re.I)
    original = re.sub(r'^#\+BEGIN_EXPORT latex\s*\n.*?^#\+END_EXPORT\s*$', '', original, flags=re.M | re.S | re.I)
    # 未公开章节只保留书名，不能生成 Org 内部链接。
    original = re.sub(r'\[\[id:[^\]]+\]\[([^\]]+)\]\]', r'\1（见全书对应章节）', original)
    used = []
    def image_link(match):
        name = match.group(1)
        src = book / 'content' / 'img' / name
        if not src.is_file():
            raise SystemExit('图片不存在：' + str(src))
        dst = SITE / 'static' / 'images' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if shutil.which('magick'):
            subprocess.run(['magick', str(src), '-resize', '1100x1100>', '-strip', str(dst)], check=True)
        else:
            shutil.copy2(src, dst)
        used.append(name)
        return '[[/images/' + name + ']]'
    original = re.sub(r'\[\[file:img/([^\]]+)\]\]', image_link, original)
    result = subprocess.run([pandoc, '--from=org', '--to=markdown', '--wrap=none'], input=original, text=True, capture_output=True, check=True)
    text = result.stdout.replace("file:///images/", "/images/")
    # Pandoc 图片属性改为普通 Markdown，便于 Hugo Goldmark 解析。
    text = re.sub(r'(!\[[^\]]*\]\([^\n]+?\))\{[^\n]*\}', r'\1', text)
    text = re.sub(r'(?m)^\[([^\]]+)\]\{[^\n]*\}$', r'\1', text)
    front = {'title':title, 'description':summary, 'summary':summary, 'weight':weight, 'ShowToc':False}
    if slug not in PUBLIC_SAMPLES:
        front['draft'] = True
    if slug == 'yiqi':
        front['aliases'] = ['/read/zidongpingheng/']
    notice = '> **试读说明**：选自《不正经拳论》，风茂著。下文保留作者的论述与个人体会。\n\n'
    (SITE/'content'/'read'/(slug+'.md')).write_text(json.dumps(front, ensure_ascii=False, indent=2)+'\n\n'+notice+text)
    print('已同步：'+title+'（图片 '+str(len(used))+' 张）')
