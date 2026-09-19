import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, TemplateRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../api.service';
import { NgbModal, NgbToastModule, NgbTooltipModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-shopping',
  standalone: true,
  imports: [CommonModule, FormsModule,NgbTooltipModule,NgbToastModule],
  templateUrl: './shopping.component.html',
  styleUrl: './shopping.component.scss'
})
export class ShoppingComponent implements OnInit{
  ids = ''; items: any = null;
  shoppingList:any[]=[];
  itemName:string="";
  itemcategory:string="";
  showtoaster ={
    show:false,
    msg:""
  };
  constructor(
    private api: ApiService,
    private modalService: NgbModal
  ) {}
  ngOnInit(): void {
     this.getAllShoppingList(); 
  }

  getAllShoppingList(){
    const shoppingListCopy:any[] = [];
    this.api.getAllShoppingList().subscribe((res:any[])=>{
      res.forEach((elem:any,idx:number)=>{
        if(shoppingListCopy.length === 0){
          shoppingListCopy.push({
            "category":elem.category,
            "itemList":[{
              "item":elem.item,
              "id":elem.id
            }]
          });
        }
        else if(shoppingListCopy.length > 0){
            if(shoppingListCopy.find(shop=>shop.category === elem.category)){
              shoppingListCopy[shoppingListCopy.findIndex(shop=>shop.category === elem.category)]["itemList"].push({
                "item":elem.item,
                "id":elem.id
              })
            }
            else{
              shoppingListCopy.push({
              "category":elem.category,
              "itemList":[{
                "item":elem.item,
                "id":elem.id
              }]
            });
          }
        }
      });
      this.shoppingList = shoppingListCopy;
    });
  }

  addItem(){
    const payload ={
        "item": this.itemName,
        "category": this.itemcategory
    }
    this.api.addItemInShoppingList(payload).subscribe((res)=>{
      this.closeModal();
      this.showtoaster.show =true;
      this.showtoaster.msg ="Item added successfully.";
    })
  }

  closeModal(){
    this.modalService.dismissAll();
  }
  open(content: TemplateRef<any>) {
		this.modalService.open(content, { ariaLabelledBy: 'modal-basic-title' });
	}
  getDismissReason(reason: any) {
	}

  deleteItem(id:number){
    this.api.deleteItemInShoppingList(id).subscribe(res=>{
      this.showtoaster.show =true;
      this.showtoaster.msg ="Item deleted successfully.";
    })
  }

}
