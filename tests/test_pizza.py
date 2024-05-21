import unittest
from maestro_pizza_maker.pizza import Pizza


class TestPizzaMethods(unittest.TestCase):

    def test_average_fat(self):
        pizza = Pizza(dough = PizzaIngredients.CLASSIC_DOUGH, 
                  sauce=PizzaIngredients.TOMATO_SAUCE, 
                  cheese = [PizzaIngredients.MOZZARELA], 
                   meat = [PizzaIngredients.HAM],
                  fruits=[PizzaIngredients.APPLE],
                  vegetables = [PizzaIngredients.ONIONS])
        pizza_average_fat = np.sum([pizza.dough.value.fat, pizza.sauce.value.fat,pizza.cheese[0].value.fat,pizza.meat[0].value.fat,pizza.fruits[0].value.fat,pizza.vegetables[0].value.fat], axis=0).mean()
        self.assertEqual(round(pizza.average_fat,5), round(pizza_average_fat,5))

    def test_taste(self):
        pizza = Pizza(dough = PizzaIngredients.CLASSIC_DOUGH, 
                  sauce=PizzaIngredients.TOMATO_SAUCE, 
                  cheese = [PizzaIngredients.MOZZARELA], 
                   meat = [PizzaIngredients.HAM],
                  fruits=[PizzaIngredients.APPLE],
                  vegetables = [PizzaIngredients.ONIONS])
        # taste = 0.05 * fat_dough + 0.2 * fat_sauce + 0.3 * fat_cheese + 0.1 * fat_fruits + 0.3 * fat_meat + 0.05 * fat_vegetables
        pizza_taste = 0.05*pizza.dough.value.fat + 0.2*pizza.sauce.value.fat + 0.3*pizza.cheese[0].value.fat+0.1*pizza.fruits[0].value.fat+0.3*pizza.meat[0].value.fat+0.05*pizza.vegeatables[0].value.fat
        self.assertEqual(pizza.taste,pizza_taste)

if __name__ == '__main__':
    unittest.main()
