# HW06: Probabilistic Reasoning

- 教师原件：[requirements/Prob-Reasoning HomeWork.pdf](requirements/Prob-Reasoning%20HomeWork.pdf)，共 7 页，每页一题，已逐页提取并查看渲染图。
- 解答：[report/answers.pdf](report/answers.pdf)，4 页简洁英文答案，延续 hw05 格式；可编辑源文件：[report/answers.tex](report/answers.tex)。
- 覆盖：多项分布与 Laplace 平滑、Bayes 公式、朴素贝叶斯、转移频率估计、连续晴天概率、两个贝叶斯网络的参数与推断。
- 第 1 题没有给用于 add-one 平滑的样本量：答案保留 N 的一般公式，并明确标注 N=100 的示例假设。第 5 题保留任意初始分布公式，并给出平稳情形的数值。若教师有补充，应按补充更新。
- 原件未说明截止时间、提交格式、文件名、页数、答案语言或 AI 使用限制。英文/PDF 是参照以往作业选择的解答形式，不能据此推断教师提交要求。
- 自查已完成；独立审查结论见 [notes/review.md](notes/review.md)（由 Reviewer 创建）。未上传、未提交 Git，未生成学校提交包。

从本目录运行：

```bash
python3 notes/check_calculations.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=results/20261108-final-answer-build report/answers.tex
```

标准库 Python 自查穷举第 1 题 70 种组成、核对第 3 题原始计数、第 4 题相邻转移、第 5 题平稳方程，以及第 6、7 题完整联合分布的归一化和查询。无外部数据或实验。计划、来源映射与阶段记录见 [notes/answer-preparation.md](notes/answer-preparation.md)，编译和自查证据在 [results/20261108-final-answer-build/](results/20261108-final-answer-build/)。
