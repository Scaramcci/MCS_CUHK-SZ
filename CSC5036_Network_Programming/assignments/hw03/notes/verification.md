# Independent verification — hw03

Role / Executor: Verifier /root/hw03_verifier；未参与被测代码、自测脚本或报告创作。
Date: 2026-10-21（UTC+8）。输入：教师 Markdown 全文、原 ZIP 全部 15 条目、notes/plan.md、notes/implementation.md、实际 src/Assignment-3；分支 codex/csc5036-hw03，基线 900f713 加未提交实现。

## Passed checks

独立测试在 `results/verification/check-20261021/local_artifacts/work/` 隔离复制并构建，不改 src、原件、自测、README 或 submission。环境 Linux x86_64、gcc 15.2.0、原 Makefile 的 C17/pthread；协议结构实测大小 140 字节。

| 原文依据 | 独立检查 | 结果与证据 |
| --- | --- | --- |
| Basic Requirements / Grading 10% | 原 Makefile 在新建隔离目录复制仅原 15 条目后 make | 退出 0，fresh-build-20261021T192444.stdout.txt / fresh-build-20261021T192444.json |
| Basic Requirements 修改边界 | 对照原 ZIP；逐行审新增内容；全部原非空行按序保留；#include 逐行相同 | 仅 main.c/server.c/utils.c 有 TODO、辅助状态/函数、日志条件新增；其余 12 条目字节相同 |
| Network setup 10% | 真实 UDP CONNECT，双向查询；20 次重复 CONNECT | 首次登记一次，重复连接不重复插入或耗尽邻居容量 |
| Flooding 20% | 四节点链路反向两跳；五节点星型；缺失文件查询 | 可达节点收到查询，响应显示真正持有者 IP/监听端口 |
| TTL 20% | 四节点链路 TTL1 与 TTL3 | TTL1 停于首邻居无响应；TTL3 转发依次 TTL2、TTL1 并由第三跳命中响应 |
| Avoid loops 20% | 三角环、原发 ID 登记、二次到达 | 每节点只转发一次、重复丢弃，流量在 TTL 耗尽前静止 |
| ID 边界 | 独立构造 160 个不同 ID 完整协议包；重发首个和末个 ID | 128 之外仍保留去重，首尾均丢弃，无越界退出 |
| Multiple responses | 仅在隔离目录中创建两个同名合成测试文件；一次查询 | 同时收到两个独立持有者响应，不把第一条结果当作结束 |
| Thread safety 20% | 五节点 12 轮、共 60 次并发来源查询 | 每条预期响应到达、进程保持存活；静态核对 ID、邻居与非可重入地址 helper 的持锁调用 |
| Concurrent operations | 主节点发出 50 次查询时四个子节点同时加入，随后所有子节点查 root 文件、root 查最后子节点文件 | 四个新邻居全部登记，双向结果到达，无死锁/异常退出 |

实际命令（从仓库根）：

```bash
python3 CSC5036_Network_Programming/assignments/hw03/results/verification/check-20261021/verify.py
python3 CSC5036_Network_Programming/assignments/hw03/results/verification/check-20261021/connect_query.py
```

两条命令实际退出状态均为 0。`verify.py` 重试时在同一隔离工作目录运行，因此现存 `build-1.txt` 是增量 make（up-to-date），不能作为新鲜构建证据。Reviewer 指出该记录缺口后，本角色另建目录重新执行无 .o/二进制的真实新鲜构建，详见下段；旧日志完整保留。节点完整命令、环境、源码哈希见 `summary.json`；并发加入见 `concurrent-join-summary.json`；各节点原始输出是同目录 `*.txt`。端口由操作系统分配；查询 ID 依教师代码按时间/PID 种子生成。测试断言后发送 SIGTERM，节点 -15 是预期测试收尾，不是程序运行失败。

## Fresh-build evidence correction

Reviewer 发现 `build-1.txt` 为增量 make 后，本角色于 2026-10-21T19:24:44+0800 新建 `results/verification/check-20261021/local_artifacts/fresh-build-20261021T192444/`，从冻结源码按原 ZIP 清单仅复制 15 个文件（构建前核实没有任何 .o 或 p2p_server），在该目录执行 `make`。命令退出 0，真实输出含 main.c、server.c、utils.c、network.c 的四次 C17 编译及最终链接。输入哈希与下列已验证版本完全一致，源码和提交 ZIP 未修改。

- stdout：`results/verification/check-20261021/fresh-build-20261021T192444.stdout.txt`
- stderr：`results/verification/check-20261021/fresh-build-20261021T192444.stderr.txt`（空，实际无 stderr）
- 命令、cwd、构建前 15 条目清单、退出状态与全部输入哈希：`results/verification/check-20261021/fresh-build-20261021T192444.json`

初次 verify.py 运行的编译输出被重试时同名 build-1.txt 覆盖，原先“fresh isolated build”对应证据引用不准确；本段补充独立新鲜构建，并明确现存旧日志只证明增量构建。未将增量日志改写为新鲜构建输出。

## Failed checks

被测有效参数/完整包的上述功能检查无失败。初次无提升权限执行在第一处 socket 创建被沙箱拒绝，退出 1；已保留 `sandbox-failure-summary.json` 和 `sandbox-failure.txt`。获得本机 loopback 权限后运行全部网络断言通过，未以失败轮替代成功轮或删除失败证据。

## Warnings / coverage limits

- 未进行 ThreadSanitizer、长时间资源压力、真实跨主机/丢包/乱序故障验证；并发运行加静态锁审查不能表述为形式化无竞态证明。
- 教师非 TODO 代码保留：stdin EOF/非法参数处理、成功查找未 closedir、UDP helper 异常包/系统调用错误处理、原邻居日志中的端口含义。它们不是本轮新增缺陷，当前要求用有效命令行与完整协议包测试。
- 新增 overflow ID 历史空间随不同查询数增长，没有退出前释放；程序按每进程只初始化一个 ID 表运行，未覆盖复用同一地址重初始化 IDlist 的库式用法。此限制不影响本次题目运行流程与评分拓扑。
- 多命中合成输入明确只用于验证，位于已忽略 local_artifacts 内，不替代教师原数据，也不进入提交包。所有隔离代码/二进制/fixture 都在此目录，本角色没有改 .gitignore。
- 最终提交 ZIP 尚未在本角色开始时组装，本结论只覆盖下列源码版本。最终包内容、命名、哈希由另一独立 Reviewer 检查，本角色不签发 Ready。

## Required fixes / handoff

当前覆盖范围内无阻断交付的代码缺陷，无必需修复。主会话可用下列版本组装原 15 条目提交包，再交与本角色不同的独立 Reviewer。若源文件改变，相关结论失效，需复验。

## Source SHA-256

- `Makefile`: `6d0c2a9780f19979441cd60fa03a9905e8e8b6aa9eb3fd171067d6839267d311`
- `main.c`: `a84b1312cc58f3552398a63c4fad83f0bda64e96149a2dec7663934fafdcf879`
- `network.c`: `7f87b1e5e3ccecbce500b38b2f9378a6506021ab701ff97b41f19b4c7b26829d`
- `network.h`: `7125cf841c994a7985ef9dd1fdebd42bfdf3882cb105a8c437d5abbce0aa4ec7`
- `server.c`: `4f5e5189b860c23cb3d36bf6cfa3ee920d38dc13448befa5795f2884d3f3548f`
- `server.h`: `b3e6a6b048dca78d35502c740371a69365e74df379093f0a658d59c3befbf9f3`
- `utils.c`: `7f0014075c34556087e9226899031b49cdfa0bb178818ff5e86cff0f77444f4a`
- `utils.h`: `e5c3f0b1278cb32c1eb0e7332c9e2240208d46aa0bb230bab676c4869337fef1`

Original ZIP SHA-256: `6ae69bd09fe08b7450502f167e6858bd56b8a94d667fb690c27f2e94ee0f73a8`.
