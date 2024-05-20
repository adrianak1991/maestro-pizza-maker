# The maestro pizza maker is aware of the fact that the fat content of the ingredients is random and it is not always the same.
# Since fat is the most important factor in taste, the maestro pizza maker wants to know how risky his pizza menu is.

# TODO: define 2 risk measures for the pizza menu and implement them (1 - Taste at Risk (TaR), 2 - Conditional Taste at Risk (CTaR), also known as Expected Shorttaste (ES)

from maestro_pizza_maker.pizza import Pizza
from maestro_pizza_maker.pizza_menu import PizzaMenu

import numpy as np

def taste_at_risk_pizza(pizza: Pizza, quantile: float) -> float:
    # TODO: implement the taste at risk measure for a pizza
    # quantile is the quantile that we want to consider
    # Hint: Similarity between the Taste at Risk and the Value at Risk is not a coincidence or is it?
    # Hint: Use function taste from Pizza class, but be aware that the higher the taste, the better -> the lower the taste, the worse
    return np.percentile(pizza.taste,quantile*100)


def taste_at_risk_menu(menu: PizzaMenu, quantile: float) -> float:
    # TODO: implement the taste at risk measure for a menu
    # quantile is the quantile that we want to consider
    # Hint: the taste of the whole menu is the sum of the taste of all pizzas in the menu, or? ;)
    return np.percentile(sum(pizza.taste for pizza in menu.pizzas),quantile*100)


def conditional_taste_at_risk_pizza(pizza: Pizza, quantile: float) -> float:
    # TODO: implement the conditional taste at risk measure for a pizza
    # quantile is the quantile that we want to consider
    # Hint: Simmilarity between the Conditional Taste at Risk and the Conditional Value at Risk is not a coincidence or is it?
    return np.mean(pizza.taste[pizza.taste <=taste_at_risk_pizza(pizza, quantile)])
    # return np.mean(pizza.taste[pizza.taste <=np.percentile(pizza.taste,quantile*100)])


def conditional_taste_at_risk_menu(menu: PizzaMenu, quantile: float) -> float:
    # TODO: implement the conditional taste at risk measure for a menu
    # Hint: the taste of the whole menu is the sum of the taste of all pizzas in the menu, or? ;) (same as for the taste at risk)
    menu_taste = sum(pizza.taste for pizza in menu.pizzas)
    return np.mean(menu_taste[menu_taste<=taste_at_risk_menu(menu,quantile)])
    # return np.mean(menu_taste[menu_taste<=np.percentile(menu_taste,quantile*100)])
