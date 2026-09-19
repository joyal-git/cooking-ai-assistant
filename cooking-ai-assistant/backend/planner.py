from typing import List, Dict, Any
import random

class MealPlanner:
    def __init__(self, recipes: List[Dict[str, Any]]):
        self.recipes = recipes

    def filter_recipes(self, diet: str = None, exclude: List[str] = None):
        exclude = exclude or []
        def ok(r):
            if diet and r.get('diet') != diet:
                return False
            ing = [i['item'] for i in r['ingredients']]
            return not any(x in ing for x in exclude)
        return [r for r in self.recipes if ok(r)]

    def plan_week(self, calories_per_day: int, diet: str = None, exclude: List[str] = None):
        candidates = self.filter_recipes(diet, exclude)
        if not candidates:
            return {"error": "No recipes match filters"}
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        plan = {}
        for d in days:
            picks = random.sample(candidates, k=min(3, len(candidates)))
            plan[d] = {
                "breakfast": picks[0],
                "lunch": picks[1 if len(picks)>1 else 0],
                "dinner": picks[2 if len(picks)>2 else 0],
            }
        plan["meta"] = {"calories_target": calories_per_day, "diet": diet}
        return plan