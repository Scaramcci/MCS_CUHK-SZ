# CSC5041 Quiz 1 — LaTeX edition

四册内容：`main.tex` 中文笔记、`notes_en.tex` 英文笔记、`tutorial_answers.tex` Tutorial 1–2 答案、`practice_papers.tex` 两套英文模拟卷（无答案）。六个笔记章节保留原内容与来源，补充双语 TikZ 图；Tutorial 1 完整 ER 图横向排版。

模板改编自仓库 `templates/latex/报告模板.zip`：保留校徽、紫金配色、A4 页边距和页眉页脚。此为个人复习资料，不是学校官方试卷。

## 编辑与编译

直接编辑 `chapters/*.tex`，图见 `figures/diagrams.tex` 和两份 SVG，公共样式见 `study-preamble.tex`。XeLaTeX、latexmk 与 TeX Live 包需安装；当前字体使用 TeX Gyre Termes/Heros、Menlo、Songti SC、Hiragino Sans GB。

在本目录执行：

```sh
./build.sh
```

PDF 输出到相邻 `pdf/`；辅助文件与日志写入临时目录，脚本显示其路径。单册可执行 `latexmk -xelatex -outdir=/tmp/csc5041-build main.tex`。内置 LaTeX 编辑器打开本目录时默认选择中文笔记；本轮内置编译因沙盒无法访问系统 Menlo 字体失败，请使用已成功验证的本地 XeLaTeX 命令及输出 PDF。

## 从 Markdown 重新生成

原 Markdown、原 SVG 和共享 ZIP 均保留未改。需要从原稿重新转换时执行 `python3 prepare_sources.py`（依赖 Pandoc、rsvg-convert）；**会覆盖 `chapters/` 以及两份 SVG/PDF 图，不覆盖手绘 TikZ 图**。日常编辑 LaTeX 后直接编译即可。`source-manifest.json` 记录 Markdown 输入哈希。

本轮作者：主 Agent（转换、排版）与 latex_figures（九类双语图）。技术检查：独立 latex_verify；最终审查：独立 review_er02。最终检查状态与交付哈希见 `build-record.json`。这些是学习资料，无学校提交或上传操作。
