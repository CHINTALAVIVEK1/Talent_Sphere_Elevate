from college.coding.database import get_interview_progress, get_bookmarks

# 1. Base handwritten high-quality questions
INTERVIEW_QUESTIONS = [
    {
        "id": "py_1",
        "category": "Python",
        "sub_type": "Programming",
        "question": "What is the difference between list and tuple in Python?",
        "answer": "1. Mutability: Lists are mutable (can be changed after creation), whereas tuples are immutable.\n2. Syntax: Lists use square brackets [] while tuples use parentheses ().\n3. Performance: Tuples are faster and consume less memory than lists due to their fixed size.\n4. Use case: Use list for homogenous elements that can change; use tuple for heterogeneous collections where data integrity must be maintained.",
        "difficulty": "Easy"
    },
    {
        "id": "py_2",
        "category": "Python",
        "sub_type": "Programming",
        "question": "Explain GIL (Global Interpreter Lock) in Python and how to bypass it.",
        "answer": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once in CPython. This makes single-threaded execution fast but limits multi-threaded CPU-bound programs.\n\nWays to bypass GIL:\n1. Use multiprocessing instead of multithreading (allocates separate processes with distinct GILs).\n2. Use alternative Python implementations like Jython or IronPython.\n3. Delegate heavy computations to C-extension libraries (e.g. NumPy, Pandas) which release GIL during computation.",
        "difficulty": "Hard"
    },
    {
        "id": "java_1",
        "category": "Java",
        "sub_type": "Programming",
        "question": "What is the difference between equals() and == in Java?",
        "answer": "1. == operator compares reference or memory locations of two objects in heap memory (checks if they point to the exact same object).\n2. equals() is a method in the Object class. It is overridden in classes like String to compare the actual values/content inside the objects.",
        "difficulty": "Easy"
    },
    {
        "id": "sql_1",
        "category": "SQL",
        "sub_type": "Programming",
        "question": "What is the difference between WHERE and HAVING clauses in SQL?",
        "answer": "1. WHERE clause filters rows BEFORE grouping (GROUP BY) takes place. It cannot contain aggregate functions.\n2. HAVING clause filters groups AFTER the GROUP BY operation is completed. It is specifically used with aggregate functions (e.g., SUM, COUNT, AVG).",
        "difficulty": "Medium"
    },
    {
        "id": "ds_1",
        "category": "Data Structures",
        "sub_type": "CS Core",
        "question": "Explain the working of a Hash Map and how collisions are resolved.",
        "answer": "A Hash Map stores key-value pairs. It uses a hash function to compute an index in an array of buckets, where the value should be stored/retrieved.\n\nCollision Resolution Methods:\n1. Chaining (Linked Lists): Each bucket points to a linked list (or balanced tree in Java 8) of entries mapping to that hash code.\n2. Open Addressing: Finds another empty bucket dynamically. Forms include:\n   - Linear Probing (checking sequentially)\n   - Quadratic Probing (checking at squared intervals)\n   - Double Hashing (using a second hash function).",
        "difficulty": "Medium"
    },
    {
        "id": "algo_1",
        "category": "Algorithms",
        "sub_type": "CS Core",
        "question": "Explain QuickSort and its time/space complexity.",
        "answer": "QuickSort is a divide-and-conquer algorithm. It selects a 'pivot' element, partitions the array so elements smaller than pivot go left and larger go right, and then recursively sorts the sub-arrays.\n\nComplexities:\n- Best/Average Case Time: O(N log N) when partitions are balanced.\n- Worst Case Time: O(N^2) when array is already sorted and pivot selection is poor.\n- Space Complexity: O(log N) auxiliary space for recursive call stack.",
        "difficulty": "Medium"
    },
    {
        "id": "os_1",
        "category": "Operating Systems",
        "sub_type": "CS Core",
        "question": "What is a Deadlock and what are the conditions required for it to occur?",
        "answer": "A Deadlock is a situation where two or more processes are unable to proceed because each is waiting for the other to release a resource.\n\nFour Coffman conditions must hold simultaneously for a deadlock:\n1. Mutual Exclusion: At least one resource must be held in non-shareable mode.\n2. Hold and Wait: A process holding resources can request new resources without releasing current ones.\n3. No Preemption: Resources cannot be forcibly taken from a process.\n4. Circular Wait: A set of processes forms a circular chain where each process waits for a resource held by the next.",
        "difficulty": "Medium"
    },
    {
        "id": "dbms_1",
        "category": "DBMS",
        "sub_type": "CS Core",
        "question": "Explain ACID properties in a Database Management System.",
        "answer": "ACID properties guarantee reliable transaction processing:\n1. Atomicity: 'All or nothing' - either the entire transaction succeeds, or all changes are rolled back.\n2. Consistency: Prevents database corruption. The database must transition from one valid state to another, satisfying all schema constraints.\n3. Isolation: Multiple transactions running concurrently do not interfere with one another.\n4. Durability: Once a transaction commits, its changes survive system crashes or power losses.",
        "difficulty": "Easy"
    },
    {
        "id": "cn_1",
        "category": "Computer Networks",
        "sub_type": "CS Core",
        "question": "What is the difference between TCP and UDP protocols?",
        "answer": "1. Connection-oriented vs. Connectionless: TCP establishes a connection (3-way handshake) before sending data; UDP sends packets directly without validation.\n2. Reliability: TCP guarantees delivery via acknowledgments and retransmissions. UDP does not guarantee delivery.\n3. Ordering: TCP maintains packet sequence ordering; UDP packets can arrive in any order.\n4. Overhead: TCP has higher overhead (header size 20-60 bytes); UDP has lower overhead (header size 8 bytes), making it ideal for streaming or gaming.",
        "difficulty": "Easy"
    },
    {
        "id": "sd_1",
        "category": "System Design",
        "sub_type": "CS Core",
        "question": "What is Load Balancing and what algorithms are commonly used?",
        "answer": "Load Balancing distributes incoming network traffic across multiple servers to prevent overload, maximize throughput, and ensure high availability.\n\nCommon Algorithms:\n1. Round Robin: Cycles sequentially through servers.\n2. Least Connections: Routes requests to the server with the fewest active connections.\n3. IP Hash: Uses the client's IP to determine the server.\n4. Weighted Round Robin/Least Connections: Factors in server capacities.",
        "difficulty": "Medium"
    },
    {
        "id": "behavior_1",
        "category": "Behavioral Interview",
        "sub_type": "Behavioral",
        "question": "How do you handle conflict in a team setting?",
        "answer": "Answer using the STAR method (Situation, Task, Action, Result):\n1. Situation: Describe a time when a conflict arose during a team project.\n2. Task: Explain the challenge (e.g., competing design directions or unequal workload).\n3. Action: Detail how you scheduled a 1-on-1 meeting, actively listened, and built a compromise.\n4. Result: Share the positive outcome (e.g. project completed ahead of schedule, improved team communication).",
        "difficulty": "Easy"
    },
    {
        "id": "comp_google_1",
        "category": "Google",
        "sub_type": "Company",
        "question": "Describe how to find the shortest path in a weighted graph with negative edge weights.",
        "answer": "1. Dijkstra's algorithm cannot be used because it assumes non-negative weights and can fail in loops.\n2. Use the Bellman-Ford algorithm, which relaxes all edges V-1 times. It runs in O(V * E) time and can detect negative cycles.\n3. If no negative cycles exist, SPFA (Shortest Path Faster Algorithm) can also be used as an optimized version of Bellman-Ford.\n4. If all-pairs shortest paths are needed, use the Floyd-Warshall algorithm which runs in O(V^3).",
        "difficulty": "Hard"
    },
    {
        "id": "comp_amazon_1",
        "category": "Amazon",
        "sub_type": "Company",
        "question": "Explain the design of an online shopping cart checkout system.",
        "answer": "Key aspects of system design:\n1. API Gateway: Routes checkout requests, handles rate limiting.\n2. Order Service: Handles order creation and tracking (utilizes SQL for ACID transaction guarantees).\n3. Inventory Service: Locks stock temporary during checkout. Uses Redis for distributed locking to avoid double-ordering.\n4. Payment Gateway Integration: Integrates Stripe/Paypal via webhooks.\n5. Event Queue: Uses Kafka to trigger post-payment steps (e.g., email notification, dispatch log).",
        "difficulty": "Hard"
    },
    {
        "id": "comp_microsoft_1",
        "category": "Microsoft",
        "sub_type": "Company",
        "question": "Given a binary tree, how do you find the lowest common ancestor (LCA) of two nodes?",
        "answer": "Recursive Approach:\n1. Start at the root node.\n2. If root matches one of the target nodes, return root.\n3. Recurse left and right subtrees.\n4. If both left and right recursion calls return non-null, it means the current node is the LCA.\n5. If only one call returns non-null, propagate that non-null return up.",
        "difficulty": "Medium"
    },
    {
        "id": "comp_meta_1",
        "category": "Meta",
        "sub_type": "Company",
        "question": "How would you design a feed ranking system (like Facebook/Instagram feed)?",
        "answer": "Architecture Components:\n1. Feed Generation Service: Combines posts from friends/pages followed.\n2. Ranking Model: A Machine Learning ranking service scoring posts based on features (affinity, recency, post type, engagement probability).\n3. Cache Layer: Pre-computes and holds top 100 posts for immediate client load.\n4. Web server layer: Pulls dynamic feed entries from database using a read-optimized NoSQL database.",
        "difficulty": "Hard"
    }
]

# 2. Concept list for generating remaining questions
CONCEPTS = [
    # Python
    ("Python", "Programming", "decorators", "decorators are functions that modify the behavior of another function without changing its source code. They are commonly used for logging, access control, caching, and rate limiting."),
    ("Python", "Programming", "generators", "generators are iterators created using the yield keyword. They yield values lazily, conserving memory for massive datasets since the entire sequence is not loaded in RAM."),
    ("Python", "Programming", "list comprehensions", "list comprehensions offer a shorter syntax when you want to create a new list based on the values of an existing list. They are concise and generally faster than traditional for loops."),
    ("Python", "Programming", "asyncio", "asyncio is a library to write concurrent code using the async/await syntax. It runs on a single-threaded event loop, making it highly efficient for IO-bound applications."),
    ("Python", "Programming", "dunder methods", "dunder (double underscore) methods like __init__ or __str__ allow user-defined classes to hook into Python's core syntax, such as operators, iteration, or string formatting."),
    
    # Java
    ("Java", "Programming", "JVM garbage collector", "the JVM Garbage Collector automatically manages memory by reclaiming heap space occupied by unreachable objects. It runs asynchronously to minimize program execution pauses."),
    ("Java", "Programming", "reflection API", "the Java Reflection API allows programs to inspect, analyze, and modify classes, interfaces, constructors, methods, and fields at runtime, bypass visibility checks, and load dynamic modules."),
    ("Java", "Programming", "lambda expressions", "lambda expressions represent instances of functional interfaces (interfaces with a single abstract method), providing a concise way to pass blocks of behavior as function parameters."),
    ("Java", "Programming", "generics", "generics enable types (classes and interfaces) to be parameterized when defining classes, methods, and interfaces, providing compile-time type safety and eliminating explicit casting."),
    
    # SQL
    ("SQL", "Programming", "index seek vs index scan", "an index seek traverses the B-Tree directly to find matching rows (very fast), whereas an index scan searches the entire index leaf level sequentially, usually indicating a missing or poorly optimized index."),
    ("SQL", "Programming", "correlated subqueries", "a correlated subquery is a subquery that uses values from the outer query. It executes once for each candidate row evaluated by the outer query, which can cause latency issues if not indexed."),
    ("SQL", "Programming", "recursive CTEs", "recursive Common Table Expressions (CTEs) reference themselves in their query definition, making them ideal for querying hierarchical structures like org charts, directories, or graphs."),
    ("SQL", "Programming", "row-level locks", "row-level locking locks only the specific row being modified, maximizing database concurrency compared to table-level locks, though it incurs higher overhead to track locks."),
    
    # Data Structures
    ("Data Structures", "CS Core", "red-black trees", "a Red-Black Tree is a self-balancing binary search tree where each node has a color attribute (red or black). Balancing rules guarantee that tree traversal operates in O(log N) runtime."),
    ("Data Structures", "CS Core", "circular linked lists", "a Circular Linked List is a list where the last node points back to the first node. It is highly useful in round-robin scheduling algorithms or buffer loops."),
    ("Data Structures", "CS Core", "adjacency lists", "an Adjacency List represents a graph as an array of linked lists or dynamic arrays, mapping each vertex to its immediate neighbors. It is highly space-efficient for sparse graphs."),
    ("Data Structures", "CS Core", "trie search trees", "a Trie (prefix tree) is an ordered tree data structure used to store associative arrays where keys are strings. It allows fast prefix matching and auto-complete searches in O(L) time where L is string length."),
    
    # Algorithms
    ("Algorithms", "CS Core", "binary search", "binary search is a search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half, running in O(log N) time."),
    ("Algorithms", "CS Core", "dijkstra pathfinding", "Dijkstra's algorithm finds the shortest path from a source node to all other nodes in a weighted graph with non-negative edge weights, running in O(V^2) or O(E log V) with a priority queue."),
    ("Algorithms", "CS Core", "dynamic programming knapsack", "the Knapsack problem uses dynamic programming to select items with given weights and values to maximize total value without exceeding a capacity limit, running in O(N * W) pseudo-polynomial time."),
    ("Algorithms", "CS Core", "breadth-first search", "Breadth-First Search (BFS) is a graph traversal algorithm that visits all neighbor nodes at the current depth before moving to nodes at the next depth level, using a queue queue container."),
    
    # OS
    ("Operating Systems", "CS Core", "virtual memory paging", "virtual memory paging maps a process's virtual address space to physical memory frames in fixed-size blocks (pages), allowing program execution to exceed physical RAM size using swap spaces."),
    ("Operating Systems", "CS Core", "mutex lock synchronization", "a Mutex (mutual exclusion) lock is a synchronization primitive used to serialize access to shared critical resources among multiple competing threads, avoiding race conditions."),
    ("Operating Systems", "CS Core", "CPU scheduling slices", "CPU scheduling slices (or time quantum) represent the fixed execution time allocated to a process in preemptive round-robin scheduling, balancing context-switch overhead and response time."),
    
    # DBMS
    ("DBMS", "CS Core", "relational database normalization", "normalization splits relational tables into smaller tables and defines relationships to eliminate data redundancy and prevent insert/update/delete anomalies."),
    ("DBMS", "CS Core", "Write-Ahead Logging (WAL)", "Write-Ahead Logging ensures database durability by writing transaction changes to a persistent append-only log file before updating the actual database data pages in memory."),
    ("DBMS", "CS Core", "database sharding", "database sharding is a horizontal partitioning technique that splits a database across separate physical servers, allowing scalability beyond the limits of a single machine."),
    
    # Networks
    ("Computer Networks", "CS Core", "TCP window size scaling", "TCP window size scaling controls flow velocity by adjusting the maximum amount of unacknowledged data a sender can transmit before receiving an ACK, avoiding buffer overflows."),
    ("Computer Networks", "CS Core", "DNS recursive queries", "a DNS recursive query contacts name servers hierarchically (Root, TLD, Authoritative) to resolve a domain name to an IP address, caching results along the way."),
    ("Computer Networks", "CS Core", "SSL/TLS handshake phases", "the SSL/TLS handshake establishes a secure session key by negotiating cipher suites, verifying certificates, and exchanging cryptographic parameters between client and server."),
    
    # System Design
    ("System Design", "CS Core", "consistent hashing ring", "consistent hashing maps keys and nodes to a circular hashing ring. It minimizes database re-sharding remapping when cache servers are added or removed under load."),
    ("System Design", "CS Core", "API Gateway rate limiting", "an API Gateway rate limiter blocks excess client queries using token bucket or sliding window logs to protect downstream services from DDoS attacks or overload."),
    ("System Design", "CS Core", "Apache Kafka partitions", "Kafka partitions allow high-throughput message processing by dividing topics across servers, enabling horizontal scaling and parallel consumer consumption."),
    
    # Behavioral
    ("Behavioral Interview", "Behavioral", "handling team conflicts", "resolving team conflicts requires holding 1-on-1 objective discussions, establishing mutually agreed metrics, focusing on technical trade-offs, and keeping the focus on customer delivery."),
    ("Behavioral Interview", "Behavioral", "unclear project scope", "handling unclear project scope requires setting up design reviews, building rapid functional prototypes, and meeting stakeholders regularly to validate assumptions early."),
    
    # Company
    ("Google", "Company", "Search indexing ranking", "Google's search indexing ranking utilizes massive MapReduce frameworks to parse document graphs, sorting results based on PageRank and machine learning relevance models."),
    ("Amazon", "Company", "DynamoDB backend store", "Amazon's core ordering services utilize DynamoDB to achieve single-digit millisecond latency at scale, leveraging consistent hashing and decentralized write logs."),
    ("Microsoft", "Company", "Azure cloud load balancing", "Azure uses software-defined load balancers routing incoming traffic across global data centers using dynamic health checks and virtual network gateways."),
    ("Meta", "Company", "TAO distributed graph store", "Meta utilizes TAO, a distributed graph cache, to store social connections, serving billions of read requests per second with eventual consistency models.")
]

# 3. Systematic generation to reach exactly 500 questions
idx = 1
while len(INTERVIEW_QUESTIONS) < 500:
    for cat, sub, concept, desc in CONCEPTS:
        if len(INTERVIEW_QUESTIONS) >= 500:
            break
            
        q_id = f"gen_{cat.lower().replace(' ', '_')}_{idx}"
        
        # We cycle through three question styles based on the index to create variation
        style_mod = idx % 3
        if style_mod == 0:
            question = f"Explain the concept of {concept} in {cat} and list its main use cases."
            answer = f"In technical engineering, {concept} refers to a core element. {desc.capitalize()} Common use cases include: 1. Optimizing resource usage.\n2. Implementing clean architecture.\n3. Managing complex state transitions dynamically."
            difficulty = "Easy"
        elif style_mod == 1:
            question = f"What are the trade-offs of utilizing {concept} in a {cat} environment?"
            answer = f"When using {concept} in {cat}, developers must balance efficiency and simplicity. {desc.capitalize()} Trade-offs include increased startup complexity versus long-term maintainability. Ensure code reviews cover this design choice."
            difficulty = "Medium"
        else:
            question = f"How would you troubleshoot performance issues related to {concept} in {cat}?"
            answer = f"Troubleshooting performance issues with {concept} in {cat} requires checking resource allocations, analyzing CPU profiling trace logs, and writing mock unit tests to isolate bottlenecks. {desc.capitalize()}"
            difficulty = "Hard"
            
        INTERVIEW_QUESTIONS.append({
            "id": q_id,
            "category": cat,
            "sub_type": sub,
            "question": question,
            "answer": answer,
            "difficulty": difficulty
        })
        idx += 1

def get_augmented_interview_questions(user_id):
    """
    Retrieves static questions augmented with SQLite progress (completed status, bookmarks, notes).
    """
    progress = get_interview_progress(user_id)
    bookmarked_ids = get_bookmarks(user_id, "interview")
    
    augmented = []
    for q in INTERVIEW_QUESTIONS:
        q_id = q["id"]
        prog = progress.get(q_id, {"completed": False, "notes": "", "last_reviewed": ""})
        is_bookmarked = q_id in bookmarked_ids
        
        q_copy = dict(q)
        q_copy.update({
            "completed": prog["completed"],
            "notes": prog["notes"],
            "bookmarked": is_bookmarked
        })
        augmented.append(q_copy)
        
    return augmented
