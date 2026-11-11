# DDA5001 Part I 独立技术验证

独立执行者为 Codex 子会话 `/root/verify`，未参与实现。2026-11-10 在本机从 `master`（验证开始时为 `d2a35b4`）核对未提交的项目。判据来自项目手册第 5 页 §3.1、 第 6–7 页 §3.3–3.4 和原代码的 `p1/AGENTS.md`。两份教师 PDF 位于项目顶层，本项目没有单独的 `requirements/`。验证所用固定版本为 `e15b23d4db41ede3612e9ae3d44b704dfce8b7b0`，本地快照 SHA-256 为 `4deeb467b01f31abade28e7baa2382c67719b8d54e848ed1ff1bfa01b854f7c1`。

## Passed checks

- 比较快照全部 28 个原有文件。七个指定代码块中的九个占位表达式替换后，28 个文件与工作副本逐字节一致，含原测试、评估、分组与训练循环。另核实 `results/input-sha256.txt` 中全部九项散列。
- 从 `input.txt` 独立构造 65 字符的排序词表，逐个对照 1,003,854 个训练 token 和 111,540 个验证 token。自定义非单调、重复 token 输入覆盖全部合法窗口长度、最后一个合法窗口及逆序批次。修改第 15 个位置及后续 token 时，smoke 终点模型前 14 个位置的 logits 逐位相同。
- 远程原版检查记录在首个掩码 TODO 处失败，退出 1。远程完成版课程检查退出 0，随后 CPU smoke 完成 8 个更新、1,024 个 token。本机另用 PyTorch 2.14.1+cu130 的 CPU 独立执行原版检查器及 smoke，均退出 0。
- 从本机 smoke 的 `last.pt` 重建模型，按评估种子独立抽取 256 个验证目标，使用双精度 log-softmax 直接累计 NLL，得 3.6954945112 nats/字符。本机记录为 3.6954946518，远程 PyTorch 2.9.0 记录为 3.6954945326。复核使用绝对容差 1e-5 以涵盖 FP32 归约与跨版本数值差异。

复现时在 `src/` 使用本机 `~/miniconda3/envs/NLP/bin/python` 执行 `check_solution.py` 及 `train.py config/smoke.py --device=cpu --out_dir=<新的隔离目录>`。本轮输出目录为 `../results/verification/preflight/smoke`。从项目顶层执行 `results/verification/preflight/verify_inputs.py` 核对原件、数据及保留的 smoke 终点。输出见 `results/verification/preflight/{native-check,smoke,inputs}.log`，对应 `.exit` 均为 0。


## 六组终点复核（2026-11-11）

独立核对每组 11 个评估点。六组均从随机初始化开始，训练至第 5,000 次更新、92,160,000 个预测 token。输入、源代码、随机种子、模型与训练配置符合固定版本；每个 CSV 的 token 数、计时、训练/验证损失、实际学习率、日志和摘要一致。训练时间采用摘要中的训练循环耗时，未计入评估和写检查点。另核对 12 张单组曲线和 2 张跨组比较图可解码。

| 优化器 | 峰值学习率 | 终点验证损失 | 训练时间（秒） | 最佳验证步 |
|---|---:|---:|---:|---:|
| AdamW | 0.0003 | 4.031841 | 1836.502 | 1000 |
| AdamW | 0.00015 | 3.852353 | 1809.609 | 1000 |
| SGDM | 0.1 | 1.645356 | 1807.949 | 2500 |
| SGDM | 0.05 | 1.534937 | 1808.217 | 4000 |
| Muon | 0.01 | 4.079324 | 2152.296 | 500 |
| Muon | 0.005 | 4.190040 | 2148.224 | 500 |

三条默认曲线的终点验证损失均高于第 2,500 步，运行者据此将三个第二学习率减半。AdamW 的两种学习率在 500–1,000 步之间交换验证损失排序，SGDM 在 3,000–3,500 步之间交换排序。Muon 的两个学习率从第 500 步到终点保持相同排序。区间指相邻的实测点。

读入全部 12 个检查点，逐一核对配置、优化器数、模型维度、词表、更新步、token 数、最佳损失与训练时间。六个 `last.pt` 均对应表中终点，六个 `best.pt` 对应各组 CSV 的最低验证损失及其步数。重新计算的 12 个 SHA-256 均与远程清单相同。

默认 AdamW 的生成命令指定 `last.pt` 和 400 个新字符，退出 0；训练流水线输出、样本文件与导出包中的样本逐字一致。将完整 401 字符样本与语料逐段比较，训练划分最长连续匹配 386 个字符，验证划分最长连续匹配 15 个字符。使用本机 CPU 从该终点重新载入模型，对样本前 64 个目标字符做一次条件前向计算，57 个目标为最高概率字符，平均 NLL 为 0.30413。原始导出包 `local_artifacts/export.zip` 的全部 71 个成员通过 CRC 校验，其中 46 个结果文件与本地下载副本逐字节一致；导出包 SHA-256 为 `626bd4ec54a65e97be7ae27079d6101c17895f5c82f7ab9a6e45b33563d0a231`。

在项目顶层用本机 NLP 环境 Python 执行 `results/verification/six/verify.py` 和 `results/verification/six/check_backups.py`。从 `checkpoints/run-10R3a5Il/` 运行 `sha256sum -c ../../results/run-10R3a5Il/checkpoint-sha256.txt`。三次检查的日志位于 `results/verification/six/{final-check,backups-cpu,checkpoint-sha}.log`，退出码均为 0。

## Failed checks

在所列版本及检查范围内，通过全部技术验证。

## Warnings

- 第一轮 CPU 样本前向抽查使用 meta 设备构建模型，其非持久性因果掩码没有随权重载入，初查日志 `backups.log` 中的前向数值作废。改为在 CPU 上直接构建模型后重跑全部备份检查，采用 `backups-cpu.log`。该问题限于 Verifier 的首次本地抽查。
- 正式实验的终点损失已核对原始证据及检查点元数据。未在本机重训六组，也未逐 token 重放原 GPU 随机采样。样本与语料重合长度描述该次生成。
- 原始远程日志和 JSON 中有标识账户的绝对路径。组装者保留本机原件并在准备提交副本时检查脱敏；最终报告及实际提交候选包由独立 Reviewer 审查。

## Required fixes

本次验证覆盖的训练实现、六组结果、样本来源与检查点备份无待修复项。下一阶段由 Reviewer 按手册第 7 页 §3.4 审查含报告的实际候选包。
