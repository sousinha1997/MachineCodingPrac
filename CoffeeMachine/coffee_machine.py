import threading

from CoffeeMachine.ingredient import Ingredient
from CoffeeMachine.coffee import Coffee
from CoffeeMachine.payment import Payment


class CoffeeMachine:
    _instance = None

    def __init__(self):
        self.ingredients = {
                            "milk" : Ingredient(name= "milk",quantity= 6),
                            "water" : Ingredient(name= "water", quantity= 7),
                            "coffee" : Ingredient(name= "coffee", quantity= 4)
                           }

        espresso = Coffee(  "espresso",
                            100,
                            {
                                    self.ingredients["water"] : 2,
                                    self.ingredients["coffee"]: 1,
                                    self.ingredients["milk"]: 0,
                                   }
                          )

        cappuccino = Coffee("cappuccino",
                            120,
                            {
                                    self.ingredients["water"]: 1,
                                    self.ingredients["milk"]: 1,
                                    self.ingredients["coffee"]: 1
                                   }
                            )

        latte = Coffee(   "latte",
                          140,
                          {
                                 self.ingredients["water"]: 1,
                                 self.ingredients["milk"]: 2,
                                 self.ingredients["coffee"]: 1
                                }
                          )

        self.coffeeMenu = [espresso, cappuccino, latte]
        self.lock = threading.Lock()

    @staticmethod
    def get_instance(self):
        if CoffeeMachine._instance is None:
            return CoffeeMachine()
        return CoffeeMachine._instance

    def display_menu(self):
        print("Menu:")
        for item in self.coffeeMenu:
            print(item.name+ ": "+ str(item.price))

    def make_payment(self, price: int) -> object:
        return Payment(price)

    def check_availability(self, item):
        for key, value in item.get_recipe().items():
            if  key.get_quantity() < value:
                print("Can't brew " + item.name +". Running low on " + str(key.name))
                return False
        return True


    def select_coffee(self, coffee):
        with self.lock:
            for item in self.coffeeMenu:
                if item.name == coffee and self.check_availability(item) == True:
                    return item
            return None


    def dispense_coffee(self, coffee, payment):
        print("Order name: " + coffee.name)
        price = coffee.get_price()
        if payment.price < price:
            print("Payment incomplete, Cannot process.")
            return None


        coffee_recipe = coffee.get_recipe()
        self.update_ingredient(coffee_recipe)
        print("Dispensing...")
        print(coffee.name + " is served. Thank you !")


    def update_ingredient(self, coffee_recipe):

        for item, amount in coffee_recipe.items():
            obj = self.ingredients[item.name]
            obj.update_quantity(amount*-1)
            if obj.get_quantity() < 3:
                print("Inventory running low for: " + item.name)






