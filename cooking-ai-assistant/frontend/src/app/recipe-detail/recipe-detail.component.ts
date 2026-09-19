import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-recipe-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recipe-detail.component.html',
  styleUrl: './recipe-detail.component.scss'
})
export class RecipeDetailComponent implements  OnInit{
  constructor(
    private api: ApiService,
    private route: ActivatedRoute 
  ) {}

  recipeData:any={};

  ngOnInit(): void {
    let recipeId:string|null = "";
    this.route.paramMap.subscribe(params => {
      recipeId = params.get('recipeId');  
    });
      this.getRecipeById(recipeId);
  }
  getRecipeById(id:string) {
    this.api.getRecipeUsindRecipeId(id).subscribe(data => {
      this.recipeData = data;
      console.log('Recipe Details Data:', this.recipeData);
    });
  }
}
