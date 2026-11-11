# DDA5001 Final Project · Part I

教师手册第 6–8 页规定七处代码填空、六次独立预训练和提交要求。代码基于 [课程仓库](https://github.com/CUHKSZ-Course/DDA5001-26Fall/tree/e15b23d4db41ede3612e9ae3d44b704dfce8b7b0/p1) 的固定版本。原始快照位于本机 `local_artifacts/upstream/`，工作副本为 `src/`，配套数据在 `src/data/shakespeare_char/`。代码和输入校验值见 `results/input-sha256.txt`。

本次按课程原配置使用单卡 RTX 4090 D、PyTorch 2.9.0+cu128、随机种子 42、评估种子 1729。每组独立初始化，目标为 5,000 次更新和 92,160,000 个预测 token。AdamW、SGDM、Muon 的默认峰值学习率分别为 0.0003、0.1、0.01。第二个峰值根据各自默认曲线决定。脚本 `notes/run-six.py` 记录选值、命令与退出码；在含 `train.py` 的新工作目录中用配置好的 Python 执行。检查通过后先做 CPU smoke，再进行正式训练。

本次运行标识为 `run-10R3a5Il`。轻量输出和日志下载至 `results/run-10R3a5Il/`，正式训练的终点和最佳检查点另存于 `checkpoints/run-10R3a5Il/`。以实际产物和退出状态为准。双人组的贡献说明由组员自行填写。

## 本地交付与补填

六组正式运行均已完成 5,000 步，累计训练时间 3.21 小时（各组 `train_seconds` 之和）。六组原始配置、逐点评估、日志、图片及样本保存在本机。12 份权重（每组 `best.pt` 和 `last.pt`）已下载并逐份核对远端 SHA-256。候选包在 [local_artifacts/candidate/part1-results.zip](local_artifacts/candidate/part1-results.zip)，报告在 [report/part1-report.pdf](report/part1-report.pdf)。

报告采用英文，一页。请在 [report/part1-report.tex](report/part1-report.tex) 末尾的 Member 1 和 Member 2 处填入各自的真实贡献。在 `report/` 内运行 `pdflatex -halt-on-error part1-report.tex`。确认 PDF 仍为一页后，从本项目目录执行 `python3 notes/package.py submission/part1-results.zip`，检查新 ZIP 内的 PDF 和文件清单。打包脚本只新建文件。原始证据保留在本机，ZIP 副本中的数据和输出路径改为相对路径。贡献尚未填写的版本保留在候选目录。

独立技术验证见 [notes/verification.md](notes/verification.md)，候选清单及哈希见 [notes/candidate-files.txt](notes/candidate-files.txt) 和 [notes/candidate-sha256.txt](notes/candidate-sha256.txt)。
