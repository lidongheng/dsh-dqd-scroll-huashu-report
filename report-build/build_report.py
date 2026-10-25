import re;
import subprocess;
from html import escape;
from pathlib import Path;


ROOT = Path(__file__).resolve().parent.parent;
MARKED_SCRIPT = ROOT / 'report-build' / 'markdown_to_html.cjs';
MARKDOWN = ROOT / 'report.md';
OUTPUT = ROOT / 'report.html';
NODE = Path('C:/Program Files/nodejs/node.exe');


def toc_row(key: str, title: str, page: int) -> str:
    return f'<div class="toc-row"><span>{escape(title)}</span><span>{page}</span></div>';


TOC_ROWS = [
    toc_row('摘要', '摘要', 2),
    toc_row('第一幕', '第一幕｜两个项目共用宿主，Python 接法不同', 4),
    toc_row('第二幕', '第二幕｜从一条 Python 命令读懂 dsh-dqd-scroll', 8),
    toc_row('第三幕', '第三幕｜沿着现有结构增加一项功能', 11),
    toc_row('工具箱', '工具箱｜后续迭代时保留哪些判断', 14),
    toc_row('参考资料', '参考资料', 15),
];


def render() -> None:
    result = subprocess.run(
        [str(NODE), str(MARKED_SCRIPT), str(MARKDOWN)],
        check=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
    );
    html_body = result.stdout;
    blocks = re.split(r'(?=<h2>.*?</h2>)', html_body, flags=re.DOTALL);
    chapters = [block for block in blocks if re.match(r'<h2>', block)];
    if len(chapters) != len(TOC_ROWS):
        raise ValueError(f'章节目录数量不一致：正文 {len(chapters)}，目录 {len(TOC_ROWS)}');

    summary = chapters[0];
    toc_html = ''.join(TOC_ROWS);
    chapter_html = ''.join(
        '<table class="pagewrap"><thead><tr><td><div class="crumb">'
        + re.sub(r'<[^>]+>', '', chapter.split('</h2>', 1)[0])
        + ' | dsh-dqd-scroll 项目学习与扩展指南</div></td></tr></thead><tbody><tr><td class="chapter">'
        + chapter
        + '</td></tr></tbody></table>'
        for chapter in chapters[1:]
    );
    document = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>从 dsh-bili-scroll 到 dsh-dqd-scroll</title>
<link rel="stylesheet" href="report.css">
<link rel="stylesheet" href="report-extra.css">
</head>
<body>
<section class="cover">
  <div class="cover-grid"></div>
  <p class="eyebrow">PYTHON PROJECT FIELD GUIDE · 2026.10</p>
  <div class="cover-rule"></div>
  <h1>从 dsh-bili-scroll 到<br>懂球帝数据项目</h1>
  <p class="cover-subtitle">Python 初学者的项目对照与扩展指南</p>
  <p class="cover-thesis">保留插件编排边界，把平台数据能力落到可独立运行的 Python CLI。</p>
  <div class="cover-meta"><span>代码结构导读</span><span>面向 Python 初学者与前端开发者</span><span>2026-10-25</span></div>
  <div class="cover-foot"><span>已实现、离线支持与待核验的接口分开说明</span><span>01 / FIELD GUIDE</span></div>
</section>
<section class="abstract">{summary}</section>
<table class="pagewrap toc-page"><thead><tr><td><div class="crumb">目录 | dsh-dqd-scroll 项目学习与扩展指南</div></td></tr></thead><tbody><tr><td>
<h2>目录</h2>{toc_html}
</td></tr></tbody></table>
{chapter_html}
</body>
</html>''';
    OUTPUT.write_text(document, encoding='utf-8');


if __name__ == '__main__':
    render();
