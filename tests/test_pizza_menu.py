import unittest

from maestro_pizza_maker.pizza import Pizza
from maestro_pizza_maker.pizza_menu import PizzaMenu

class TestPizzaMenuMethods(unittest.TestCase):

    def setUp(self):
        pizza1 = Pizza(sauce=PizzaIngredients.CREAM_SAUCE, dough=PizzaIngredients.CLASSIC_DOUGH)
        pizza2 = Pizza(dough = PizzaIngredients.THIN_DOUGH, sauce=PizzaIngredients.CREAM_SAUCE, cheese = [PizzaIngredients.MOZZARELA])
        pizza3 = Pizza(dough = PizzaIngredients.THIN_DOUGH, sauce=PizzaIngredients.TOMATO_SAUCE, cheese = [PizzaIngredients.CHEDDAR], meat = [PizzaIngredients.HAM],  vegetables = [PizzaIngredients.MUSHROOMS])
        pizza4 = Pizza(dough = PizzaIngredients.CLASSIC_DOUGH, sauce=PizzaIngredients.TOMATO_SAUCE, cheese = [PizzaIngredients.MOZZARELA],  vegetables = [PizzaIngredients.ONIONS, PizzaIngredients.PEPPER])
        pizza5 = Pizza(dough = PizzaIngredients.WHOLEMEAL_DOUGH, sauce=PizzaIngredients.CREAM_SAUCE, cheese = [PizzaIngredients.PARMESAN], fruits=[PizzaIngredients.APPLE], vegetables = [PizzaIngredients.ONIONS])
        
        pizza_menu = PizzaMenu(pizzas=[pizza1,pizza2,pizza3,pizza4])
        pass
        
    def test_len(self):
        self.asserEqual(len(pizza_menu),4)

    def test_add_pizza(self):
        pizza_menu.add_pizza(pizza5)
        self.assertEqual(len(pizza_menu),5)

    def test_remove_pizza(self):
        pizza_menu.remove_pizza(pizza1)
        self.assertEqual(len(pizza_menu),4)
        pizza_menu.add_pizza(pizza1)

    def test_cheapest_pizza(self):
        self.assertEqual(pizza_menu.cheapest_pizza,pizza1)

if __name__ == '__main__':
    unittest.main()


