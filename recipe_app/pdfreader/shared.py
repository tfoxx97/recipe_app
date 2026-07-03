def parse_ingredients(line: str):
    ing = {"quantity": None, "ing_name": None}
    for word in line.split():
        if word.isdigit() or isfraction(word) or is_quantity(word):
            if ing["quantity"] is None:
                ing["quantity"] = word
            else:
                ing["quantity"] += " " + word
        else:
            if ing["ing_name"] is None:
                ing["ing_name"] = word
            else:
                ing["ing_name"] += " " + word

    return ing

def isfraction(s: str):
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 2 and all(part.isdigit() for part in parts):
            return True
    return False

def is_quantity(s: str):
    acceptable_measurements = [
        "cup", "cups", "teaspoon", "teaspoons", "tablespoon", "tablespoons", "pound", "pounds", "ounce", "ounces",
        "tsp", "tbsp", "lb", "lbs", "oz", "g", "kg", "ml", "l", "clove", "cloves", "slice", "slices", "can", "cans", "package", 
        "packages", "stick", "sticks", "pinch", "pinches", "dash", "dashes", "bunch", "bunches", "head", "heads", "piece", "pieces", 
        "quart", "quarts", "gallon", "gallons", "liter", "liters", "milliliter", "milliliters", "gram", "grams", "kilogram", "kilograms",
        "cutlet", "cutlets"]
    
    if s in acceptable_measurements:
        return True
    
    return False