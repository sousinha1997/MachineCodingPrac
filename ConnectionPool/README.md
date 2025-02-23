# Connection Pool 

Connection Pool is a mechanism to handle database connections efficiently, instead of opening and closing a new connection everytime, it maintains a pool of reusable connections to improve performance and resource managemnet.


## Concepts Used

1. Thread Safety: Multiple threads should be able to acquire and release connections safely.
2. Object Pooling: Maintain a fixed number of connections that should be reused. 
3. Synchronization(Locking): Prevent race conditions when multiple threads try to access the pool. 
4. Lazy initialization: Only create connection when they are requested.
5. Timeout Handling: Ensure connections are returned to the pool after fixed number of time.
6. Connection Validation: Check if connection is alive before returning it.