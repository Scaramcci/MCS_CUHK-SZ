# hw03 计划与题意核对

Role / Executor: Planner，主会话 /root。输入基线：900f713，2026-10-21。

## 来源与范围

原文 `../Assignment-3_Flooding_and_Peer-to-peer_Search.md` 全文及原包全部 15 条目已读。没有已有作业 README、requirements/ 或下级 AGENTS/override，原件保留原位。原文 CSC4303 与课程目录 CSC5036 编号不同，沿用现有归属。

| 原文章节 | 要求 / 提交物 | 验收 |
| --- | --- | --- |
| Basic Requirements | Unix、C17、GNU Make；只填 main.c 4、server.c 9、utils.c 6 处 TODO，可增辅助函数及日志条件，不增头文件 | 原包逐行差异审查，其余文件哈希不变 |
| Grading Criteria Parts | 编译 10%、连接 10%、泛洪 20%、TTL 20%、去重 20%、mutex 并发安全 20% | make；三到五进程网络测试；静态锁检查 |
| Three-Party Example / Objectives | 链路远程命中；TTL=1 首跳停止、TTL=3 三跳命中；三角环去重 | 自动进程测试核对真实日志 |
| Submission | 原八个源码/头文件/Makefile 与七个空测试文件，保留 Assignment-3/ 结构；不含 README、自建测试、构建缓存 | ZIP 内清单与原包对照 |

截止 2026-11-01 23:59 UTC+8。ZIP 命名 226040255_hw3.zip。不要求报告，不新增报告。学号仅用于 ZIP 命名，不写进代码或日志。

## 执行顺序

1. 从 ZIP 复制到 src/Assignment-3，保留原件。
2. utils TODO：初始化包、ID 存取、邻居维护、排除查询源的泛洪。main TODO：邻居登记、CONNECT、mutex 和服务线程、注册本地查询并泛洪。server TODO：接收分发、连接、去重、命中直回源、TTL 递减转发、显示响应。
3. 同一 mutex 保护 ID、邻居及非可重入网络地址 helper；条件变量确保本机完成绑定后发送 CONNECT；保留原 ABI。
4. `make -C src/Assignment-3`；`python3 tests/integration.py` 覆盖链路、TTL、环路、多命中、并发。记录版本、命令、退出状态和节点输出。主会话仅签发自测。
5. 独立 Verifier 复现并设计补充检查。修复后复验。组装 submission 后交不同独立 Reviewer 审实际 ZIP，最后用户上传。

## 边界与交接

原代码非 TODO 的参数 strcpy/atoi、stdin EOF、findInDirectory 早返回未 closedir、UDP helper 异常包与错误循环保持不动。使用有效 CLI、有效目录、协议包和打开的终端输入验证；说明未覆盖跨主机和长时间资源行为。轻量日志可跟踪，数据和构建物留本机。无外部资料研究或报告需求。

Next role: Implementer 主会话 → 独立 Verifier → 独立 Reviewer。
