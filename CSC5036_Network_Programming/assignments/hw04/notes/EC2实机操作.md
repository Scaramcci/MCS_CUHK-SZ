# hw04 实机操作

准备好课程 AWS Academy 账号、本机终端和与实例匹配的 SSH 私钥。作业一讲义第 9 页介绍课程 Lab 入口，第 20–26、31、39–40 页介绍密钥、实例公网地址和文件传输。本次实例配置、测试和提交格式以 [hw04 教师要求](../requirements/Assignment-4.md) 为准。截止时间为北京时间 2026-11-15 23:59。

## 1. 从课程账号进入 EC2

登录作业一使用的 AWS Academy 课程，进入 **Modules → Launch Learner Lab → Start Lab**。等 AWS 指示灯变绿，点 **AWS** 打开课程控制台，搜索 **EC2**，进入 **Instances**。如果已有账号但看不到这门课的 Learner Lab，请先向助教确认课程入口。

选课程允许的 Region。若有自己的旧实例，同时满足 t3.small、Ubuntu Server 24.04 LTS、64-bit x86 (AMD64)，可选中它并执行 **Instance state → Start instance**。否则点 **Launch instances**，按下表创建一台。

| 设置 | 选择 |
| --- | --- |
| Name | hw04-chord |
| AMI | Ubuntu Server 24.04 LTS，64-bit (x86) |
| Instance type / Number of instances | t3.small / 1 |
| Key pair | 选当前 Region 中与本机 .pem 匹配的密钥对；若重新创建，下载 .pem 并保存在本机 |
| Network settings | 本机直连 SSH 用可分配公网 IPv4 的子网，启用公网 IPv4，入站允许 SSH / TCP 22，来源 My IP |
| Storage | 保留该 AMI 默认根卷大小 |

若课程 Lab 无法选择 t3.small，请联系助教。等实例显示 **Running**，状态检查通过，点开实例，复制本次的 **Public IPv4 address**。即使复用旧实例，也用控制台当前显示的地址。5001、5002、5003、5004 和 5010 由同一实例内部的节点使用，安全组只需配置 SSH。

## 2. 在本机上传已审查的 ZIP

打开本机 Bash 终端。修改下面 KEY 和 HOST 两行，用实际 .pem 文件路径和公网地址替换示例值。这里上传的是已完成的候选包，requirements 里的教师 ZIP 是起始代码。

```bash
cd /home/scarramcci/Project/MCS_CUHK-SZ/CSC5036_Network_Programming/assignments/hw04
KEY="$HOME/Downloads/你的密钥.pem"
HOST="实例当前公网IPv4"
ZIP=results/candidate/20261104T074144997572Z/226040255_hw4.zip
chmod 400 "$KEY"
sha256sum "$ZIP"
scp -i "$KEY" "$ZIP" "ubuntu@$HOST:~/226040255_hw4.zip"
ssh -i "$KEY" "ubuntu@$HOST"
```

ZIP 的 SHA-256 应为 `12b0688cd6bce4012f075a532f853a144277c98cc11b00009c468a6fa4389121`。连接超时先核对 Lab 状态、最新公网地址及 SSH 入站的 My IP。出现 `Permission denied (publickey)` 时核对用户名 `ubuntu` 和实例详情中的 Key pair name。[AWS SSH 与 SCP 操作说明](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html)

## 3. 在 EC2 上解压并运行

SSH 登录后执行。每次使用新的实验目录，记录系统、代码版本和完整输出。实例类型在 EC2 控制台的 Instance type 栏核对为 t3.small。

```bash
mkdir -p ~/hw04-runs
RUN=$(mktemp -d ~/hw04-runs/run-XXXXXXXX)
cd "$RUN"
{ date -u; cat /etc/os-release; uname -m; /usr/bin/python3 --version; } | tee environment.txt
sha256sum ~/226040255_hw4.zip
```

确认 Ubuntu 24.04、x86_64、系统 Python 3.12.x，并核对 ZIP 哈希与第 2 步一致。若缺少 unzip，执行 `sudo apt update && sudo apt install -y unzip`。继续在同一个 SSH 窗口执行以下命令，等测试结束后再输入下一组。

```bash
unzip ~/226040255_hw4.zip
cd Assignment-4
sha256sum chord_node.py test_dht.py > ../source-sha256.txt
/usr/bin/python3 test_dht.py > ../output_dht.txt 2>&1
echo "$?" > ../exit-status.txt
cat ../output_dht.txt
echo "$RUN"
```

最后一行显示本次目录，例如 `/home/ubuntu/hw04-runs/run-AbCd1234`。记下实际路径以便下载。测试会等待各节点稳定，输出已重定向，执行期间终端暂时安静是正常现象。

## 4. 核对结果并取回记录

在输出中查找 `All retrieval tests: Success`、`Get non-existent key: Success`、`Duplicate key test (overwrite): Success` 和 `All keys accessible after transfer: Success`。教师脚本会捕获异常，即使退出码是 0 也可能出现 `Test failed with error` 或某行 `Failed`。保留完整日志以便定位失败阶段。

再看两处实际数据。节点 30 加入后，SHA-1 哈希模 32 落在 24–30 的键应由节点 1 迁到 30，其他键留在原属节点，每键只出现一次。节点 15 停止后，最后一组 finger table 按第 1 至第 5 项应如下。基础功能与故障恢复加分项分别检查。

| 节点 | 故障恢复后的五个 finger ID |
| --- | --- |
| 1 | 8, 8, 8, 23, 23 |
| 8 | 23, 23, 23, 23, 30 |
| 23 | 30, 30, 30, 1, 8 |
| 30 | 1, 1, 8, 8, 23 |

在 SSH 窗口输入 `exit` 回到刚才的本机终端。将下面 REMOTE_RUN 改成上一步显示的实际路径。

```bash
REMOTE_RUN='/home/ubuntu/hw04-runs/run-替换为实际值'
DEST="results/ec2-$(basename "$REMOTE_RUN")"
mkdir -p "$DEST"
for file in environment.txt source-sha256.txt exit-status.txt output_dht.txt; do
    scp -i "$KEY" "ubuntu@$HOST:$REMOTE_RUN/$file" "$DEST/"
done
ls -lh "$DEST"
```

把本地结果目录告诉我，并说明控制台显示的实例类型，我就可以核对实机输出和已审查的代码版本。若测试报错，也保留同一组文件。

## 5. 停止实例与交付

确认日志已取回后，在 EC2 勾选本次实例，点 **Instance state → Stop instance**，等待状态变为 **Stopped**，然后按课程页面说明结束 Lab。本次 Blackboard 提交物为测试通过的 `226040255_hw4.zip`，包内共两个文件，分别是 `Assignment-4/chord_node.py` 和 `Assignment-4/test_dht.py`。运行记录留在本地。
