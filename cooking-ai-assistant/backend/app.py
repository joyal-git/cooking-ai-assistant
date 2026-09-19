import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware

from ai_assistant import LocalAssistant
from planner import MealPlanner

from fastapi import FastAPI
from pydantic import BaseModel
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from fastapi.middleware.cors import CORSMiddleware

global SHOPPINGlIST
BASE = Path(__file__).resolve().parent
RECIPES = json.loads((BASE/'recipe_db.json').read_text())
SHOPPINGlIST = json.loads((BASE/'shopping_list.json').read_text())
TIMERLIST = json.loads((BASE/'timer_list.json').read_text())
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
    

@app.get("/api/recipes/{rid}")
def get_recipe(rid: str):
    for r in RECIPES:
        if r['id'] == rid: return r
    return {"error": "Recipe not found"}


@app.get("/api/shoppingList/all")
def get_all_shoppingList_data():
    return SHOPPINGlIST

@app.get("/api/timerList/all")
def get_all_shoppingList_data():
    return TIMERLIST

@app.post("/api/shoppinglist/add")
def addShoppingListDataToJson(
     itemName: Optional[object] = Body(None)
):
    with open("C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/shopping_list.json", 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        length = len(file_data)
        itemName["id"]=length+1
        
        # Append new data to the 'emp_details' list
        file_data.append(itemName)
        
        # Move the cursor to the beginning of the file
        file.seek(0)
        
        # Write the updated data back to the file
        json.dump(file_data, file, indent=4)


@app.post("/api/timerlist/add")
def addTimerListDataToJson(
     itemName: Optional[object] = Body(None)
):
    with open("C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/timer_list.json", 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        length = len(file_data)
        itemName["id"]=length+1
        
        # Append new data to the 'emp_details' list
        file_data.append(itemName)
        
        # Move the cursor to the beginning of the file
        file.seek(0)
        
        # Write the updated data back to the file
        json.dump(file_data, file, indent=4)


@app.delete("/api/shoppinglist/delete")
def deleteItemFromShoppingList(
     id: int = Query(None)
):
    filePath="C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/shopping_list.json"
    try:
        with open(filePath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filePath}'.")
        return
    initial_length = len(data)
    # Assuming data is a list of dictionaries, and each dictionary has an 'id' key
    data = [item for item in data if item.get('id') != id]

    if len(data) == initial_length:
        print(f"No item with ID  found to delete.")
    else:
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Item with ID  deleted successfully from sd.")


@app.delete("/api/tiemrlist/delete")
def deleteItemFromTimerList(
     id: int = Query(None)
):
    filePath="C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/timer_list.json"
    try:
        with open(filePath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filePath}'.")
        return
    initial_length = len(data)
    # Assuming data is a list of dictionaries, and each dictionary has an 'id' key
    data = [item for item in data if item.get('id') != id]

    if len(data) == initial_length:
        print(f"No item with ID  found to delete.")
    else:
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Item with ID  deleted successfully from sd.")





    



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

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# def chat(req: ChatRequest):
#     # Simple AI response (replace with OpenAI later)
#     reply = f"You said: {req.message}"
#     return {"reply": reply}

@app.post("/api/chat")
def chat(payload: Dict[str, Any] = Body(...)):
    message = payload.get('message', '')
    context = {'pantry': payload.get('pantry', []), 'diet': payload.get('diet')}
    reply = assistant.answer(message, context)
    return {"reply": reply}

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


# class MyHandler(FileSystemEventHandler):
#         def __init__(self, json_file_path, callback_function):
#             self.json_file_path = json_file_path
#             self.callback_function = callback_function

#         def on_modified(self, event):
#             if event.src_path == self.json_file_path:
#                 print(f"JSON file '{self.json_file_path}' modified. Reloading data...")
#                 self.callback_function()


# def load_json_data(file_path):
#         try:
#             with open(file_path, 'r') as f:
#                 return json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError) as e:
#             print(f"Error loading JSON data: {e}")
#             return None

# def refresh_app_data():
#         new_data = load_json_data("C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/shopping_list.json")
#         if new_data is not None:
#             SHOPPINGlIST = new_data
#             print(SHOPPINGlIST)
#             print("App data refreshed successfully.")
#             # Add any other logic here to update your application state

#     # Example usage:
# if __name__ == "__main__":
#         app_data = {}  # Initial app data
#         json_file = '"C:/Users/Joyal/OneDrive/Documents/Desktop/cooking_assiatant/cooking-ai-assistant/backend/shopping_list.json"'

#         # Initial load
#         app_data = load_json_data(json_file)
#         print(f"Initial app data: {app_data}")

#         event_handler = MyHandler(json_file, refresh_app_data)
#         observer = Observer()
#         observer.schedule(event_handler, path='.', recursive=False)
#         observer.start()

#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             observer.stop()
#         observer.join()