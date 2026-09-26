# CSC4303 Assignment-1: EC2 Measurement (2 questions)

### Deadline: 23:59, Sep 27, Sunday

---

### Name:

### Student Id:

---

## Question: Measure the EC2 Network performance

1. (2 mark) The metrics of network performance include **TCP bandwidth** and **round-trip time (RTT)**. Within the same region, what network performance is experienced between instances of the same type and different types? In order to answer this question, you need to complete the following table.

   | Type                    | TCP b/w (Mbps) | RTT (ms) |
   | ----------------------- | -------------- | -------- |
   | `t3.medium`-`t3.medium` |                |          |
   | `m5.large`-`m5.large`   |                |          |
   | `c5n.large`-`c5n.large` |                |          |
   | `t3.medium`-`c5n.large` |                |          |
   | `m5.large`-`c5n.large`  |                |          |
   | `m5.large`-`t3.medium`  |                |          |

   > Region: US East (N. Virginia)

2. (2 mark) What about the network performance for instances deployed in different regions? In order to answer this question, you need to complete the following table.

   | Connection              | TCP b/w (Mbps) | RTT (ms) |
   | ----------------------- | -------------- | -------- |
   | N. Virginia-Oregon      |                |          |
   | N. Virginia-N. Virginia |                |          |
   | Oregon-Oregon           |                |          |

   > All instances are `c5.large`.
