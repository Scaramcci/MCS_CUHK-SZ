# 2026-10-28 提交前复查（主会话自查）

Executor: /root，原实现者，不能代签独立验证或 Reviewer 结论。当前 master / 0f4a407；原教师材料与 HEAD 一致，无新增下级 AGENTS/override、无 requirements/；教师原件仍保留在作业根。

## 任务与检查依据

重新读取教师 Markdown 全文、原 ZIP 全 15 条目、当前全部 C 源码/头文件/Makefile 与 notes/plan.md。按照 Basic Requirements、Objectives、Three-Party Example、Grading Criteria Parts、Submission 核查：C17 原 Makefile、邻居连接、泛洪、TTL、环路去重、mutex 并发、限定 TODO 修改、最终包清单与命名。无报告或额外文档提交要求。

## 实际运行与结果

- Python ZIP/哈希审计：最终 ZIP CRC 正常，条目名/顺序与原包完全一致；15 项逐一等于 src；只 main.c/server.c/utils.c 有变化；原有非空行没有删改，include 完全一致；其余 12 项逐字节一致。
- 从 **实际提交 ZIP** 各自全新解压至 results/preflight-20261028T210300/local_artifacts/gcc/Assignment-3 和 clang/Assignment-3，分别运行 `make COMPILER=gcc`、`make COMPILER=clang`；两者退出 0，各含四个 C17 编译和链接。未复用旧二进制。完整命令、环境版本和每项 SHA-256 见 [audit.json](../results/preflight-20261028T210300/audit.json)，编译 stdout/stderr 位于同目录。
- 从仓库根实际执行 `python3 CSC5036_Network_Programming/assignments/hw03/tests/integration.py`，获准仅本机 loopback socket；退出 0，证据 [summary.json](../results/selftest-20261028T210303/summary.json)。覆盖本地命中、两跳反向查找、四节点 TTL1/TTL3、三角环路处理一次并停止、五节点并发。此脚本 make 是 src 的增量构建，全新构建证据见前项，不能混称。
- 原始 ZIP 和教师 Markdown 与 HEAD Git blob 字节一致。提交包 10,406 字节，无超过 10 MiB 交付文件，无 README/自建测试/缓存/二进制/内部记录。无修改分支、Git index、其他课程、教师原件或最终 ZIP。

## 当前结果与范围

本轮自查未发现需修改源码或重打包的问题。测试沿用教师有效 CLI、打开的终端输入和完整协议包；原非 TODO 的 EOF/参数处理、目录句柄早返回、网络 helper 异常处理保留；未做跨主机、丢包故障或长期资源测试。独立验证与 Reviewer 按本轮新记录另外出具结论。

受检候选：`submission/226040255_hw3.zip`；SHA-256 `c30d31fd5c2f386599ccc05dbed6ee3f1f1757f3772b8dd574b20c6b6dfb4790`。保留原候选，无需更换版本。

Next role: 独立 Verifier → 与 Verifier 不同的独立 Reviewer 审实际包。用户自行上传 Blackboard。

## References

[计划](plan.md)；[原实现交接](implementation.md)；[教师原文](../Assignment-3_Flooding_and_Peer-to-peer_Search.md)。
