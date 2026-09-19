import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit{
  constructor(
    private router: Router,
    private apiService: ApiService  
  ) {}

  redirectToPage(page: string): void {
    this.router.navigate([`/${page}`]); 
  }
  ngOnInit(): void {
    this.getData();
  }

  getData(){
    this.apiService.nutrition('r001').subscribe(data => {
      console.log('Search Recipes Data:', data);
    });
  }
}
