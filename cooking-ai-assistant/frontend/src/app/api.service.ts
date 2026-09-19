import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private API = environment.apiUrl;
  constructor(private http: HttpClient) {}

  searchRecipes(opts: { query?: string; diet?: string; ingredients?: string; max_time?: number; difficulty?: string,cuisine?:string }): Observable<any[]> {
    let params = new HttpParams();
    Object.entries(opts).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') params = params.set(k, String(v)); });
    return this.http.get<any[]>(`${this.API}/api/recipes`, { params });
  }

  getAllRecipe(): Observable<any> {
    return this.http.get(`${this.API}/api/recipes`);
  }

  getAllShoppingList(): Observable<any> {
    return this.http.get(`${this.API}/api/shoppingList/all`);
  }

  getAllTimerList(): Observable<any> {
    return this.http.get(`${this.API}/api/timerList/all`);
  }

  addItemInShoppingList(payload:{}): Observable<any> {
    return this.http.post(`${this.API}/api/shoppinglist/add`,payload);
  }

  addTimerInTimerList(payload:{}): Observable<any> {
    return this.http.post(`${this.API}/api/timerlist/add`,payload);
  }

  deleteItemInShoppingList(id:number): Observable<any> {
    const params = new HttpParams().set('id', id);
    return this.http.delete(`${this.API}/api/shoppinglist/delete`, { params });
  }

  deleteTimerInTimerList(id:number): Observable<any> {
    const params = new HttpParams().set('id', id);
    return this.http.delete(`${this.API}/api/tiemrlist/delete`, { params });
  }

  getRecipeUsindRecipeId(id:string): Observable<any> {
    return this.http.get(`${this.API}/api/recipes/${id}`);
  }

  chat(payload: { message: string; pantry?: string[]; diet?: string | null }): Observable<any> {
    return this.http.post(`${this.API}/api/chat`, payload);
  }

  plan(payload: { calories_per_day: number; diet?: string | null; exclude?: string[] }): Observable<any> {
    return this.http.post(`${this.API}/api/plan`, payload);
  }

  shoppingList(ids: string[]): Observable<any> {
    return this.http.post(`${this.API}/api/shopping-list`, ids);
  }

  nutrition(recipe_id: string): Observable<any> {
    const params = new HttpParams().set('recipe_id', recipe_id);
    return this.http.get(`${this.API}/api/nutrition`, { params });
  }

  substitutions(ingredient: string): Observable<any> {
    const params = new HttpParams().set('ingredient', ingredient);
    return this.http.get(`${this.API}/api/substitutions`, { params });
  }
}
