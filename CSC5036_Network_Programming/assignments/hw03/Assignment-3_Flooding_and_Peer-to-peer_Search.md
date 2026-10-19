# CSC4303 Assignment-3: Flooding and Peer-to-peer Search

### Deadline: November 1st, 2026, 23:59 (UTC+8)

### Name: 

### Student ID: 

This is not a group assignment. **You are not allowed to copy or look at code from other students.** However, you are welcome to discuss the assignments with other students without sharing code. 

Let's get started!

## Overview
This assignment outlines the implementation of a basic simulation of a peer-to-peer (P2P) file search protocol using flooding mechanism, akin to the Gnutella protocol. In this flooding-based protocol, when a peer searches for a file, it floods query messages to all its neighbors, who in turn flood to their neighbors, allowing the query to propagate through the P2P network until the file is found or the search expires.

## Basic Requirements
As for the whole project:
- It must be written in C on a Unix-like Operating System (like Linux or macOS).
- You should use `gcc` or `clang` supporting C17 standard as the compiler (you can use features up to C17).
- Make sure GNU Make is installed in your system.
  On Ubuntu (including an Ubuntu EC2 instance), install the build tools if needed and check their versions:

  ```bash
  sudo apt update
  sudo apt install -y build-essential
  gcc --version
  make --version
  ```

- **If you are using Windows,** you can either use **WSL2**, MSYS2, or Cygwin to compile and run this assignment.
    - See [Microsoft WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install) for details
    - ⚠️ **Recommended: Use WSL2.** MSYS2 and Cygwin are not tested and use them as your own risk.
- You may also use a virtual machine locally or on AWS EC2 as your development environment
- ⚠️ **Keep an eye on AWS Cost Billing if you choose EC2!**

We provide several helper function files for you: **`utils.c`**, **`utils.h`**, **`network.c`**, and **`network.h`**, with **`network.c`** offering UDP communication APIs. You may choose to use these provided functions. Make sure your implementation follows the command-line call examples (you will see the command-line call examples under **three-party example**).

Your responsibility is to implement the operational procedure in **`main.c`**, **`server.c`**, and **`utils.c`**, ensuring they meet the criteria for command-line call examples. You are required to fill in the TODOs in the three files. For existing functions, you are only allowed to write code in the TODOs and should not modify other parts. As an exception, you may add necessary control flow around the provided log statements so that each message is printed only when appropriate. However, you can implement your own auxiliary functions outside if needed. Do not include other header files.

For **`main.c`**: **4 TODOs**

- Parse the command-line arguments, record neighbor information, and send CONNECT requests to all neighbors to establish connections.
- Handle server operations (you may consider using a mutex to safely share the neighbor structure between threads).
- Make sure the query ID List and Neighbor List data structures are maintained.

For **`server.c`**: **9 TODOs**

- Init a server that loops and receive packets.
- Read the packet and determine the packet type (there are three types: CONNECT, QUERY, and RESPONSE).
- If the packet is a CONNECT type, establish the connection between the server and the packet sender; add the packet sender as a neighbor.
- If the packet is a QUERY type:
    - Check if the query packet has a duplicated ID based on its ID.
    - Search the target directory for the queried file.
    - If the queried file is found, sends a response back to the server that initialized the query.
    - If the file is not found and TTL (Time To Live) is greater than 1, decrease TTL by 1 and flood the query to all neighbors except the original query source.
    - The search fails silently if there are no search results from any reachable server, and the host may receive multiple responses if the query is flooded to multiple server. (you may consider sharing the query ID structure between threads for this purpose).
- If the packet is a RESPONSE type, print out the search response.

For **`utils.c`**: **6 TODOs**

- Implement the functions in **`utils.c`** to support the operations in **`main.c`** and **`server.c`**.


## Objectives

You must achieve three goals to ensure the protocol functions correctly:

1. **Basic Query Flooding**
    
    Confirm that a query packet is distributed to all neighboring servers.
    
    * Procedure:
        1. Launch connected server instances on different terminals, each with a unique port and directory.
        2. Initiate a query for a file that does not exist in any node's directory, using a sufficiently large TTL.
        3. Make sure that all other servers receive the query packet.
    * Expected Outcome: Each server receives the query packet.
2. **Loop Avoidance**
    
    Ensure the system prevents endless looping of query packets in a network with loops.
    
    * Procedure:
        1. Set up a network with at least one loop.
        2. Issue a query request from a server within the loop.
        3. Monitor query packet flow to ensure each query ID is processed at most once per server; duplicate copies should be discarded.
    * Expected Outcome: Query packets do not loop indefinitely; servers discard duplicate queries without forwarding them again.
3. **TTL Control**
    
    Verify that the Time-to-Live (TTL) mechanism restricts query packet propagation.
    
    * Procedure:
        1. Assign a low TTL value (e.g., 1) to query packets.
        2. Send a query from one server.
        3. Check that the query packet is not forwarded beyond immediate neighbors as the TTL expires.
    * Expected Outcome: Query packets do not extend beyond their TTL scope, preventing excess network traffic and loop risks.

## Testing Environment Setup

The test environment consists of multiple directories, each representing a server with a unique file. Use multiple terminals to run the compiled "p2p_server" binary with necessary arguments to simulate the distributed network.

```
.
├── Makefile
├── dir1
│   ├── file1
│   └── file2
├── dir2
│   └── file3
├── dir3
│   └── file4
├── dir4
│   ├── file5
│   └── file6
├── dir5
│   └── file7
├── main.c
├── network.c
├── network.h
├── server.c
├── server.h
├── utils.c
└── utils.h
```

After completing the TODOs, run the following command in the assignment directory to build `p2p_server`:

```bash
make
```

**Usage**:

```console
$ ./p2p_server PORT_NUM TTL DIR [NEIGHBOR_HOST NEIGHBOR_PORT]...
```

Each optional neighbor must be specified as a host–port pair.

Run all nodes on the same machine in separate terminals, with each terminal in the assignment directory. Start the nodes in the order shown and wait for each node to print `[CONNECT] Successfully bind with the port: ...` before starting the next. Stop all nodes with Ctrl+C before switching to another test.

### Three-Party Example
⚠️ The following are examples for three-party communications. You should strictly follow the output format in your implementation. However, the content of the output (for example, filename and directory name) should follow the exact layout. **YOU SHOULD NOT DIRECTLY COPY THE EXAMPLE OUTPUT AND HARD-CODE IT INTO YOUR CODE!**

The examples show key log messages only. Message order may vary because nodes and threads run concurrently.

***Test*: *Flooding query and TTL Control***

(Bob being a neighbor to Alice, Carol being a neighbor to Bob)

```bash
# Initialize Alice as the boostrap server
(terminal Alice) $ ./p2p_server 49151 1 dir1

# Bob being a neighbor connected to Alice
(terminal Bob)   $ ./p2p_server 49152 2 dir2 127.0.0.1 49151 

# Carol being a neighbor connected to Bob
(terminal Carol) $ ./p2p_server 49153 2 dir3 127.0.0.1 49152  
```  

In Carol's terminal, search for `file1`:

```text
file1
```

Carol should receive:

```ini
[SERVER INFO] Received new packet: RESPONSE packet
[FILE] File file1 found on address 127.0.0.1, with port 49151
```

Bob forwards the query to Alice because TTL allows another hop. Alice's log should show:

```ini
[SERVER INFO] Received new packet: QUERY packet
[RESPON] File file1 found, responding to query.
```

Now search for `file4` (in Carol's directory) in Alice's terminal:

```text
file4
```

Bob's log should show:

```ini
[SERVER INFO] Received new packet: QUERY packet
[TTL] Packet TTL expired, stopping forwarding.
```

Bob would not forward the packet to Carol address due to the initial TTL being 1. As a result, the packet will expire at Bob. This proves the file flooding query and TTL control.  



***Test: Avoid Loops***

(Bob being a neighbor to Alice, Carol being a neighbor to Bob and Carol being a neighbor to Alice.)

Now all three parties are connected with each other as neighbors. 

```bash
# Initialize Alice as the boostrap server
(terminal Alice) $ ./p2p_server 49151 64 dir1

# Bob being a neighbor connected to Alice
(terminal Bob)   $ ./p2p_server 49152 2 dir2 127.0.0.1 49151 

# Carol being a neighbor connected to Bob
(terminal Carol) $ ./p2p_server 49153 2 dir3 127.0.0.1 49152 127.0.0.1 49151
```

In Alice's terminal, search for `missing_file`, which does not exist in any node's directory:

```text
missing_file
```

Bob and Carol each process the query once and forward it. When another copy with the same ID arrives, they discard it.

Look for the following messages in Bob's and Carol's terminals. The ID and message order may vary.

```text
[TTL] Forwarding packet with TTL=63
[DUPLICATE ID] Duplicate packet with ID <ID> detected. Ignoring and discarding.
```

Query forwarding should stop without TTL expiration. This verifies that duplicate-ID checking prevents repeated forwarding in the loop.

***Test: TTL Control***

```bash
# Initialize nodes in a chain topology
(terminal Alice) $ ./p2p_server 49151 1 dir1

# Bob connects to Alice
(terminal Bob)   $ ./p2p_server 49152 2 dir2 127.0.0.1 49151

# Carol connects to Bob
(terminal Carol) $ ./p2p_server 49153 2 dir3 127.0.0.1 49152

# David connects to Carol
(terminal David) $ ./p2p_server 49154 2 dir4 127.0.0.1 49153
```

In Alice's terminal, search for `file5` (in David's directory) with TTL=1:

```text
file5
```

Bob's log should show:

```ini
[SERVER INFO] Received new packet: QUERY packet
[TTL] Packet TTL expired, stopping forwarding.
```

Carol and David should not receive this query because TTL expired at Bob. Alice should receive no search response.

Stop all four nodes with Ctrl+C. Restart them in the same order using the commands above, but change Alice's TTL from 1 to 3:

```bash
./p2p_server 49151 3 dir1
```

Then search for `file5` again in Alice's terminal. Bob should forward the query with TTL=2, and Carol should forward it with TTL=1.

David should find the file and respond:

```ini
[SERVER INFO] Received new packet: QUERY packet
[RESPON] File file5 found, responding to query.
```

Alice should then receive:

```ini
[FILE] File file5 found on address 127.0.0.1, with port 49154
```

David can respond to a query with TTL=1 because a node searches its local directory before deciding whether to forward the query. This demonstrates that the TTL control mechanism works as expected.


## Grading Criteria Parts

(10%): Pass Makefile compiling (you need to write at least some meaningful codes).

(10%): Network is well setup, i.e. server node can be joined to existing node by passing appropriate command line arguments.

(20%): Successful in flooding query.

(20%): Successful in TTL Control.

(20%): Successful in avoiding loops.

(20%): Thread safety is properly implemented with mutexes and supports concurrent operations.


We will test your code with three to five servers with different neighbored topologies on a Unix-like server machine. So your implementation should be robust to handle with multiple servers running in different terminals. 

## Submission

1. Complete the required TODOs in the starter code.
2. Repack the code package, including your completed source files, header files, `Makefile`, and the original test directories and files supplied with the starter code, into one ZIP file. Keep the original file names and directory structure. Do not include `README.md` or any additional test files you created yourself.
3. Name the ZIP file `<Your_ID>_hw3.zip` (replace `<Your_ID>` with your student ID) and upload it to Blackboard.
4. **Late Submission Policy:** Each student’s first late assignment across the entire course receives **80% of the mark earned (mark × 0.8)**, and all subsequent late assignments receive **0 marks**.
