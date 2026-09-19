import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScheduleCalanderComponent } from './schedule-calander.component';
import { CalendarModule, DateAdapter, MOMENT } from 'angular-calendar';
import moment from 'moment';
import { SchedulerModule } from 'angular-calendar-scheduler';
import { LOCALE_ID } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
@NgModule({
  declarations: [
    ScheduleCalanderComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    CalendarModule.forRoot({
      provide: DateAdapter,
      useFactory: adapterFactory,
    }),
    SchedulerModule.forRoot({
      locale: 'en',
      headerDateFormat: 'daysRange',
      logEnabled: true,
    }),
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'en-US' },
    { provide: MOMENT, useValue: moment },
  ],
   exports: [ScheduleCalanderComponent],
})
export class ScheduleCalanderModule { }
