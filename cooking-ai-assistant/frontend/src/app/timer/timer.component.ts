import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, TemplateRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbModal, NgbToastModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-timer',
  standalone: true,
  imports: [CommonModule, FormsModule,NgbTooltipModule,NgbToastModule],
  templateUrl: './timer.component.html',
  styleUrl: './timer.component.scss'
})
export class TimerComponent  implements OnInit{
  ids = ''; 
  items: any = null;
  timerList:any[]=[];
  timerName:string="";
  timerDuration:number|null;
  timerTimings={
    minutes:0,
    seconds:0
  }
  showtoaster ={
    show:false,
    msg:""
  };
  constructor(
    private api: ApiService,
    private modalService: NgbModal
  ) {}
  ngOnInit(): void {
    this.getAllTimerList();
    // this.timer(10);
  }

  addTimer(){
    const payload ={
        "timerName": this.timerName,
        "timerDuration": this.timerDuration
    }
    this.api.addTimerInTimerList(payload).subscribe((res)=>{
      this.closeModal();
      this.showtoaster.show =true;
      this.showtoaster.msg ="Timer added successfully.";
    })
  }

  closeModal(){
    this.modalService.dismissAll();
  }
  open(content: TemplateRef<any>) {
    this.modalService.open(content, { ariaLabelledBy: 'modal-basic-title' });
  }

  deleteItem(id:number){
    this.api.deleteTimerInTimerList(id).subscribe(res=>{
      this.showtoaster.show =true;
      this.showtoaster.msg ="Timer deleted successfully.";
    })
  }

  getAllTimerList(){
    this.api.getAllTimerList().subscribe((res:any[])=>{
      this.timerList = res;
    });
  }
  startTimer(id:number,minute:any) {
    this.timerList[id]["timershow"] = true;
    this.timerList[id]["timerdisplay"]=minute+" Minutes"
    let seconds: number = minute * 60;
    let textSec: any = "0";
    let statSec: number = 60;

    const prefix = minute < 10 ? "0" : "";

    const timer = setInterval(() => {
       if(this.timerList[id]["timershow"] === false){
         this.timerList[id]["timerdisplay"] = minute+" Minutes";
          clearInterval(timer);
          return;
      }
      seconds--;
      if (statSec != 0) statSec--;
      else statSec = 59;

      if (statSec < 10) {
        textSec = "0" + statSec;
      } else textSec = statSec;
      this.timerList[id]["timerdisplay"] = `${prefix}${Math.floor(seconds / 60)}:${textSec}`;
      this.timerList[id]["timershow"] = true;

      if (seconds == 0) {
        clearInterval(timer);
      }
    }, 1000);
  }
  resetTimer(id:number){
    this.timerList[id].timershow = false;
  }
}

