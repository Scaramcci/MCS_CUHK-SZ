# CSC4303 Assignment-4: Chord DHT (100 points + 20 bonus points)

### Deadline: November 15, 2026, 23:59 (UTC+8)

### Name:

### Student ID:

## Overview

This assignment involves implementing the **Chord Distributed Hash Table (DHT)** protocol, a scalable peer-to-peer lookup protocol that provides a way to locate keys in a distributed network environment. Chord is notable for its simplicity, provable correctness, and performance guarantees.

Your task is to implement the core algorithms of a Chord DHT including key lookup, node join, stabilization mechanisms, key storage, and (optionally) fault tolerance.

## Background

The Chord protocol specifies how to find the location of keys, how new nodes join the system, and how to recover from node failures. Each node in a Chord system maintains a routing table called a **finger table** that enables fast key lookups in **O(log N)** time, where N is the number of nodes in the system.

Chord arranges nodes in a logical ring where each node has a **successor** and a **predecessor**. Keys are assigned to nodes based on consistent hashing, which provides load balancing and minimizes the number of keys that must move when nodes join or leave the system.

## Required Experimental Environment

**Complete and run this assignment on one `t3.small` Amazon EC2 instance in your course's AWS Academy Learner Lab.** Running the assignment on a personal computer, a local virtual machine, or a different instance type is not a supported course environment. All grading runs will use the environment below.

| Item | Required Configuration |
|------|------------------------|
| Platform | AWS Academy Learner Lab |
| EC2 instance | One `t3.small` instance (2 vCPUs, 2 GiB RAM) |
| Operating system | Ubuntu Server 24.04 LTS, 64-bit x86 (AMD64) |
| Runtime | System Python 3.12; Python standard library |
| Node deployment | Multiple Chord nodes within this single instance |
| Node communication | TCP over `127.0.0.1`, using the original test ports |

The test script creates multiple `Node` objects and TCP server threads in one Python process. Keep the original addresses and ports in `test_dht.py` unchanged. No deployment across multiple EC2 instances is required. 
### Setup and Execution

1. Start your Learner Lab session and open its AWS console. Launch one `t3.small` instance with Ubuntu Server 24.04 LTS (x86-64) in a Region permitted by your course's Learner Lab. The default root volume is sufficient; retain at least the AMI's required minimum. Connect to the instance terminal. If the required instance type is unavailable in your lab, contact the teaching staff.
2. Install or check the tools on the instance:

   ```bash
   sudo apt update
   sudo apt install -y python3 unzip zip
   python3 --version
   ```

3. Upload and extract the starter package on the instance. Complete the TODOs in `chord_node.py`, then run:

   ```bash
   cd Assignment-4
   python3 test_dht.py
   ```

   Run one test suite at a time and wait for it to finish before starting another.

4. The nodes use ports `5001`, `5002`, `5003`, `5004`, and `5010` inside the instance. These ports do not need inbound security-group rules because node communication stays on `127.0.0.1`. Configure access for your terminal connection method; for direct SSH, allow TCP port 22 from your own IP address.
5. Package and download your code using the submission instructions below. Stop the instance when you finish working and follow your Learner Lab's session instructions.

## Project Structure

```
.
├── README.md           # This file
├── chord_node.py       # Node implementation (YOUR WORK HERE)
└── test_dht.py         # Test suite (do not modify)
```

### Key Classes and Attributes

The `Node` class in `chord_node.py` provides the following attributes:

| Attribute     | Type                          | Description                                      |
|---------------|-------------------------------|--------------------------------------------------|
| `node_id`     | `int`                         | This node's identifier on the ring               |
| `host`        | `str`                         | Hostname / IP address                            |
| `port`        | `int`                         | TCP port for the node's server                   |
| `m`           | `int`                         | Number of bits in the identifier space (default 5) |
| `max_id`      | `int`                         | Size of the ring: `2^m`                          |
| `predecessor` | `(id, host, port)` or `None`  | Predecessor node address                         |
| `successor`   | `(id, host, port)`            | Successor node address                           |
| `finger`      | `list` of `(id, host, port)`  | Finger table (1-indexed, size `m+1`)             |
| `next`        | `int`                         | Index of the next finger to fix (1 to m)         |
| `data`        | `dict`                        | Local key-value storage                          |

### Provided Methods (do not modify)

- `remote_call(node_addr, command, params)` — Send a command to another node (or handle locally). Supported commands: `"find_successor"`, `"closest_preceding_node"`, `"get_predecessor"`, `"notify"`, `"ping"`, `"store"`, `"retrieve"`, `"get_data"`, `"transfer_keys"`.
- `run_server()` / `handle_client()` — TCP server that dispatches incoming commands.
- `stop()` — Gracefully shut down the node.

## Assignment Requirements

### Part 1: Core Chord Protocol

Implement the following methods in `chord_node.py`:

1. **`in_interval(id, start, end, inclusive_right=True)`** — Check if `id` falls within the interval `(start, end]` (or `(start, end)`) on the ring, handling wraparound.
2. **`find_successor(id)`** — Find the successor node for a given identifier.
3. **`closest_preceding_node(id)`** — Scan the finger table to find the closest preceding node.
4. **`create()`** — Create a new Chord ring with this node as the only member.
5. **`join(existing_node_addr)`** — Join an existing Chord ring via a known node.
6. **`stabilize()`** — Verify this node's immediate successor and notify it.
7. **`notify(node_addr)`** — Handle notification from a potential predecessor.
8. **`fix_fingers()`** — Refresh one finger table entry per call.

> **Note**: The stabilization protocol (`stabilize`, `fix_fingers`) is called manually in the test suite. In a real system, these would run periodically in the background.

### Part 2: Key Storage and Retrieval

9. **`hash_key(key)`** — Hash a string key to an identifier in `[0, 2^m - 1]`. Use `hashlib` (e.g. SHA-1) and take modulo `2^m`.
10. **`put(key, value)`** — Store a key-value pair in the DHT by routing to the responsible node.
11. **`get(key)`** — Retrieve a value from the DHT by routing to the responsible node.
12. **`transfer_keys(new_node_addr)`** — Transfer keys to a newly joined node that is now responsible for them.

### Part 3: Failure Recovery (Bonus, 20 points)

13. **`check_predecessor()`** — Check if the predecessor has failed; if so, set it to `None`.

   It is suggested to maintain a **successor-list** for fault tolerance. You may create additional helper methods as needed. `check_predecessor()` is called manually in the test suite to simulate periodic execution.

    > **Note**: Key replication for storage recovery is out of scope for this assignment.

## Testing

A comprehensive test suite is provided in `test_dht.py`. **Do not modify this file.** The test suite verifies:

| Test Function                    | What it tests                                        |
|----------------------------------|------------------------------------------------------|
| `create_chord_network`           | Ring creation, join, stabilization, finger tables    |
| `test_chord_key_storage`         | Key-value storage and retrieval from all nodes       |
| `test_edge_cases`                | Non-existent keys, duplicate key overwrites          |
| `test_key_transfer_with_new_node`| Key redistribution when a new node joins             |
| `test_node_failure_recovery`     | Finger table repair after a node failure (bonus)     |

Run on the required Learner Lab `t3.small` instance:

```bash
python3 test_dht.py
```

Optionally save output for your own debugging (do not include it in your submission):

```bash
python3 test_dht.py > output_dht.txt 2>&1
```

The test script prints many results instead of enforcing them with assertions, and its top-level exception handler may still leave a zero exit status after a failure. A completion banner or zero exit status alone does not establish correctness. Check the actual results, key distribution, and routing tables.

The script also runs the optional failure-recovery stage. Failure in this bonus stage does not by itself invalidate required functionality that passed earlier. Grading evaluates the required and bonus components separately.

## References

Stoica, I., Morris, R., Karger, D., Kaashoek, M. F., & Balakrishnan, H. (2001). Chord: A scalable peer-to-peer lookup service for internet applications. _ACM SIGCOMM Computer Communication Review_, 31(4), 149-160.

## Submission Guidelines

1. Complete the required TODOs in **`chord_node.py`** and test your implementation in the required Learner Lab `t3.small` environment.
2. Submit **code only** in one ZIP file. Include your completed `chord_node.py` and the original, unmodified `test_dht.py`. Keep these file names and the following directory structure:

   ```text
   <Your_ID>_hw4.zip
   └── Assignment-4/
       ├── chord_node.py
       └── test_dht.py
   ```

   Do not include `README.md`, `output_dht.txt`, reports, screenshots, `__pycache__`, virtual environments, SSH keys, or additional test files. No report, saved results, or screenshots are required.

3. Name the ZIP file **`<Your_ID>_hw4.zip`**, replacing `<Your_ID>` with your student ID, and upload it to **Blackboard**. For example, student ID `123456789` must submit `123456789_hw4.zip`. Do not rename either Python file or add an extra parent directory.

   From the parent directory of `Assignment-4`, replace `123456789` with your own student ID and create a fresh ZIP:

   ```bash
   zip 123456789_hw4.zip Assignment-4/chord_node.py Assignment-4/test_dht.py
   unzip -l 123456789_hw4.zip
   ```

   Ensure a previous ZIP with the same name is not present, since updating an existing ZIP can retain old files. The archive must contain only the two Python files shown above.

4. **Late Submission Policy:** Each student’s first late assignment across the entire course receives **80% of the mark earned (mark × 0.8)**, and all subsequent late assignments receive **0 marks**.

## Grading Criteria

**The final mark is determined by the behavior of the submitted code when the TA run it on a single AWS Academy Learner Lab `t3.small` EC2 instance, with multiple nodes inside that instance, using Ubuntu 24.04 LTS and Python 3.12.** Student-provided logs, reports, screenshots, or results from another environment are not grading evidence.

The required programming tasks remain those of the original Assignment 4. The written-report component is removed. The assignment uses a **100-point base scale**, with **20 optional bonus points** for failure recovery.

| Component | Base Weight | Points | Runtime Criteria |
|-----------|-------------|--------|------------------|
| **Basic Chord Protocol** | 40% | 40 | Correct ring creation, joining, interval/wraparound lookup, stabilization, and finger tables. Evaluate lookup results and the resulting predecessor/successor/finger state. |
| **Key Storage and Retrieval** | 40% | 40 | Correct key-value storage and retrieval through the nodes, missing-key behavior, and duplicate-key overwrite. |
| **Key Transfers** | 20% | 20 | Correct transfer of key responsibility and data placement after a new node joins, with existing keys still retrievable. |
| **Failure Recovery (Bonus)** | — | +20 | Detect a failed node and repair predecessor, successor, and finger-table state so surviving nodes can route correctly. Key replication and recovery of data held only by the failed node are not required. |

Teaching staff will use the original test suite and runtime checks of the required behavior, including checking routing tables and key ownership rather than relying only on printed success messages. The provided test file and network methods must remain unmodified. Do not hard-code example outputs or test-specific node/key results. There is no separate report score or speed-performance score.

The base components total **100 points**. The optional failure-recovery component adds up to **20 points**, so the maximum score for this assignment is **120 points before any late-submission penalty**.

Good luck, and enjoy implementing your distributed hash table!
