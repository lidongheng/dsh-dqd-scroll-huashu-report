# dsh-dqd-scroll 华数报告

本仓库保存围绕 `dsh-dqd-scroll` v0.3.0 编写的项目报告和学习材料，面向有前端经验、正在学习 Python、Node.js 进程协作和 DSH 插件开发的读者。

## 学习路线

- [10 周独立开发学习路线（PDF）](learing-path.pdf)
- [学习路线源稿（Markdown）](learing-path.md)
- [学习路线网页预览（HTML）](learing-path.html)

学习路线从插件加载和 Python CLI 调用链开始，逐步覆盖 Node.js 文件操作、SQLite 数据流、跨进程调用、设置页与调度，最后以独立完成同类插件作为毕业项目。

## 项目报告

- [项目对比报告源稿（Markdown）](report.md)
- [项目对比报告网页预览（HTML）](report.html)
- [项目报告 PDF](report.pdf)
- [修订版项目报告 PDF](report-updated.pdf)

## 报告构建文件

`report-build/` 保存 Markdown 转换、HTML 排版和 PDF 渲染脚本，以及用于 Markdown 转换的 `marked` 发行文件。Playwright 依赖和临时版面检查图片不纳入版本控制。渲染脚本目前使用报告生成环境中的 Node.js、Python 和 Chrome 路径；克隆后如需重新构建 PDF，需要先按本机环境调整这些路径并安装 Playwright。

