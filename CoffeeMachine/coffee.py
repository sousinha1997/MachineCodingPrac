
class Coffee:

    def __init__(self, name: str, price: int, recipe: dict):
        self.name = name
        self.price = price
        self.recipe = recipe

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> int:
        return self.price

    def get_recipe(self) -> dict:
        return self.recipe
