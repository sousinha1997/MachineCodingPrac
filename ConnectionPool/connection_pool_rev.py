import random
import threading
import queue
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")


class Connection:
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.lock = threading.Lock()  # Ensures thread safety for in_use flag
        self.in_use = False

    def execute_query(self, query):
        try:
            logging.info(f"Executing query on connection {self.conn_id}: {query}")
            time.sleep(random.uniform(0.1, 0.5))  # Simulating query execution time
            return f"Got result from connection {self.conn_id}"
        except Exception as e:
            logging.error(f"Query execution failed on connection {self.conn_id}: {e}")
            return None

    def close(self):
        logging.info(f"Closing connection {self.conn_id}")


class ConnectionPool:
    def __init__(self, max_size=5, timeout=5):
        if max_size <= 0:
            raise ValueError("max_size must be a positive integer.")

        self.max_size = max_size
        self.timeout = timeout
        self.connections = queue.Queue(max_size)
        self._initialize_connections()

    def _initialize_connections(self):
        """Prepares the connection pool with connections"""
        for i in range(self.max_size):
            conn = Connection(i)
            self.connections.put(conn)

    def acquire_connection(self):
        """Acquires an available connection from the pool within the timeout"""
        try:
            conn = self.connections.get(timeout=self.timeout)
            with conn.lock:  # Ensuring thread safety when modifying in_use
                conn.in_use = True
            return conn
        except queue.Empty:
            raise Exception("No available connections. Try again later")

    def release_connection(self, conn):
        """Releases a connection back to the pool"""
        with conn.lock:
            conn.in_use = False
        self.connections.put(conn)

    def close_all_connections(self):
        """Closes all connections in the pool"""
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()


def worker(pool, worker_id):
    try:
        conn = pool.acquire_connection()
        logging.info(f"Worker {worker_id} acquired connection {conn.conn_id}")

        result = conn.execute_query(f"SELECT * FROM USERS WHERE ID = {worker_id}")
        if result:
            logging.info(f"Worker {worker_id} got result: {result}")

        pool.release_connection(conn)
        logging.info(f"Worker {worker_id} released connection {conn.conn_id}")

    except Exception as exc:
        logging.error(f"Worker {worker_id} failed: {exc}")


if __name__ == "__main__":
    pool = ConnectionPool(max_size=3)
    threads = []

    for i in range(5):
        t = threading.Thread(target=worker, args=(pool, i), name=f"Worker-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pool.close_all_connections()
