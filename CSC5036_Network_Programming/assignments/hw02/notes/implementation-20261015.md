# 2026-10-15 提交准备记录

执行者：Codex主会话，Implementer / 打包者；独立Verifier为 /root/verify_hw02，独立Reviewer为 /root/review_hw02。授权：整理代码呈现、按要求重测并准备可直接提交ZIP，不上传。工作分支codex/hw02-submission，未提交Git。

来源：Assignment-2_ Socket Programming.md 的 Basic Socket Programming、Simple File Transfer、Dive Deeper、Build/Testing，以及用户贴出的TA提交邮件。教师原件未改；无额外课程/作业AGENTS或requirements目录，原件位于hw02根目录。

仅在TODO新增区域删除BEGIN/END内部标记、简化三条注释、展开单行错误处理。results/20261015-style-cleanup/token-comparison.json确认4个C非注释词法token与HEAD前版一致；todo-scope.json确认全部非TODO原文及4个辅助文件字节不变。更新tests/check_todo_only.py使用原ZIP固定文本片段检查，不依赖源码标记。

实际自测：python3 tests/integration.py，退出0，记录results/20261015-115947/run.json。严格告警编译、30并发文本回显、教师三个脚本、5个10MB和2个50MB文件SHA-256、分片/合并文件头、空文件、慢头、错误恢复通过。源测试数据在data/raw/20261015-115947，构建/接收文件在local_artifacts/20261015-115947/build，均只留本地；未覆盖旧运行输出。

独立复验：results/verification-20261015/verification.md，已实际完成严格编译、30并发文本、64MiB二进制传输哈希、30并发文件和异常恢复；记录含源码哈希与命令。结论属于独立Verifier。原骨架send/poll及EOF协议的边界保留在README及验证报告中，未声称所有异常路径已修复。

通过检查后组装submission/Assignment-2.zip，内部仅原8个根文件，大小8964字节，SHA256 058216a4588309bb35c932cfff02e3c7c9dd2db61ffc882539c30aa4454351af。逐文件与自测源码字节和哈希核对，ZIP CRC检查通过。清单在results/submission-20261015/manifest.json。

最终包结论以独立Reviewer写入results/submission-review-20261015/review.md为准；打包者不代填通过结论。提交包未上传Blackboard。ZIP被仓库规则忽略，本机保留；未自动Git commit或push。

完成：独立Verifier补做了实际ZIP全新解包→cmake ..→make，退出0，见results/verification-20261015/package-build.json；独立Reviewer在results/submission-review-20261015/review.md签发该确切ZIP的Ready。最终哈希再核对一致。以上是引用他人的独立结论，不是作者自行批准。
