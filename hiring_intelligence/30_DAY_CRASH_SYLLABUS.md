# 🚀 30-DAY CRASH SYLLABUS: HOW TO CRACK ANY MNC FRESHER EXAM & INTERVIEW

> Designed specifically to clear **Amazon OA, Google GOC, Microsoft Codility, Goldman Sachs HackerRank, TCS NQT (Prime/Digital), Infosys HackWithInfy, and Accenture Cognitive/Coding**.

---

## 📅 THE 4-WEEK INTENSIVE PREPARATION ROADMAP

```
Week 1: High-Frequency Data Structures (Arrays, Strings, HashMaps, Two Pointers, Linked Lists)
Week 2: Non-Linear Structures & Algorithms (Trees, BSTs, Heaps, Graphs, Dynamic Programming)
Week 3: Core Computer Science Fundamentals (DBMS & SQL, OS, Computer Networks, OOPs)
Week 4: Mock OAs, Amazon 16 Leadership Principles, Project Defense, & HR SuperDay Rounds
```

---

### 🧩 WEEK 1: FOUNDATION DSA (HIGH ACCURACY SPEED)
*Target: Solve 5 problems daily on LeetCode. Focus on pattern recognition.*

1. **Two Pointers & Sliding Window**:
   - Two Sum (Sorted & Unsorted)
   - Best Time to Buy and Sell Stock
   - Longest Substring Without Repeating Characters
   - Container With Most Water
   - 3Sum
2. **Fast & Slow Pointers / Linked Lists**:
   - Reverse a Linked List
   - Detect Cycle in a Linked List (Floyd’s Algorithm)
   - Merge Two Sorted Lists
   - Remove Nth Node From End of List
3. **Prefix Sum & Hash Maps**:
   - Subarray Sum Equals K
   - Group Anagrams
   - Valid Anagram & Valid Parentheses (Stack)

---

### 🌲 WEEK 2: TREES, GRAPHS & DYNAMIC PROGRAMMING
*Target: Essential for Google, Amazon, Microsoft, and TCS Prime rounds.*

1. **Binary Trees & Binary Search Trees**:
   - Maximum Depth of Binary Tree
   - Invert Binary Tree
   - Lowest Common Ancestor (LCA) in Binary Tree & BST
   - Binary Tree Level Order Traversal (BFS)
   - Validate Binary Search Tree
2. **Graphs (BFS / DFS / Shortest Path)**:
   - Number of Islands (Grid DFS)
   - Clone Graph
   - Course Schedule (Topological Sort / Cycle Detection)
   - Rotting Oranges (Multi-source BFS)
   - Dijkstra's Algorithm (Shortest path using Min-Heap)
3. **Dynamic Programming (Knapsack & Subsequences)**:
   - Climbing Stairs / House Robber
   - 0/1 Knapsack Problem
   - Longest Increasing Subsequence (LIS)
   - Longest Common Subsequence (LCS)
   - Coin Change (Min coins)

---

### 💻 WEEK 3: CORE CS FUNDAMENTALS (INTERVIEW CRUSHERS)

#### 1. Database Management Systems (DBMS & SQL)
- **ACID Properties**: Atomicity, Consistency, Isolation, Durability.
- **Transactions & Concurrency**: Dirty Read, Non-repeatable Read, Phantom Read. Isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable).
- **Indexing**: Why B+ Trees are used instead of Binary Search Trees for disk storage. Clustered vs Non-Clustered index.
- **SQL Queries to Practice**:
  * Finding the Nth highest salary:
    ```sql
    SELECT DISTINCT salary FROM Employee ORDER BY salary DESC LIMIT 1 OFFSET N-1;
    ```
  * INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN.
  * GROUP BY with HAVING clause vs WHERE clause.

#### 2. Operating Systems (OS)
- **Process vs Thread**: Process has its own address space; threads share process memory (heap, code, data) but have independent stacks and program counters.
- **Virtual Memory & Paging**: Logical vs Physical address; Page Table, TLB (Translation Lookaside Buffer), Page Fault handling.
- **CPU Scheduling**: Round Robin, FCFS, Shortest Job First (SJF).
- **Synchronization**: Mutex (Mutual Exclusion lock) vs Semaphore (Counting signaling mechanism).
- **Deadlock 4 Conditions**: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.

#### 3. Computer Networks (CN)
- **OSI 7 Layers**: Physical, Data Link, Network, Transport, Session, Presentation, Application.
- **TCP vs UDP**: TCP is connection-oriented, reliable, with flow & congestion control (3-way handshake: SYN, SYN-ACK, ACK). UDP is connectionless, fast, header size 8 bytes vs 20 bytes.
- **DNS Resolution**: What happens when you type `https://google.com` in a browser?
  1. Browser checks cache (Browser -> OS -> Router -> ISP).
  2. Resolves via DNS Root Server -> TLD Server (.com) -> Authoritative Nameserver.
  3. TCP 3-way handshake established.
  4. TLS/SSL handshake for HTTPS encryption.
  5. HTTP GET request sent; Web server responds with HTML/CSS/JS.

#### 4. Object-Oriented Programming (OOPs)
- **Encapsulation**: Binding data and functions together into a single unit (class) with access specifiers (`private`, `public`, `protected`).
- **Abstraction**: Hiding internal implementation and showing only functionality (Interfaces and Abstract classes).
- **Inheritance**: Code reusability (`extends` in Java, `:` in C++).
- **Polymorphism**:
  * Compile-time (Method Overloading)
  * Run-time (Method Overriding using `virtual` in C++ or `@Override` in Java).

---

### 🏆 WEEK 4: BEHAVIORAL & AMAZON 16 LEADERSHIP PRINCIPLES

For every interview, prepare **4 stories in the STAR format** (Situation, Task, Action, Result):
1. **Customer Obsession / Deliver Results**: A time you went above and beyond to build something usable.
2. **Ownership / Bias for Action**: A time you spotted a critical bug or performance slowdown in a college project and took the initiative to fix it without being told.
3. **Have Backbone; Disagree and Commit**: A time you had a technical disagreement with a team member and how you resolved it using data.
4. **Learn and Be Curious**: A time you learned a completely new framework or language in 48 hours for a hackathon.
