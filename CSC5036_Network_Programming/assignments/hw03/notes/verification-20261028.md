# hw03 独立技术复验 — 2026-10-28

Role / Executor: 独立 Verifier `/root/hw03_verifier`。本角色从未参与被测实现；只写本记录及本轮隔离证据。原件、源码、README、提交 ZIP、旧证据均未修改。当前 `master`，commit `0f4a40736f0af5ab23a55b50af6229de7cdaef66`；没有创建分支或 worktree。其他课程现有未提交文件保持不动。

## Inputs / version

已重新核对根 README、最新 AGENTS、课程/作业 README、agents/verifier.md、旧计划、教师 Markdown 全文及原包全 15 条目与实际源码。目标路径没有下级 AGENTS/override；当前作业无 requirements 目录，原件保留在作业根。本轮使用 validating-implementations 技能，但遵守任务限定只写本作业 notes 与隔离 results，不额外创建根文档。

直接测试 `submission/226040255_hw3.zip`：

`c30d31fd5c2f386599ccc05dbed6ee3f1f1757f3772b8dd574b20c6b6dfb4790`

原件 `Assignment-3.zip`：

`6ae69bd09fe08b7450502f167e6858bd56b8a94d667fb690c27f2e94ee0f73a8`

本轮证据目录：`results/verification/check-20261028-210245/`。`static-package.json` 记录完整提交清单和逐文件 SHA-256，全部源码与当前 src 字节一致；`original-submitted.diff` 保存与原包对照。测试/构建临时文件与合成同名 fixture 只在已忽略 `local_artifacts/`，不进入提交包。

## Passed checks

| 教师原文依据 | 本轮实际独立检查 | 结果 / 证据 |
| --- | --- | --- |
| Basic Requirements / Grading 10% 编译 | 从实际提交 ZIP 解压到新建目录，构建前仅原 15 个文件，无 .o 和可执行文件，原 Makefile `make` | 退出 0，`build-1.txt` 含四个 C17 编译命令及最终链接，绝非 up-to-date；`summary.json` 记录真实 cwd/argv |
| Basic Requirements 修改范围 | 原件与提交逐条字节对比并人工审新增行 | 只 main.c/server.c/utils.c 有 TODO、必要辅助函数/状态、日志条件新增；所有原非空行按序保留，所有 include 不变；其余 12 个条目字节一致 |
| Basic Requirements / 原 packet ABI | 头文件与原件字节相同；独立 C helper 读取 sizeof/offsetof，核对测试 ctypes 布局 | packet_t 140 字节；ID=0，descriptor=4，message=5，hostname=69，TTL=133，port=136。`abi.txt`、`abi-commands.json` |
| Network setup 10% | 真实 UDP 连接与反向两跳查询；20 次重复 CONNECT | 正确登记监听端口，双向可查询；重复 CONNECT 只新增一次，`chain1-*`、`loop-history-*` |
| Flooding 20% / Objectives 1 | 五节点星型缺失文件查询，四个叶子均收到 QUERY；反向两跳命中直回源 | 全部可达节点收到，命中结果 IP/port 对应实际持有者，`star-concurrent-*`、`chain1-*` |
| TTL Control 20% | 四节点链，源 TTL1 与 TTL3 | TTL1 停于第一邻居、远端无 QUERY/无 RESPONSE；TTL3 中间转发为 2、1，第三跳 TTL1 接收者仍能本地命中，`chain1-*`、`chain3-*` |
| Avoid loops 20% | 三角环高 TTL 查询 | 两邻居各转发一次，重复丢弃，流量在 TTL 耗尽前静止，`loop-history-*` |
| ID 边界 / 去重 | 独立构造 160 个不同 ID 完整 QUERY 包；再发送首/末 ID | 超过原数组 128 后首尾均仍去重，无越界异常退出，`loop-history-node0.txt` |
| Multiple responses | 两个隔离目录创建标明合成用途的同名文件，单次查询 | 同时接收两个独立持有者响应，`star-concurrent-node0.txt` |
| Thread safety 20% | 五节点 12 轮共 60 次并发来源搜索、接收线程同时工作 | 每条预期响应到达，全部进程存活，`star-concurrent-*`；静态审共享 ID、邻居与地址 helper 的锁范围 |
| Concurrent operations | 四叶同时加入时 root 发 50 条查询；随后各叶查询 root 文件、root 查询最后加入叶文件 | 四个连接全部登记且双向查询成功，无死锁，`concurrent-join-*` |

本轮真实执行命令（从仓库根）：

```bash
python3 CSC5036_Network_Programming/assignments/hw03/results/verification/check-20261028-210245/verify.py
python3 CSC5036_Network_Programming/assignments/hw03/results/verification/check-20261028-210245/connect_query.py
```

两条命令退出状态均为 0；socket 权限仅为本机 loopback 的已授权独立测试使用，无外部服务器/云资源。`execution.json` 记录测试脚本 SHA、命令退出状态。`summary.json` / `concurrent-join-summary.json` 包含所有节点 argv、cwd、动态端口、源码哈希、实际时间和进程收尾状态；节点原始输出均为同目录 txt。节点测试后 SIGTERM 的 -15 为预期收尾，非测试失败。

环境：Linux-7.0.0-38-generic-x86_64-with-glibc2.43，gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0。C17/pthread 使用教师原 Makefile；测试工具为 Python 标准库与 GNU stdbuf。端口由 OS 分配；程序查询 ID 保留原时间/PID 种子，非确定性但断言检查协议性质，不依赖具体随机 ID。

## Failed checks

本轮上述检查无失败，没有发现需要退回实现者修复的功能缺陷或确切违反教师改动约束的新增代码。未用旧证据代替本次运行，也未覆盖任何旧记录。

## Warnings / limits

- 测试脚本由已审查的旧独立测试改编，新增提交 ZIP 解压、构建前清单和真实编译断言；所有本轮结果写新目录。多响应测试只在隔离副本加两个同名合成文件，不改提交 ZIP。
- 未用 ThreadSanitizer、形式化证明、长时间压力、不同机器/不同 ABI、丢包和网络故障验证。线程安全结论限于静态锁审查与本轮实际并发运行。否定传播/静止检查采用 0.2/0.25 秒本机等待窗口，不构成任意网络延迟保证。
- 继承的非 TODO 行仍存在：main 的 atoi/strcpy、fgets EOF 未处理、目录查找成功路径未 closedir、网络 helper 对短包/系统调用失败处理不完善。教师仅允许 TODO/辅助函数/日志条件变更，且用户要求最小改动；本轮使用合法参数、有效目录、完整协议包、持续打开 stdin。这些遗留问题不冒充已修复，也不在本次规定运行方式下构成新缺陷。
- 辅助 overflow ID 历史随不同 ID 增长；本题每进程一次初始化一个 IDlist，未覆盖当作通用库重初始化/多表复用的行为。长期内存/目录句柄压力未测。
- 未执行 Blackboard 上传；本角色不签最终 Ready。实际包清单、命名及最终批准仍需不同独立 Reviewer。

## Required fixes / next role

当前冻结版本在本轮覆盖范围内无必需修复。交独立 Reviewer 审本轮证据与实际提交包；若源码或 ZIP 变化，相关检查须重新执行。

## Source SHA-256

- `Makefile`: `6d0c2a9780f19979441cd60fa03a9905e8e8b6aa9eb3fd171067d6839267d311`
- `main.c`: `a84b1312cc58f3552398a63c4fad83f0bda64e96149a2dec7663934fafdcf879`
- `network.c`: `7f87b1e5e3ccecbce500b38b2f9378a6506021ab701ff97b41f19b4c7b26829d`
- `network.h`: `7125cf841c994a7985ef9dd1fdebd42bfdf3882cb105a8c437d5abbce0aa4ec7`
- `server.c`: `4f5e5189b860c23cb3d36bf6cfa3ee920d38dc13448befa5795f2884d3f3548f`
- `server.h`: `b3e6a6b048dca78d35502c740371a69365e74df379093f0a658d59c3befbf9f3`
- `utils.c`: `7f0014075c34556087e9226899031b49cdfa0bb178818ff5e86cff0f77444f4a`
- `utils.h`: `e5c3f0b1278cb32c1eb0e7332c9e2240208d46aa0bb230bab676c4869337fef1`
