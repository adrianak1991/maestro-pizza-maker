# class representing the pizza menu

from dataclasses import dataclass
from typing import List

import pandas as pd
import warnings

from maestro_pizza_maker.pizza import Pizza


@dataclass
class PizzaMenu:
    pizzas: List[Pizza]

    def to_dataframe(self, sort_by: str, descendent: bool) -> pd.DataFrame:
        # TODO: transform the list of pizzas into a pandas dataframe, where each row represents a pizza
        # and it contains the following columns: name, price, protein, average_fat, carbohydrates, calories and ingredients
        # where ingredients is a list of ingredients.
        # The dataframe should be sorted by the column specified by the sort_by parameter
        # and the order of sorting should be specified by the descendent parameter
        # (descendent=True means that the dataframe should be sorted in a descendent order)
        #
        # Example:
        #
        # pizza_menu = PizzaMenu(pizzas=[Pizza(sauce=PizzaIngredients.CREAM_SAUCE, dough=PizzaIngredients.CLASSIC_DOUGH)])
        # pizza_menu.to_dataframe(sort_by="price", descendent=True)
        #
        # should return a dataframe with a single row and the following columns:
        # name, price, protein, average_fat, carbohydrates, calories, ingredients
        # where the name column contains the name of the pizza, price contains the price of the pizza,
        # protein contains the protein content of the pizza, average_fat contains the average_fat content of the pizza,
        # carbohydrates contains the carbohydrates content of the pizza, calories contains the calories content of the pizza
        # and ingredients contains a list of ingredients that the pizza contains
        #
        # The dataframe should be sorted by the price column in a descendent order
        ### Sorting by ingredients is not defined
        pizzas_df = []
        for pizza in self.pizzas:
            pizzas_df.append(
                {
                    "name": pizza.name,
                    "price": pizza.price,
                    "protein": pizza.protein,
                    "average_fat": pizza.average_fat,
                    "carbohydrates": pizza.carbohydrates,
                    "calories": pizza.calories,
                    "ingredients": pizza.ingredients,
                }
            ) 
        if sort_by!="ingredients":
            return pd.DataFrame(pizzas_df).sort_values(by = sort_by, ascending=not descendent)
        else:
            warnings.warn("Sorting by ingredients is not defined")
            return pd.DataFrame(pizzas_df)
       
    @property
    def cheapest_pizza(self) -> Pizza:
        # TODO: return the cheapest pizza from the menu
       return min(self.pizzas, key=lambda pizza: pizza.price)

    @property
    def most_expensive_pizza(self) -> Pizza:
        # TODO: return the most expensive pizza from the menu
       return max(self.pizzas, key=lambda pizza: pizza.price)
        
    @property
    def most_caloric_pizza(self) -> Pizza:
        # TODO: return the most caloric pizza from the menu
        return max(self.pizzas, key=lambda pizza: pizza.calories)

    @property
    def fewest_calories_pizza(self) -> Pizza:
        # TODO: return the fewest calories pizza from the menu
        return min(self.pizzas, key=lambda pizza: pizza.calories)
        
    @property
    def most_protein_pizza(self) -> Pizza:
        # TODO: return the most proteinaceous pizza from the menu
        return max(self.pizzas, key=lambda pizza: pizza.protein)
        
    def get_most_fat_pizza(self, quantile: float = 0.5) -> Pizza:
        # TODO: return the most fat pizza from the menu
        # consider the fact that fat is random and it is not always the same, so you should return the pizza that has the most fat in the quantile of cases specified by the quantile parameter
        return max(self.pizzas, key=lambda pizza: np.percentile(pizza.fat,quantile*100))

    def add_pizza(self, pizza: Pizza) -> None:
        # TODO: code a function that adds a pizza to the menu
        self.pizzas.append(pizza)
        pass

    def remove_pizza(self, pizza: Pizza) -> None:
        # TODO: code a function that removes a pizza from the menu
        # do not forget to check if the pizza is actually in the menu
        # if it is not in the menu, raise a ValueError
        if (pizza in self.pizzas):
            self.pizzas.remove(pizza)
        else:
            raise ValueError("The pizza, you want to remove, is not an element of the menu.")
        pass

    def __len__(self) -> int:
        # TODO: return the number of pizzas in the menu
        return len(self.pizzas)
