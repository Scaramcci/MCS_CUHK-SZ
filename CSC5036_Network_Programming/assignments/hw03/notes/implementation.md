# Implementer 交接

Executor: 主会话 /root；分支 codex/csc5036-hw03；日期 2026-10-21。

原件 `Assignment-3.zip` 与教师 Markdown 未修改。工作副本 `src/Assignment-3/` 仅 main.c、server.c、utils.c 有变更，位于 TODO、新辅助函数和日志控制处；network.c、三个头文件、Makefile、七个空测试文件保持原样。未新增头文件。

实现 CONNECT 双向邻居、源地址保存、直回源 RESPONSE、先查文件后判 TTL、原发查询注册 ID、接收去重、mutex 保护共享状态及非可重入网络 helper、绑定启动同步。128 个 ID 之外用辅助链表保留历史，避免固定数组越界或历史驱逐造成环路；其空间随不同查询数增长。辅助状态只在持共享锁时访问。

实际命令：`make -C src/Assignment-3`；`python3 tests/integration.py`（从作业目录执行等价路径）。自测脚本保留真实进程输出和 SHA-256。首轮 results/selftest-20261021T191812 因沙箱禁止创建 socket 失败；重试已使用获准本机 loopback 权限，results/selftest-20261021T191817 全部断言通过，退出 0。程序由测试脚本 SIGTERM 停止，日志中的 -15 是正常测试收尾。

覆盖：四节点 TTL1/TTL3 链路、两跳反向查询、本地命中、三节点环路去重及静止、五节点同时查询。无付费云环境或外部服务器。日志时间为执行主机时区，元数据携带时区信息。

限制：原非 TODO 代码的 stdin EOF、参数解析、目录句柄早返回、UDP helper 对异常数据包与系统调用错误的处理均保留。测试使用合法命令行和完整协议包；未声称已测试跨主机或不可靠网络。没有独立验证或最终审查结论，由后续独立角色出具。

Next role: 独立 Verifier 复现评分条件、边界与并发，并审查修改范围；只允许写 results/verification/ 和 notes/verification.md，禁止修实现。
