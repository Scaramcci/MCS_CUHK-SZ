# hw03 独立最终审查

Role / Executor: Reviewer `/root/hw03_reviewer`；未参与实现、自测或独立技术验证。
Date: 2026-10-21（UTC+8）。仓库基线 `900f713`，分支 `codex/csc5036-hw03`，实现为未提交副本。本角色仅写本记录，未修改代码、说明、原件、验证输出或提交包。

## Critical issues

无。已直接读取最终 ZIP 全部条目并做 CRC、目录清单和内容哈希检查；无缺失源码、错误版本、额外数据、凭据、二进制或内部记录。结论只覆盖下面的确切候选。

## Major issues

无未解决项。审查中发现旧独立构建日志 `build-1.txt` 仅含 up-to-date，不能支持“全新构建”表述；已退回原 Verifier。Verifier 在新的隔离目录仅复制原 15 个文件、确认无对象文件/可执行文件后重新执行 `make`，记录退出 0、四次 C17 编译和最终链接；本角色读取了新 stdout、空 stderr、JSON 命令/输入哈希并再次与 ZIP 逐项比对一致。`notes/verification.md` 已如实纠正原日志被重试覆盖的记录失误，未将旧日志改写成新输出。该证据缺口已关闭，源码和 ZIP 均未变。

## Minor issues / coverage limits

无须为此次交付修复的 Minor。保留原非 TODO 的参数、stdin EOF、目录成功早返回未 closedir、UDP helper 异常包与系统调用错误处理；这是用户/教师要求限制下的原代码边界，说明和独立验证均已明示。新增 overflow ID 历史随查询数增长，未覆盖库式重初始化；当前每进程一个 ID 表的作业流程已验证。未做 TSAN、长期压力、跨主机或丢包故障测试，不把并发实测及静态锁审查表述为形式化无竞态证明。

## Submission checklist

一手来源：教师 `Assignment-3_Flooding_and_Peer-to-peer_Search.md` 的 Basic Requirements、Objectives、Three-Party Example、Grading Criteria Parts、Submission；原 `Assignment-3.zip` 全部条目。本作业没有 requirements/、下级 AGENTS/override；原件保留原位。根 README、AGENTS、角色与课程/作业 README 已读取。

| 教师要求 | 审查结果 | 证据 |
| --- | --- | --- |
| C / Unix / C17 / 原 Makefile（10%） | 通过 | 原 Makefile 未变；独立全新构建 `fresh-build-20261021T192444.stdout.txt`、stderr.txt、json，退出 0 |
| CONNECT 与邻居加入（10%） | 通过 | 核对监听端口随 CONNECT 携带；独立双向查找、重复连接及四节点并发加入记录 |
| 泛洪（20%） | 通过 | 原发 ID 先登记；转发保留源地址/端口/ID，排除原查询源；四节点链、五节点星型的独立输出 |
| TTL（20%） | 通过 | 先查文件再判断 TTL<=1；只有未命中且 TTL>1 才递减；TTL1/TTL3 独立日志 |
| 环路去重（20%） | 通过 | 接收 ID 检查与登记在同一临界区；三角环一次处理后静止；160 ID 后首尾仍去重 |
| mutex / 并发（20%） | 通过（已声明覆盖范围） | ID、邻居与非可重入地址 helper 调用均受锁保护；启动条件变量；独立五节点 60 次查询及查询时并发加入 |
| 指定 19 处 TODO / 最小改动 / 无额外头文件 | 通过 | 直接逐行比对原 ZIP 与提交 ZIP：仅 main.c、server.c、utils.c 有 TODO 内容、辅助状态/函数和日志控制新增，未删改原非空行，includes 完全一致 |
| 保留源码、头文件、Makefile 与原测试目录 | 通过 | ZIP 内清单与原包完全相同，共 15 项；原七个空文件字节一致 |
| 文件名和结构 | 通过 | 用户提供的学号对应 ZIP 命名；所有条目位于原 Assignment-3/ 目录 |
| 排除 README、自建测试、缓存、二进制与内部记录 | 通过 | submission/ 仅该 ZIP，包内无其他条目 |
| 原件保护 | 通过 | 原 ZIP 与教师 Markdown 分别比对 HEAD Git blob，字节完全一致 |
| 报告、PDF、引用与图表 | N/A | 教师没有要求这些提交物，本包未额外加入 |
| 上传 Blackboard | 未执行 | 按仓库规则由用户自行提交；Ready 不等于已上传 |

本角色实际执行只读 Python ZIP 审计（`ZipFile.namelist/read/testzip`、`hashlib.sha256`、`difflib.unified_diff`）、Git blob 对照与忽略规则检查；审阅独立测试脚本 `verify.py`、`connect_query.py`、两个 JSON 摘要及实际节点输出。没有另行运行网络测试，不将 Verifier 的实测冒充本角色运行。

## Exact candidate and version

- 最终候选：`submission/226040255_hw3.zip`，10,406 字节，展开共 23,476 字节。
- ZIP SHA-256：`c30d31fd5c2f386599ccc05dbed6ee3f1f1757f3772b8dd574b20c6b6dfb4790`。
- 原 ZIP SHA-256：`6ae69bd09fe08b7450502f167e6858bd56b8a94d667fb690c27f2e94ee0f73a8`。
- 教师 Markdown SHA-256：`6330ed6ee3128ba299ac32c16a958b38d390726f6ebd52dfb7c6a03d3215b4a9`。
- 全 15 条目尺寸与 SHA-256 见 `results/package-20261021T192231.json`，已由本角色独立重算并核对。八个构建输入与 Verifier 的 `summary.json` 及新全量构建输入哈希一致；七个测试文件均为原始空文件。

| ZIP 内确切条目 | 字节 |
| --- | ---: |
| Assignment-3/main.c | 4618 |
| Assignment-3/server.c | 5774 |
| Assignment-3/utils.c | 5443 |
| Assignment-3/network.c | 2820 |
| Assignment-3/server.h | 688 |
| Assignment-3/utils.h | 2931 |
| Assignment-3/network.h | 684 |
| Assignment-3/Makefile | 518 |
| Assignment-3/dir1/file1 | 0 |
| Assignment-3/dir1/file2 | 0 |
| Assignment-3/dir2/file3 | 0 |
| Assignment-3/dir3/file4 | 0 |
| Assignment-3/dir4/file5 | 0 |
| Assignment-3/dir4/file6 | 0 |
| Assignment-3/dir5/file7 | 0 |

变更的三个文件 SHA-256：

- main.c：`a84b1312cc58f3552398a63c4fad83f0bda64e96149a2dec7663934fafdcf879`
- server.c：`4f5e5189b860c23cb3d36bf6cfa3ee920d38dc13448befa5795f2884d3f3548f`
- utils.c：`7f0014075c34556087e9226899031b49cdfa0bb178818ff5e86cff0f77444f4a`

## Final readiness

**Ready**，限上述 ZIP 和哈希版本。必需功能已独立验证、实际包已独立审查，无未解决 Critical/Major。Ready 表示此版本准备就绪，不代表上传、教师认可或保证分数。若更改候选或源码，受影响的验证和本结论需要重新检查。

Next: 主会话汇总此记录并交付 ZIP；用户决定是否上传 Blackboard。
