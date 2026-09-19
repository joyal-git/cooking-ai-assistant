import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../api.service';
import { Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule,RouterOutlet],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss'
})
export class SearchComponent implements OnInit {
  query = ''; diet = ''; ingredients = ''; max_time: number | null = null; difficulty = '';
  // results: any[] = []; loading = false;
  recipeData: any[] = []; 
  difficultyLevel: string = ''; 
  selectedCusine: string = '';


  constructor(
    private api: ApiService,
    private router : Router
  ) {}
  ngOnInit(): void {
    this.getAllRecipes();
  }

  // async onSearch() {
  //   this.loading = true;
  //   this.api.searchRecipes({ query: this.query, diet: this.diet, ingredients: this.ingredients, max_time: this.max_time ?? undefined, difficulty: this.difficulty })
  //     .subscribe({ next: (d:any) => { this.results = d; this.loading = false; }, error: _ => { this.loading = false; } });
  // }
  getAllRecipes() {
    this.api.getAllRecipe().subscribe(data => {
      this.recipeData = data;
      console.log('All Recipes Data:', this.recipeData);
    });
  }
  findRecipeDetails(id: string) {
    this.router.navigate(["recipe/"+id]);  
    // console.log('Selected Recipe ID:', id);
    // this.api.nutrition(id).subscribe(data => {
    //   console.log('Recipe Nutrition Data:', data);
    // }); 
    // this.api.substitutions('paneer').subscribe(data => {
    //   console.log('Ingredient Substitutions Data:', data);
    // });
  }
  getSingleRecipe(event: any) {
    this.query = event.target.value;
    this.api.searchRecipes({ query: this.query, difficulty:this.difficultyLevel,cuisine:this.selectedCusine }).subscribe(data => {
      this.recipeData = data;
    });
  }
  getSingleRecipeOnCusine(event: any) {
    this.selectedCusine = event.target.value;
    this.api.searchRecipes({ query: this.query, difficulty:this.difficultyLevel,cuisine:this.selectedCusine }).subscribe(data => {
      this.recipeData = data;
    });
  }

  getSingleRecipeOnlevel(event: any) {
    this.difficultyLevel = event.target.value;
    this.api.searchRecipes({ query: this.query, difficulty:this.difficultyLevel,cuisine:this.selectedCusine }).subscribe(data => {
      this.recipeData = data;
    });
  }   
}
