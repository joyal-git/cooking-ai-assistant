import { Routes } from '@angular/router';
import { SearchComponent } from './pages/search/search.component';
import { ChatComponent } from './pages/chat/chat.component';
import { PlanComponent } from './pages/plan/plan.component';
import { NutritionComponent } from './pages/nutrition/nutrition.component';
import { ShoppingComponent } from './pages/shopping/shopping.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { NoPageFoundComponent } from './pages/no-page-found/no-page-found.component';
import { TimerComponent } from './timer/timer.component';
import { RecipeDetailComponent } from './recipe-detail/recipe-detail.component';

const routes: Routes = [
  { path: 'recipe', component: SearchComponent },
  { path: 'recipe/:recipeId', component: RecipeDetailComponent },
  { path: 'chat', component: ChatComponent },
  { path: 'plan', component: PlanComponent },
  { path: 'nutrition', component: NutritionComponent },
  { path: 'shopping', component: ShoppingComponent },
  { path: 'home', component: HomePageComponent },
  { path: 'timer', component: TimerComponent }
];

export default routes;