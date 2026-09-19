import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware

from .ai_assistant import LocalAssistant
from .planner import MealPlanner

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



    
BASE = Path(__file__).resolve().parent
RECIPES = json.loads((BASE/'recipe_db.json').read_text())

SUBS = json.loads((BASE/'ingredients_subs.json').read_text())
NUTRI = json.loads((BASE/'nutrition_dbtest.json').read_text())

assistant = LocalAssistant(RECIPES, SUBS)
planner = MealPlanner(RECIPES)

app = FastAPI(title="Cooking AI Assistant API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/tetttt")
async  def test():
    return {"message": "API is working!"}
    
@app.get("/api/recipes")
def list_recipes(
    query: Optional[str] = Query(None),
    diet: Optional[str] = Query(None),
    ingredients: Optional[str] = Query(None),
    max_time: Optional[int] = Query(None),
    difficulty: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None)
):
    q = (query or '').lower()
    inc = set(x.strip().lower() for x in (ingredients or '').split(',') if x.strip())
    def ok(r):
        print(r.get('cuisine').lower())
        if diet and r.get('diet') != diet: return False
        if difficulty and r.get('difficulty') != difficulty: return False
        if max_time and r.get('time_minutes', 999) > max_time: return False
        if cuisine and r.get('cuisine').lower() != cuisine: return False
        if q:
            in_name = q in r['name'].lower()
            in_tags = any(q in t.lower() for t in r.get('tags', []))
            if not (in_name or in_tags): return False
        if inc:
            ing_items = set(i['item'].lower() for i in r['ingredients'])
            if not inc.issubset(ing_items): return False
        return True
    return [r for r in RECIPES if ok(r)]

@app.get("/recipes")
def get_recipes():
    """Return all recipes (client-side filtering option)."""
    return {"recipes": RECIPES}

@app.get("/filter")
def filter_recipes(
    search: Optional[str] = Query("", description="search text"),
    cuisine: Optional[str] = Query("", description="cuisine"),
    level: Optional[str] = Query("", description="level/difficulty"),
):
    """Server-side filtered results. All params optional."""
    s = (search or "").strip().lower()
    c = (cuisine or "").strip()
    l = (level or "").strip()

    def matches(r):
        name_ok = s == "" or s in r.get("name", "").lower() or s in r.get("description", "").lower()
        cuisine_ok = c == "" or r.get("cuisine", "") == c
        level_ok = l == "" or r.get("difficulty", "") == l or r.get("level", "") == l
        return name_ok and cuisine_ok and level_ok

    filtered = [r for r in RECIPES if matches(r)]
    return {"recipes": filtered}

# @app.get("/api/recipes/{rid}")
# def get_recipe(rid: str):
#     for r in RECIPES:
#         if r['id'] == rid: return r
#     return {"error": "Recipe not found"}

@app.get("/api/substitutions")
def substitutions(ingredient: str = Query(...)):
    subs = SUBS.get(ingredient.lower(), [])
    return {"ingredient": ingredient, "substitutions": subs}

@app.get("/api/nutrition")
def nutrition(recipe_id: str = Query(...)):
    for r in RECIPES:
        if r['id'] == recipe_id:
            total = {"calories":0, "protein":0, "fat":0, "carbs":0, "fiber":0, "sodium":0}
            missing = []
            for ing in r['ingredients']:
                item = ing['item'].lower()
                grams = ing['grams']
                if item in NUTRI:
                    n = NUTRI[item]
                    factor = grams/100.0
                    for k in total:
                        total[k] += n.get(k,0)*factor
                else:
                    missing.append(item)
            total = {k: round(v, 1) for k,v in total.items()}
            return {"recipe": r['name'], "recipe_id": recipe_id, "total": total, "unknown_ingredients": missing}
    return {"error": "Recipe not found"}

@app.post("/api/plan")
def plan(calories_per_day: int = Body(2000), diet: Optional[str] = Body(None), exclude: Optional[List[str]] = Body(None)):
    return planner.plan_week(calories_per_day, diet, exclude or [])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    # Simple AI response (replace with OpenAI later)
    reply = f"You said: {req.message}"
    return {"reply": reply}

# @app.post("/api/chat")
# def chat(payload: Dict[str, Any] = Body(...)):
#     message = payload.get('message', '')
#     context = {'pantry': payload.get('pantry', []), 'diet': payload.get('diet')}
#     reply = assistant.answer(message, context)
#     return {"reply": reply}

@app.post("/api/shopping-list")
def shopping_list(recipe_ids: List[str] = Body(...)):
    items: Dict[str, float] = {}
    for rid in recipe_ids:
        r = next((x for x in RECIPES if x['id']==rid), None)
        if not r: continue
        for ing in r['ingredients']:
            items[ing['item']] = items.get(ing['item'], 0) + ing['grams']
    items = {k: round(v, 0) for k,v in items.items()}
    return {"items": items}


