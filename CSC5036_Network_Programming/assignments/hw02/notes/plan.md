# hw02 实现计划
执行者：Codex 主会话；授权：实现并连续执行全部本地测试，不上传。
来源：Assignment-2_ Socket Programming.md 的 Basic Socket Programming、Simple File Transfer、Dive Deeper，以及用户提供的助教邮件。

骨架分析：socket_server.c:30 起缺少初始化和 poll/accept；socket_client.c:18 起缺少连接和接收；file_client.c:59 指定 1024 字节文件名头；file_server.c:110 起缺少文件接收实现。原件完整保留，工作副本在 src/。

1. 补全基础通信 TODO；完整处理发送/接收短读写、EINTR、对端断开，服务器保留 poll 和 backlog=3。
2. 补全文件传输 TODO；每个客户端独立记录文件名头进度和 FILE 指针，流式写盘，以 EOF 结束，不用累计 int 字节数限制文件大小；保留原文件协议、CMake 和脚本。
3. 用原 CMake 构建四个程序并开启编译告警；用提供的三个脚本测试，校验所有生成文件的 SHA-256；增加分片文件名头、二进制回显、空文件、慢客户端并发、异常断开等集成测试。命令和输入/代码哈希保存在 results/<run-id>/。

自动验收：cmake -S src -B src/build && cmake --build src/build；python3 tests/integration.py。预期所有断言通过、服务器持续存活。人工验收不作为本轮本地测试的前提。
范围：不提交 Blackboard，不声称独立验证，不组装已审查最终包；不自动提交 Git。用户重写后需重新测试。

## 2026-10-10 TODO-only修订
用户明确要求不修改非TODO语句。恢复四个C文件的全部原始字节，仅在各TODO注释后添加带BEGIN/END标记的实现；原CMake与脚本不改。用 tests/check_todo_only.py 移除新增块后逐字节比对ZIP。原基础回显固定strlen/send语义不能声称二进制或完全短写健壮性，因此基础测试对齐题目的文本消息要求；文件测试继续使用二进制、分片/合并头及大文件哈希。重新构建、自测、独立验证与审查，旧结论仅属旧版本。
