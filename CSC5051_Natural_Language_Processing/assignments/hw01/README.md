# Exploring Word Embeddings

状态（2026-10-21）：已从原版 Notebook 重新补全并运行；实现者自查通过，未进行独立验证/审查，未提交。

## 要求与来源

- 教师原件：`requirements/Assignment_1.pdf`，第 1 页。
- 原版 Notebook：`results/input-snapshot/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb`。
- 用户于 2026-10-21 提供补充：CBoW 可用 sum/average；Task 2.1 与 Task 1 末尾的 CBoW 图比较；Task 2 可用 GloVe Twitter 25 或 Google News 300，并注明选择。
- 本次选择平均上下文和 `glove-twitter-25`，已在 Notebook 中注明。
- 原要求截止时间：2026-10-23 23:59（原文未注明时区），Blackboard 提交 `.ipynb`；使用教师提供的 Colab Notebook。本次记录为本地执行结果。

## 当前文件与改动范围

`report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb` 是当前版本，直接基于原版重新填写。除原本空白的 cell 2 添加随机种子设置外，只改任务代码和答案；其余教师代码、训练循环、超参数、辅助函数和绘图保持原样。完整源码比较及运行记录见 `notes/original-rebuild.md`。

原先扩展版本保存在 `local_artifacts/before-original-rebuild-20261021T112415Z/`。2026-10-10 的 notes/plan.md、notes/implementation.md 和旧运行证据为历史记录，不能代表当前 Notebook。所有本地数据与历史记录保留。

姓名、学号留空，需学生填写并审阅答案。尚未组装 `submission/`。

## 本地运行

VS Code 选择 conda NLP 的 `Python (NLP)` 内核，重启后顺序运行。原版代码使用 CUDA，需可用 NVIDIA GPU。本次使用本机 RTX 4090 Laptop GPU。

为保留教师固定的 Bokeh 3.2.0，NLP 环境使用 NumPy 1.26.4；其余实际版本见 `results/original_20261021T112508_726671Z/packages.txt`。原始安装/下载单元格仍保留。运行脚本将 PATH 指向当前 conda 环境，并隔离继承的 ROS PYTHONPATH。

从本作业目录实际执行：

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s -u notes/execute_original.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s tests/self_check.py
```

以上本机解释器路径用于记录真实命令；其他机器替换为对应环境的 Python。Notebook 源码无本机绝对路径。

## 数据与证据

- 原版 Quora 数据获取地址保留在 Notebook 安装单元格，本地路径仍为 `report/quora.zip` 和 `report/train.csv`。train.csv SHA256：`5f28dbe0bb01b39a793f36567d18fe7cf34d20bbca69ff85b131d7c2186f9914`。
- GloVe 与 NLTK 缓存：`data/downloads/`；运行脚本设置对应缓存路径。模型为 Gensim 的 `glove-twitter-25`。
- 本轮执行、最终源码审计和依赖记录：`results/original_20261021T112508_726671Z/`。
- 本轮日志：`results/original-rebuild-console-20261021.txt`、`results/original-rebuild-self-check-20261021.txt`。
- 数据、缓存和旧版本本地备份不提交 Git；Notebook 和轻量文字证据可跟踪。学校提交清单与 Git 跟踪清单分别核对。
