import threading

class Ingredient:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity
        self.lock = threading.Lock()

    def get_name(self) -> str:
        return self.name

    def get_quantity(self) -> int:
        with self.lock:
            return self.quantity

    def update_quantity(self, amount: str):
        with self.lock:
            self.quantity +=amount

