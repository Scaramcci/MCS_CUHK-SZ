# Assignment 2: Socket Programming

原始要求：[Assignment-2_ Socket Programming.md](Assignment-2_%20Socket%20Programming.md)；原始骨架：[Assignment-2.zip](Assignment-2.zip)，均未修改。

## 当前实现：只补 TODO

四个C程序在 `src/`。所有新增代码均位于原TODO注释紧后，以 `BEGIN/END TODO IMPLEMENTATION` 标记。移除这些新增块后，四个C文件与原ZIP逐字节一致（包括原换行和注释）；CMakeLists.txt和三个脚本内容也完全一致。没有通过宏替换或绕开原有代码。

```bash
python3 tests/check_todo_only.py
```

该检查对四个C文件分别确认7/5/11/8处TODO补全；证据见 `results/todo-only-scope-check.json`。上一版非TODO改动已恢复；旧代码保存在 `results/before-todo-only/`，旧记录仅适用于旧版。

实现包含 poll 最多30个客户端、backlog=3、文本回显；文件协议为1024字节补零文件名头、每连接独立状态、二进制逐块写盘，并以 EOF 结束，不依赖32MB累计计数或整文件缓冲区。原骨架的文本回显使用strlen，故不声称基础echo支持含NUL的任意二进制；文件内容不受此限制。

环境已具备：Ubuntu、gcc 15.2、CMake 4.2，无需安装。原CMake构建四个程序，严格告警 `-Wall -Wextra -Wpedantic -Werror` 通过。

## 构建与运行

在本作业目录执行：

```bash
cmake -S src -B src/build
cmake --build src/build
```

基础通信：一个终端进入 `src/build/` 执行 `./socket_server`，另一个终端进入同目录执行 `./socket_client` 或 `bash ../con.sh`。

文件传输：在 `src/` 执行 `./generator.sh`；一个终端进入 `src/build/` 执行 `./file_server`，另一个终端进入同目录执行 `./file_client ../file1.zip` 或 `bash ../con_file.sh`。使用 `sha256sum ../file1.zip file1.zip` 校验内容。两个服务器都使用8080端口，须依次运行；Ctrl+C停止服务器。默认监听地址按骨架为INADDR_ANY，客户端连接127.0.0.1。

## 测试与证据

```bash
python3 tests/integration.py
```

需8080端口空闲。测试启停自身服务器、构建程序并调用教师三个脚本，每次生成约150MB随机源测试文件及接收副本；随机数据仅用于传输校验，没有固定种子，输入哈希和数据路径保存在运行记录，源数据位于Git忽略的 `data/raw/<run-id>/`。

新版主会话自测：`results/20261010-085313/run.json`，退出0。单客户端、教师30客户端脚本、长文本及30路精确文本回显、7个教师生成文件并发传输与SHA-256、分片/合并文件名头、空文件、慢发送者、不合法连接后继续服务、无服务器错误退出全部通过。

新版独立验证与审查记录分别放在 `results/independent-verifier-todo-only/`、`results/independent-reviewer-todo-only/`。以各自实际生成的结论为准。旧版 `results/20261010-082831/` 和旧独立记录不是新版验证证据。

## 保留原骨架后的边界

基础回显保留原有单次send及strlen，不提供任意二进制回显、完全短写恢复或恶意慢读者隔离保证；TODO内忽略SIGPIPE避免对端断开杀死服务器。原poll错误分支也保留原样。

文件协议沿用EOF而没有声明长度或成功ACK，不能凭客户端退出码断言服务端写盘成功；正常完整性以源/目标哈希一致为准。提前正常关闭可能留下部分文件；同名上传仍可能覆盖，不提供同名并发协调。未对无限大小做实测。

## 提交

按助教邮件只交包含原8个根目录文件的ZIP，不交报告、截图、测试数据或build缓存。此次按用户要求完成代码与测试，尚未组装/审查最终ZIP，未上传Blackboard或自动提交Git。截止时间为2026-10-16 23:59（原文未注明时区）。用户重写后须重新测试。
