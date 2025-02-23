import random
import threading
import queue
import time


class Connection:

    def __init__(self,conn_id):
        self.conn_id = conn_id
        self.in_use = False

    def execute_query(self, query):
        print(f"Executing query on connection {self.conn_id} : {query}"),
        time.sleep(random.uniform(0.1,0.5))
        return f"Got result from connection {self.conn_id}"

    def close(self, conn_id):
        print(f"Closing connection {self.conn_id}")


class ConnectionPool:

    def __init__(self, max_size= 5, timeout= 5):
        self.max_size = max_size
        self.timeout = timeout
        self.lock = threading.Lock()
        self.connections = queue.Queue(max_size)
        self._initialize_connection()


    def _initialize_connection(self):
        for i in range(self.max_size):
            conn = Connection(i)
            self.connections.put(conn)

    def acquire_connection(self):
        try:
            conn = self.connections.get(timeout=self.timeout)
            conn.in_use = True
            return conn
        except queue.Empty:
            raise Exception("No available connections. Try again later")

    def release_connection(self,conn):
        with self.lock:
            conn.in_use = False
            self.connections.put(conn)

    def shutdown_pool(self):
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close(conn.conn_id)

def worker(pool, id):
    try:
        conn = pool.acquire_connection()
        print(f"Worker {id} acquire connection")
        result = conn.execute_query(f'SELECT * FROM USERS WHERE ID = {id}')
        print(f"Worker {id} execute query")
        pool.release_connection(conn)
        print(f"Worker {id} release connection {conn.conn_id}")
    except Exception as exc:
        print(f"Worker {id} failed, {exc}")



if __name__ == "__main__":
    pool = ConnectionPool(max_size=3)
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(pool,i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pool.shutdown_pool()





