# hw03 — Flooding and Peer-to-peer Search

原始要求：[教师原文](Assignment-3_Flooding_and_Peer-to-peer_Search.md)，配套原件：[Assignment-3.zip](Assignment-3.zip)。原文课程号 CSC4303，按现有仓库归属 CSC5036。截止：2026-11-01 23:59（UTC+8）。

## 代码与运行

工作副本在 `src/Assignment-3/`。只补三个指定 C 文件的 TODO、必要辅助函数与日志条件；网络 helper、头文件、Makefile 和测试目录保持原样。原件未改。Unix、gcc C17、GNU Make、pthread；无需第三方 C 库。

```bash
cd src/Assignment-3
make
./p2p_server 49151 1 dir1
# 另开终端，进入同一目录：
./p2p_server 49152 2 dir2 127.0.0.1 49151
./p2p_server 49153 2 dir3 127.0.0.1 49152
```

等待每个节点完成绑定再启动下一个，在终端逐行输入文件名。Ctrl+C 停止。其他拓扑见教师原文。请使用有效目录、端口、TTL 和成对邻居参数；非 TODO 的原有参数解析、stdin EOF 与目录句柄早返回逻辑保留。

## 检查与交接

从本作业目录运行 `python3 tests/integration.py`，使用真实 loopback UDP 与多进程，需允许本机 socket。测试脚本依赖 Python 3 和 GNU stdbuf，仅用于开发，不入提交包。输出在 `results/selftest-<time>/`；每次保留命令、版本哈希、环境、节点日志与结论。原包七个空文件是教师测试 fixture，只留本机，最终 ZIP 仍完整包含。

- [计划](notes/plan.md)、[代码梳理](notes/research.md)、[实现与自测](notes/implementation.md)。
- 自测通过：链路、TTL1/TTL3、环路、本地与远程查找、五节点并发。[独立验证](notes/verification.md)也已通过，包括多结果响应、重复连接、160 个 ID、五节点并发与并发加入；[独立最终审查](notes/review.md)结论为 Ready。
- 提交物按原文仅一个 ZIP：`submission/226040255_hw3.zip`，保留原包结构，不含 README、自建测试、内部记录或编译物。已组装；逐项哈希见 `results/package-20261021T192231.json`。[独立最终审查](notes/review.md)结论为 Ready；用户自行上传 Blackboard，尚未提交。

## 2026-10-28 提交前复查

本轮从实际提交 ZIP 全新解压，GCC/Clang 使用原 Makefile 均编译通过；主会话网络自测与独立复验全部评分项通过。独立 Reviewer 核对实际 15 项包清单和本轮证据，结论 **Ready**，无必需修复，因此源码和 ZIP 未改动、未重打包。

记录：[主会话自查](notes/preflight-20261028.md)、[独立复验](notes/verification-20261028.md)、[独立最终审查](notes/review-20261028.md)。提交仍用 `submission/226040255_hw3.zip`（SHA-256 `c30d31fd5c2f386599ccc05dbed6ee3f1f1757f3772b8dd574b20c6b6dfb4790`），仅表示此版本已检查，尚未上传 Blackboard。运行范围和保留的教师非 TODO 代码限制详见独立记录。
