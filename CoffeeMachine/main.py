import threading

from CoffeeMachine.coffee_machine import CoffeeMachine
from CoffeeMachine.payment import Payment

class CoffeeOrderThread(threading.Thread):
    def __init__(self, coffee_machine, order, amount):
        threading.Thread.__init__(self)
        self.coffee_machine = coffee_machine
        self.order = order
        self.amount = amount

    def run(self):
        try:
            print("\n***********************************************\n")

            coffee_obj = self.coffee_machine.select_coffee(self.order)

            if coffee_obj:
                payment = Payment(self.amount)
                self.coffee_machine.dispense_coffee(coffee_obj, payment)

        except Exception as e:
            print(f"Error processing {self.order}: {e}")

if __name__ == "__main__":

    # Display initial menu
    coffee_machine = CoffeeMachine()
    coffee_machine.display_menu()
    count = 0

    # Order details
    orders = ["espresso", "latte", "latte", "espresso", "cappuccino"]
    amounts = [40, 550, 400, 100, 300]

    # List to store thread objects
    threads = []

    # Create and start threads for each order
    for order, amount in zip(orders, amounts):
        thread = CoffeeOrderThread(coffee_machine, order, amount)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


    print("All orders processed!")