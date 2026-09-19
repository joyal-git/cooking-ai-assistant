import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-nutrition',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './nutrition.component.html',
  styleUrl: './nutrition.component.scss'
})
export class NutritionComponent {
  rid = ''; data: any = null;
  constructor(private api: ApiService) {}
  fetch() { if (!this.rid) return; this.api.nutrition(this.rid).subscribe(d => this.data = d); }
}
