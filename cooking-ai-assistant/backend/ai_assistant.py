from typing import Dict, Any, List
import re

class LocalAssistant:
    """Lightweight rule-based cooking assistant."""
    def __init__(self, recipes: List[Dict[str, Any]], subs: Dict[str, List[str]]):
        self.recipes = recipes
        self.subs = subs

    def suggest_by_pantry(self, pantry: List[str], diet: str = None):
        pantry_set = set(x.lower() for x in pantry)
        def score(r):
            ing = set(i['item'].lower() for i in r['ingredients'])
            overlap = len(ing & pantry_set)
            # Favor quick recipes
            return overlap*2 - r.get('time_minutes', 30)/30
        candidates = [r for r in self.recipes if (not diet or r.get('diet')==diet)]
        ranked = sorted(candidates, key=score, reverse=True)
        return ranked[:5]

    def get_substitutions(self, item: str):
        return self.subs.get(item.lower(), [])

    def answer(self, message: str, context: Dict[str, Any]):
        msg = message.lower()
        m = re.search(r"substitut(e|ion) for ([a-z ]+)", msg)
        if m:
            item = m.group(2).strip()
            subs = self.get_substitutions(item)
            if subs:
                return f"You can substitute {item} with: {', '.join(subs)}. Adjust seasoning to taste."
            return f"I don't have a direct substitution for {item}. Consider similar flavor/texture."

        if "what can i cook" in msg or "suggest recipe" in msg:
            pantry = context.get('pantry', [])
            diet = context.get('diet')
            if not pantry:
                return "Tell me your pantry and any diet preferences; I’ll suggest recipes."
            picks = self.suggest_by_pantry(pantry, diet)
            names = ', '.join(r['name'] for r in picks)
            return f"Based on your pantry, try: {names}. Want step-by-step for any?"

        if "safe" in msg or "food safety" in msg:
            return "Keep raw/cooked separate, wash hands, cook chicken to ~75°C, refrigerate leftovers within 2 hours."

        return "I can help with substitutions, timing, step-by-step, nutrition estimates, and meal planning. Ask me anything!"