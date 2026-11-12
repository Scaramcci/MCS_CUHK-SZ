# EC2 实机运行

主会话于 2026-11-12 在用户提供的课程实验实例运行 hw04，运行目录为 ~/hw04-runs/ec2-20261112103924264Z/Assignment-4。SSH 上传原样候选 226040255_hw4.zip 后，以 sha256sum -c 核对 ZIP 的 SHA-256 为 12b0688cd6bce4012f075a532f853a144277c98cc11b00009c468a6fa4389121，再用系统 Python 的 zipfile 模块解压。

实际运行命令为 `/usr/bin/python3 test_dht.py > ../output_dht.txt 2>&1`。执行一轮未经修改的教师测试，原端口，随机写入节点由教师脚本选择。environment.txt、source-sha256.txt、exit-status.txt 和 output_dht.txt 从该运行目录取回。实例类型来自 EC2 的 DMI product_name；课程账号归属依据用户提供的实例上下文。
