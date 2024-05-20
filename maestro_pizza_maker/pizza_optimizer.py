# The maestro pizza maker is aware that pizza creation is a complex process and it is not always possible to create a pizza that satisfies all the constraints.
# Therefore maestro wants to create a pizza that will satisfy as many constraints as possible to avoid the risk creating disappointing pizzas like pizza Hawaii.
# To do so, maestro wants to use the optimization techniques.

# TODO: implement the pizza optimizer that will create a pizza that will satisfy all the constraints and will maximize following objective functions:
# obj = Expected_value(taste(pizza)) - lambda * price(pizza), where lambda is a parameter that will be provided by the maestro pizza maker
# hint: use the mip library and the following documentation: https://www.python-mip.com/
# hint: you can find inspiration in the minimize_price function


from dataclasses import dataclass, field

import numpy as np

from mip import Model, xsum, minimize, maximize, INTEGER, BINARY, OptimizationStatus

from maestro_pizza_maker.ingredients import IngredientType, PizzaIngredients
from maestro_pizza_maker.pizza import Pizza


@dataclass
class ValueBounds:
    min: float = 0.0
    max: float = np.inf


@dataclass
class PizzaConstraintsValues:
    price: ValueBounds = field(default_factory=lambda: ValueBounds())
    protein: ValueBounds = field(default_factory=lambda: ValueBounds())
    fat: ValueBounds = field(default_factory=lambda: ValueBounds())
    carbohydrates: ValueBounds = field(default_factory=lambda: ValueBounds())
    calories: ValueBounds = field(default_factory=lambda: ValueBounds())


@dataclass
class PizzaConstraintsIngredients:
    cheese: int = 0
    fruits: int = 0
    meat: int = 0
    vegetables: int = 0
    dough: int = 1
    sauce: int = 1


def minimize_price(
    constraints_values: PizzaConstraintsValues,
    constraints_ingredients: PizzaConstraintsIngredients) -> Pizza:
    """"""
    model = Model(solver_name='CBC')

    # sets
    ingredients = [ingredient for ingredient in PizzaIngredients]
    ingredients_names = [ingredient.name for ingredient in ingredients]

    # variables
    x = [
        model.add_var(var_type=INTEGER, lb=0, ub=1, name=ingredient)
        for ingredient in ingredients_names
    ]

    # objective function
    model.objective = minimize(
        xsum(x[i] * ingredients[i].value.price for i in range(len(ingredients)))
    )

    # constraints
    model += (
        xsum(x[i] * ingredients[i].value.protein for i in range(len(ingredients)))
        >= constraints_values.protein.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.protein for i in range(len(ingredients)))
        <= constraints_values.protein.max
    )
    model += (
        xsum(x[i] * ingredients[i].value.fat.mean() for i in range(len(ingredients)))
        >= constraints_values.fat.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.fat.mean() for i in range(len(ingredients)))
        <= constraints_values.fat.max
    )
    model += (
        xsum(x[i] * ingredients[i].value.carbohydrates for i in range(len(ingredients)))
        >= constraints_values.carbohydrates.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.carbohydrates for i in range(len(ingredients)))
        <= constraints_values.carbohydrates.max
    )
    model += (
        xsum(x[i] * ingredients[i].value.calories for i in range(len(ingredients)))
        >= constraints_values.calories.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.calories for i in range(len(ingredients)))
        <= constraints_values.calories.max
    )

    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.DOUGH
        )
        == constraints_ingredients.dough
    )
    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.SAUCE
        )
        == constraints_ingredients.sauce
    )
    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.CHEESE
        )
        == constraints_ingredients.cheese
    )
    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.MEAT
        )
        == constraints_ingredients.meat
    )
    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.VEGETABLE
        )
        == constraints_ingredients.vegetables
    )
    model += (
        xsum(
            x[i]
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.FRUIT
        )
        == constraints_ingredients.fruits
    )

    # optimize
    model.optimize()

    # check solution
    if model.status != OptimizationStatus.OPTIMAL:
        raise Exception(
            "The model is not optimal -> likely no solution found (infeasible))"
        )

    # solution
    return Pizza(
        dough=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.DOUGH and x[i].x == 1
        ][0],
        sauce=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.SAUCE and x[i].x == 1
        ],
        cheese=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.CHEESE and x[i].x == 1
        ],
        meat=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.MEAT and x[i].x == 1
        ],
        vegetables=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.VEGETABLE and x[i].x == 1
        ],
        fruits=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.FRUIT and x[i].x == 1
        ],
    )


def maximize_taste_penalty_price(
    constraints_values: PizzaConstraintsValues,
    constraints_ingredients: PizzaConstraintsIngredients,
    lambda_param: float = 0.5) -> Pizza:
    # TODO: implement this function (description at the top of the file)
    # recomendation: use latex notation to describe the suggested model

    ###### DESCRIPTION OF THE MODEL #####
    # Parameters\\
    # $n$ - number of all ingredients\\
    # $N = \{1,2,\ldots,n\}$ - indexes of all ingredients
    # $N_d, N_s, N_c, N_f, N_m, N_v$ - sets representing indexes to the ingredients of the respective types: dough, sauce, cheese, fruit, meat, vegetables\\
    # It holds: $N = \bigcup\limits_{type\in\{d,s,c,f,m,v\}} N_{type}$\\
    
    # $w = (w_1,w_2,\ldots,w_n)\in\mathds{R}^n$ - vector of weights assigned to the ingredients depending on the type appearing in the formula of taste\\
    # $f = (f_1,f_2,\ldots,f_n)$ - vector of random variables representing fat of the ingredients\\
    
    # $p = (p_1,p_2,\ldots,p_n) \in\{\mathds{R_+}\cup\{0\}\}^n$ - vector of prices of the ingredients\\

    # $pro = (pro_1,pro_2,\ldots,pro_n)\in\{\mathds{R_+}\cup\{0\}\}^n$ - vector of protein values in the ingredients \\
    # $pro^{min},pro^{max}$ - limits on the protein value in pizza \\
    
    # $car = (car_1,car_2,\ldots,car_n)\in\{\mathds{R_+}\cup\{0\}\}^n$ - vector of carbohydrates values in the ingredients \\
    # $car^{min},car^{max}$ - limits on the carbohydrates value in pizza \\
    
    # $cal = (cal_1,cal_2,\ldots,cal_n)\in\{\mathds{R_+}\cup\{0\}\}^n$ - vector of calories of the ingredients \\
    # $cal^{min},cal^{max}$ - limits on the calories value in pizza \\
    
    # $y = (y_d,y_s,y_c,y_f,y_m,y_v)\in\mathds{N}^6$ - required number of the respective types of ingredients \\
    
    # Decision variables \\
    # $x = (x_1,x_2,\ldots,x_n) \in \{0,1\}^n$ - binary decision variables, denoting information if the given ingredient is in the pizza\\
    
    # Objective function \\
    # $\mathds{E}\left(\sum_{i=1}^n\left(x_i*w_i*f_i\right)\right) - \lambda \left(\sum_{i=1}^n x_i*p_i\right)$\\
    
    # Constraints \\
    #\begin{align*}
    # &pro^{min}\leq \sum\limits_{i=1}^n x_i*pro_i \leq pro^{max}\\
    # &car^{min}\leq \sum\limits_{i=1}^n x_i*car_i \leq car^{max}\\
    # &cal^{min}\leq \sum\limits_{i=1}^n x_i*cal_i \leq cal^{max}\\
    # &\sum\limits_{i\in N_d} x_i = y_d\\
    # &\sum\limits_{i\in N_s} x_i = y_s\\
    # &\sum\limits_{i\in N_c} x_i = y_c\\
    # &\sum\limits_{i\in N_f} x_i = y_f\\
    # &\sum\limits_{i\in N_m} x_i = y_m\\
    # &\sum\limits_{i\in N_v} x_i = y_v
    #\end{align*}

    # Final problem \\
    # \begin{equation*}
    # \begin{array}{ll}
    # \max\limits_{x\in\{0,1\}^n} & \mathds{E}\left(\sum_{i=1}^n\left(x_i*w_i*f_i\right)\right) - \lambda \left(\sum_{i=1}^n x_i*p_i\right)\\
    # s.t. & pro^{min}\leq \sum\limits_{i=1}^n x_i*pro_i \leq pro^{max}\\
    #  & car^{min}\leq \sum\limits_{i=1}^n x_i*car_i \leq car^{max}\\
    #  & cal^{min}\leq \sum\limits_{i=1}^n x_i*cal_i \leq cal^{max}\\
    #  & \sum\limits_{i\in N_d} x_i = y_d\\
    #  & \sum\limits_{i\in N_s} x_i = y_s\\
    #  & \sum\limits_{i\in N_c} x_i = y_c\\
    #  & \sum\limits_{i\in N_f} x_i = y_f\\
    #  & \sum\limits_{i\in N_m} x_i = y_m\\
    #  & \sum\limits_{i\in N_v} x_i = y_v
    # \end{array}
    # \end{equation*}
    ######
    
    model = Model(solver_name='CBC')
    
    # sets
    ingredients = [ingredient for ingredient in PizzaIngredients]
    ingredients_names = [ingredient.name for ingredient in ingredients]
    n = len(ingredients)
    
    # variables
    x = [
        model.add_var(var_type=BINARY, name=ingredient)
        for ingredient in ingredients_names
    ]

    # objective function
    model.objective = maximize(xsum(x[i]*np.mean(ingredients[i].value.fat)*Pizza.weights[ingredients[i].value.type.name] for i in range(n))
       - lambda_param*xsum(x[i] * ingredients[i].value.price for i in range(n))
    )

    # constraints
    model += (
        xsum(x[i] * ingredients[i].value.protein for i in range(n))
        >= constraints_values.protein.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.protein for i in range(n))
        <= constraints_values.protein.max
    )
    model += (
        xsum(x[i] * ingredients[i].value.carbohydrates for i in range(n))
        >= constraints_values.carbohydrates.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.carbohydrates for i in range(n))
        <= constraints_values.carbohydrates.max
    )
    model += (
        xsum(x[i] * ingredients[i].value.calories for i in range(n))
        >= constraints_values.calories.min
    )
    model += (
        xsum(x[i] * ingredients[i].value.calories for i in range(n))
        <= constraints_values.calories.max
    )

    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.DOUGH
        )
        == constraints_ingredients.dough
    )
    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.SAUCE
        )
        == constraints_ingredients.sauce
    )
    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.CHEESE
        )
        == constraints_ingredients.cheese
    )
    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.MEAT
        )
        == constraints_ingredients.meat
    )
    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.VEGETABLE
        )
        == constraints_ingredients.vegetables
    )
    model += (
        xsum(
            x[i]
            for i in range(n)
            if ingredients[i].value.type == IngredientType.FRUIT
        )
        == constraints_ingredients.fruits
    )

    # optimize
    model.optimize()

    # check solution
    if model.status != OptimizationStatus.OPTIMAL:
        raise Exception(
            "The model is not optimal -> likely no solution found (infeasible))"
        )

    # solution
    return Pizza(
        dough=[
            ingredients[i].value
            for i in range(n)
            if ingredients[i].value.type == IngredientType.DOUGH and x[i].x == 1
        ][0],
        sauce=[
            ingredients[i].value
            for i in range(n)
            if ingredients[i].value.type == IngredientType.SAUCE and x[i].x == 1
        ][0],
        cheese=[
            ingredients[i].value
            for i in range(n)
            if ingredients[i].value.type == IngredientType.CHEESE and x[i].x == 1
        ],
        meat=[
            ingredients[i].value
            for i in range(n)
            if ingredients[i].value.type == IngredientType.MEAT and x[i].x == 1
        ],
        vegetables=[
            ingredients[i].value
            for i in range(n)
            if ingredients[i].value.type == IngredientType.VEGETABLE and x[i].x == 1
        ],
        fruits=[
            ingredients[i].value
            for i in range(len(ingredients))
            if ingredients[i].value.type == IngredientType.FRUIT and x[i].x == 1
        ],
    )

