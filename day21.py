def occurences(food_list):
    '''
    Get ingredient with allergen occurences, ingredient occurences, and allergen occurences.

    Both ingredient with allergen occurences and allergen occurences
    will be used to identify ingredients without allergens.

    Ingredient occurences will be used to sum number of times
    ingredients without allergens appear in any food.
    '''
    ingredient_occurences = {}
    allergen_occurences = {}
    ingredient_allergen_occurences = {}

    for food in food_list:
        if '(' in food:
            ingredients, allergens = food.split(' (')
            allergens = allergens.replace('contains ', '').replace(')', '').split(', ')

            for a in allergens:
                allergen_occurences.setdefault(a, 0)
                allergen_occurences[a] += 1

        else:
            ingredients, allergens = food, []

        ingredients = ingredients.split(' ')

        for i in ingredients:
            allergen_count = ingredient_allergen_occurences.setdefault(i, {})

            for a in allergens:
                allergen_count.setdefault(a, 0)
                allergen_count[a] += 1

            ingredient_occurences.setdefault(i, 0)
            ingredient_occurences[i] += 1

    return ingredient_allergen_occurences, ingredient_occurences, allergen_occurences


def ingredients_without_allergens(ingredients_and_allergen, allergen_occurences):
    '''
    For any tentative allergen per ingredient,
    if said allergen's occurence doesn't match the total allergen's occurences,
    said ingredient likely isn't an allergen.
    So we pop said allergen from said ingredient's tentative allergen occurence.

    Example: if ingredient 'asdasdasd' has {'dairy': 1} and allergen_occurences['dairy'] == 3,
    likely 'asdasdasd' isn't a dairy allergen.
    So we pop 'dairy' from the tentative allergen occurence of 'asdasdasd'

    If the ingredient ends up without any allergen occurences, append to no_allergens.
    '''

    no_allergens = []

    for i, a in ingredients_and_allergen.items():
        for allergen, count in allergen_occurences.items():
            if allergen in a and a[allergen] != count:
                a.pop(allergen)

        if not a:
            no_allergens.append(i)

    return no_allergens


def sort_ingredients_by_allergen(ingredients_and_allergen, without_allergens):

    # Remove ingredients without allergens
    # from the original ingredients_and_allergen
    for i in no_allergens:
        ingredients_and_allergen.pop(i)

    # The allergen occurence isn't important,
    # so make it a list of allergens instead
    for i, a in ingredients_and_allergen.items():
        ingredients_and_allergen[i] = list(a.keys())

    # As per instruction, each allergen is only found in one ingredient
    # and ingredients have 0 or 1 allergen(s).
    # General concept:
    # Loop through each ingredient and get the allergens.
    # If only one allergen, remove said allergen from
    # the possible allergens in other ingredients.
    # Let's hope this works.
    while not all(len(a) == 1 for a in ingredients_and_allergen.values()):
        for i, a in ingredients_and_allergen.items():
            if len(a) == 1:
                ingredient = a[0]
                for i2, a in ingredients_and_allergen.items():
                    if i != i2 and ingredient in a:
                        a.remove(ingredient)

    return ','.join(sorted(ingredients_and_allergen.keys(), key=lambda i: ingredients_and_allergen[i][0]))

if __name__ == '__main__':
    test = [
        'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
        'trh fvjkl sbzzf mxmxvkd (contains dairy)',
        'sqjhc fvjkl (contains soy)',
        'sqjhc mxmxvkd sbzzf (contains fish)'
    ]

    ingredients_and_allergen, ingredient_occurences, allergen_occurences = occurences(test)
    no_allergens = ingredients_without_allergens(
        ingredients_and_allergen, allergen_occurences
    )
    assert sum(c for i, c in ingredient_occurences.items() if i in no_allergens) == 5

    assert sort_ingredients_by_allergen(ingredients_and_allergen, no_allergens) == 'mxmxvkd,sqjhc,fvjkl'

    with open('inputs/day21.txt') as f:
        food_list = [l.strip() for l in f.readlines() if l.strip()]
    ingredients_and_allergen, ingredient_occurences, allergen_occurences = occurences(food_list)
    no_allergens = ingredients_without_allergens(
        ingredients_and_allergen, allergen_occurences
    )

    assert sum(c for i, c in ingredient_occurences.items() if i in no_allergens) == 2075
    assert sort_ingredients_by_allergen(ingredients_and_allergen, no_allergens) == 'zfcqk,mdtvbb,ggdbl,frpvd,mgczn,zsfzq,kdqls,kktsjbh'

