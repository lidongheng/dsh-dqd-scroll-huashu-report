import re;
import subprocess;
from html import escape;
from pathlib import Path;


ROOT = Path(__file__).resolve().parent.parent;
MARKED_SCRIPT = ROOT / 'report-build' / 'markdown_to_html.cjs';
MARKDOWN = ROOT / 'learing-path.md';
OUTPUT = ROOT / 'learing-path.html';
NODE = Path('C:/Program Files/nodejs/node.exe');
REPORT_TITLE = 'dsh-dqd-scroll 独立开发学习路线';


def toc_row(key: str, title: str, page: int) -> str:
    return f'<div class="toc-row" data-key="{escape(key)}"><span>{escape(title)}</span><span>{page}</span></div>';


TOC_ROWS = [
    toc_row('摘要', '摘要', 2),
    toc_row('第一幕', '第一幕｜先把眼前这条调用链看明白', 4),
    toc_row('第二幕', '第二幕｜10 周学习路线：从读懂到能改', 6),
    toc_row('第三幕', '第三幕｜毕业项目：从空目录独立做出同类插件', 14),
    toc_row('工具箱', '工具箱｜以后遇到陌生项目就问这六个问题', 15),
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
        + ' | 独立开发学习路线</div></td></tr></thead><tbody><tr><td class="chapter">'
        + chapter
        + '</td></tr></tbody></table>'
        for chapter in chapters[1:]
    );
    document = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{REPORT_TITLE}</title>
<link rel="stylesheet" href="report.css">
<link rel="stylesheet" href="report-extra.css">
<link rel="stylesheet" href="report-build/learning-path.css">
</head>
<body>
<section class="cover learning-cover">
  <div class="cover-grid"></div>
  <p class="eyebrow">PYTHON + NODE.JS PROJECT ROADMAP · 2026.10</p>
  <div class="cover-rule"></div>
  <h1>从看懂 dsh-dqd-scroll<br>到独立做出同类插件</h1>
  <p class="cover-subtitle">给前端开发者的 10 周项目学习路线</p>
  <p class="cover-thesis">从你现在卡住的调用链出发，逐步学会自己划分目录、进程、数据与插件边界。</p>
  <div class="cover-meta"><span>约 60–80 小时</span><span>从离线 SQLite 路径到 DSH 插件</span><span>2026-10-25</span></div>
  <div class="cover-foot"><span>代码阅读、练习任务、毕业项目与验收标准</span><span>01 / LEARNING PATH</span></div>
</section>
<section class="abstract">{summary}</section>
<table class="pagewrap toc-page"><thead><tr><td><div class="crumb">目录 | 独立开发学习路线</div></td></tr></thead><tbody><tr><td>
<h2>目录</h2>{toc_html}
</td></tr></tbody></table>
{chapter_html}
</body>
</html>''';
    OUTPUT.write_text(document, encoding='utf-8');


if __name__ == '__main__':
    render();
