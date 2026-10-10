# Exploring Word Embeddings

状态：Notebook 已补全并在本地 conda NLP 环境运行；实现者自查通过，尚未进行独立验证/审查，未提交。

Word2Vec 训练、词向量探索与应用。

## 原始材料

- `requirements/Assignment_1.pdf`

## 要求与待核实事项

原要求：2026-10-23 23:59 前在 Blackboard 提交 .ipynb；使用教师提供的 Colab notebook。现已在 `report/` 中补全并本地运行 notebook；本地执行记录不代表教师已确认允许替代 Colab。

## 后续工作目录

按需建立 `src/`、`report/`、`results/` 和 `submission/`；涉及手写内容可加 `handwritten/`、`notes/`。

`requirements/` 中原件不直接修改；需要编辑时复制到自己的工作目录。`submission/` 只保存最终实际提交版本。截止时间以教师最新通知为准。


## 本地运行

- 文件：`report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb`。
- VS Code 选择 `Python (NLP)` 内核；安装依赖后重启旧内核，再按顺序运行。
- 已安装 PyTorch、Matplotlib、scikit-learn、nbclient、nbformat、gdown，并更新 Bokeh 以适配 NumPy 2。
- 注册的 `nlp` 内核隔离继承的 ROS PYTHONPATH。Notebook 自动选择 CUDA/CPU，随机种子为 42。
- 数据：沿用已有 `report/train.csv`；预训练词向量及 NLTK 分词资源缓存在 `data/downloads/`。
- 姓名、学号留空，需学生填写并审阅答案。

从本作业目录执行（实际使用的命令）：

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s -u notes/execute_notebook.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s tests/self_check.py
```

环境本机路径仅用于记录本次实际命令；Notebook 本身不依赖该绝对路径，其他机器可使用对应 NLP 环境的 Python。
要求解析见 `notes/plan.md`，实现与运行证据见 `notes/implementation.md`。原收到的未完成 Notebook 保存在 `results/input-snapshot/`。各次执行的输入、输出、状态和依赖版本单独保存在 `results/execution_*/`，训练记录与检查点保存在对应 `results/<run-id>/`。其中一次重跑遇到 NLTK 3.8 资源路径兼容问题，失败记录已保留，随后修复。

尚未组装 `submission/`；未宣称独立验证或最终提交包审查通过。
