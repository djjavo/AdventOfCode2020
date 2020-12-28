import utils
import re
import math
import copy
import collections
import itertools
import random


def initialise():
    global ingredients

    date = utils.loadInputFile("input_21.txt")

    ingredients = []
    allergens = []

    for line in date:

        ingredients.append(line.split(" (contains")[0].split())
        allergens.append(line.split(" (contains")[1][:-1].replace(",", "").split())

    freqAllergens = collections.Counter([item for sublist in allergens for item in sublist])
    freqIngredients = collections.Counter([item for sublist in ingredients for item in sublist])

    failed = True

    # brute force random approach
    while failed:

        tempAllergens = copy.deepcopy(allergens)
        tempIngredients = copy.deepcopy(ingredients)

        failed = False

        translatedIngredients = {}

        # optimisation: sort so that most common ingredient is first
        for k, v in sorted(freqAllergens.items(), key=lambda item: item[1], reverse=True):

            # find all lists that have ingredient k
            containing = [idx for idx, x in enumerate(tempAllergens) if k in x]

            commonIngredients = set(tempIngredients[containing[0]])

            for x in containing[1:]:
                # find common values by using a set intersection
                commonIngredients = commonIngredients.intersection(tempIngredients[x])

            try:
                # choose a random ingredient from the intersection
                ingredientToRemove = random.choice(list(commonIngredients))
                translatedIngredients[k] = ingredientToRemove
            except:
                # if no common value, error
                failed = True
                break

            for ingredient in tempIngredients:
                # remove that value from ingredients
                if ingredientToRemove in ingredient:
                    ingredient.remove(ingredientToRemove)

    print("Part 1:", len([item for sublist in tempIngredients for item in sublist]))
    print("Part 2:", ",".join([v for k, v in sorted(translatedIngredients.items(), key=lambda item: item[0])]))


initialise()
