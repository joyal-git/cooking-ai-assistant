import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ScheduleCalanderModule } from '../../modules/schedule-calander/schedule-calander.module';
@Component({
  selector: 'app-plan',
  standalone: true,
  imports: [CommonModule, FormsModule,ScheduleCalanderModule],
  templateUrl: './plan.component.html',
  styleUrl: './plan.component.scss'
})
export class PlanComponent { }
